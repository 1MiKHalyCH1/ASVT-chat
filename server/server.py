from socket import *
from utils import send_msg, recv_msg, addr_to_str, get_user_by_addr
from struct import error
from message_storage import MessageStorage

import config
import threading

MAX_MSG_LEN = 60
MAX_USER_LEN = 8
USERS = dict()


def register(conn, addr):
    login = recv_msg(conn)

    try:
        login = login.decode()
    except Exception:
        send_msg(conn, b"Can't decode login!")
        print("[-] Can't decode login!")
        return False

    if not login:
        send_msg(conn, b"Bad login!")
        print("[-] ({}) empty login!".format(addr_to_str(addr)))
        return False
    
    if len(login) > MAX_USER_LEN:
        send_msg(conn, b"Login is too long!")
        print("[-] ({}) Username '{}' is greater then {} chars!".format(addr_to_str(addr), login, MAX_USER_LEN))
        return False

    if login not in USERS:
        if addr[0] not in USERS.values():
            USERS[login] = addr[0]
            send_msg(conn, "Hello, {}".format(login).encode())
            print("[+] '{}'({}) registered!".format(login, addr_to_str(addr)))
            return True
        else:
            user = get_user_by_addr(addr, USERS)
            send_msg(conn, "{} was used before!".format(addr_to_str(addr)).encode())
            print("[-] '{}'({}) used address of {}!".format(login, addr_to_str(addr), user))
            return False
    elif USERS.get(login, "") == addr[0]:
        send_msg(conn, "Nice to see you, {}".format(login).encode())
        print("[+] '{}'({}) logined!".format(login, addr_to_str(addr)))
        return True
    else:
        send_msg(conn, "'{}' already exists!".format(login).encode())
        print("[-] '{}'({}) already exists!".format(login, addr_to_str(addr)))
        return False


def get_users(conn, addr):
    send_msg(conn, str(len(USERS)).encode())
    for user in USERS:
        send_msg(conn, user.encode())
    print("[+] users sended to {}".format(addr_to_str(addr)))


def logout(conn, addr, ms):
    user = get_user_by_addr(addr, USERS)
    if user:
        del USERS[user]
    ms.get_messages_for_user(user)
    send_msg(conn, b"U've been successfully logouted")
    print("[+] {}({}) logouted".format(user, addr_to_str(addr)))


def send(conn, addr, ms):
    user_to = recv_msg(conn).decode()
    context = recv_msg(conn).decode()
    user_from = get_user_by_addr(addr, USERS)

    if len(context) > MAX_MSG_LEN:
        send_msg(conn, "Massage is too long! Max length = {}!".format(MAX_MSG_LEN).encode())
        print("[-] '{}'({}) sended message of length {}!".format(user_from, addr_to_str(addr)), len(context))
        return False
    
    if not user_from:
        send_msg(conn, b"U aren't registered!")
        print("[-] User isn't regitered!")
        return False
    
    if user_to not in USERS:
        send_msg(conn, "User '{}' doesn't exist!".format(user_to).encode())
        print("[-] There are not user '{}' in system!".format(user_to))
        return False
    
    ms.add_message(user_from, user_to, context)
    send_msg(conn, b"Message added to storage!")
    print("[+] Message ('{}') from '{}'({}) sent to '{}'".format(context, user_from, addr_to_str(addr), user_to))
    return True


def sendall(conn, addr, ms):
    context = recv_msg(conn).decode()
    user_from = get_user_by_addr(addr, USERS)

    if len(context) > MAX_MSG_LEN:
        send_msg(conn, "Massage is too long! Max length = {}!".format(MAX_MSG_LEN).encode())
        print("[-] '{}'({}) sended message of length {}!".format(user_from, addr_to_str(addr)), len(context))
        return False

    if not user_from:
        send_msg(conn, b"U aren't registered!")
        print("[-] User isn't regitered!")
        return False
    
    for user_to in USERS:
        if user_to != user_from:
            ms.add_message(user_from, user_to, context)
            print("[+] Message ('{}') from '{}'({}) sent to '{}'".format(context, user_from, addr_to_str(addr), user_to))

    send_msg(conn, b"Message added to storage!")


def receive(conn, addr, ms):
    user_to = get_user_by_addr(addr, USERS)
    
    if not user_to:
        send_msg(conn, b"U aren't registered!")
        print("[-] User isn't regitered!")
        return False
    
    msgs = ms.get_messages_for_user(user_to)
    send_msg(conn, str(len(msgs)).encode())
    for msg in msgs:
        send_msg(conn, msg.user_from.encode())
        send_msg(conn, msg.msg.encode())
    return True


def handler(conn, addr, ms):
    try:
        while True:
            msg = recv_msg(conn)
            print("[+] '{}' from {}".format(msg.decode(), addr_to_str(addr)))
            if msg == b"register":
                if not register(conn, addr):
                    break
            elif msg == b"users":
                get_users(conn, addr)
            elif msg == b"logout":
                logout(conn, addr, ms)
            elif msg == b"send":
                if not send(conn, addr, ms):
                    break
            elif msg == b"receive":
                receive(conn, addr, ms)
            elif msg == b"sendall":
                sendall(conn, addr, ms)
            else:
                break
    except error:
        print("[-] Can't read more from {}".format(addr))
    except Exception as ex:
        print("[-] Exception: {}".format(ex))
    finally:
        conn.close()


class Server:
    def __init__(self, ip, port):
        self.addr = ip, port
        self.ms = MessageStorage()

    def start(self, connections):
        with socket() as s:
            s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
            s.bind(self.addr)
            s.listen(connections)

            print("[+] Server starts on {}".format(addr_to_str(self.addr)))
            while True:
                conn, addr = s.accept()
                conn.settimeout(10)
                print("[+] {} connected!".format(addr_to_str(addr)))
                thread = threading.Thread(target=handler, args=(conn, addr, self.ms))
                thread.daemon = True
                thread.start()


if __name__ == "__main__":
    server = Server(config.IP, config.PORT)
    try:
        server.start(config.CONNECTIONS)
    except Exception as ex:
        print("[-] Server stoped because of: {}".format(ex))
    except KeyboardInterrupt:
        print("[-] Server stoped!")

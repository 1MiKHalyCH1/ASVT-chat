from socket import *
from utils import send_msg, recv_msg, addr_to_str, get_user_by_addr
from struct import error
from message import MessageStorage

import config
import threading

USERS = dict()


def register(conn, addr):
    login = recv_msg(conn).decode()

    if not login:
        send_msg(conn, "Bad login!".encode())
        return False
        print("[+] '{}'({}) registered!".format(login, addr_to_str(addr)))

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


def logout(conn, addr):
    user = get_user_by_addr(addr)
    if user:
        del USERS[user]
    send_msg(conn, "U've been successfully logouted".format().encode())
    print("[+] {}({}) logouted".format(user, addr_to_str(addr)))


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
                logout(conn, addr)
            else:
                break
    except error:
        print("[-] Can't read more from {}".format(addr))
    except Exception as ex:
        print("[-] Exception: {}".format(ex))
    finally:
        user = get_user_by_addr(addr, USERS)
        if user:
            del USERS[user]
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

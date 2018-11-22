from socket import *
from command_utils import send_msg, recv_msg

ADDR = "10.97.167.134", 31337


def register(s, login):
    send_msg(s, b"register")
    send_msg(s, login)
    print(recv_msg(s).decode())


def get_users(s):
    send_msg(s, b"users")
    return [recv_msg(s) for _ in range(int(recv_msg(s)))]

def send(s, msg, user_to):
    send_msg(s, b"send")
    send_msg(s, user_to)
    send_msg(s, msg)
    print(recv_msg(s).decode())

def sendall(s, msg):
    send_msg(s, b"sendall")
    send_msg(s, msg)
    print(recv_msg(s).decode())

def recv(s):
    send_msg(s, b"receive")
    return ["From '{}': {}".format(recv_msg(s).decode(),recv_msg(s).decode()) for _ in range(int(recv_msg(s)))]

def logout(s):
    send_msg(s, b"logout")
    print(recv_msg(s))


if __name__ == "__main__":
    login = "MKHCH".encode()
    user_to = login

    with socket() as s:
        s.connect(ADDR)
        register(s, login)
        print(get_users(s))
        sendall(s, b"Hello all!")
        send(s, "Hello, {}!".format(login.decode()).encode(), user_to)
        print(recv(s))
        logout(s)

from socket import *
from command_utils import send_msg, recv_msg
from message_utils import pack_msg

ADDR = "localhost", 31337


def register(s, login):
    send_msg(s, b"register")
    send_msg(s, login)
    print(recv_msg(s))


def get_users(s):
    send_msg(s, b"users")
    return [recv_msg(s) for _ in range(int(recv_msg(s)))]


def logout(s):
    send_msg(s, b"logout")
    print(recv_msg(s))


if __name__ == "__main__":
    login = b""

    with socket() as s:
        s.connect(ADDR)
        register(s, login)
        users = get_users(s)
        print(users)
        # logout(s)

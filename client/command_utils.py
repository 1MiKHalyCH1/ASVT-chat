from struct import pack, unpack


def send_msg(s, msg):
    msg_len = pack("<I", len(msg))
    s.send(msg_len + msg)


def recv_msg(s):
    msg_len = unpack("<I", s.recv(4))[0]
    return s.recv(msg_len)
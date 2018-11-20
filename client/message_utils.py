from struct import pack

def pack_msg(msg, recv_username):
    packed_username = pack("<I", len(recv_username)) + recv_username.encode()
    packed_context = pack("<I", len(msg)) + msg.encode()
    return packed_username + packed_context
from collections import defaultdict


class Message:
    def __init__(self, user_from, user_to, msg):
        self.user_from = user_from
        self.user_to = user_to
        self.msg = msg

class MessageStorage:
    def __init__(self):
        self.__storage = defaultdict(list)

    def add_message(self, user_from, user_to, msg_context):
        msg = Message(user_from, user_to, msg_context)
        self.__storage[user_to].append(msg)

    def get_messages_for_user(self, user):
        res = self.__storage[user]
        del self.__storage[user]
        return res

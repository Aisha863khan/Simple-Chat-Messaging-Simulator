from .session import ChatSession

class ChatSessionBuilder:
    def __init__(self):
        self.reset()

    def reset(self):
        self._name = None
        self._members = []
        self._seed_messages = []
        return self

    def set_name(self, name: str):
        self._name = name
        return self

    def add_member(self, member: str):
        self._members.append(member)
        return self

    def add_seed_message(self, message):
        self._seed_messages.append(message)
        return self

    def build(self):
        s = ChatSession(name=self._name or 'Conversation', members=self._members)
        for m in self._seed_messages:
            s.add_message(m)
        self.reset()
        return s


import uuid
from datetime import datetime
from typing import List

class ChatSession:
    def __init__(self, name: str = 'Conversation', members: List[str] = None):
        self.session_id = str(uuid.uuid4())
        self.name = name
        self.members = members or []
        self.messages = []
        self.unread_count = 0
        self.is_online = True
        self.last_seen = datetime.now()

    def add_message(self, message):
        self.messages.append(message)
        # increment unread if message not sent by You
        sender = getattr(message, 'sender', '')
        if str(sender).lower() != 'you':
            self.unread_count += 1

    def clear_unread(self):
        self.unread_count = 0

    def search(self, query: str):
        q = query.lower()
        return [m for m in self.messages
                if q in getattr(m, 'text', '').lower() or q in getattr(m, 'sender', '').lower()]


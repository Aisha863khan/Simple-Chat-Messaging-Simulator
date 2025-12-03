from .base_message import Message

class SystemMessage(Message):
    def __init__(self, text: str):
        super().__init__(sender='[SYSTEM]', text=text)

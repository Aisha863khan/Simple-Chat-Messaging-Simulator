from .text_message import TextMessage
from .system_message import SystemMessage

class MessageFactory:
    @staticmethod
    def create(message_type: str, sender: str, text: str):
        t = message_type.lower()
        if t == 'text':
            return TextMessage(sender=sender, text=text)
        if t == 'system':
            return SystemMessage(text=text)
        raise ValueError('Unknown message type: ' + message_type)


from .base_message import Message

class MessageDecorator(Message):
    def __init__(self, wrapped: Message):
        # don't call Message.__init__: we wrap an existing message
        self.wrapped = wrapped

    @property
    def sender(self):
        return self.wrapped.sender

    @property
    def text(self):
        return self.wrapped.text

    @property
    def timestamp(self):
        return self.wrapped.timestamp

    def render(self):
        return self.wrapped.render()

class TimestampDecorator(MessageDecorator):
    def render(self):
        ts = self.wrapped.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        return f"[{ts}] {self.wrapped.render()}"

class EmphasisDecorator(MessageDecorator):
    def render(self):
        base = self.wrapped.render()
        if getattr(self.wrapped, 'sender', '').lower() == 'you':
            return f"** {base} **"
        return base

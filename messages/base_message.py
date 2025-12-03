from dataclasses import dataclass
from datetime import datetime

@dataclass
class Message:
    sender: str
    text: str
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

    def render(self):
        return f"{self.sender}: {self.text}"


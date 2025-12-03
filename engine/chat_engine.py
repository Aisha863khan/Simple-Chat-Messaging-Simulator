from patterns.singleton import Singleton
from patterns.observer import Observable
import queue
import threading
import time

class ChatEngine(Observable, metaclass=Singleton):
    def __init__(self):
        super().__init__()
        self.sessions = []  # list of ChatSession
        self.outgoing = queue.Queue()
        # start background thread to process outgoing messages
        t = threading.Thread(target=self._process_outgoing, daemon=True)
        t.start()

    def create_session(self, session):
        self.sessions.append(session)
        self.notify('session_created', session)
        return session

    def get_session(self, session_id):
        for s in self.sessions:
            if s.session_id == session_id:
                return s
        return None

    def route_message(self, session_id, message):
        session = self.get_session(session_id)
        if not session:
            return
        session.add_message(message)
        # notify observers (GUI)
        self.notify('message_received', {'session': session, 'message': message})

    def send_message(self, session_id, message):
        # put into outgoing queue to simulate network
        self.outgoing.put((session_id, message))

    def _process_outgoing(self):
        while True:
            try:
                session_id, message = self.outgoing.get(timeout=0.5)
            except Exception:
                time.sleep(0.1)
                continue
            # simulate delay
            time.sleep(0.35)
            # deliver
            self.route_message(session_id, message)

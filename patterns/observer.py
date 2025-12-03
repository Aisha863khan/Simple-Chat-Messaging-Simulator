class Observer:
    def update(self, event_type, payload):
        raise NotImplementedError

class Observable:
    def __init__(self):
        self._observers = []

    def subscribe(self, obs: Observer):
        if obs not in self._observers:
            self._observers.append(obs)

    def unsubscribe(self, obs: Observer):
        if obs in self._observers:
            self._observers.remove(obs)

    def notify(self, event_type, payload):
        for o in list(self._observers):
            try:
                o.update(event_type, payload)
            except Exception as e:
                print('Observer error:', e)


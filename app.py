from engine.chat_engine import ChatEngine
from ui.gui import ChatGUI
from engine.builder import ChatSessionBuilder
from messages.factory import MessageFactory
import threading
import time

def seed_demo(engine: ChatEngine):
    b = ChatSessionBuilder()

    # Friends
    s1 = (b.set_name('Friends')
            .add_member('Ali')
            .add_member('Sara')
            .add_member('You')
            .add_seed_message(MessageFactory.create('text', 'Ali', 'Hey everyone!'))
            .add_seed_message(MessageFactory.create('text', 'Sara', 'Hi Ali!'))
            .build())

    b.reset()
    # Work
    s2 = (b.set_name('Work')
            .add_member('Boss')
            .add_member('You')
            .add_seed_message(MessageFactory.create('text', 'Boss', 'Deadline is Friday'))
            .add_seed_message(MessageFactory.create('text', 'You', 'Me and sara are still working on the project'))
            .build())

    b.reset()
    # Study Group
    s3 = (b.set_name('Study Group')
            .add_member('Ayesha')
            .add_member('Hina')
            .add_member('You')
            .add_seed_message(MessageFactory.create('text', 'Ayesha', 'Don’t forget the assignment due tomorrow!'))
            .add_seed_message(MessageFactory.create('text', 'Hina', 'Let’s study together tonight.'))
            .build())

    b.reset()
    # Family
    s4 = (b.set_name('Family')
            .add_member('Mom')
            .add_member('Dad')
            .add_member('You')
            .add_seed_message(MessageFactory.create('text', 'Mom', 'Dinner is at 8 PM.'))
            .add_seed_message(MessageFactory.create('text', 'Dad', 'Bring milk on your way home.'))
            .build())

    b.reset()
    # Creators Hub
    s5 = (b.set_name('Creators Hub')
            .add_member('Zara')
            .add_member('Bilal')
            .add_member('You')
            .add_seed_message(MessageFactory.create('text', 'Zara', 'New reel idea: Café Aesthetic Shots!'))
            .add_seed_message(MessageFactory.create('text', 'Bilal', 'Let’s shoot this weekend.'))
            .build())

    b.reset()
    s6 = (b.set_name('Support')
            .add_member('SupportBot')
            .add_member('You')
            .add_seed_message(MessageFactory.create('text', 'SupportBot', 'Welcome to support chat.'))
            .build())

    b.reset()
    s7 = (b.set_name('Design Team')
            .add_member('Nida')
            .add_member('You')
            .add_seed_message(MessageFactory.create('text', 'Nida', 'Wireframe v2 ready.'))
            .build())

    for s in (s1, s2, s3, s4, s5, s6, s7):
        engine.create_session(s)

    # simulated incoming messages
    def simulate():
        time.sleep(2)
        engine.route_message(s1.session_id, MessageFactory.create('text', 'Ali', 'Anyone free this weekend?'))
        time.sleep(1.5)
        engine.route_message(s2.session_id, MessageFactory.create('text', 'Boss', 'Reminder: update status.'))
        time.sleep(2)
        engine.route_message(s3.session_id, MessageFactory.create('text', 'Hina', 'I am starting the chapter now.'))
        time.sleep(2)
        engine.route_message(s4.session_id, MessageFactory.create('text', 'Mom', 'Don’t be late!'))
        time.sleep(2)
        engine.route_message(s5.session_id, MessageFactory.create('text', 'Zara', 'Check Pinterest for ideas!'))

    threading.Thread(target=simulate, daemon=True).start()


if __name__ == '__main__':
    engine = ChatEngine()
    seed_demo(engine)
    app = ChatGUI(engine)
    app.mainloop()

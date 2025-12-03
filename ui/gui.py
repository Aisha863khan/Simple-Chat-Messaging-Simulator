import tkinter as tk
from tkinter import scrolledtext, simpledialog, messagebox
from patterns.observer import Observer
from messages.decorators import TimestampDecorator
from messages.factory import MessageFactory
from messages.system_message import SystemMessage
from datetime import datetime
import threading
import time

# ---------------- Pastel Yellow Theme ----------------
BG = "#fada74"
PANEL = "#f1c946"
FG = '#333333'
ACCENT = "#755F0B"
MUTED = '#666666'

class ChatGUI(tk.Tk, Observer):
    def __init__(self, engine):
        super().__init__()
        self.engine = engine
        self.engine.subscribe(self)

        self.title("Simple Chat Simulator - Pastel Yellow")
        self.geometry("1000x650")
        self.configure(bg=BG)

        self.selected_session_id = None
        self._index_to_sid = []

        self.build_ui()
        self.refresh_sessions()
        self.after(500, self._periodic_refresh)

    # ----------------- Build UI -----------------
    def build_ui(self):
        # LEFT PANEL
        left = tk.Frame(self, bg=PANEL, width=300)
        left.pack(side=tk.LEFT, fill=tk.Y)

        # Search Title
        search_title = tk.Label(left, text="Search", bg=PANEL, fg=FG, font=("Arial", 14, "bold"))
        search_title.pack(anchor='w', padx=12, pady=(12,0))

        # SEARCH BAR
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(left, textvariable=self.search_var, bg='#fff1b3', fg=FG, insertbackground=FG, font=("Arial", 12))
        search_entry.pack(padx=12, pady=(2,10), fill=tk.X)
        self.search_var.trace_add('write', lambda *_: self.refresh_sessions())

        # Chats Title under search bar
        chats_title = tk.Label(left, text="Chats", bg=PANEL, fg=FG, font=("Arial", 14, "bold"))
        chats_title.pack(anchor='w', padx=12, pady=(0,4))

        # SESSION LIST
        self.session_listbox = tk.Listbox(left, bg='#fff6d6', fg=FG, selectbackground=ACCENT, activestyle='none', font=("Arial", 12))
        self.session_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=6)
        self.session_listbox.bind('<<ListboxSelect>>', self.on_session_select)

        # NEW / SEARCH BUTTONS
        btn_frame = tk.Frame(left, bg=PANEL)
        btn_frame.pack(fill=tk.X, padx=10, pady=8)
        tk.Button(btn_frame, text='New', command=self.create_new_session, bg=ACCENT, fg=FG).pack(side=tk.LEFT, padx=4)
        tk.Button(btn_frame, text='Search', command=self.search_in_session, bg=ACCENT, fg=FG).pack(side=tk.LEFT, padx=4)

        # RIGHT PANEL
        right = tk.Frame(self, bg=BG)
        right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # RIGHT PANEL HEADER
        self.chat_title = tk.Label(right, text='No session selected', bg=BG, fg=FG, font=('Arial', 16, 'bold'))
        self.chat_title.pack(anchor='w', padx=12, pady=8)

        self.status_label = tk.Label(right, text='', bg=BG, fg=MUTED)
        self.status_label.pack(anchor='w', padx=12)

        # MESSAGES AREA
        self.chat_area = scrolledtext.ScrolledText(right, bg='#fffde6', fg=FG, state=tk.DISABLED, wrap=tk.WORD, font=("Helvetica", 12))
        self.chat_area.pack(fill=tk.BOTH, expand=True, padx=12, pady=8)

        # TYPING INDICATOR
        self.typing_var = tk.StringVar(value='')
        self.typing_label = tk.Label(right, textvariable=self.typing_var, bg=BG, fg=MUTED, font=('Arial', 10, 'italic'))
        self.typing_label.pack(anchor='w', padx=12, pady=(0, 6))

        # MESSAGE ENTRY
        bottom = tk.Frame(right, bg=PANEL)
        bottom.pack(fill=tk.X, padx=12, pady=10)
        self.message_entry = tk.Entry(bottom, bg='#fff5b8', fg=FG, insertbackground=FG, font=('Arial', 12))
        self.message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8))
        self.message_entry.bind('<Return>', self.on_send_clicked)
        tk.Button(bottom, text='Send', command=self.on_send_clicked, bg=ACCENT, fg=FG).pack(side=tk.LEFT)

    # ----------------- Observer -----------------
    def update(self, event_type, payload):
        if event_type == 'session_created':
            self.refresh_sessions()
        elif event_type == 'message_received':
            session = payload['session']
            message = payload['message']
            if session.session_id == self.selected_session_id:
                self.append_message(message)
            else:
                self.refresh_sessions()

    # ----------------- Session Handling -----------------
    def _periodic_refresh(self):
        self.refresh_sessions()
        self.update_status()
        self.after(1000, self._periodic_refresh)

    def refresh_sessions(self):
        self.session_listbox.delete(0, tk.END)
        self._index_to_sid = []
        q = self.search_var.get().lower() if hasattr(self, 'search_var') else ''
        for s in self.engine.sessions:
            if q and q not in s.name.lower():
                continue
            label = s.name
            if s.unread_count:
                label = f"* {label} ({s.unread_count})"
            self.session_listbox.insert(tk.END, label)
            self._index_to_sid.append(s.session_id)

    def on_session_select(self, event):
        sel = event.widget.curselection()
        if not sel:
            return
        idx = sel[0]
        sid = self._index_to_sid[idx]
        self.open_session(sid)

    def open_session(self, session_id):
        session = self.engine.get_session(session_id)
        if not session:
            return
        self.selected_session_id = session.session_id
        session.clear_unread()
        self.refresh_sessions()
        self.chat_title.config(text=session.name)
        self.update_status()
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.delete('1.0', tk.END)
        for m in session.messages:
            decorated = TimestampDecorator(m)
            self.chat_area.insert(tk.END, decorated.render() + '\n')
        self.chat_area.config(state=tk.DISABLED)
        self.chat_area.see(tk.END)

    def append_message(self, message):
        self.chat_area.config(state=tk.NORMAL)
        decorated = TimestampDecorator(message)
        self.chat_area.insert(tk.END, decorated.render() + '\n')
        self.chat_area.config(state=tk.DISABLED)
        self.chat_area.see(tk.END)

    # ----------------- New Session & Messages -----------------
    def create_new_session(self):
        name = simpledialog.askstring('New Session', 'Enter session name:')
        if not name:
            return
        from engine.builder import ChatSessionBuilder
        b = ChatSessionBuilder()
        s = b.set_name(name).add_member('You').build()
        s.add_message(SystemMessage(f'Session "{name}" created at {datetime.now().strftime("%H:%M:%S")}'))
        self.engine.create_session(s)
        self.refresh_sessions()

    def on_send_clicked(self, event=None):
        text = self.message_entry.get().strip()
        if not text or not self.selected_session_id:
            return
        msg = MessageFactory.create('text', 'You', text)
        self.append_message(msg)
        self.message_entry.delete(0, tk.END)
        self.engine.send_message(self.selected_session_id, msg)
        threading.Thread(target=self.simulate_typing_and_auto_reply, args=(self.selected_session_id,), daemon=True).start()

    def simulate_typing_and_auto_reply(self, session_id):
        session = self.engine.get_session(session_id)
        if not session:
            return
        for dots in ['.', '..', '...']:
            self.typing_var.set(f"{session.name} is typing{dots}")
            time.sleep(0.4)
        self.typing_var.set('')
        reply = MessageFactory.create('text', 'Bot', 'Auto-reply: how can i help you!')
        self.engine.route_message(session_id, reply)

    # ----------------- Status & Search -----------------
    def update_status(self):
        session = self.engine.get_session(self.selected_session_id) if self.selected_session_id else None
        if not session:
            self.status_label.config(text='')
            return
        if session.is_online:
            self.status_label.config(text='Online', fg=ACCENT)
        else:
            self.status_label.config(text=f'Last seen at {session.last_seen.strftime("%H:%M")}', fg=MUTED)

    def search_in_session(self):
        if not self.selected_session_id:
            messagebox.showinfo('No session selected', 'Open a session and then search.')
            return
        q = simpledialog.askstring('Search', 'Enter search query:')
        if not q:
            return
        session = self.engine.get_session(self.selected_session_id)
        results = session.search(q)
        if not results:
            messagebox.showinfo('Search', 'No matches found.')
            return
        win = tk.Toplevel(self)
        win.title('Search results')
        txt = scrolledtext.ScrolledText(win, width=80, height=20)
        txt.pack(fill=tk.BOTH, expand=True)
        for m in results:
            txt.insert(tk.END, TimestampDecorator(m).render() + '\n')
        txt.config(state=tk.DISABLED)

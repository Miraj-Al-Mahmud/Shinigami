import os
import re
import sqlite3
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import time
import regex as re

DB_FILE = "view_history.db"

# Regex pattern for typical episode filenames
EPISODE_PATTERN = re.compile(r"(?P<show>.+?)\.?[ _-]?S(?P<season>\d{2})E(?P<episode>\d{2})", re.IGNORECASE)

class VideoTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TV Series Tracker")
        self.root.geometry("600x400")
        
        self.directory = tk.StringVar()
        self.is_monitoring = False

        self.setup_database()
        self.create_widgets()

    def setup_database(self):
        self.conn = sqlite3.connect(DB_FILE)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT,
                show TEXT,
                season INTEGER,
                episode INTEGER,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()

    def create_widgets(self):
        frm = tk.Frame(self.root)
        frm.pack(pady=10)

        tk.Label(frm, text="Watch Folder:").pack(side=tk.LEFT)
        tk.Entry(frm, textvariable=self.directory, width=40).pack(side=tk.LEFT, padx=5)
        tk.Button(frm, text="Browse", command=self.browse_folder).pack(side=tk.LEFT)

        self.start_btn = tk.Button(self.root, text="Start Monitoring", command=self.toggle_monitoring)
        self.start_btn.pack(pady=5)

        self.tree = ttk.Treeview(self.root, columns=("Filename", "Show", "S", "E", "Next"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.pack(fill=tk.BOTH, expand=True)

    def browse_folder(self):
        path = filedialog.askdirectory()
        if path:
            self.directory.set(path)

    def toggle_monitoring(self):
        if not self.is_monitoring:
            self.is_monitoring = True
            self.start_btn.config(text="Stop Monitoring")
            threading.Thread(target=self.monitor_folder, daemon=True).start()
        else:
            self.is_monitoring = False
            self.start_btn.config(text="Start Monitoring")

    def monitor_folder(self):
        seen = set()
        while self.is_monitoring:
            folder = self.directory.get()
            if os.path.isdir(folder):
                for file in os.listdir(folder):
                    if file.endswith((".mp4", ".mkv", ".avi")) and file not in seen:
                        seen.add(file)
                        match = EPISODE_PATTERN.search(file)
                        if match:
                            show = match.group("show").replace(".", " ").strip()
                            season = int(match.group("season"))
                            episode = int(match.group("episode"))
                            self.save_to_db(file, show, season, episode)
                            self.display_entry(file, show, season, episode)
            time.sleep(5)

    def save_to_db(self, filename, show, season, episode):
        self.cursor.execute(
            "INSERT INTO history (filename, show, season, episode) VALUES (?, ?, ?, ?)",
            (filename, show, season, episode)
        )
        self.conn.commit()

    def display_entry(self, filename, show, season, episode):
        next_episode = f"S{season:02}E{episode+1:02}"
        self.tree.insert("", "end", values=(filename, show, season, episode, next_episode))

def main():
    root = tk.Tk()
    app = VideoTrackerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

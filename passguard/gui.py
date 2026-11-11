import tkinter as tk
from tkinter import messagebox, scrolledtext
from datetime import datetime
from passguard.checker import check_strength, get_strength_label
from passguard.generator import generate_password
from passguard.hasher import hash_password
from passguard.history import HistoryManager


class PassGuardApp:
    """Main application window for PassGuard."""

    # Color theme
    BG_COLOR = "#1e1e2e"
    CARD_BG = "#2a2a3c"
    TEXT_COLOR = "#e0e0e0"
    ACCENT_GREEN = "#4CAF50"
    ACCENT_BLUE = "#2196F3"
    ACCENT_RED = "#f44336"
    ACCENT_PURPLE = "#9c27b0"
    INPUT_BG = "#3a3a4c"
    BORDER_COLOR = "#444466"

    def __init__(self):
        self.history_manager = HistoryManager()
        self.root = tk.Tk()
        self.root.title("PassGuard - Password Security App")
        self.root.geometry("700x600")
        self.root.resizable(False, False)
        self.root.configure(bg=self.BG_COLOR)
        self.create_widgets()

    def create_widgets(self):
        """Create all the UI widgets with a modern dark theme."""

        # --- Title Header ---
        title_frame = tk.Frame(self.root, bg=self.BG_COLOR)
        title_frame.pack(fill=tk.X, padx=20, pady=(15, 5))
        tk.Label(title_frame, text="🔐 PassGuard", font=("Segoe UI", 20, "bold"),
                 fg=self.ACCENT_GREEN, bg=self.BG_COLOR).pack(anchor=tk.W)
        tk.Label(title_frame, text="Password Security Desktop App", font=("Segoe UI", 10),
                 fg="#888899", bg=self.BG_COLOR).pack(anchor=tk.W)

        # --- Main Content Area ---
        main_frame = tk.Frame(self.root, bg=self.BG_COLOR)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # --- Card 1: Password Input & Strength ---
        card1 = tk.Frame(main_frame, bg=self.CARD_BG, highlightbackground=self.BORDER_COLOR, highlightthickness=1)
        card1.pack(fill=tk.X, pady=5)

        tk.Label(card1, text="🔑 Password Checker", font=("Segoe UI", 12, "bold"),
                 fg=self.TEXT_COLOR, bg=self.CARD_BG).pack(anchor=tk.W, padx=15, pady=(12, 5))

        input_frame = tk.Frame(card1, bg=self.CARD_BG)
        input_frame.pack(fill=tk.X, padx=15, pady=5)
        self.password_var = tk.StringVar()
        self.password_entry = tk.Entry(input_frame, textvariable=self.password_var, show="*",
                                       font=("Consolas", 13), bg=self.INPUT_BG, fg=self.TEXT_COLOR,
                                       insertbackground=self.ACCENT_GREEN, relief=tk.FLAT, bd=0, width=40)
        self.password_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.password_entry.bind("<KeyRelease>", self.on_password_change)

        # Strength bar
        bar_frame = tk.Frame(card1, bg=self.CARD_BG)
        bar_frame.pack(fill=tk.X, padx=15, pady=(5, 12))
        self.strength_label = tk.Label(bar_frame, text="Start typing to check strength",
                                       font=("Segoe UI", 10), fg="#888899", bg=self.CARD_BG)
        self.strength_label.pack(anchor=tk.W)
        self.strength_bar_bg = tk.Canvas(bar_frame, width=620, height=12, bg="#3a3a4c",
                                         highlightthickness=0, bd=0)
        self.strength_bar_bg.pack(fill=tk.X, pady=3)
        self.strength_bar_fg = self.strength_bar_bg.create_rectangle(0, 0, 0, 12, fill="#555566", outline="")

        # --- Card 2: Password Generator ---
        card2 = tk.Frame(main_frame, bg=self.CARD_BG, highlightbackground=self.BORDER_COLOR, highlightthickness=1)
        card2.pack(fill=tk.X, pady=5)

        tk.Label(card2, text="⚡ Password Generator", font=("Segoe UI", 12, "bold"),
                 fg=self.TEXT_COLOR, bg=self.CARD_BG).pack(anchor=tk.W, padx=15, pady=(12, 5))

        gen_frame = tk.Frame(card2, bg=self.CARD_BG)
        gen_frame.pack(fill=tk.X, padx=15, pady=5)
        self.generated_var = tk.StringVar()
        self.generated_entry = tk.Entry(gen_frame, textvariable=self.generated_var,
                                        font=("Consolas", 12), bg=self.INPUT_BG, fg=self.ACCENT_GREEN,
                                        relief=tk.FLAT, bd=0, state="readonly", width=40)
        self.generated_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        btn_frame = tk.Frame(card2, bg=self.CARD_BG)
        btn_frame.pack(padx=15, pady=(0, 12))
        tk.Button(btn_frame, text="⚡ Generate", command=self.generate,
                  bg=self.ACCENT_GREEN, fg="white", font=("Segoe UI", 10, "bold"),
                  relief=tk.FLAT, cursor="hand2", bd=0, width=12).pack(side=tk.LEFT, padx=3)
        tk.Button(btn_frame, text="📋 Copy", command=self.copy_password,
                  bg=self.ACCENT_BLUE, fg="white", font=("Segoe UI", 10, "bold"),
                  relief=tk.FLAT, cursor="hand2", bd=0, width=10).pack(side=tk.LEFT, padx=3)
        tk.Button(btn_frame, text="💾 Save", command=self.save_password,
                  bg="#FF9800", fg="white", font=("Segoe UI", 10, "bold"),
                  relief=tk.FLAT, cursor="hand2", bd=0, width=10).pack(side=tk.LEFT, padx=3)

        # --- Card 3: SHA-256 Hash ---
        card3 = tk.Frame(main_frame, bg=self.CARD_BG, highlightbackground=self.BORDER_COLOR, highlightthickness=1)
        card3.pack(fill=tk.X, pady=5)

        tk.Label(card3, text="🔒 SHA-256 Hash", font=("Segoe UI", 12, "bold"),
                 fg=self.TEXT_COLOR, bg=self.CARD_BG).pack(anchor=tk.W, padx=15, pady=(12, 5))

        hash_frame = tk.Frame(card3, bg=self.CARD_BG)
        hash_frame.pack(fill=tk.X, padx=15, pady=5)
        self.hash_text = scrolledtext.ScrolledText(hash_frame, height=2, font=("Consolas", 9),
                                                   bg=self.INPUT_BG, fg=self.ACCENT_PURPLE,
                                                   insertbackground=self.ACCENT_PURPLE,
                                                   relief=tk.FLAT, bd=0, state=tk.DISABLED,
                                                   wrap=tk.WORD)
        self.hash_text.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        hash_btn_frame = tk.Frame(card3, bg=self.CARD_BG)
        hash_btn_frame.pack(padx=15, pady=(0, 12))
        tk.Button(hash_btn_frame, text="📋 Copy Hash", command=self.copy_hash,
                  bg=self.ACCENT_PURPLE, fg="white", font=("Segoe UI", 10, "bold"),
                  relief=tk.FLAT, cursor="hand2", bd=0, width=12).pack(side=tk.LEFT, padx=3)

        # --- Card 4: History (Collapsible) ---
        card4 = tk.Frame(main_frame, bg=self.CARD_BG, highlightbackground=self.BORDER_COLOR, highlightthickness=1)
        card4.pack(fill=tk.BOTH, expand=True, pady=5)

        # Clickable header for collapsing
        self.history_collapsed = False
        self.history_header = tk.Label(card4, text="📜 History ▼", font=("Segoe UI", 12, "bold"),
                                       fg=self.ACCENT_BLUE, bg=self.CARD_BG, cursor="hand2")
        self.history_header.pack(fill=tk.X, padx=15, pady=(12, 5))
        self.history_header.bind("<Button-1>", self.toggle_history)

        self.history_content = tk.Frame(card4, bg=self.CARD_BG)
        self.history_content.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 5))

        hist_frame = tk.Frame(self.history_content, bg=self.CARD_BG)
        hist_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        self.history_text = scrolledtext.ScrolledText(hist_frame, height=5, font=("Consolas", 9),
                                                      bg=self.INPUT_BG, fg=self.TEXT_COLOR,
                                                      insertbackground=self.ACCENT_GREEN,
                                                      relief=tk.FLAT, bd=0, state=tk.DISABLED)
        self.history_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        hist_btn_frame = tk.Frame(self.history_content, bg=self.CARD_BG)
        hist_btn_frame.pack(padx=0, pady=(0, 12))
        tk.Button(hist_btn_frame, text="🗑️ Clear History", command=self.clear_history,
                  bg=self.ACCENT_RED, fg="white", font=("Segoe UI", 10, "bold"),
                  relief=tk.FLAT, cursor="hand2", bd=0, width=15).pack(side=tk.LEFT, padx=3)

    def on_password_change(self, event):
        """Update strength bar and hash when password changes."""
        password = self.password_var.get()
        if not password:
            self.strength_label.config(text="Start typing to check strength", fg="#888899")
            self.strength_bar_bg.coords(self.strength_bar_fg, 0, 0, 0, 12)
            self.hash_text.config(state=tk.NORMAL)
            self.hash_text.delete(1.0, tk.END)
            self.hash_text.config(state=tk.DISABLED)
            return
        score = check_strength(password)
        label = get_strength_label(score)
        color = self.get_color(score)
        self.strength_label.config(text=f"Strength: {label} ({score}/100)", fg=color)
        width = int(620 * score / 100)
        self.strength_bar_bg.coords(self.strength_bar_fg, 0, 0, width, 12)
        self.strength_bar_bg.itemconfig(self.strength_bar_fg, fill=color)
        # Update hash display
        hashed = hash_password(password)
        self.hash_text.config(state=tk.NORMAL)
        self.hash_text.delete(1.0, tk.END)
        self.hash_text.insert(tk.END, hashed)
        self.hash_text.config(state=tk.DISABLED)
        self.history_manager.add(password, score, label)
        self.update_history_display()

    def get_color(self, score):
        """Return color based on strength score."""
        if score >= 80:
            return "#4CAF50"
        elif score >= 60:
            return "#76c900"
        elif score >= 40:
            return "#FF9800"
        else:
            return "#f44336"

    def generate(self):
        """Generate a random password and display it."""
        pwd = generate_password()
        self.generated_var.set(pwd)
        self.generated_entry.config(state=tk.NORMAL)
        self.generated_entry.config(state="readonly")

    def copy_password(self):
        """Copy generated password to clipboard."""
        pwd = self.generated_var.get()
        if pwd:
            self.root.clipboard_clear()
            self.root.clipboard_append(pwd)
            messagebox.showinfo("Copied", "Password copied to clipboard!", parent=self.root)
        else:
            messagebox.showwarning("Empty", "Generate a password first!", parent=self.root)

    def copy_hash(self):
        """Copy SHA-256 hash to clipboard."""
        hashed = self.hash_text.get(1.0, tk.END).strip()
        if hashed:
            self.root.clipboard_clear()
            self.root.clipboard_append(hashed)
            messagebox.showinfo("Copied", "Hash copied to clipboard!", parent=self.root)
        else:
            messagebox.showwarning("Empty", "Type a password to see the hash!", parent=self.root)

    def toggle_history(self, event):
        """Toggle the history section visibility."""
        self.history_collapsed = not self.history_collapsed
        if self.history_collapsed:
            self.history_content.pack_forget()
            self.history_header.config(text="📜 History ▶")
        else:
            self.history_content.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 5))
            self.history_header.config(text="📜 History ▼")

    def save_password(self):
        """Save the generated password to a file."""
        pwd = self.generated_var.get()
        if pwd:
            try:
                with open("saved_passwords.txt", "a", encoding="utf-8") as f:
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    f.write(f"[{timestamp}] {pwd}\n")
                messagebox.showinfo("Saved", "Password saved to saved_passwords.txt!", parent=self.root)
            except Exception as e:
                messagebox.showerror("Error", f"Could not save password:\n{e}", parent=self.root)
        else:
            messagebox.showwarning("Empty", "Generate a password first!", parent=self.root)

    def clear_history(self):
        """Clear the history."""
        self.history_manager.clear()
        self.update_history_display()

    def update_history_display(self):
        """Update the history text display."""
        self.history_text.config(state=tk.NORMAL)
        self.history_text.delete(1.0, tk.END)
        for entry in self.history_manager.get_history():
            line = f"  ⏰ {entry['time']}  |  Score: {entry['score']}  |  {entry['label']}\n"
            self.history_text.insert(tk.END, line)
        self.history_text.config(state=tk.DISABLED)

    def run(self):
        """Start the application."""
        self.root.mainloop()

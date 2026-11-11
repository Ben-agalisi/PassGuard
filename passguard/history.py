from datetime import datetime


class HistoryManager:
    """Manage the password check history."""
    def __init__(self):
        self.history = []

    def add(self, password, score, label):
        """Add a password check to the history."""
        entry = {
            'password': '****',
            'score': score,
            'label': label,
            'time': datetime.now().strftime('%H:%M:%S'),
        }
        self.history.append(entry)

    def clear(self):
        """Clear all history entries."""
        self.history = []

    def get_history(self):
        """Return the history list."""
        return self.history
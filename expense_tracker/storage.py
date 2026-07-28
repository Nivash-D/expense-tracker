"""Handles loading and saving expenses to a JSON file on disk."""

import json
from pathlib import Path
from typing import List

from expense_tracker.models import Expense

DEFAULT_DATA_FILE = Path.home() / ".expense_tracker" / "expenses.json"


class Storage:
    def __init__(self, filepath: Path = DEFAULT_DATA_FILE):
        self.filepath = filepath
        self.filepath.parent.mkdir(parents=True, exist_ok=True)
        if not self.filepath.exists():
            self._write([])

    def _read(self) -> List[dict]:
        with open(self.filepath, "r") as f:
            return json.load(f)

    def _write(self, data: List[dict]) -> None:
        with open(self.filepath, "w") as f:
            json.dump(data, f, indent=2)

    def load_all(self) -> List[Expense]:
        raw = self._read()
        return [Expense.from_dict(item) for item in raw]

    def save_all(self, expenses: List[Expense]) -> None:
        self._write([e.to_dict() for e in expenses])

    def next_id(self) -> int:
        expenses = self.load_all()
        if not expenses:
            return 1
        return max(e.id for e in expenses) + 1

    def add(self, expense: Expense) -> None:
        expenses = self.load_all()
        expenses.append(expense)
        self.save_all(expenses)

    def delete(self, expense_id: int) -> bool:
        expenses = self.load_all()
        filtered = [e for e in expenses if e.id != expense_id]
        if len(filtered) == len(expenses):
            return False  # nothing was deleted
        self.save_all(filtered)
        return True

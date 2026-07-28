"""Data model for a single expense entry."""

from dataclasses import dataclass, asdict
from datetime import date


@dataclass
class Expense:
    id: int
    amount: float
    category: str
    description: str
    date: str  # stored as ISO format string, e.g. "2026-07-28"

    @classmethod
    def create(cls, id: int, amount: float, category: str, description: str, expense_date: str = None):
        """Factory method: builds an Expense, defaulting date to today."""
        return cls(
            id=id,
            amount=round(amount, 2),
            category=category.strip().lower(),
            description=description.strip(),
            date=expense_date or date.today().isoformat(),
        )

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Expense":
        return cls(**data)

"""Command-line interface for the expense tracker."""

import argparse
import sys
from collections import defaultdict

from expense_tracker.models import Expense
from expense_tracker.storage import Storage


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="expense",
        description="A simple command-line expense tracker.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # add
    add_parser = subparsers.add_parser("add", help="Add a new expense")
    add_parser.add_argument("--amount", type=float, required=True, help="Amount spent")
    add_parser.add_argument("--category", type=str, required=True, help="Category, e.g. food, transport")
    add_parser.add_argument("--description", type=str, default="", help="Optional note")
    add_parser.add_argument("--date", type=str, default=None, help="Date in YYYY-MM-DD (defaults to today)")

    # list
    list_parser = subparsers.add_parser("list", help="List expenses")
    list_parser.add_argument("--category", type=str, default=None, help="Filter by category")

    # summary
    summary_parser = subparsers.add_parser("summary", help="Show total spending, grouped by category")

    # delete
    delete_parser = subparsers.add_parser("delete", help="Delete an expense by ID")
    delete_parser.add_argument("id", type=int, help="ID of the expense to delete")

    return parser


def cmd_add(args, storage: Storage):
    expense = Expense.create(
        id=storage.next_id(),
        amount=args.amount,
        category=args.category,
        description=args.description,
        expense_date=args.date,
    )
    storage.add(expense)
    print(f"Added expense #{expense.id}: ${expense.amount:.2f} [{expense.category}] {expense.description}")


def cmd_list(args, storage: Storage):
    expenses = storage.load_all()
    if args.category:
        expenses = [e for e in expenses if e.category == args.category.strip().lower()]

    if not expenses:
        print("No expenses found.")
        return

    print(f"{'ID':<5}{'Date':<12}{'Amount':<10}{'Category':<15}Description")
    print("-" * 60)
    for e in sorted(expenses, key=lambda x: x.date):
        print(f"{e.id:<5}{e.date:<12}${e.amount:<9.2f}{e.category:<15}{e.description}")


def cmd_summary(args, storage: Storage):
    expenses = storage.load_all()
    if not expenses:
        print("No expenses found.")
        return

    totals = defaultdict(float)
    for e in expenses:
        totals[e.category] += e.amount

    grand_total = sum(totals.values())

    print(f"{'Category':<15}Total")
    print("-" * 30)
    for category, total in sorted(totals.items(), key=lambda x: -x[1]):
        print(f"{category:<15}${total:.2f}")
    print("-" * 30)
    print(f"{'TOTAL':<15}${grand_total:.2f}")


def cmd_delete(args, storage: Storage):
    success = storage.delete(args.id)
    if success:
        print(f"Deleted expense #{args.id}")
    else:
        print(f"No expense found with ID {args.id}")
        sys.exit(1)


def main():
    parser = build_parser()
    args = parser.parse_args()
    storage = Storage()

    commands = {
        "add": cmd_add,
        "list": cmd_list,
        "summary": cmd_summary,
        "delete": cmd_delete,
    }
    commands[args.command](args, storage)


if __name__ == "__main__":
    main()

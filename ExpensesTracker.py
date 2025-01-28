import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

FILE_NAME = "expenses.csv"

def initialize_file():
    if not os.path.exists(FILE_NAME):
        df = pd.DataFrame(columns=["Date", "Category", "Amount", "Description"])
        df.to_csv(FILE_NAME, index=False)

def add_expense(date, category, amount, description):
    expense = pd.DataFrame({
        "Date": [date],
        "Category": [category],
        "Amount": [amount],
        "Description": [description],
    })
    df = pd.read_csv(FILE_NAME, dtype={"Date": str, "Category": str, "Amount": float, "Description": str})
    expense = expense.dropna(axis=1, how='all')
    df = pd.concat([df, expense], ignore_index=True)
    df.to_csv(FILE_NAME, index=False)
    print("Expense added successfully!")

def view_expenses():
    df = pd.read_csv(FILE_NAME)
    if df.empty:
        print("No expenses found.")
    else:
        print(df)

def plot_expenses_by_category():
    df = pd.read_csv(FILE_NAME)
    if df.empty:
        print("No expenses to plot.")
        return
    category_totals = df.groupby("Category")["Amount"].sum().sort_values(ascending=False)
    colors = plt.get_cmap('tab10').colors
    plt.figure(figsize=(8, 8))
    category_totals.plot(kind="pie", autopct="%.2f%%", colors=colors, startangle=90, legend=False)
    plt.title("Expenses by Category", fontsize=14)
    plt.ylabel("")
    plt.tight_layout()
    plt.show()

def plot_expenses_over_time():
    df = pd.read_csv(FILE_NAME)
    if df.empty:
        print("No expenses to plot.")
        return
    df["Date"] = pd.to_datetime(df["Date"])
    time_series = df.groupby("Date")["Amount"].sum()
    plt.figure(figsize=(10, 6))
    time_series.plot(kind="line", marker="o", color='b', linestyle='-', linewidth=2, markersize=6)
    plt.title("Expenses Over Time", fontsize=14)
    plt.xlabel("Date", fontsize=12)
    plt.ylabel("Total Expense", fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def get_valid_input(prompt, input_type, error_msg="Invalid input. Please try again."):
    while True:
        try:
            user_input = input(prompt)
            if input_type == "date":
                datetime.strptime(user_input, "%Y-%m-%d")
            elif input_type == "float":
                user_input = float(user_input)
            return user_input
        except ValueError:
            print(error_msg)

def main_menu():
    initialize_file()
    while True:
        print("\n--- Personal Expense Tracker ---")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Plot Expenses by Category")
        print("4. Plot Expenses Over Time")
        print("5. Exit")
        choice = input("Enter your choice (1-5): ")
        if choice == "1":
            date = get_valid_input("Enter date (YYYY-MM-DD): ", "date")
            category = input("Enter category (e.g., Food, Rent, Entertainment): ")
            amount = get_valid_input("Enter amount: ", "float")
            description = input("Enter description: ")
            add_expense(date, category, amount, description)
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            plot_expenses_by_category()
        elif choice == "4":
            plot_expenses_over_time()
        elif choice == "5":
            print("Exiting the tracker. Goodbye!")
            break
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main_menu()

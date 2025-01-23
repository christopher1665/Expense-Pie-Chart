import csv
import os
import matplotlib.pyplot as plt

CSV_FILE_NAME = "expenses.csv"

def read_expenses_from_csv():
    expenses_by_month = {}
    try:
        with open(CSV_FILE_NAME, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                month = int(row["Month"])
                expenses = {key: float(value) for key, value in row.items() if key != "Month"}
                if month not in expenses_by_month:
                    expenses_by_month[month] = expenses
    except FileNotFoundError:
        print(f"Error: File '{CSV_FILE_NAME}' not found. Please ensure the file exists.")
        expenses_by_month = {'error': 0}
    return expenses_by_month

def save_expenses_to_csv(expenses, month):
    file_exists = os.path.isfile(CSV_FILE_NAME)

    if file_exists:
        with open(CSV_FILE_NAME, mode='r') as file:
            rows = list(csv.reader(file))
        if len(rows) > 12:
            print("More than 12 months of data found. Deleting the oldest month...")
            with open(CSV_FILE_NAME, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(rows[:1] + rows[2:])

    try:
        with open(CSV_FILE_NAME, mode='a' if file_exists else 'w', newline='') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["Month", "Rent", "Gas", "Food", "Clothing", "Car payments", "Misc"])
            writer.writerow([month] + list(expenses.values()))
        print(f"Expenses for month {month} successfully saved to '{CSV_FILE_NAME}'.")
    except Exception as e:
        print(f"Error saving expenses to file: {e}")

def get_expenses_from_user():
    categories = ["Rent", "Gas", "Food", "Clothing", "Car payments", "Misc"]
    expenses = {}
    print("Enter your expenses for the following categories:")
    for category in categories:
        while True:
            try:
                amount = float(input(f"{category}: $"))
                expenses[category] = amount
                break
            except ValueError:
                print("Please enter a valid number.")
    return expenses

def plot_expenses_pie_chart(expenses, title="Expense Distribution"):
    labels = expenses.keys()
    sizes = expenses.values()
    total_expenses = sum(sizes)

    print(f"\nSummary of {title}:")
    for category, amount in expenses.items():
        print(f"  {category}: ${amount:.2f}")
    print(f"\nTotal Expenses: ${total_expenses:.2f}")

    plt.figure(figsize=(8, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title(f"{title} (Total: ${total_expenses:.2f})")
    plt.axis('equal')
    plt.show()

def get_valid_menu_choice():
    while True:
        choice = input()
        if choice.isdigit() and choice in {"1", "2", "3"}:
            return choice
        print("Invalid choice. Please enter 1, 2, or 3.")

def get_valid_month_choice(available_months):
    while True:
        print(f"Available months: {', '.join(map(str, available_months))}")
        print("Enter the month you want to display or '0' for all months combined:")
        choice = input("Your choice: ").strip()
        if choice.isdigit():
            choice = int(choice)
            if choice == 0 or choice in available_months:
                return choice
        print("Invalid choice. Please select a valid option.")

def main():
    current_month = 1

    while True:
        print("\nWelcome to the Expense Pie Chart Program!")
        print("1. Add expenses to the CSV file.")
        print("2. Read and display expenses (specific month or all months).")
        print("3. Exit the program.")

        choice = get_valid_menu_choice()
        
        if choice == "1":
            while True:
                expenses = get_expenses_from_user()
                save_expenses_to_csv(expenses, current_month)

                current_month += 1
                if current_month > 12:
                    current_month = 1  # Wrap around to January
                    break
        elif choice == "2":
            expenses_by_month = read_expenses_from_csv()
            if not expenses_by_month:
                print("No expenses found in the CSV file.")
            elif expenses_by_month == {'error': 0}:
                None
            else:
                available_months = sorted(expenses_by_month.keys())
                selected_month = get_valid_month_choice(available_months)
                
                if selected_month == 0:
                    # Combine all months into one summary
                    combined_expenses = {}
                    for month_expenses in expenses_by_month.values():
                        for category, amount in month_expenses.items():
                            combined_expenses[category] = combined_expenses.get(category, 0) + amount
                    plot_expenses_pie_chart(combined_expenses, title="All Months Combined")
                else:
                    # Display the selected month
                    plot_expenses_pie_chart(expenses_by_month[selected_month], title=f"Month {selected_month}")
        elif choice == "3":
            print("Exiting the program. Goodbye!")
            break

if __name__ == "__main__":
    main()

def get_participants():
    num_participants = int(input("How many participants? "))
    participants = []
    balances = {}
    for _ in range(num_participants):
        name = input("Enter participant name: ")
        participants.append(name)
        balances[name] = 0.0
    return participants, balances

def add_expenses(balances):
    while True:
        cmd = input("Add expense? (y/n) ").lower()
        if cmd != 'y':
            break
        payer = input("Who paid? ")
        try:
            amount = float(input("How much? "))
        except ValueError:
            print("Invalid amount. Please enter a valid number.")
            continue

        if payer in balances:
            balances[payer] += amount

def calculate_share(participants, balances):
    total_expenses = sum(balances.values())
    share = total_expenses / len(participants)
    return total_expenses, share

def display_summary(participants, balances, share):
    print("\nExpense Summary:")
    for name in participants:
        balance = balances[name] - share
        if balance > 0:
            print(f"{name} should receive {balance:.2f}")
        elif balance < 0:
            print(f"{name} should pay {-balance:.2f}")
        else:
            print(f"{name} is settled")

def main():
    print("Friends Expense Splitter")
    participants, balances = get_participants()
    add_expenses(balances)
    total_expenses, share = calculate_share(participants, balances)
    print(f"\nTotal expenses: {total_expenses:.2f}")
    display_summary(participants, balances, share)

if __name__ == "__main__":
    main()
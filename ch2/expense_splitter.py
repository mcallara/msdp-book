def main():
    print("Friends Expense Splitter")
    num_participants = int(input("How many participants? "))
    participants = []
    balances = {}
    for _ in range(num_participants):
        name = input("Enter participant name: ")
        participants.append(name)
        balances[name] = 0.0

    while True:
        cmd = input("Add expense? (y/n) ").lower()
        if cmd != 'y':
            break
        payer = input("Who paid? ")
        amount = input("How much? ")
        amount =  float(amount)  
        if payer in balances:
            balances[payer] += amount

    total_expenses = sum(balances.values())
    share = total_expenses / len(participants)
    print("\nExpense Summary:")
    for name in participants:
        balance = balances[name] - share
        if balance > 0:
            print(f"{name} should receive {balance:.2f}")
        elif balance < 0:
            print(f"{name} should pay {-balance:.2f}")
        else:
            print(f"{name} is settled")

if __name__ == "__main__":
    main()

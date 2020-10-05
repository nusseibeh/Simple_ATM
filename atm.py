#! /usr/bin/python3
class MyAccount:
    def __init__(self, name, card_number, pin_number, account_number=None, balance=None):
        self.name = name
        self.card_number = card_number
        self.pin_number = pin_number
        self.account_number = account_number

        self.balance = balance

    def getBalance(self):
        return self.balance
    
    def deposit(self, amount):
        self.balance += amount
    
    def withdraw(self, amount):
        self.balance -= amount

class MyAtm:
    def __init__(self, cash=0, accounts=None):
        self.cash = cash
        self.accounts = accounts

    def home(self):
        """ Default state of the ATM. Waits for a card to be inserted """
        card_number = input("Welcome to Bear Bank ATM! Please insert your debit card to continue\n>> ")
        if card_number in ['q','Q','quit','Quit','QUIT','exit','EXIT']:
            print("HOSTILE INPUT DETECTED! ABORTING ATM CONTROL SOFTWARE!")
            exit()
        else:
            self.readCard(card_number)

    def readCard(self, card_number):
        """ Function that reads the card.
            Functions that interface with the card reader should be called here """
        # TODO: Add HW function calls that read the card here
        print("Card Read")
        cards = [str(account.card_number) for account in self.accounts]
        avail_accounts = [account for account in self.accounts]
        if card_number not in cards:
            print("Card number could not be found in database")
            return -1
        else:
            customer_account = avail_accounts[cards.index(card_number)]
        self.readPin(customer_account)

    def readPin(self, customer_account):
        """ Function that reads the pin number from user """
        attempts = 0
        while(attempts < 3):
            pin_number = input("Please enter in your pin number...\n>> ")
            print("Authenticating...")
            if pin_number == str(customer_account.pin_number):
                print("Pin number is correct")
                self.chooseAccount(customer_account)
                break
            else:
                print("Pin number does not match.")
                attempts += 1


    def chooseAccount(self, customer_account):
        """ Function that allows user to select their account to transact with"""
        print("Accounts available: {}".format(customer_account.account_number))
        attempts = 0
        while(attempts < 3):
            account_selected = input("Select account\n>> ")
            if account_selected == str(customer_account.account_number):
                print("You selected account: {}".format(account_selected))
                self.accountHome(customer_account)
                return 1
            else:
                attempts += 1
        return -1

    def accountHome(self, account):
        """ Landing page for customer's account. Options are check balance, withdraw, deposit, or exit """
        print("Welcome {}! What would you like to do today?".format(account.name))
        print("Options:")
        while(True):
            action = input("Check Balance [B], Withdraw Cash [W], Deposit Cash [D], or Exit [E]\n>> ")
            if action.lower() == 'b':
                print("Current balance: ${}".format(self.getBalance(account)))
            elif action.lower() == 'w':
                amount = input("How much would you like to withdraw?\n>> ")
                self.withdraw(account, amount)
            elif action.lower() == 'd':
                amount = input("How much would you like to deposit?\n>> ")
                self.deposit(account, amount)
            elif action.lower() == 'e':
                print("Thank you. Returning to Home Screen...")
                return 1
            else:
                print("Command not recognized")

    def getBalance(self, account):
        """ Function that returns the balance of the provided customer account """
        return account.balance

    def deposit(self, account, amount):
        """ Function that deposits the provided amount of money into the provided customer account.
            A check on the money being deposited should be done in here """
        # TODO: Add function calls that interface with the money reader hardware here
        self.cash += int(amount)
        account.deposit(int(amount))
        print("Depositing ${}. Current balance is ${}".format(amount,account.balance))
        pass

    def withdraw(self, account, amount):
        """ Function that withdraws the provided amount of money from the provided customer account.
            A check on the money being withdrawn should be done in here """
        # TODO: Add function calls that interface with the money reader hardware here
        balance = account.getBalance()
        if balance < int(amount):
            print("Insufficient funds in account. Current balance is ${}, requested withdrawal of ${}".format(balance, amount))
            return -1
        elif int(amount) > self.cash:
            print("Insufficient funds in ATM. Sorry!")
            return -1
        else:
            self.cash -= int(amount)
            account.withdraw(int(amount))
            print("Withdrawing ${} from account. Current balance ${}".format(int(amount),account.balance))
            return 1
        return -1

    def exit(self):
        """ Function that determines user has either walked away or is done with their transaction """
        print("Transaction complete. Return to Home Screen")
        self.home()
        pass

    # The following methods are not implemented, but are stubbed for future devlopment
    
    def depositHWCtrl(self, amount):
        """ Function to interface with the ATM's cash bin and electronics to receive cash.
            Should include a check from the sensor to confirm deposit amount and counterfeit measures """
        pass

    def withdrawHWCtrl(self, amount):
        """ Function to interface with the ATM's cash bin and electronics to dispense cash """
        pass

    def checkWithBank(self, bankName, APIcommand):
        """ Function to connect with a Bank's API.
            Should include the ability to check credentials and balance """
        pass

if __name__ == "__main__":
    
    annisAccount = MyAccount("Annis",12345, 1234, 1111,0)
    annisAccount.deposit(1000)
    nusseibehAccount = MyAccount("Nusseibeh",9876, 4321, 2222, 500)
    billAccount = MyAccount("Bill",10101, 5678, 3333, 100)
    BearAtm = MyAtm(100000,[annisAccount,nusseibehAccount,billAccount])

    print(" ")
    print("ATM Setup")
    print("---------")
    print("Current cash in ATM: ${}".format(BearAtm.cash))
    for account in [annisAccount, nusseibehAccount, billAccount]:
        print(" ")
        print("Name on card: {}".format(account.name))
        print("Card number: {}".format(account.card_number))
        print("Pin number: {}".format(account.pin_number))
        print("Account number: {}".format(account.account_number))
        print("Current balance: ${}".format(account.balance))
    print("---------")

    while True:
        print(" ")
        BearAtm.home()

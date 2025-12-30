import sqlite3
import os
from cogs import record_grade
from cogs import remove_grade
from cogs import standard_detail

# Connect to the database
db = sqlite3.connect("Grade-Tracker.db")
cursor = db.cursor()


# Function to clean the terminal
def clearScreen():
    if os.name == "nt":  # If the operating system is Windows
        os.system("CLS")
    else:  # If the operating system is NOT Windows
        os.system("clear")


def main():
    clearScreen()
    print("\nHello, Welcome to your NCEA Grade Tracker")
    while True:
        print("\nWhat would you like to do?")
        print("")
        print("1. Record your grade")
        print("2. Remove your recorded grade")
        print("3. See your grade for a standard")
        print("\n4. Exit")
        print("5. Help")

        answer = input(">_ ").strip()
        if answer == "1":  # RECORD GRADE
            record_grade.record_grade()
            continue
        elif answer == "2":  # REMOVE GRADE
            remove_grade.remove_grade()
            continue
        elif answer == "3":  # STANDARD DETAILS
            standard_detail.standard_detail()
            continue
        elif answer == "4":  # EXIT
            break
        else:  # OTHER
            clearScreen()
            print("INVALID INPUT")
            continue


if __name__ == "__main__":
    main()

import sqlite3
import os
from lib import record_grade
from lib import remove_grade
from lib import standard_detail
from lib import student_detail
from console import ansi

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
        print("\nWhat would you like to do?\n")
        print("1. Record Grade")
        print("2. Remove Grade")
        print("3. Standard Result")
        print("4. Student Anaylsis")
        print(f"{ansi.Colors.RED}\n5. Exit{ansi.Colors.DEFAULT}")

        answer = input("\n>_ ").strip()
        if answer == "1":  # RECORD GRADE
            record_grade.record_grade()
            continue
        elif answer == "2":  # REMOVE GRADE
            remove_grade.remove_grade()
            continue
        elif answer == "3":  # STANDARD DETAILS
            standard_detail.standard_detail()
            continue
        elif answer == "4":  # STUDENT ANALYSIS
            student_detail.student_detail()
            continue
        elif answer == "5":  # EXIT
            break
        else:  # OTHER
            clearScreen()
            print("INVALID INPUT")
            continue


if __name__ == "__main__":
    main()

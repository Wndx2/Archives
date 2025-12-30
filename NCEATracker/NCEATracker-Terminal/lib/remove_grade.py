import sqlite3
import os

# Connect to the database
db = sqlite3.connect("Grade-Tracker.db")
cursor = db.cursor()


# Function to clean the terminal
def clearScreen():
    if os.name == "nt":  # If the operating system is Windows
        os.system("CLS")
    else:  # If the operating system is NOT Windows
        os.system("clear")


def remove_grade():
    student_id = 1  # Default student ID for personal tracker
    cursor.execute(
        "SELECT first_name, last_name FROM student WHERE student_id = ?", (student_id,)
    )
    student = cursor.fetchone()
    if not student:
        clearScreen()
        print("Default user (student ID 1) not found.")
        print("Please set up your user profile from the main menu.")
        return
    # Get the standard number from the user
    while True:
        print("\nPlease enter the number of the standard")
        standard_number = input("> ").strip()
        try:
            standard_number = int(standard_number)
            # Look for the NZQA standard in the database
            cursor.execute(
                "SELECT standard_type, level, domain, title, credits, assessment_type FROM standard WHERE standard_number = ?",
                (standard_number,),
            )
            standard = cursor.fetchone()
            if not standard:
                print("Standard not found.")
                continue
            st_type, level, domain, title, credits, assess_type = standard
            # Check if the user matches the standard they are looking for
            print(
                f"\nDo you mean {st_type} Standard - Level {level} {domain} - {title} - {credits} {assess_type} Credit(s)?"
            )
            answer = input("Yes or No > ").strip().lower()
            if answer == "yes":
                break
            if answer == "no":
                print("Please try again")
                continue
            else:
                print("Please enter Yes or No")
                continue
        except ValueError:
            print("Standard number must be an integer.")
    # See the result exist or not
    cursor.execute(
        "SELECT score FROM student_standard_grade WHERE student_id = ? AND standard_number = ?",
        (
            student_id,
            standard_number,
        ),
    )
    exist = cursor.fetchone()
    if not exist:
        clearScreen()
        print(
            f"\nYou do not have any grade recorded for standard {standard_number} yet."
        )
        print("Please try again after your grade is recorded")
        return
    else:
        score = exist[0]
        cursor.execute("SELECT name FROM grade WHERE score = ?", (score,))
        grade_name = cursor.fetchone()[0]
        # Let the user know that the result has founded if exist
        print(
            f"\nWe found the record that you have {score}, which means {grade_name} for standard {standard_number}!"
        )
        while True:
            # Ask user again to remove the result or not
            print(
                f"\nAre you sure you want to remove your grade for standard {standard_number}?"
            )
            print("If you remove the record, it cannot be cancelled.")
            answer = input("Yes or No > ").strip().lower()
            if answer == "yes":
                # Delete query
                cursor.execute(
                    "DELETE FROM student_standard_grade WHERE student_id = ? AND standard_number = ?",
                    (
                        student_id,
                        standard_number,
                    ),
                )
                db.commit()
                clearScreen()
                print("\nCompleted! Your grade record has been removed.")
                return
            elif answer == "no":
                clearScreen()
                print("Operation cancelled by user")
                return
            else:
                print("Please enter Yes or No")
                continue

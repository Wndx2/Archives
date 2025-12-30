import sqlite3
import os
from tabulate import tabulate

# Connect to the database
db = sqlite3.connect("Grade-Tracker.db")
cursor = db.cursor()


# Function to clean the terminal
def clearScreen():
    if os.name == "nt":  # If the operating system is Windows
        os.system("CLS")
    else:  # If the operating system is NOT Windows
        os.system("clear")


def student_detail():
    # Get the student ID from the user
    while True:
        print("\nPlease enter the ID of the student that you want to see the data")
        student_id = input("> ").strip()
        try:
            student_id = int(student_id)
            break
        except ValueError:
            print("Student ID must be an integer.")
    cursor.execute(
        "SELECT first_name, last_name FROM student WHERE student_id = ?", (student_id,)
    )
    student = cursor.fetchone()
    if not student:
        clearScreen()
        print("Student not found.")
        return
    # Check if the user matches the person they are looking for.
    while True:
        print(f"\nAre you looking for {student[0]} {student[1]}?")
        answer = input("Yes or No > ").strip().lower()
        if answer == "yes":
            break
        elif answer == "no":
            clearScreen()
            print("Please try again.")
            print("You can see the list of all students from choosing 3 on the menu.")
            return
        else:
            print("Please enter Yes or No")
            continue
    while True:
        # Option
        print(f"\nWhat would you like to do for {student[0]} {student[1]}?")
        print("1. View all Standards results")
        print("2. View all Achievement Standards results")
        print("3. View all Unit Standards results")
        print("4. Student's Pass Rate")
        print("5. Total gained credits")
        print("6. Exit")
        answer = input("> ").strip()
        if answer in {"1", "2", "3", "4", "5", "6"}:
            break
        else:
            print("INVALID INPUT, please enter the integer between 1 - 6")
    # See ALL recorded result
    if answer == "1":
        cursor.execute(
            """SELECT
                       student_standard_grade.standard_number,
                       standard.standard_type,
                       standard.level,
                       standard.domain,
                       standard.title,
                       standard.credits,
                       student_standard_grade.score,
                       grade.name
                       FROM student_standard_grade
                       JOIN standard
                       ON student_standard_grade.standard_number = standard.standard_number
                       JOIN grade
                       ON student_standard_grade.score = grade.score
                       WHERE student_standard_grade.student_id = ?
                       ORDER BY student_standard_grade.standard_number""",
            (student_id,),
        )
        result = cursor.fetchall()
        if result:
            clearScreen()
            headers = [
                "Standard No.",
                "Type",
                "Level",
                "Domain",
                "Title",
                "Credits",
                "Score",
                "Grade",
            ]
            print(tabulate(result, headers=headers, tablefmt="fancy_grid"))
        else:
            # If the result has not founded
            clearScreen()
            print("No standards result found for this student.")
            return
    # See ALL Achievement Standard result
    elif answer == "2":
        cursor.execute(
            """SELECT
                       student_standard_grade.standard_number,
                       standard.standard_type,
                       standard.level,
                       standard.domain,
                       standard.title,
                       standard.credits,
                       student_standard_grade.score,
                       grade.name
                       FROM student_standard_grade
                       JOIN standard
                       ON student_standard_grade.standard_number = standard.standard_number
                       JOIN grade
                       ON student_standard_grade.score = grade.score
                       WHERE student_standard_grade.student_id = ?
                       AND standard.standard_type = 'Achievement'
                       ORDER BY student_standard_grade.standard_number""",
            (student_id,),
        )
        result = cursor.fetchall()
        if result:
            clearScreen()
            headers = [
                "Standard No.",
                "Type",
                "Level",
                "Domain",
                "Title",
                "Credits",
                "Score",
                "Grade",
            ]
            print(tabulate(result, headers=headers, tablefmt="fancy_grid"))
        else:
            # If the result has not founded
            clearScreen()
            print("No Achievement Standards result found for this student.")
            return
    elif answer == "3":
        cursor.execute(
            """SELECT
                       student_standard_grade.standard_number,
                       standard.standard_type,
                       standard.level,
                       standard.domain,
                       standard.title,
                       standard.credits,
                       student_standard_grade.score,
                       grade.name
                       FROM student_standard_grade
                       JOIN standard
                       ON student_standard_grade.standard_number = standard.standard_number
                       JOIN grade
                       ON student_standard_grade.score = grade.score
                       WHERE student_standard_grade.student_id = ?
                       AND standard.standard_type = 'Unit'
                       ORDER BY student_standard_grade.standard_number""",
            (student_id,),
        )
        result = cursor.fetchall()
        if result:
            clearScreen()
            headers = [
                "Standard No.",
                "Type",
                "Level",
                "Domain",
                "Title",
                "Credits",
                "Score",
                "Grade",
            ]
            print(tabulate(result, headers=headers, tablefmt="fancy_grid"))
        else:
            # If the result has not founded
            clearScreen()
            print("No Unit Standards result found for this student.")
            return
    # Pass rate
    elif answer == "4":
        # Total attempted standard count
        cursor.execute(
            "SELECT COUNT(*) FROM student_standard_grade WHERE student_id = ?",
            (student_id,),
        )
        total_attempted = cursor.fetchone()[0]
        if total_attempted == 0:
            clearScreen()
            print("This student has not attempted any standards yet.")
            return
        # Total achieved standard count
        cursor.execute(
            "SELECT COUNT(*) FROM student_standard_grade WHERE student_id = ? AND score >= 3",
            (student_id,),
        )
        total_passed = cursor.fetchone()[0]
        # Pass rate calculation
        pass_rate = round(total_passed / total_attempted * 100, 2)
        clearScreen()
        print(
            f"\nPass rate for {student[0]} {student[1]}: {pass_rate}%, ({total_passed}/{total_attempted})"
        )
    elif answer == "5":
        cursor.execute(
            """
            SELECT SUM(standard.credits)
            FROM student_standard_grade
            JOIN standard
            ON student_standard_grade.standard_number = standard.standard_number
            WHERE student_standard_grade.student_id = ?""",
            (student_id,),
        )
        tot_attempt_credits = cursor.fetchone()[0]
        cursor.execute(
            """
            SELECT SUM(standard.credits)
            FROM student_standard_grade
            JOIN standard
            ON student_standard_grade.standard_number = standard.standard_number
            WHERE student_standard_grade.student_id = ?
            AND student_standard_grade.score >= 3""",
            (student_id,),
        )
        tot_gained_credits = cursor.fetchone()[0]
        if tot_attempt_credits == 0:
            tot_attempt_credits = "0"
        if tot_gained_credits == 0:
            tot_gained_credits = "0"
        clearScreen()
        print(
            f"Total attempted credits of {student[0]} {student[1]}: {tot_attempt_credits} Credits"
        )
        print(
            f"Total gained credits of {student[0]} {student[1]}: {tot_gained_credits} Credits"
        )
    elif answer == "6":
        clearScreen()
        print("Operation cancelled by user")
        return

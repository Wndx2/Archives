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


def standard_detail():
    # Get the standard number from the user
    while True:
        print("\nPlease enter the number of the standard that you want to see the data")
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
                f"\nDo you mean {st_type} Standard - Level {level} {domain} - {standard_number} {title} - {credits} {assess_type} Credit(s)?"
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

    student_id = 1  # Default student ID for personal tracker
    cursor.execute(
        """SELECT
                student_standard_grade.score, 
                grade.name 
                FROM student_standard_grade 
                JOIN grade 
                ON grade.score = student_standard_grade.score 
                WHERE student_standard_grade.standard_number = ? 
                AND student_standard_grade.student_id = ?""",
        (standard_number, student_id),
    )
    grade_info = cursor.fetchone()

    if grade_info:
        score, grade_name = grade_info
        clearScreen()
        print(f"\nYour grade for Standard {standard_number} - {title}:")
        print(f"Score: {score}")
        print(f"Grade: {grade_name}")
    else:
        clearScreen()
        print(f"\nYou have not attempted Standard {standard_number} yet.")

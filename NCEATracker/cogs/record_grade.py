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


def record_grade():
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
    # Check if the student already has the grade of that standard
    cursor.execute(
        "SELECT score FROM student_standard_grade WHERE student_id = ? AND standard_number = ?",
        (student_id, standard_number),
    )
    exist = cursor.fetchone()
    # If the grade of that standard has already recorded
    if exist:
        current_score = exist[0]
        cursor.execute("SELECT name FROM grade WHERE score = ?", (current_score,))
        current_name = cursor.fetchone()[0]
        print(
            f"\nWarning: {student[0]} {student[1]} already has a score of {current_score}, {current_name} for standard {standard_number}."
        )
        while True:
            # Ask user to replace or not
            print("Do you want to replace it with a new score?")
            answer = input("Yes or No > ").strip().lower()
            if answer == "yes":
                while True:
                    print("\nPlease enter the new score (0 to 8)")
                    score = input("> ").strip()
                    try:
                        score = int(score)
                        if 0 <= score <= 8:
                            break
                        else:
                            print("Score must be between 0 to 8.")
                            continue
                    except ValueError:
                        print("Score must be an integer.")
                cursor.execute(
                    "UPDATE student_standard_grade SET score = ? WHERE student_id = ? AND standard_number = ?",
                    (score, student_id, standard_number),
                )
                db.commit()
                # Automatically bring the name of the grade based on the score
                cursor.execute("SELECT name FROM grade WHERE score = ?", (score,))
                result = cursor.fetchone()
                grade_name = result[0]
                clearScreen()
                # Print the result
                print(
                    f"\nCompleted! {student[0]} {student[1]}'s {standard_number}, {title} result is replaced to {score}, which means {grade_name}!"
                )
                return
            elif answer == "no":
                clearScreen()
                print("Operation cancelled by user")
                return
            else:
                print("Please enter Yes or No")
    else:
        # Get the score from the user
        while True:
            print("\nPlease enter the score (0 to 8)")
            score = input("> ").strip()
            try:
                score = int(score)
                if score < 0 or score > 8:
                    print("Score must be between 0 to 8.")
                else:
                    break
            except ValueError:
                print("Score must be an integer.")
        cursor.execute(
            "INSERT INTO student_standard_grade (student_id, standard_number, score) VALUES (?, ?, ?)",
            (student_id, standard_number, score),
        )
        db.commit()
        # Automatically bring the name of the grade based on the score
        cursor.execute("SELECT name FROM grade WHERE score = ?", (score,))
        result = cursor.fetchone()
        grade_name = result[0]
        # Print the result
        clearScreen()
        print(
            f"\nCompleted! {student[0]} {student[1]} got {score}, which means {grade_name} in {standard_number}, {title}"
        )

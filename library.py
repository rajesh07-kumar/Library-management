
from db_connection import con
from datetime import date
import mysql.connector
cur = con.cursor()
def get_number(message):
    while True:
        try:
            number = int(input(message))
            if number > 0:
                return number
            print("Enter a positive number!")
        except ValueError:
            print("Enter a valid number!")
def add_book():
    title = input("Book Name: ")
    author = input("Author: ")
    if title == "" or author == "":
        print("Fields cannot be empty!")
        return
    quantity = get_number("Quantity: ")
    sql = "INSERT INTO books (title,author,quantity,available) VALUES (%s,%s,%s,%s)"
    cur.execute(sql, (title,author,quantity,quantity))
    con.commit()
    print("Book Added Successfully!")
def show_all_information():
    sql = """SELECT b.book_id,b.title,b.author,s.student_id,s.student_name,i.issue_id,i.issue_date,i.return_date
    FROM books b
    LEFT JOIN issued_books i ON b.book_id=i.book_id
    LEFT JOIN students s ON i.student_id=s.student_id"""
    cur.execute(sql)
    records = cur.fetchall()
    if len(records) == 0:
        print("No Records Found!")
        return
    print("-" * 120)
    print(f"{'Book ID':<10}{'Book Name':<18}{'Author':<15}{'Student ID':<12}{'Student Name':<18}{'Issue ID':<10}{'Issue Date':<15}{'Return Date':<15}")
    print("-" * 120)
    for row in records:
        print(f"{str(row[0]):<10}{row[1]:<18}{row[2]:<15}{str(row[3] or '-'):<12}{str(row[4] or '-'):<18}{str(row[5] or '-'):<10}{str(row[6] or '-'):<15}{str(row[7] or '-'):<15}")
    print("-" * 120)
def add_student():
    name = input("Student Name: ")
    if name == "":
        print("Student name cannot be empty!")
        return
    cur.execute("INSERT INTO students (student_name) VALUES (%s)", (name,))
    con.commit()
    print("Student Added Successfully!")
def show_students():
    cur.execute("SELECT * FROM students")
    records = cur.fetchall()
    if len(records) == 0:
        print("No Students Found!")
        return
    print("Student ID    Student Name")
    for row in records:
        print(row[0], "          ", row[1])
def delete_student():
    student_id = get_number("Student ID: ")
    cur.execute("SELECT * FROM students WHERE student_id=%s", (student_id,))
    student = cur.fetchone()
    if student is None:
        print("Student Not Found!")
        return
    cur.execute("SELECT * FROM issued_books WHERE student_id=%s", (student_id,))
    issue = cur.fetchone()
    if issue is not None:
        print("Cannot delete! Student has issue records.")
        return
    cur.execute("DELETE FROM students WHERE student_id=%s", (student_id,))
    con.commit()
    print("Student Deleted Successfully!")
def issue_book():
    book_id = get_number("Book ID: ")
    student_id = get_number("Student ID: ")
    cur.execute("SELECT available FROM books WHERE book_id=%s", (book_id,))
    book = cur.fetchone()
    if book is None:
        print("Book Not Found!")
        return
    if book[0] <= 0:
        print("Book Not Available!")
        return
    cur.execute("SELECT student_name FROM students WHERE student_id=%s", (student_id,))
    student = cur.fetchone()
    if student is None:
        print("Student Not Found!")
        return
    cur.execute("INSERT INTO issued_books (book_id,student_id,issue_date) VALUES (%s,%s,%s)", (book_id,student_id,date.today()))
    issue_id = cur.lastrowid
    cur.execute("UPDATE books SET available=available-1 WHERE book_id=%s", (book_id,))
    con.commit()
    print("Book Issued Successfully!")
    print("Student Name:", student[0])
    print("Issue ID:", issue_id)
def return_book():
    issue_id = get_number("Issue ID: ")
    cur.execute("SELECT book_id FROM issued_books WHERE issue_id=%s AND return_date IS NULL", (issue_id,))
    book = cur.fetchone()
    if book is None:
        print("Invalid Issue ID or Already Returned!")
        return
    cur.execute("UPDATE books SET available=available+1 WHERE book_id=%s", (book[0],))
    cur.execute("UPDATE issued_books SET return_date=%s WHERE issue_id=%s", (date.today(),issue_id))
    con.commit()
    print("Book Returned Successfully!")
def menu():
    while True:
        print("\n===== LIBRARY MANAGEMENT SYSTEM =====")
        print("1. Add Book")
        print("2. Show All Information")
        print("3. Issue Book")
        print("4. Return Book")
        print("5. Add Student")
        print("6. Show Students")
        print("7. Delete Student")
        print("8. Exit")
        choice = input("Enter Choice: ")
        try:
            if choice == "1":
                add_book()
            elif choice == "2":
                show_all_information()
            elif choice == "3":
                issue_book()
            elif choice == "4":
                return_book()
            elif choice == "5":
                add_student()
            elif choice == "6":
                show_students()
            elif choice == "7":
                delete_student()
            elif choice == "8":
                print("Thank you!")
                break
            else:
                print("Invalid Choice!")
        except mysql.connector.Error as error:
            con.rollback()
            print("MySQL Error:", error)
try:
    menu()
finally:
    cur.close()
    con.close()
    print("Database Connection Closed.")

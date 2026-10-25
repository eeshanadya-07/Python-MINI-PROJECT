import random
import math

# --- Topic 11.5: Custom Exception Example ---
class BookLimitExceededError(Exception):
    """Custom exception raised when borrowing exceeds maximum book limit (3 books)."""
    pass

class InvalidDaysError(Exception):
    """Custom exception raised for zero or negative borrowing days."""
    pass


# --- Topic 8.2: OOP Member Account Class ---
class MemberAccount:
    def __init__(self, member_id, name, pin):
        self.member_id = member_id
        self.name = name
        self.pin = pin
        self.borrowed_books = []  # Topic 4: Lists (Active borrowed books)
        self.reading_days = []    # Topic 4: Lists (Days logged per session)

    def borrow_book(self, book_title, days):
        if days <= 0:
            raise InvalidDaysError("Borrowing duration must be greater than zero days.")
        if len(self.borrowed_books) >= 3:
            raise BookLimitExceededError(
                f"Borrow limit reached! You already have {len(self.borrowed_books)} active books."
            )
        self.borrowed_books.append(book_title)
        self.reading_days.append(days)
        self.log_to_file(
            f"BORROWED: '{book_title}' for {days} days | Active Books: {len(self.borrowed_books)}"
        )
        return len(self.borrowed_books)

    # --- Topic 11.4: Book Return & Fine Calculation Program ---
    def return_book(self, book_title, late_days):
        if late_days < 0:
            raise InvalidDaysError("Late days cannot be negative.")
        if book_title not in self.borrowed_books:
            raise ValueError(f"Book '{book_title}' is not in your active borrowed list.")
        
        self.borrowed_books.remove(book_title)
        fine = late_days * 15.0  # Rs. 15 per overdue day
        self.log_to_file(
            f"RETURNED: '{book_title}' | Late Days: {late_days} | Fine Paid: Rs. {fine:.2f}"
        )
        return fine

    # --- Topic 10.4: Append Data to File ---
    def log_to_file(self, message):
        filename = f"ledger_{self.member_id}.txt"
        with open(filename, "a") as file:
            file.write(message + "\n")


# --- Topic 6.2: Math & Random Module (PIN Generator) ---
def generate_pin():
    digits = "0123456789"
    pin = ""
    for _ in range(4):
        pin += random.choice(digits)
    return pin


# --- Topic 1.3: Arithmetic Operations (Membership Plan & Discount Calculator) ---
def membership_fee_estimator(months):
    monthly_rate = 150.0
    base_cost = months * monthly_rate
    student_discount = base_cost * 0.15  # 15% PCU Student Discount
    net_cost = base_cost - student_discount
    gst_amount = net_cost * 0.18         # 18% GST
    final_payable = net_cost + gst_amount

    print(f"\n--- Membership Fee Breakdown ({months} Months) ---")
    print(f"Base Fee (Rs. 150/month) : Rs. {base_cost:.2f}")
    print(f"Student Discount (15%)   : -Rs. {student_discount:.2f}")
    print(f"GST (18%)                : +Rs. {gst_amount:.2f}")
    print(f"Total Payable Amount     : Rs. {final_payable:.2f}")


# --- Topic 9.1: Linear Search Implementation ---
def find_member(members_list, target_id):
    for member in members_list:
        if member.member_id == target_id:
            return member
    return None


# --- Topic 4.2 & 9.3: Sum, Average, Min & Max of List Elements ---
def analyze_reading_durations(days_list):
    if len(days_list) == 0:
        print("\nNo borrowing durations recorded in this session yet.")
        return

    total_days = 0
    longest = days_list[0]
    shortest = days_list[0]

    for d in days_list:
        total_days += d
        if d > longest:
            longest = d
        if d < shortest:
            shortest = d

    average = total_days / len(days_list)

    print("\n--- Session Reading Analytics ---")
    print(f"Total Books Borrowed : {len(days_list)}")
    print(f"Total Reading Days   : {total_days} days")
    print(f"Average Duration     : {average:.2f} days/book")
    print(f"Longest Borrow Plan  : {longest} days")
    print(f"Shortest Borrow Plan : {shortest} days")


# --- Topic 10.1 & 11.2: Read Data & File Not Found Handler ---
def read_ledger(member_id):
    filename = f"ledger_{member_id}.txt"
    print(f"\n--- Digital Library Ledger (Member ID: {member_id}) ---")
    try:
        with open(filename, "r") as file:
            content = file.read()
            print(content.strip())
    except FileNotFoundError:
        print("No ledger file found yet. Borrow a book first!")


# --- MAIN MENU (Topic 2: Conditionals & Topic 3: Loops) ---
def main():
    members = []
    next_member_id = 5001

    print("==================================================")
    print("  WELCOME TO PYTHON CLI SMART LIBRARY SYSTEM")
    print("==================================================")

    while True:
        print("\nMAIN MENU:")
        print("1. Register New Library Member")
        print("2. Access Member Portal (Login)")
        print("3. Exit System")

        choice = input("Enter your choice (1-3): ").strip()

        if choice == "1":
            name = input("Enter Student / Member Name: ").strip()
            if not name:
                print("Error: Member name cannot be empty.")
                continue

            pin = generate_pin()
            new_member = MemberAccount(next_member_id, name, pin)
            new_member.log_to_file(f"Library Membership Activated for {name}")
            members.append(new_member)

            print("\nMembership Created Successfully!")
            print(f"Member ID     : {next_member_id}")
            print(f"Generated PIN : {pin} (Please remember this!)")
            next_member_id += 1

        elif choice == "2":
            try:
                id_input = int(input("Enter Member ID: "))
            except ValueError:
                print("Error: Member ID must be digits only.")
                continue

            current_member = find_member(members, id_input)
            if current_member is None:
                print("Error: Member ID not found!")
                continue

            pin_input = input("Enter 4-Digit PIN: ").strip()
            if pin_input != current_member.pin:
                print("Error: Incorrect PIN! Access Denied.")
                continue

            print(f"\nWelcome to the Library Portal, {current_member.name}!")

            while True:
                print("\n--- LIBRARY MEMBER SERVICES ---")
                print("1. View Active Books & Membership Fee Calculator")
                print("2. Issue / Borrow a Book")
                print("3. Return a Book & Calculate Overdue Fine")
                print("4. Session Reading Analytics (Sum, Avg, Min, Max)")
                print("5. View Saved Library Ledger (File)")
                print("6. Daily Study Schedule Planner (Math Module)")
                print("7. Logout")

                sub_choice = input("Select Service (1-7): ").strip()

                if sub_choice == "1":
                    print(f"\nActive Borrowed Books ({len(current_member.borrowed_books)}/3): {current_member.borrowed_books}")
                    try:
                        m_input = int(input("Enter months to estimate renewal fee: "))
                        if m_input > 0:
                            membership_fee_estimator(m_input)
                        else:
                            print("Error: Months must be greater than zero.")
                    except ValueError:
                        print("Error: Please enter a valid integer for months.")

                elif sub_choice == "2":
                    title = input("Enter Book Title to Borrow: ").strip()
                    if not title:
                        print("Error: Book title cannot be empty.")
                        continue
                    try:
                        days = int(input("Enter number of days to borrow: "))
                        count = current_member.borrow_book(title, days)
                        print(f"Success! '{title}' issued. Active books: {count}/3")
                    except ValueError:
                        print("Error: Please enter a valid integer for days.")
                    except (InvalidDaysError, BookLimitExceededError) as e:
                        print(f"Issue Failed: {e}")

                elif sub_choice == "3":
                    title = input("Enter Book Title to Return: ").strip()
                    try:
                        late = int(input("Enter overdue days (0 if returned on time): "))
                        fine = current_member.return_book(title, late)
                        print(f"Book returned successfully! Overdue Fine: Rs. {fine:.2f}")
                    except ValueError as e:
                        print(f"Return Error: {e}")
                    except InvalidDaysError as e:
                        print(f"Return Failed: {e}")

                elif sub_choice == "4":
                    analyze_reading_durations(current_member.reading_days)

                elif sub_choice == "5":
                    read_ledger(current_member.member_id)

                elif sub_choice == "6":
                    try:
                        total_pages = int(input("Enter total pages in book: "))
                        target_days = int(input("Enter days available to finish: "))
                        if total_pages <= 0 or target_days <= 0:
                            print("Error: Pages and days must be greater than zero.")
                            continue
                        pages_per_day = math.ceil(total_pages / target_days)
                        print(f"To finish on time, read at least {pages_per_day} pages per day.")
                    except ValueError:
                        print("Error: Invalid numeric input for pages or days.")

                elif sub_choice == "7":
                    print("Logging out safely...")
                    break
                else:
                    print("Invalid choice! Please select between 1 and 7.")

        elif choice == "3":
            print("\nThank you for using the Python CLI Smart Library System. Goodbye!")
            break
        else:
            print("Invalid selection! Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main()
import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from decimal import Decimal  # Import Decimal for precise arithmetic

# Database connection
def connect_to_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",  # Replace with your DB user
            password="hyabusaferrari@123",  # Replace with your DB password
            database="banking_dbms_system"
        )
        return conn
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        return None

# Create Account Function
def create_account():
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        try:
            sql = "INSERT INTO customers (first_name, last_name, phone_no, email, address) VALUES (%s, %s, %s, %s, %s)"
            values = (entry_first_name.get(), entry_last_name.get(), entry_phone_no.get(), entry_email.get(), entry_address.get())
            cursor.execute(sql, values)
            conn.commit()
            customer_id = cursor.lastrowid
            branch_id = branch_var.get()
            cursor.execute("INSERT INTO accounts (customer_id, branch_id, balance) VALUES (%s, %s, %s)", (customer_id, branch_id, 0.00))
            conn.commit()
            messagebox.showinfo("Success", "Account created successfully!")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error: {err}")
        finally:
            conn.close()

# Check Balance Function
def check_balance():
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        try:
            account_id = entry_account_id.get()
            cursor.execute("SELECT balance FROM accounts WHERE account_id = %s", (account_id,))
            result = cursor.fetchone()
            if result:
                messagebox.showinfo("Balance", f"Current Balance: ${result[0]:.2f}")
            else:
                messagebox.showerror("Error", "Account not found!")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error: {err}")
        finally:
            conn.close()

# Perform Transaction Function
def perform_transaction():
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        try:
            account_id = entry_account_id.get()
            if not account_id:
                messagebox.showerror("Error", "Please enter a valid Account ID!")
                return
            
            cursor.execute("SELECT balance FROM accounts WHERE account_id = %s", (account_id,))
            result = cursor.fetchone()
            if not result:
                messagebox.showerror("Error", "Invalid Account ID! Account not found.")
                return
            
            balance = Decimal(result[0])
            transaction_type = transaction_type_var.get().lower()
            amount = entry_amount.get()
            if not amount or float(amount) <= 0:
                messagebox.showerror("Error", "Please enter a valid transaction amount!")
                return
            amount = Decimal(amount)

            if transaction_type == "withdraw":
                if balance < amount:
                    messagebox.showerror("Error", "Insufficient balance!")
                    return
                new_balance = balance - amount
            elif transaction_type == "deposit":
                new_balance = balance + amount
            else:
                messagebox.showerror("Error", "Invalid transaction type!")
                return

            cursor.execute("UPDATE accounts SET balance = %s WHERE account_id = %s", (new_balance, account_id))
            cursor.execute(
                "INSERT INTO Transactions (account_id, transaction_type, amount) VALUES (%s, %s, %s)",
                (account_id, transaction_type, amount)
            )
            conn.commit()
            messagebox.showinfo("Success", f"{transaction_type.capitalize()} successful! New Balance: ${new_balance:.2f}")
        except ValueError:
            messagebox.showerror("Error", "Invalid amount entered!")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Database Error: {err}")
        finally:
            conn.close()

# Take Loan Function
def take_loan():
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        try:
            customer_id = entry_customer_id.get()
            loan_amount = entry_loan_amount.get()
            if not customer_id or not loan_amount or float(loan_amount) <= 0:
                messagebox.showerror("Error", "Please enter valid Customer ID and Loan Amount!")
                return
            loan_amount = Decimal(loan_amount)
            
            cursor.execute("INSERT INTO Loans (customer_id, loan_amount) VALUES (%s, %s)", (customer_id, loan_amount))
            conn.commit()
            messagebox.showinfo("Success", f"Loan of ${loan_amount:.2f} granted successfully!")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error: {err}")
        finally:
            conn.close()

# Tkinter GUI
root = tk.Tk()
root.title("PES Bank")
root.geometry("600x700")  # Set window size
root.resizable(False, False)

# Set background color
root.configure(bg="#f0f8ff")  # Light blue

# Custom styling
style = ttk.Style()
style.theme_use("clam")
style.configure("TButton", font=("Arial", 12), padding=5, background="#007bff", foreground="white")
style.configure("TLabel", font=("Arial", 12), background="#f0f8ff", foreground="#333")
style.configure("TEntry", padding=5)
style.map("TButton", background=[("active", "#0056b3")])

frame = tk.Frame(root, padx=10, pady=10, bg="#f0f8ff")
frame.pack(fill=tk.BOTH, expand=True)

# Labels and Entries for Customer Details
tk.Label(frame, text="First Name:", bg="#f0f8ff", fg="#333", font=("Arial", 12)).grid(row=0, column=0, pady=5, sticky=tk.W)
entry_first_name = ttk.Entry(frame)
entry_first_name.grid(row=0, column=1, pady=5)

tk.Label(frame, text="Last Name:", bg="#f0f8ff", fg="#333", font=("Arial", 12)).grid(row=1, column=0, pady=5, sticky=tk.W)
entry_last_name = ttk.Entry(frame)
entry_last_name.grid(row=1, column=1, pady=5)

tk.Label(frame, text="Address:", bg="#f0f8ff", fg="#333", font=("Arial", 12)).grid(row=2, column=0, pady=5, sticky=tk.W)
entry_address = ttk.Entry(frame)
entry_address.grid(row=2, column=1, pady=5)

tk.Label(frame, text="Phone Number:", bg="#f0f8ff", fg="#333", font=("Arial", 12)).grid(row=3, column=0, pady=5, sticky=tk.W)
entry_phone_no = ttk.Entry(frame)
entry_phone_no.grid(row=3, column=1, pady=5)

tk.Label(frame, text="Email:", bg="#f0f8ff", fg="#333", font=("Arial", 12)).grid(row=4, column=0, pady=5, sticky=tk.W)
entry_email = ttk.Entry(frame)
entry_email.grid(row=4, column=1, pady=5)

tk.Label(frame, text="Branch:", bg="#f0f8ff", fg="#333", font=("Arial", 12)).grid(row=5, column=0, pady=5, sticky=tk.W)
branch_var = tk.IntVar()
branch_dropdown = ttk.Combobox(frame, textvariable=branch_var, values=[1, 2, 3])
branch_dropdown.grid(row=5, column=1, pady=5)

tk.Button(frame, text="Create Account", command=create_account).grid(row=6, column=0, columnspan=2, pady=10)

# Check Balance Section
tk.Label(frame, text="Account ID:", bg="#f0f8ff", fg="#333", font=("Arial", 12)).grid(row=7, column=0, pady=5, sticky=tk.W)
entry_account_id = ttk.Entry(frame)
entry_account_id.grid(row=7, column=1, pady=5)
tk.Button(frame, text="Check Balance", command=check_balance).grid(row=8, column=0, columnspan=2, pady=10)

# Transaction Section
tk.Label(frame, text="Transaction Type:", bg="#f0f8ff", fg="#333", font=("Arial", 12)).grid(row=9, column=0, pady=5, sticky=tk.W)
transaction_type_var = tk.StringVar(value="Withdraw")
transaction_type_dropdown = ttk.Combobox(frame, textvariable=transaction_type_var, values=["Withdraw", "Deposit"])
transaction_type_dropdown.grid(row=9, column=1, pady=5)

tk.Label(frame, text="Amount:", bg="#f0f8ff", fg="#333", font=("Arial", 12)).grid(row=10, column=0, pady=5, sticky=tk.W)
entry_amount = ttk.Entry(frame)
entry_amount.grid(row=10, column=1, pady=5)
tk.Button(frame, text="Perform Transaction", command=perform_transaction).grid(row=11, column=0, columnspan=2, pady=10)

# Loan Section
tk.Label(frame, text="Customer ID:", bg="#f0f8ff", fg="#333", font=("Arial", 12)).grid(row=12, column=0, pady=5, sticky=tk.W)
entry_customer_id = ttk.Entry(frame)
entry_customer_id.grid(row=12, column=1, pady=5)

tk.Label(frame, text="Loan Amount:", bg="#f0f8ff", fg="#333", font=("Arial", 12)).grid(row=13, column=0, pady=5, sticky=tk.W)
entry_loan_amount = ttk.Entry(frame)
entry_loan_amount.grid(row=13, column=1, pady=5)

tk.Button(frame, text="Take Loan", command=take_loan).grid(row=14, column=0, columnspan=2, pady=10)

root.mainloop()

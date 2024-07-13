import string
import random
from tkinter import *
from tkinter import messagebox
import sqlite3

# Connect to the database and create table if it doesn't exist
with sqlite3.connect("users.db") as db:
    cursor = db.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users(Username TEXT NOT NULL, GeneratedPassword TEXT NOT NULL);")
cursor.execute("SELECT * FROM users")
db.commit()
db.close()

# GUI class definition
class GUI():
    def __init__(self, master):
        self.master = master
        self.username = StringVar()
        self.passwordlen = IntVar()
        self.generatedpassword = StringVar()
        self.n_username = StringVar()
        self.n_generatedpassword = StringVar()
        self.n_passwordlen = IntVar()
        
        # Configure root window
        root.title('Password Generator')
        root.geometry('660x500')
        root.config(bg='#3498db')  # Changed color to light blue
        root.resizable(False, False)

        # Title Label
        self.label = Label(text=":PASSWORD GENERATOR:", anchor=N, fg='white', bg='#3498db', font='arial 20 bold underline')
        self.label.grid(row=0, column=1)

        # Blank Labels for spacing
        self.blank_label1 = Label(text="", bg='#3498db')
        self.blank_label1.grid(row=1, column=0, columnspan=2)
        
        self.blank_label2 = Label(text="", bg='#3498db')
        self.blank_label2.grid(row=2, column=0, columnspan=2)    

        self.blank_label3 = Label(text="", bg='#3498db')
        self.blank_label3.grid(row=3, column=0, columnspan=2)    

        # Username Label and TextField
        self.user = Label(text="Enter User Name: ", font='times 15 bold', bg='#3498db', fg='white')
        self.user.grid(row=4, column=0)

        self.textfield = Entry(textvariable=self.n_username, font='times 15', bd=6, relief='ridge')
        self.textfield.grid(row=4, column=1)
        self.textfield.focus_set()

        self.blank_label4 = Label(text="", bg='#3498db')
        self.blank_label4.grid(row=5, column=0)

        # Password Length Label and TextField
        self.length = Label(text="Enter Password Length: ", font='times 15 bold', bg='#3498db', fg='white')
        self.length.grid(row=6, column=0)

        self.length_textfield = Entry(textvariable=self.n_passwordlen, font='times 15', bd=6, relief='ridge')
        self.length_textfield.grid(row=6, column=1)
        
        self.blank_label5 = Label(text="", bg='#3498db')
        self.blank_label5.grid(row=7, column=0)

        # Generated Password Label and TextField
        self.generated_password = Label(text="Generated Password: ", font='times 15 bold', bg='#3498db', fg='white')
        self.generated_password.grid(row=8, column=0)

        self.generated_password_textfield = Entry(textvariable=self.n_generatedpassword, font='times 15', bd=6, relief='ridge', fg='#e74c3c')
        self.generated_password_textfield.grid(row=8, column=1)
   
        self.blank_label6 = Label(text="", bg='#3498db')
        self.blank_label6.grid(row=9, column=0)

        self.blank_label7 = Label(text="", bg='#3498db')
        self.blank_label7.grid(row=10, column=0)

        # Generate Password Button
        self.generate = Button(text="GENERATE PASSWORD", bd=3, relief='solid', padx=1, pady=1, font='Verdana 15 bold', fg='#2c3e50', bg='#2ecc71', command=self.generate_pass)
        self.generate.grid(row=11, column=1)

        self.blank_label8 = Label(text="", bg='#3498db')
        self.blank_label8.grid(row=12, column=0)

        # Accept Button
        self.accept = Button(text="ACCEPT", bd=3, relief='solid', padx=1, pady=1, font='Helvetica 15 bold italic', fg='#2980b9', bg='#ecf0f1', command=self.accept_fields)
        self.accept.grid(row=13, column=1)

        self.blank_label9 = Label(text="", bg='#3498db')
        self.blank_label9.grid(row=14, column=1)

        # Reset Button
        self.reset = Button(text="RESET", bd=3, relief='solid', padx=1, pady=1, font='Helvetica 15 bold italic', fg='#2980b9', bg='#ecf0f1', command=self.reset_fields)
        self.reset.grid(row=15, column=1)

    # Function to generate a random password
    def generate_pass(self):
        upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        lower = "abcdefghijklmnopqrstuvwxyz"
        chars = "@#%&()\"?!"
        numbers = "1234567890"
        upper = list(upper)
        lower = list(lower)
        chars = list(chars)
        numbers = list(numbers)
        name = self.textfield.get()
        leng = self.length_textfield.get()

        with sqlite3.connect("users.db") as db:
            cursor = db.cursor()

        # Validate the username and length inputs
        if name == "":
            messagebox.showerror("Error", "Name cannot be empty")
            return

        if not name.isalpha():
            messagebox.showerror("Error", "Name must be a string")
            self.textfield.delete(0, 25)
            return

        try:
            length = int(leng)
        except ValueError:
            messagebox.showerror("Error", "Length must be a number")
            return

        if length < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters long")
            return

        self.generated_password_textfield.delete(0, length)

        # Generate a random password with the specified length
        u = random.randint(1, length - 3)
        l = random.randint(1, length - 2 - u)
        c = random.randint(1, length - 1 - u - l)
        n = length - u - l - c

        password = random.sample(upper, u) + random.sample(lower, l) + random.sample(chars, c) + random.sample(numbers, n)
        random.shuffle(password)
        gen_passwd = "".join(password)
        self.generated_password_textfield.insert(0, gen_passwd)

    # Function to accept and save the generated password
    def accept_fields(self):
        with sqlite3.connect("users.db") as db:
            cursor = db.cursor()
            find_user = ("SELECT * FROM users WHERE Username = ?")
            cursor.execute(find_user, [(self.n_username.get())])

            if cursor.fetchall():
                messagebox.showerror("Error", "This username already exists! Please use another username")
            else:
                insert = ("INSERT INTO users(Username, GeneratedPassword) VALUES(?, ?)")
                cursor.execute(insert, (self.n_username.get(), self.n_generatedpassword.get()))
                db.commit()
                messagebox.showinfo("Success!", "Password generated successfully")

    # Function to reset input fields
    def reset_fields(self):
        self.textfield.delete(0, 25)
        self.length_textfield.delete(0, 25)
        self.generated_password_textfield.delete(0, 25)

# Main loop to run the GUI application
if __name__ == '__main__':
    root = Tk()
    pass_gen = GUI(root)
    root.mainloop()

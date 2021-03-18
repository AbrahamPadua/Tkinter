from tkinter import Tk, Canvas, PhotoImage, Label, Entry, Button, messagebox, END
from random import choice, randint, shuffle
from json.decoder import JSONDecodeError
# import pyperclip
import json

FONT = ("Arial", 10, "normal")


def search():
    website = web_entry.get().lower()
    try:
        with open("secrets.json") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showerror("Error", "No Data File Found.")
    else:
        if website in data:
            email = data[website].get('email')
            password = data[website].get('password')
            messagebox.showinfo(title="Email and Password",
                                message=f"Email: {email} \nPassword: {password}")
        else:
            messagebox.showerror("Error", f"No details for {website} exists.")


def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y',
               'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = [choice(letters) for i in range(randint(8, 10))]
    password_list += [choice(numbers) for i in range(randint(2, 4))]
    password_list += [choice(symbols) for i in range(randint(2, 4))]

    shuffle(password_list)

    password = "".join(password_list)
    pass_entry.delete(0, END)
    pass_entry.insert(0, password)


def main_window():

    window = Tk()
    window.title("Password Manager")
    window.config(padx=50, pady=50, bg="#f4f5db")

    canvas = Canvas(width=210, height=210, bg="#f4f5db", highlightthickness=0)
    photo = PhotoImage(file="logo.png")
    canvas.create_image(105, 105, image=photo)
    canvas.grid(row=0, column=1)

    web = Label(text="Website:", font=FONT, bg="#f4f5db", highlightthickness=0)
    web.grid(row=1, column=0)

    web_entry = Entry()
    web_entry.grid(row=1, column=1, sticky="EW")

    search = Button(text="Search", command=search, width=15)
    search.grid(row=1, column=2, sticky="EW")

    email = Label(text="Email/Username:", font=FONT,
                  bg="#f4f5db", highlightthickness=0)
    email.grid(row=2, column=0)

    email_entry = Entry()
    email_entry.grid(row=2, column=1, columnspan=2, sticky="EW")

    password = Label(text="Password:", font=FONT,
                     bg="#f4f5db", highlightthickness=0)
    password.grid(row=3, column=0)

    pass_entry = Entry()
    pass_entry.grid(row=3, column=1, sticky="EW")

    gen_password = Button(text="Generate Password", command=generate_password)
    gen_password.grid(row=3, column=2, sticky="EW")

    add = Button(text="Add", width=46, command=add_password)
    add.grid(row=4, column=1, columnspan=2)

    window.mainloop()


def login():
    with open("secrets.json") as data_file:
        data = json.load(data_file)
    if security.get() == data["security password"]:
        main_window()
    else:
        messagebox.showerror(
            "Invalid Password", "You have input an invalid password.\nApp is closing...")
        start_window.destroy(0)


def save():
    security_password = security.get()
    new_data = {
        "security password": security_password,
    }
    if len(security_password) and not security_password.startswith("Enter New Password"):
        with open("secrets.json", "w") as data_file:
            json.dump(new_data, data_file, indent=4)
        main_window()
    else:
        messagebox.showerror("Invalid Password", "Input a Valid Password")
        security.delete(0, END)
        security.insert("Enter New Password")


def add_password():
    website = web_entry.get().lower()
    user_email = email_entry.get()
    new_pass = pass_entry.get()

    new_data = {
        website: {
            "email": user_email,
            "password": new_pass,
        }
    }

    if len(website) and len(user_email) and len(new_pass):
        is_ok = messagebox.askokcancel(
            title="website", message=f"These are the details entered: \nEmail: {user_email} \nPassword: {new_pass} \nIs it ok to save?")

        if is_ok:
            try:
                with open("secrets.json", "r") as data_file:
                    data = json.load(data_file)
            except FileNotFoundError:
                with open("secrets.json", "w") as data_file:
                    json.dump(new_data, data_file, indent=4)
            else:
                data.update(new_data)
                with open("secrets.json", "w") as data_file:
                    json.dump(data, data_file, indent=4)
            finally:
                web_entry.delete(0, END)
                email_entry.delete(0, END)
                pass_entry.delete(0, END)
    else:
        messagebox.showerror(
            "Empty Entries", "All Entries Must be Filled.")


start_window = Tk()
start_window.title("Password Manager")
start_window.config(padx=50, pady=50, bg="#f4f5db")

canvas = Canvas(width=210, height=210, bg="#f4f5db", highlightthickness=0)
photo = PhotoImage(file="logo.png")
canvas.create_image(105, 105, image=photo)
canvas.grid(row=0, column=1)

password_label = Label(text="Password: ", font=("Arial", 20, "normal"),
                       bg="#f4f5db", highlightthickness=0)
password_label.grid(row=1, column=0)

security = Entry()
security.grid(row=1, column=1, columnspan=2)

with open("secrets.json", "w+") as data_file:
    try:
        data = json.load(data_file)
    except JSONDecodeError:
        security.insert(0, "Enter New Password")
        save = Button(text="Save", command=save, width=10)
        save.grid(row=2, column=1)
    else:
        if "security password" in data:
            login = Button(text="Login", command=login)
            login.grid(row=2, column=1)

start_window.mainloop()

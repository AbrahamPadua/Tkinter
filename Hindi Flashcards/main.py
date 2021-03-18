from tkinter import Tk, Menu, PhotoImage, Button, Canvas
import json
import pandas as pd
import random
import datetime
import os
from calendar import monthrange


BACKGROUND_COLOR = "#B1DDC6"
LANGUAGE_FONT = ("Arial", 40, "italic")
WORD_FONT = ("data/Mangal Regular.tff", 60, "bold")

data = pd.read_csv("data/hindi.csv")
to_learn = data.to_dict(orient="records")
month_now, day_now, year_now = datetime.datetime.now().strftime("%D").split("/")

mastered = []
if os.path.exists("data/to learn.json"):
    with open("data/to learn.json", "r") as data_file:
        learn_next_time = json.load(data_file)
else:
    learn_next_time = {}


class Hindi_Flashcards():
    def __init__(self, window):
        self.window = window
        self.window.title("Hindi Flashcards")
        self.window.configure(padx=50, pady=50, bg=BACKGROUND_COLOR)

        self.flashcard = Canvas(width=800, height=500,
                                highlightthickness=0, bg=BACKGROUND_COLOR)
        self.flashcard.grid(row=0, column=0, columnspan=3)

        self.back_flashcard_image = PhotoImage(file="images/card_back.png")
        self.front_flashcard_image = PhotoImage(file="images/card_front.png")
        self.front = self.flashcard.create_image(
            400, 250, image=self.front_flashcard_image)

        self.current_language = "English"
        self.language = self.flashcard.create_text(
            400, 150, text="Language", font=LANGUAGE_FONT)
        self.word = self.flashcard.create_text(
            400, 263, text="word", font=WORD_FONT)

        self.check_image = PhotoImage(file="images/right.png")
        self.next_image = PhotoImage(file="images/next.png")
        self.ekis_image = PhotoImage(file="images/wrong.png")

        self.ekis = Button(image=self.ekis_image, highlightthickness=0,
                           command=self.ekis_pressed, state="disabled")
        self.ekis.grid(row=1, column=0)

        self.show = Button(image=self.next_image,
                           command=self.show_pressed, state="disabled")
        self.show.grid(row=1, column=1)

        self.check = Button(image=self.check_image,
                            highlightthickness=0, command=self.first_check)
        self.check.grid(row=1, column=2)

        menubar = Menu(self.window, tearoff=0)
        menubar.add_command(label="Save Progress", command=self.save)
        menubar.add_command(label="Delete Progress", command=self.delete)
        self.window.configure(menu=menubar)

    def show_pressed(self):
        if self.current_language == "English":
            self.flashcard.itemconfigure(
                self.front, image=self.front_flashcard_image)
            self.flashcard.itemconfigure(
                self.language, text="Hindi", fill="black")
            self.flashcard.itemconfigure(
                self.word, text=self.current_card["Hindi"], fill="black")
            self.current_language = "Hindi"
        else:
            self.flashcard.itemconfigure(
                self.front, image=self.back_flashcard_image)
            self.flashcard.itemconfigure(
                self.language, text="English", fill="white")
            self.flashcard.itemconfigure(
                self.word, text=self.current_card["English"], fill="white")
            self.current_language = "English"

    def next_card(self):
        # Check if the word is already learned else append it to learn_next_time
        while True:
            self.current_card = random.choice(to_learn)
            word = self.current_card["Hindi"]
            if word in learn_next_time:
                if int(day_now) >= learn_next_time.get(word, [0, 0, 0, 0])[0] and int(month_now) >= learn_next_time.get(word, [0, 0, 0, 0])[1] and int(year_now) >= learn_next_time.get(word, [0, 0, 0, 0])[2]:
                    break
                else:
                    continue
            elif word in mastered:
                break
            else:
                break

        self.flashcard.itemconfigure(
            self.front, image=self.front_flashcard_image)
        self.flashcard.itemconfigure(
            self.language, text="Hindi", fill="black")
        self.flashcard.itemconfigure(
            self.word, text=self.current_card["Hindi"], fill="black")
        self.current_language = "Hindi"

    def first_check(self):
        if self.show["state"] == "disabled":
            self.show["state"] = "normal"
        if self.ekis["state"] == "disabled":
            self.ekis["state"] = "normal"

        self.next_card()

        self.flashcard.itemconfigure(
            self.front, image=self.front_flashcard_image)
        self.flashcard.itemconfigure(
            self.language, text="Hindi", fill="black")
        self.flashcard.itemconfigure(
            self.word, text=self.current_card["Hindi"], fill="black")
        self.current_language = "Hindi"

        self.check.configure(command=self.check_pressed)

    def check_pressed(self):
        self.next_card()
        self.add_to_known()

    # Will show a next button and flip the flashcard
    def ekis_pressed(self):
        self.show_pressed()
        self.ekis.configure(command=self.ekis_ekis_pressed)
        self.check.configure(command=self.ekis_check_pressed)

    # When checked was pressed after clicking ekis
    def ekis_check_pressed(self):
        self.next_card()
        self.ekis.configure(command=self.ekis_pressed)
        self.check.configure(command=self.check_pressed)

    # When ekis was clicked after clicking ekis
    def ekis_ekis_pressed(self):
        self.next_card()
        self.ekis.configure(command=self.ekis_pressed)
        self.check.configure(command=self.check_pressed)

    # Append the word to learn_next_time and calculate when to learn it.
    def add_to_known(self):

        # fix function fixes the overflow in dates
        def fix(day, month, year):
            # monthrange gets how many days in a month
            days = monthrange(year, month)[1]
            if day > days:
                day = day - monthrange(year, month)
                month += 1
            if month > 12:
                month -= 12
                year += 1
            return day, month, year

        def add_to_json(word, day, month, year, times):
            day, month, year = fix(day, month, year)
            data = [day, month, year, times]
            learn_next_time[word] = data

        word = self.current_card["Hindi"]
        times = learn_next_time.get(word, [0, 0, 0, 0])

        if times[3] == 0:
            day = int(day_now) + 1
            month = int(month_now)
            year = int(year_now)
            times = 1
            add_to_json(word, day, month, year, times)
        elif times[3] == 1:
            day = times[0] + 2
            month = times[1]
            year = times[2]
            times = 2
            add_to_json(word, day, month, year, times)
        elif times[3] == 2:
            day = times[0] + 3
            month = times[1]
            year = times[2]
            times = 3
            add_to_json(word, day, month, year, times)
        elif times[3] == 3:
            day = times[0] + 5
            month = times[1]
            year = times[2]
            times = 5
            add_to_json(word, day, month, year, times)
        elif times[3] == 5:
            day = times[0] + 8
            month = times[1]
            year = times[2]
            times = 8
            add_to_json(word, day, month, year, times)
        elif times[3] == 8:
            mastered.append(word)
            learn_next_time.pop(word)

    def save(self):
        with open("data/to learn.json", "w") as data_file:
            json.dump(learn_next_time, data_file, indent=4)

    def delete(self):
        global learn_next_time

        learn_next_time = {}
        if os.path.exists("data/to learn.json"):
            os.remove("data/to learn.json")


if __name__ == "__main__":
    window = Tk()
    window = Hindi_Flashcards(window)
    window.window.mainloop()

from tkinter import *
import pandas as pd
import random


def next_card():
    flashcard.itemconfigure(
        front, image=back_flashcard_image)


BACKGROUND_COLOR = "#B1DDC6"
LANGUAGE_FONT = ("Arial", 40, "italic")
WORD_FONT = ("data/Mangal Regular.tff", 60, "bold")

data = pd.read_csv("data/hindi.csv")
to_learn = data.to_dict(orient="records")


window = Tk()
window.title("Hindi Flashcards")
window.configure(padx=50, pady=50, bg=BACKGROUND_COLOR)

flashcard = Canvas(width=800, height=500,
                   highlightthickness=0, bg=BACKGROUND_COLOR)
flashcard.grid(row=0, column=0, columnspan=2)

front_flashcard_image = PhotoImage(file="images/card_front.png")
back_flashcard_image = PhotoImage(file="images/card_back.png")
front = flashcard.create_image(
    400, 250, image=front_flashcard_image)

current_language = "English"
language = flashcard.create_text(
    400, 150, text="Language", font=LANGUAGE_FONT)
word = flashcard.create_text(
    400, 263, text="word", font=WORD_FONT)

ekis_image = PhotoImage(file="images/wrong.png")
ekis = Button(image=ekis_image, highlightthickness=0,
              command=next_card)
ekis.grid(row=1, column=0)

check_image = PhotoImage(file="images/right.png")
check = Button(image=check_image,
               highlightthickness=0, command=next_card)
check.grid(row=1, column=1)

window.mainloop()

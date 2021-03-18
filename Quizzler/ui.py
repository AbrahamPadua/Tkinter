from tkinter import *

THEME_COLOR = "#375362"
FONT = ("Arial", 20, "italic")


class QuizInterface:
    def __init__(self, quiz):
        self.quiz = quiz

        self.window = Tk()
        self.window.configure(padx=20, pady=20, bg=THEME_COLOR)
        self.window.title("Quizzler")

        # self.menu_button = Menubutton(self.window, text="Menu")
        self.menubar = Menu(self.window)
        self.menu = Menu(self.menubar, tearoff=0)
        self.menu.add_command(label="Restart", command=self.restart)
        self.menu.add_command(label="Reset", command=self.reset)
        self.menu.add_command(label="Quit", command=self.close_game)
        self.menubar.add_cascade(label="Menu", menu=self.menu)
        self.window.configure(menu=self.menubar)

        self.score_label = Label(text="Score: 0", font=("Courier", 10, "normal"), bg=THEME_COLOR, fg="white",
                                 highlightthickness=0)
        self.score_label.grid(row=0, column=1)

        self.canvas = Canvas(width=300, height=250, bg="white")
        self.canvas.grid(row=1, column=0, columnspan=2, pady=50)
        self.question = self.canvas.create_text(
            150, 125, text=self.quiz.current_question, font=FONT, fill=THEME_COLOR, width=280, anchor=CENTER)

        false_image = PhotoImage(file="images/false.png")
        self.false = Button(image=false_image,
                            command=self.false_pressed, highlightthickness=0)
        self.false.grid(row=2, column=0)

        true_image = PhotoImage(file="images/true.png")
        self.true = Button(
            image=true_image, command=self.true_pressed, highlightthickness=0)
        self.true.grid(row=2, column=1)

        self.question_config()

        self.window.mainloop()

    def question_config(self):
        question = self.quiz.next_question()
        self.canvas.itemconfigure(self.question, text=question)
        self.score_label.configure(text=f"Score: {self.quiz.score}")
        self.canvas.configure(bg="white")
        self.false.configure(state=NORMAL)
        self.true.configure(state=NORMAL)

    def true_pressed(self):
        self.check_answer("True")

    def false_pressed(self):
        self.check_answer("False")

    def check_answer(self, answer):

        def show_score():
            self.canvas.configure(bg="white")
            self.canvas.itemconfigure(
                self.question, text=f"Your score is {self.quiz.score}/{len(self.quiz.question_list)}")

        is_right = self.quiz.check_answer(answer)
        if is_right:
            self.canvas.configure(bg="green")
        else:
            self.canvas.configure(bg="red")

        self.false.configure(state=DISABLED)
        self.true.configure(state=DISABLED)
        if self.quiz.question_number < 10:
            self.window.after(1000, self.question_config)
        else:
            self.window.after(1000, show_score)

    def reset(self):
        pass

    def restart(self):
        pass

    def close_game(self):
        self.window.destroy()

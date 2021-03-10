from tkinter import *

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
timer = None

# ---------------------------- TIMER RESET ------------------------------- #


def reset():
    global reps
    window.after_cancel(timer)
    canvas.itemconfig(time, text="00:00")
    title.config(text="Timer", fg=GREEN)
    check_marks.config(text="")
    reps = 0

# ---------------------------- TIMER MECHANISM ------------------------------- #


def countdown(count):
    global timer
    minutes = f"{int(count/60)}"
    seconds = f"{count%60}"
    if len(seconds) == 1:
        seconds = f"0{seconds}"
    if len(minutes) == 1:
        minutes = f"0{minutes}"
    canvas.itemconfig(time, text=f"{minutes}:{seconds}")
    if count > 0:
        timer = window.after(1000, countdown, count-1)
    else:
        start()
        if reps % 2 == 1:
            mark = f"{reps//2*'✔'}"
            check_marks.config(text=mark)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #


def start():
    global reps
    if reps % 2 == 0:
        countdown(60 * 25)
        title.config(text="Work", fg=GREEN)
    elif reps % 8 == 0:
        countdown(60 * 20)
        title.config(text="Break", fg=RED)
    else:
        countdown(60 * 5)
        title.config(text="Break", fg=PINK)
    reps += 1
# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)

title = Label(text="Timer", fg=GREEN, font=(FONT_NAME, 50, "bold"), bg=YELLOW)
title.grid(column=1, row=0)

canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
photo = PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=photo)
canvas.grid(row=1, column=1)
time = canvas.create_text(100, 130, text="00:00", fill="white",
                          font=(FONT_NAME, 35, "bold"))

start_butt = Button(text="Start", command=start, highlightthickness=0)
start_butt.grid(row=2, column=0)

reset_butt = Button(text="Reset", command=reset, highlightthickness=0)
reset_butt.grid(row=2, column=2)

check_marks = Label(fg=GREEN, bg=YELLOW)
check_marks.grid(column=1, row=3)

window.mainloop()

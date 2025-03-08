from tkinter import *
import pandas as pd
from random import choice
from tkinter import messagebox, filedialog


def next_card():
    global current_card, front_language
    canvas.itemconfig(canvas_image, image=front_img)
    current_card = choice(cards)
    canvas.itemconfig(language_text, text=front_language, fill="black")
    canvas.itemconfig(word_text, text=f"{current_card[front_language]}", fill="black")

def flip_card():
    global back_language
    canvas.itemconfig(canvas_image, image=back_img)
    canvas.itemconfig(language_text, text=back_language, fill="white")
    canvas.itemconfig(word_text, text=f"{current_card[back_language]}", fill="white")

def remove_card():
    global cards
    cards.remove(current_card)
    next_card()

def on_closing():
    global cards
    if messagebox.askyesno("Progress", "Save your progress?"):
        pd.DataFrame(cards).to_csv("./data/words_to_learn.csv", index=False)
    window.destroy()

def import_csv():
    file_path = filedialog.askopenfilename(
        title= "Select a Text File", filetypes = [("CSV files", "*.csv")])

    global cards
    try:
        df = pd.read_csv(file_path)
        cards = df.to_dict(orient="records")
    except FileNotFoundError:
        pass
    except Exception as error_message:
        messagebox.showinfo(title="Data", message=f"{error_message}")
    else:
        window.protocol("WM_DELETE_WINDOW", on_closing)
        canvas.itemconfig(initial_message, text="")
        pd.DataFrame(cards).to_csv("./data/words.csv", index=False)
        show_button.grid(column=0, row=2, columnspan=2, pady=(40, 0))
        wrong_button.grid(column=0, row=1)
        right_button.grid(column=1, row=1)
        global front_language, back_language, columns
        columns = list(df.columns)
        front_language = columns[0]
        back_language = columns[1]
        import_button.grid_forget()
        next_card()

BACKGROUND_COLOR = "#B1DDC6"
SHOW_BUTTON_COLOR = "#7abf9c"
LANGUAGE_FONT = ("Arial", 15, "italic")
WORD_FONT = ("Arial", 25, "bold")
SHOW_BUTTON_FONT = ("Arial", 10, "bold")


# UI
window = Tk()
window.title("Flashcard")
window.config(bg=BACKGROUND_COLOR, padx=50, pady=50)


canvas = Canvas(width=392, height=258, highlightthickness=0, bg=BACKGROUND_COLOR)
front_img = PhotoImage(file="./images/card_front.png")
back_img = PhotoImage(file="./images/card_back.png")
canvas_image = canvas.create_image(196, 129)
language_text = canvas.create_text(196, 60, font=LANGUAGE_FONT)
word_text = canvas.create_text(196, 129, font=WORD_FONT)
initial_message = canvas.create_text(196, 129, font=("Arial", 11, "bold"))
canvas.grid(column=0, row=0, columnspan=2)

# BUTTONS
show_button = Button(text="Show answer", bg=SHOW_BUTTON_COLOR, fg="white", font=SHOW_BUTTON_FONT,
                     activebackground=SHOW_BUTTON_COLOR, activeforeground="white", relief="groove", command=flip_card)
show_button.grid(column=0, row=2, columnspan=2, pady=(40,0))

wrong_image = PhotoImage(file="./images/wrong.png")
wrong_button = Button(image=wrong_image, highlightthickness=0, borderwidth=0, activebackground=BACKGROUND_COLOR, command=next_card)
wrong_button.grid(column=0, row=1)

right_image = PhotoImage(file="./images/right.png")
right_button = Button(image=right_image, highlightthickness=0, borderwidth=0, activebackground=BACKGROUND_COLOR, command=remove_card)
right_button.grid(column=1, row=1)
# MAIN

current_card = {}
cards = []
front_language = ""
back_language = ""

try:
    data = pd.read_csv("./data/words_to_learn.csv")
except FileNotFoundError:
    try:
        data = pd.read_csv("./data/words.csv")
    except FileNotFoundError:
        import_button = Button(text="Import CSV", bg=SHOW_BUTTON_COLOR, fg="white", font=SHOW_BUTTON_FONT,
                             activebackground=SHOW_BUTTON_COLOR, activeforeground="white",
                             command=import_csv)
        import_button.grid(column=0, row=0, columnspan=2)
        show_button.grid_forget()
        right_button.grid_forget()
        wrong_button.grid_forget()
    else:
        window.protocol("WM_DELETE_WINDOW", on_closing)
        cards = data.to_dict(orient="records")
        columns = list(data.columns)
        front_language = columns[0]
        back_language = columns[1]
        next_card()
else:
    window.protocol("WM_DELETE_WINDOW", on_closing)
    cards = data.to_dict(orient="records")
    columns = list(data.columns)
    front_language = columns[0]
    back_language = columns[1]
    next_card()


window.mainloop()
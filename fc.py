import tkinter as tk
from tkinter import font as tkFont
import tkinter.simpledialog
import tkinter.messagebox

import json
from pathlib import Path

def load_flashcards():
    file_name = "x.json"
    cur_dir = Path(__file__).parent
    file_path = cur_dir / file_name
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_flashcards(flashcards):
    file_name = "x.json"
    cur_dir = Path(__file__).parent
    file_path = cur_dir / file_name
    with open(file_path, 'w') as file:
        json.dump(flashcards, file, indent=4)

def create_fonts():
    question_answer_font = tkFont.Font(family="Poppins", size=60)
    button_font = tkFont.Font(family="Poppins", size=20)
    return question_answer_font, button_font

# Initialize the root window first
app = tk.Tk()
app.title("Flashcards App")
app.geometry("1080x720")
app.config(bg="#000000")  # Background color of the app
app.resizable(False, False)

# Now create the fonts, after the root window
tk_poppins_qa_font, tk_poppins_button_font = create_fonts()

# Update the status bubble function
def update_status():
    # Make sure this function can safely handle being called
    # before flashcards are loaded or status_label is defined
    if 'status_label' in globals():
        status_text = f"Question {current_card + 1} of {len(flashcards)}"
        status_label.config(text=status_text)

def flip_card(event=None):
    global show_answer, flashcards, current_card
    if show_answer:
        card_label.config(text="Question: " + flashcards[current_card]["question"])
        show_answer = False
    else:
        card_label.config(text="Answer: " + flashcards[current_card]["answer"])
        show_answer = True
    update_status()

def next_card(event=None):
    global current_card, show_answer, flashcards
    if flashcards:
        current_card = (current_card + 1) % len(flashcards)
        flip_card()

def add_card():
    def save_card():
        question = question_entry.get()
        answer = answer_entry.get()
        if question and answer:
            flashcards.append({"question": question, "answer": answer})
            save_flashcards(flashcards)
            add_window.destroy()
            next_card()
            update_status()

    add_window = tk.Toplevel(app)
    add_window.title("Add Flashcard")
    add_window.geometry("600x400")  # Set the size of the pop-up window

    # Set the pop-up window background to match the app's theme if necessary
    add_window.config(bg="#000000") 

    tk.Label(add_window, text="Question:", font=tk_poppins_button_font, bg="#000000", fg="#FFFFFF").pack(pady=(20, 10))
    question_entry = tk.Entry(add_window, font=tk_poppins_button_font)
    question_entry.pack(pady=(0, 20))

    tk.Label(add_window, text="Answer:", font=tk_poppins_button_font, bg="#000000", fg="#FFFFFF").pack(pady=(10, 10))
    answer_entry = tk.Entry(add_window, font=tk_poppins_button_font)
    answer_entry.pack(pady=(0, 20))

    save_button = tk.Button(add_window, text="Save", command=save_card, font=tk_poppins_button_font, fg="#000000")
    save_button.pack(pady=(20, 10))

def update_card():
    if not flashcards:
        return  # No cards to update
    
    def save_update():
        # Get the updated question and answer from the entry fields
        updated_question = question_entry.get()
        updated_answer = answer_entry.get()
        # Update the current card with new values
        flashcards[current_card]['question'] = updated_question
        flashcards[current_card]['answer'] = updated_answer
        # Save the updated list of flashcards
        save_flashcards(flashcards)
        # Close the update window
        update_window.destroy()
        # Refresh the displayed card (in case the current card was updated)
        flip_card()
    
    update_window = tk.Toplevel(app)
    update_window.title("Update Flashcard")
    update_window.geometry("600x400")
    update_window.config(bg="#000000")  # Optional: Set background to match the app theme

    # Pre-populate the entry fields with the current card's data
    current_question = flashcards[current_card]['question']
    current_answer = flashcards[current_card]['answer']

    tk.Label(update_window, text="Question:", font=tk_poppins_button_font, bg="#000000", fg="#FFFFFF").pack(pady=(20, 10))
    question_entry = tk.Entry(update_window, font=tk_poppins_button_font)
    question_entry.pack(pady=(0, 20))
    question_entry.insert(0, current_question)  # Pre-fill with current question

    tk.Label(update_window, text="Answer:", font=tk_poppins_button_font, bg="#000000", fg="#FFFFFF").pack(pady=(10, 10))
    answer_entry = tk.Entry(update_window, font=tk_poppins_button_font)
    answer_entry.pack(pady=(0, 20))
    answer_entry.insert(0, current_answer)  # Pre-fill with current answer

    save_button = tk.Button(update_window, text="Save Update", command=save_update, font=tk_poppins_button_font, fg="#000000")
    save_button.pack(pady=(20, 10))



def delete_card():
    global flashcards
    if flashcards:
        del flashcards[current_card]
        save_flashcards(flashcards)
        next_card()

def skip_to_question():
    global current_card, flashcards
    if not flashcards:
        tk.messagebox.showinfo("Error", "No flashcards available.")
        return

    # Ask for the question number
    question_num = tk.simpledialog.askinteger("Skip to Question", "Enter question number:",
                                              minvalue=1, maxvalue=len(flashcards))
    
    if question_num is not None:
        current_card = question_num - 1  # Adjust for zero-based indexing
        flip_card()


# GUI setup
flashcards = load_flashcards()
current_card = 0
show_answer = False

card_label = tk.Label(app, font=tk_poppins_qa_font, wraplength=500, bg="#6A5ACD", fg="#FFFFFF")
card_label.pack(expand=True, fill="both")
flip_card()

app.bind("<Button-1>", flip_card)

# Button setup, with black font color as requested
add_button = tk.Button(app, text="Add Flashcard", command=add_card, font=tk_poppins_button_font, fg="#000000")
add_button.pack(side=tk.LEFT, padx=20, pady=20)

delete_button = tk.Button(app, text="Delete Flashcard", command=delete_card, font=tk_poppins_button_font, fg="#000000")
delete_button.pack(side=tk.RIGHT, padx=20, pady=20)

next_button = tk.Button(app, text="Next", command=next_card, font=tk_poppins_button_font, fg="#000000")
next_button.pack(side=tk.BOTTOM, pady=20)

update_button = tk.Button(app, text="Update Flashcard", command=update_card, font=tk_poppins_button_font, fg="#000000")
update_button.pack(side=tk.LEFT, padx=20, pady=20)

status_label = tk.Label(app, bg="#6A5ACD", fg="#FFFFFF", font=tk_poppins_button_font)
status_label.pack(side=tk.BOTTOM, fill="x")

skip_button = tk.Button(app, text="Skip to Question", command=skip_to_question, font=tk_poppins_button_font, fg="#000000")
skip_button.place(relx=0.5, y=app.winfo_reqheight() - 100, anchor="s")

# Now it's safe to load flashcards and update the GUI based on them
flashcards = load_flashcards()
current_card = 0
show_answer = False

# Initialize the GUI state based on loaded flashcards
if flashcards:  # Ensure there are flashcards before trying to display them
    flip_card()

app.mainloop()

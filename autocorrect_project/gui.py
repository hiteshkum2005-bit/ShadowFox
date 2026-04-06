import tkinter as tk
from spellchecker import SpellChecker

spell = SpellChecker()

def correct_text():
    text = input_text.get("1.0", tk.END).strip()
    words = text.split()

    corrected = []
    for word in words:
        correction = spell.correction(word)
        if correction is None:
            corrected.append(word)
        else:
            corrected.append(correction)

    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, " ".join(corrected))


def clear_text():
    input_text.delete("1.0", tk.END)
    output_text.delete("1.0", tk.END)


# Create window
root = tk.Tk()
root.title("Autocorrect Keyboard System")
root.geometry("500x400")

# Title
title = tk.Label(root, text="Autocorrect System", font=("Arial", 16, "bold"))
title.pack(pady=10)

# Input Label
input_label = tk.Label(root, text="Enter Text:")
input_label.pack()

# Input Box
input_text = tk.Text(root, height=5, width=50)
input_text.pack(pady=5)

# Buttons Frame
btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

# Correct Button
correct_btn = tk.Button(btn_frame, text="Correct Text", command=correct_text)
correct_btn.grid(row=0, column=0, padx=10)

# Clear Button
clear_btn = tk.Button(btn_frame, text="Clear", command=clear_text)
clear_btn.grid(row=0, column=1, padx=10)

# Output Label
output_label = tk.Label(root, text="Corrected Text:")
output_label.pack()

# Output Box
output_text = tk.Text(root, height=5, width=50)
output_text.pack(pady=5)

# Run app
root.mainloop()
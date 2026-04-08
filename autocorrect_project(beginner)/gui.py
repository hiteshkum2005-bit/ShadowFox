from spellchecker import SpellChecker
import re
spell = SpellChecker()
def extract_punctuation(word: str) -> tuple[str, str, str]:
    match = re.match(r'^(\W*)(.*?)(\W*)$', word)
    if match:
        return match.group(1), match.group(2), match.group(3)
    return "", word, ""
def is_misspelled(word: str) -> bool:
    return word.lower() in spell.unknown([word.lower()])
def get_suggestions(word: str, max_suggestions: int = 5) -> list[str]:
    return list(spell.candidates(word.lower()))[:max_suggestions]
def get_correction(word: str, preserve_case: bool = True) -> str | None:
    word_lower = word.lower()
    if word_lower not in spell.unknown([word_lower]):
        return None
    correction = spell.correction(word_lower)
    if correction and preserve_case:
        if word[0].isupper():
            correction = correction.capitalize()
    return correction
def correct_word(word: str) -> str:
    prefix, core, suffix = extract_punctuation(word)
    lower_core = core.lower()
    if is_misspelled(lower_core):
        correction = get_correction(lower_core)
        if correction:
            core = correction
    return prefix + core + suffix
def correct_text(text: str) -> str:
    words = text.split()
    return " ".join(correct_word(word) for word in words)
def get_error_count(text: str) -> int:
    return sum(1 for word in text.split() if is_misspelled(word.lower()))
import tkinter as tk
from tkinter import ttk
suggestions_window = None
def show_suggestions(event, word, start_idx, end_idx):
    global suggestions_window
    _, core, _ = extract_punctuation(word)
    lower_core = core.lower()
    if not is_misspelled(lower_core):
        return
    try:
        suggestions_window.destroy()
    except (NameError, tk.TclError):
        pass
    suggestions = get_suggestions(lower_core)
    if not suggestions:
        return
    suggestions_window = tk.Toplevel(root)
    suggestions_window.wm_overrideredirect(True)
    x = root.winfo_pointerx() + 10
    y = root.winfo_pointery() + 10
    suggestions_window.geometry(f"+{x}+{y}")
    suggestions_window.configure(bg="#f0f0f0")
    suggestions_window.attributes("-alpha", 0.95)
    header_frame = tk.Frame(suggestions_window, bg="#4a90d9", padx=10, pady=5)
    header_frame.pack(fill=tk.X)
    tk.Label(
        header_frame,
        text=f'"{core}" -> ',
        font=("Segoe UI", 10, "bold"),
        fg="white",
        bg="#4a90d9"
    ).pack(side=tk.LEFT)
    tk.Label(
        header_frame,
        text=f"{len(suggestions)} suggestions",
        font=("Segoe UI", 9),
        fg="#d0e0f0",
        bg="#4a90d9"
    ).pack(side=tk.RIGHT)
    list_frame = tk.Frame(suggestions_window, bg="white")
    list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    clicked = tk.StringVar(value=suggestions[0])
    for suggestion in suggestions:
        btn = tk.Radiobutton(
            list_frame,
            text=suggestion,
            variable=clicked,
            value=suggestion,
            font=("Segoe UI", 10),
            bg="white",
            activebackground="#e8f0ff",
            anchor=tk.W,
            padx=10,
            pady=3,
            command=lambda s=suggestion: clicked.set(s)
        )
        btn.pack(fill=tk.X, pady=1)
    btn_frame = tk.Frame(suggestions_window, bg="#f0f0f0", pady=5)
    btn_frame.pack(fill=tk.X)
    tk.Button(
        btn_frame,
        text="Apply",
        command=lambda: apply_correction(clicked, start_idx, end_idx, word),
        bg="#4CAF50",
        fg="white",
        font=("Segoe UI", 9, "bold"),
        padx=15,
        pady=3,
        relief=tk.FLAT,
        cursor="hand2"
    ).pack(side=tk.LEFT, padx=5)
    tk.Button(
        btn_frame,
        text="Cancel",
        command=suggestions_window.destroy,
        bg="#9e9e9e",
        fg="white",
        font=("Segoe UI", 9),
        padx=15,
        pady=3,
        relief=tk.FLAT,
        cursor="hand2"
    ).pack(side=tk.RIGHT, padx=5)
    def on_key_press(e):
        if e.keysym == "Escape":
            suggestions_window.destroy()
        elif e.keysym == "Return":
            apply_correction(clicked, start_idx, end_idx, word)
    suggestions_window.bind("<KeyPress>", on_key_press)
    clicked.set(suggestions[0])
    suggestions_window.focus()
def apply_correction(clicked, word_start, word_end, original_word):
    selected = clicked.get()
    prefix, core, suffix = extract_punctuation(original_word)
    if selected and selected != core:
        if core[0].isupper():
            selected = selected.capitalize()
        input_text.delete(word_start, word_end)
        input_text.insert(word_start, prefix + selected + suffix)
    suggestions_window.destroy()
    highlight_errors()
    update_status()
def highlight_errors():
    input_text.tag_remove("error", "1.0", tk.END)
    input_text.tag_remove("underline", "1.0", tk.END)
    text = input_text.get("1.0", "end-1c")
    if not text.strip():
        return
    words = text.split()
    start_index = "1.0"
    for word in words:
        idx = input_text.search(r'\m' + word + r'\M', start_index, tk.END, regexp=True)
        if idx:
            _, core, _ = extract_punctuation(word)
            lower_core = core.lower()
            if is_misspelled(lower_core):
                input_text.tag_add("error", idx, f"{idx}+{len(word)}c")
                input_text.tag_add("underline", idx, f"{idx}+{len(word)}c")
            start_index = f"{idx}+{len(word)}c"
def auto_correct_word(event):
    cursor_pos = input_text.index(tk.INSERT)
    line_start = input_text.index(f"{cursor_pos} linestart")
    line_text = input_text.get(line_start, cursor_pos)
    words = line_text.split()
    if not words:
        return
    last_word = words[-1]
    prefix, core, suffix = extract_punctuation(last_word)
    lower_core = core.lower()
    if is_misspelled(lower_core):
        correction = get_correction(lower_core)
        if correction:
            corrected_word = prefix + correction + suffix
            start_pos = f"{cursor_pos} - {len(last_word)} chars"
            input_text.delete(start_pos, cursor_pos)
            input_text.insert(start_pos, corrected_word)
            highlight_errors()
            update_status()
    return None
def on_text_click(event):
    highlight_errors()
    update_status()
    text = input_text.get("1.0", "end-1c").strip()
    if not text:
        return
    words = text.split()
    index = input_text.index(tk.INSERT)
    for word in words:
        idx = input_text.search(r'\m' + word + r'\M', "1.0", tk.END, regexp=True)
        while idx:
            end_idx = f"{idx}+{len(word)}c"
            if input_text.compare(idx, "<=", index) and input_text.compare(index, "<=", end_idx):
                show_suggestions(event, word, idx, end_idx)
                return
            idx = input_text.search(r'\m' + word + r'\M', end_idx, tk.END, regexp=True)
def correct_all():
    text = input_text.get("1.0", "end-1c").strip()
    if not text:
        return
    corrected = correct_text(text)
    input_text.delete("1.0", tk.END)
    input_text.insert("1.0", corrected)
    highlight_errors()
    update_status()
def clear_text():
    input_text.delete("1.0", tk.END)
    input_text.tag_remove("error", "1.0", tk.END)
    input_text.tag_remove("underline", "1.0", tk.END)
    update_status()
def update_status():
    text = input_text.get("1.0", "end-1c").strip()
    word_count = len(text.split()) if text else 0
    char_count = len(text)
    error_count = get_error_count(text)
    status_bar.config(
        text=f"Words: {word_count} | Characters: {char_count} | Errors: {error_count}"
    )
root = tk.Tk()
root.title("Autocorrect System")
root.geometry("650x550")
root.configure(bg="#f5f5f5")
root.resizable(True, True)
style = ttk.Style()
style.theme_use("clam")
header_frame = tk.Frame(root, bg="#4a90d9", pady=15)
header_frame.pack(fill=tk.X)
tk.Label(
    header_frame,
    text="Autocorrect System",
    font=("Segoe UI", 18, "bold"),
    fg="white",
    bg="#4a90d9"
).pack()
controls_frame = tk.Frame(root, bg="#f5f5f5", pady=10)
controls_frame.pack(fill=tk.X, padx=20)
instructions_label = tk.Label(
    controls_frame,
    text="Press SPACE after word to auto-correct | Click underlined word for suggestions",
    font=("Segoe UI", 9, "italic"),
    fg="#666",
    bg="#f5f5f5"
)
instructions_label.pack(side=tk.RIGHT)
input_frame = tk.Frame(root, bg="#f5f5f5", padx=20)
input_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 5))
tk.Label(input_frame, text="Input:", font=("Segoe UI", 11, "bold"), bg="#f5f5f5").pack(anchor=tk.W)
input_text = tk.Text(
    input_frame,
    height=7,
    width=60,
    font=("Segoe UI", 12),
    bg="white",
    relief=tk.SOLID,
    bd=1,
    wrap=tk.WORD,
    padx=10,
    pady=10
)
input_text.pack(fill=tk.BOTH, expand=True, pady=(5, 10))
input_text.tag_configure("error", foreground="#c0392b", background="#fdecea")
input_text.tag_configure("underline", underline=True)
input_text.bind("<KeyRelease>", on_text_click)
input_text.bind("<Button-1>", on_text_click)
input_text.bind("<space>", auto_correct_word)
btn_frame = tk.Frame(root, bg="#f5f5f5", pady=5)
btn_frame.pack()
correct_btn = tk.Button(
    btn_frame,
    text="Correct All",
    command=correct_all,
    bg="#4CAF50",
    fg="white",
    font=("Segoe UI", 10, "bold"),
    padx=20,
    pady=8,
    relief=tk.FLAT,
    cursor="hand2"
)
correct_btn.pack(side=tk.LEFT, padx=10)
clear_btn = tk.Button(
    btn_frame,
    text="Clear",
    command=clear_text,
    bg="#e74c3c",
    fg="white",
    font=("Segoe UI", 10),
    padx=20,
    pady=8,
    relief=tk.FLAT,
    cursor="hand2"
)
clear_btn.pack(side=tk.LEFT, padx=10)
status_bar = tk.Label(
    root,
    text="Words: 0 | Characters: 0 | Errors: 0",
    font=("Segoe UI", 9),
    fg="#666",
    bg="#e0e0e0",
    anchor=tk.W,
    padx=15,
    pady=5
)
status_bar.pack(fill=tk.X, side=tk.BOTTOM)
update_status()
root.mainloop()
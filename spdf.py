import tkinter as tk
from tkinter import filedialog, scrolledtext, ttk, font as tkfont
from PyPDF2 import PdfReader
import time

def read_pdf(file_path, loading_bar):
    reader = PdfReader(file_path)
    num_pages = len(reader.pages)
    text = ''
    for page_num in range(num_pages):
        page = reader.pages[page_num]
        page_text = page.extract_text().strip()
        text += page_text + '\n' if page_text else ''
        # Update loading bar
        loading_bar['value'] = (page_num + 1) * (100 / num_pages)
        loading_bar.update()
        # Simulate loading delay
        time.sleep(0.0001)

    return text


def choose_file():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if file_path:
        entry.delete(0, tk.END)
        entry.insert(0, file_path)

def display_pdf_content():
    file_path = entry.get()
    if file_path:
        loading_screen = tk.Toplevel(root)
        loading_screen.title("Loading...")

        loading_label = tk.Label(loading_screen, text="Loading PDF...")
        loading_label.pack()

        loading_bar = ttk.Progressbar(loading_screen, orient="horizontal", length=300, mode="determinate")
        loading_bar.pack(pady=10)

        # Process events to update the main window
        root.update_idletasks()

        pdf_text = read_pdf(file_path, loading_bar)
        text_box.delete('1.0', tk.END)
        text_box.insert(tk.END, pdf_text)

        loading_screen.destroy()
def change_font(font_name):
    global custom_font
    custom_font = tkfont.Font(family=font_name, size=font_size.get())
    text_box.configure(font=custom_font)

def change_font_size(event=None):
    global custom_font
    custom_font.configure(size=font_size.get())
    text_box.configure(font=custom_font)

def change_text_alignment(event=None):
    alignment = alignment_var.get().lower()
    text_box.tag_configure("alignment", justify=alignment)
    text_box.tag_add("alignment", "1.0", "end")

root = tk.Tk()
root.title("Simple PDF Reader")
root.geometry("800x600")

label = tk.Label(root, text="Select PDF file:")
label.pack()

entry = tk.Entry(root, width=50)
entry.pack()

browse_button = tk.Button(root, text="Browse", command=choose_file)
browse_button.pack()

read_button = tk.Button(root, text="Read PDF", command=display_pdf_content)
read_button.pack()

text_box = scrolledtext.ScrolledText(root, width=80, height=30)
text_box.pack(fill=tk.BOTH, expand=True)
text_box.pack_propagate(False)

font_label = tk.Label(root, text="Select Font:")
font_label.pack()

font_options = ["Arial", "Times New Roman", "Courier New", "Verdana", "Helvetica", "Georgia", "Comic Sans MS", "Impact"]
font_dropdown = tk.OptionMenu(root, tk.StringVar(root, font_options[0]), *font_options, command=change_font)
font_dropdown.pack()

font_size_label = tk.Label(root, text="Font Size:")
font_size_label.pack()

font_size = tk.Scale(root, from_=8, to=36, orient=tk.HORIZONTAL, command=change_font_size)
font_size.set(12)
font_size.pack()

alignment_label = tk.Label(root, text="Text Alignment:")
alignment_label.pack()

alignment_var = tk.StringVar(root, "left")
alignment_dropdown = tk.OptionMenu(root, alignment_var, "Left", "Center", "Right", command=change_text_alignment)
alignment_dropdown.pack()

custom_font = tkfont.Font(family=font_options[0], size=font_size.get())
text_box.configure(font=custom_font)

root.mainloop()

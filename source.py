import tkinter as tk
from tkinter import INSERT, filedialog
from tkinter import messagebox
from turtle import pos
import os

global selected
selected = False

class Menubar:

    def __init__(self, parent):
        font_specs = ("ubuntu", 10)

        menubar = tk.Menu(parent.master, font=font_specs)
        parent.master.config(menu=menubar)

        file_dropdown = tk.Menu(menubar, font=font_specs, tearoff=0)
        file_dropdown.add_command(label="New File",
                                  accelerator="Ctrl+N",
                                  command=parent.new_file)
        file_dropdown.add_command(label="Open File",
                                  accelerator="Ctrl+O",
                                  command=parent.open_file)
        file_dropdown.add_command(label="Save",
                                  accelerator="Ctrl+S",
                                  command=parent.save)
        file_dropdown.add_command(label="Save As",
                                  accelerator="Ctrl+Shift+S",
                                  command=parent.save_as)
        file_dropdown.add_separator()
        file_dropdown.add_command(label="Exit",
                                  command=parent.master.destroy)

        edit_dropdown = tk.Menu(menubar, font=font_specs, tearoff=0)
        edit_dropdown.add_command(label="Cut",
                                  command=parent.cut_text,
                                  accelerator="Ctrl+X")
        edit_dropdown.add_command(label="Copy",
                                  command=parent.copy_text,
                                  accelerator="Ctrl+C")
        edit_dropdown.add_command(label="Paste",
                                  command=parent.paste_text,
                                  accelerator="Ctrl+V")

        options_dropdown = tk.Menu(menubar, font=font_specs, tearoff=0)
        options_dropdown.add_command(label="Dark Mode: ON",
                                     command=parent.dark_on)
        options_dropdown.add_command(label="Dark Mode: OFF",
                                     command=parent.dark_off)

        about_dropdown = tk.Menu(menubar, font=font_specs, tearoff=0)
        about_dropdown.add_command(label="Release Notes",
                                   command=self.show_release_notes)
        about_dropdown.add_separator()
        about_dropdown.add_command(label="About",
                                   command=self.show_about_message)
        about_dropdown.add_command(label="GitHub Repository",
                                   command=parent.repo)

        menubar.add_cascade(label="File", menu=file_dropdown)
        menubar.add_cascade(label="Edit", menu=edit_dropdown)
        menubar.add_cascade(label="Options", menu=options_dropdown)
        menubar.add_cascade(label="About", menu=about_dropdown)

    def show_about_message(self):
        box_title = "About Texter"
        box_message = "The best text editor in python \nBy xKotelek"
        messagebox.showinfo(box_title, box_message)

    def show_release_notes(self):
        box_title = "Release Notes"
        box_message = "Version 1.0 - The first version :)"
        messagebox.showinfo(box_title, box_message)


class Statusbar:

    def __init__(self, parent):

        font_specs = ("classic", 12)
        
        self.status = tk.StringVar()
        self.status.set("Texter - 1.0")

        label = tk.Label(parent.textarea, textvariable=self.status, fg="black",
                         bg="lightgrey", anchor='sw', font=font_specs)
        label.pack(side=tk.BOTTOM, fill=tk.BOTH)

    def update_status(self, *args):
        if isinstance(args[0], bool):
            self.status.set("Your File Has Been Saved!")
        else:
            self.status.set("Texter - 1.0")


class Texter:

    def __init__(self, master):
        master.title("Untitled - Texter")
        master.geometry("1200x700")

        font_specs = ("Courier", 14)

        self.master = master
        self.filename = None

        self.textarea = tk.Text(master, font=font_specs)
        self.scroll = tk.Scrollbar(master, command=self.textarea.yview)
        self.textarea.configure(yscrollcommand=self.scroll.set)
        self.textarea.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.menubar = Menubar(self)
        self.statusbar = Statusbar(self)

        self.bind_shortcuts()

    def set_window_title(self, name=None):
        if name:
            self.master.title(name + " - Texter")
        else:
            self.master.title("Untitled - Texter")

    def new_file(self, *args):
        self.textarea.delete(1.0, tk.END)
        self.filename = None
        self.set_window_title()

    def open_file(self, *args):
        self.filename = filedialog.askopenfilename(
            defaultextension=".txt",
            filetypes=[("All Files", "*.*"),
                       ("Text Files", "*.txt"),
                       ("Python Scripts", "*.py"),
                       ("Markdown Documents", "*.md"),
                       ("JavaScript Files", "*.js"),
                       ("HTML Documents", "*.html"),
                       ("CSS Documents", "*.css")])
        if self.filename:
            self.textarea.delete(1.0, tk.END)
            with open(self.filename, "r") as f:
                self.textarea.insert(1.0, f.read())
            self.set_window_title(self.filename)
    
    def save(self, *args):
        if self.filename:
            try:
                textarea_content = self.textarea.get(1.0, tk.END)
                with open(self.filename, "w") as f:
                    f.write(textarea_content)
                self.statusbar.update_status(True)
            except Exception as e:
                print(e)
        else:
            self.save_as()

    def dark_on(self):
        main_color = "#000000"
        second_color = "#373737"
        text_color = "white"

        master.config(bg=main_color)
        self.textarea.config(bg=second_color, fg=text_color)
        
         

    def dark_off(self):
        main_color = "#FFFFFF"
        second_color = "#FFFFFF"
        text_color = "black"

        master.config(bg=main_color)
        self.textarea.config(bg=second_color, fg=text_color)
        

    def cut_text(self):
        global selected
        if self.textarea.selection_get():
            selected = self.textarea.selection_get()
            self.textarea.delete("sel.first", "sel.last")

    def copy_text(self):
        global selected
        if self.textarea.selection_get():
            selected = self.textarea.selection_get()

    def paste_text(self):
        if selected:
            position = self.textarea.index(INSERT)
            self.textarea.insert(position, selected)

    def repo(self):
        os.system("start https://github.com/PanSkrzynia/texter")

    def save_as(self, *args):
        try:
            new_file = filedialog.asksaveasfilename(
                initialfile="Untitled.txt",
                defaultextension=".txt",
                filetypes=[("All Files", "*.*"),
                        ("Text Files", "*.txt"),
                        ("Python Scripts", "*.py"),
                        ("Markdown Documents", "*.md"),
                        ("JavaScript Files", "*.js"),
                        ("HTML Documents", "*.html"),
                        ("CSS Documents", "*.css")])
            textarea_content = self.textarea.get(1.0, tk.END)
            with open(new_file, "w") as f:
                f.write(textarea_content)
            self.filename = new_file
            self.set_window_title(self.filename)
            self.statusbar.update_status(True)
        except Exception as e:
            print(e)

    def bind_shortcuts(self):
        self.textarea.bind('<Control-n>', self.new_file)
        self.textarea.bind('<Control-o>', self.open_file)
        self.textarea.bind('<Control-s>', self.save)
        self.textarea.bind('<Control-S>', self.save_as)
        self.textarea.bind('<Key>', self.statusbar.update_status)
        


if __name__ == "__main__":
    master = tk.Tk()
    pt = Texter(master)
    master.mainloop()

    master.bind('<Control-x>', Texter.cut_text)
    master.bind('<Control-c>', Texter.copy_text)
    master.bind('<Control-v>', Texter.paste_text)


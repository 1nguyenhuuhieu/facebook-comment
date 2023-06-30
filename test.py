import tkinter as tk
from tkinter import filedialog
from configparser import ConfigParser
import subprocess

class ConfigApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Config App")
        self.geometry("400x200")
        self.config_parser = ConfigParser()

        self.file_path = tk.StringVar()
        self.comments_folder = tk.StringVar()
        self.images_folder = tk.StringVar()
        self.comment_total = tk.IntVar()

        self.create_widgets()

    def create_widgets(self):
        # Select Groups File
        groups_label = tk.Label(self, text="Select Groups File:")
        groups_label.pack()
        groups_frame = tk.Frame(self)
        groups_frame.pack()

        groups_entry = tk.Entry(groups_frame, textvariable=self.file_path)
        groups_entry.pack(side=tk.LEFT)

        groups_button = tk.Button(groups_frame, text="Browse", command=self.browse_file)
        groups_button.pack(side=tk.LEFT)

        # Select Comments Folder
        comments_label = tk.Label(self, text="Select Comments Folder:")
        comments_label.pack()
        comments_frame = tk.Frame(self)
        comments_frame.pack()

        comments_entry = tk.Entry(comments_frame, textvariable=self.comments_folder)
        comments_entry.pack(side=tk.LEFT)

        comments_button = tk.Button(comments_frame, text="Browse", command=self.browse_folder)
        comments_button.pack(side=tk.LEFT)

        # Select Images Folder
        images_label = tk.Label(self, text="Select Images Folder:")
        images_label.pack()
        images_frame = tk.Frame(self)
        images_frame.pack()

        images_entry = tk.Entry(images_frame, textvariable=self.images_folder)
        images_entry.pack(side=tk.LEFT)

        images_button = tk.Button(images_frame, text="Browse", command=self.browse_folder)
        images_button.pack(side=tk.LEFT)

        # Comment Total
        comment_total_label = tk.Label(self, text="Comment Total:")
        comment_total_label.pack()

        comment_total_entry = tk.Entry(self, textvariable=self.comment_total)
        comment_total_entry.pack()

        # Run Button
        run_button = tk.Button(self, text="Run", command=self.run_main)
        run_button.pack()

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        self.file_path.set(file_path)

    def browse_folder(self):
        folder_path = filedialog.askdirectory()
        if self.focus_get().get() == self.comments_folder.get():
            self.comments_folder.set(folder_path)
        elif self.focus_get().get() == self.images_folder.get():
            self.images_folder.set(folder_path)

    def run_main(self):
        config_dict = {
            "GroupsFile": self.file_path.get(),
            "CommentsFolder": self.comments_folder.get(),
            "ImagesFolder": self.images_folder.get(),
            "CommentTotal": str(self.comment_total.get())
        }

        self.config_parser.read_dict(config_dict)
        config_file_path = "config.ini"

        with open(config_file_path, "w") as config_file:
            self.config_parser.write(config_file)

        subprocess.run(["python", "main.py"])

if __name__ == "__main__":
    app = ConfigApp()
    app.mainloop()

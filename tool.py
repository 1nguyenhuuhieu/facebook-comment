import tkinter as tk
from tkinter import filedialog
import configparser
import os


class AppConfigApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("App Configuration")
        self.config_file_path = ""

        self.file_path_txt = ""
        self.comments_folder_path = ""
        self.images_folder_path = ""
        self.comment_total = 0

        self.create_widgets()

    def create_widgets(self):
        # File Path Field: txt file named "groups"
        file_path_label = tk.Label(self, text="File Path (groups):")
        file_path_label.grid(row=0, column=0, sticky="e")

        self.file_path_txt = tk.Entry(self)
        self.file_path_txt.grid(row=0, column=1, padx=5, pady=5)

        file_path_btn = tk.Button(self, text="Browse", command=self.browse_file_path)
        file_path_btn.grid(row=0, column=2)

        # Folder Path Field: "comments"
        comments_folder_path_label = tk.Label(self, text="Folder Path (comments):")
        comments_folder_path_label.grid(row=1, column=0, sticky="e")

        self.comments_folder_path = tk.Entry(self)
        self.comments_folder_path.grid(row=1, column=1, padx=5, pady=5)

        comments_folder_path_btn = tk.Button(self, text="Browse", command=self.browse_comments_folder_path)
        comments_folder_path_btn.grid(row=1, column=2)

        # Folder Path Field: "images"
        images_folder_path_label = tk.Label(self, text="Folder Path (images):")
        images_folder_path_label.grid(row=2, column=0, sticky="e")

        self.images_folder_path = tk.Entry(self)
        self.images_folder_path.grid(row=2, column=1, padx=5, pady=5)

        images_folder_path_btn = tk.Button(self, text="Browse", command=self.browse_images_folder_path)
        images_folder_path_btn.grid(row=2, column=2)

        # Integer Field: "comment total"
        comment_total_label = tk.Label(self, text="Comment Total:")
        comment_total_label.grid(row=3, column=0, sticky="e")

        self.comment_total = tk.Entry(self)
        self.comment_total.grid(row=3, column=1, padx=5, pady=5)

        # API Field: "api"
        api_label = tk.Label(self, text="API proxy key:")
        api_label.grid(row=4, column=0, sticky="e")

        self.api = tk.Entry(self)
        self.api.grid(row=4, column=1, padx=5, pady=5)

        # Save and Load Buttons
        save_button = tk.Button(self, text="Save Config", command=self.save_config)
        save_button.grid(row=5, column=0, padx=5, pady=5)

        load_button = tk.Button(self, text="Load Config", command=self.load_config)
        load_button.grid(row=5, column=1, padx=5, pady=5)

        # Run main.py Button
        run_button = tk.Button(self, text="Run main.py", command=self.run_main)
        run_button.grid(row=5, column=2, padx=5, pady=5)

    def browse_file_path(self):
        file_path = filedialog.askopenfilename(filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
        if file_path:
            self.file_path_txt.delete(0, tk.END)
            self.file_path_txt.insert(0, file_path)

    def browse_comments_folder_path(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.comments_folder_path.delete(0, tk.END)
            self.comments_folder_path.insert(0, folder_path)

    def browse_images_folder_path(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.images_folder_path.delete(0, tk.END)
            self.images_folder_path.insert(0, folder_path)

    def save_config(self):
        config = configparser.ConfigParser()
        config["Paths"] = {
            "file_path": self.file_path_txt.get(),
            "comments_folder_path": self.comments_folder_path.get(),
            "images_folder_path": self.images_folder_path.get()
        }
        config["Settings"] = {
            "comment_total": str(self.comment_total.get()),
            "api": str(self.api.get())
        }

        save_path = filedialog.asksaveasfilename(defaultextension=".ini", filetypes=(("INI Files", "*.ini"), ("All Files", "*.*")))
        if save_path:
            with open(save_path, "w") as config_file:
                config.write(config_file)
            self.config_file_path = save_path

    def load_config(self):
        config_path = filedialog.askopenfilename(filetypes=(("INI Files", "*.ini"), ("All Files", "*.*")))
        if config_path:
            config = configparser.ConfigParser()
            config.read(config_path)

            if "Paths" in config and "Settings" in config:
                paths = config["Paths"]
                settings = config["Settings"]

                self.file_path_txt.delete(0, tk.END)
                self.file_path_txt.insert(0, paths.get("file_path", ""))

                self.comments_folder_path.delete(0, tk.END)
                self.comments_folder_path.insert(0, paths.get("comments_folder_path", ""))

                self.images_folder_path.delete(0, tk.END)
                self.images_folder_path.insert(0, paths.get("images_folder_path", ""))

                self.comment_total.delete(0, tk.END)
                self.comment_total.insert(0, settings.get("comment_total", ""))

                self.api.delete(0, tk.END)
                self.api.insert(0, settings.get("api", ""))

            self.config_file_path = config_path

    def run_main(self):
        if self.config_file_path and os.path.isfile(self.config_file_path):
            os.system(f"python main.py --config {self.config_file_path}")
        else:
            print("Please save or load a valid config file before running main.py")


if __name__ == "__main__":
    app = AppConfigApp()
    app.mainloop()

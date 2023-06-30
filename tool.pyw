import tkinter as tk
from tkinter import filedialog
import configparser

class ConfigApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Config App")
        
        # Create the labels and entry fields
        self.file_path_label = tk.Label(self, text="File Path:")
        self.file_path_label.grid(row=0, column=0, sticky="e")
        self.file_path_entry = tk.Entry(self)
        self.file_path_entry.grid(row=0, column=1, padx=5, pady=5)
        
        self.groups_label = tk.Label(self, text="Groups:")
        self.groups_label.grid(row=1, column=0, sticky="e")
        self.groups_entry = tk.Entry(self)
        self.groups_entry.grid(row=1, column=1, padx=5, pady=5)
        
        self.comments_folder_label = tk.Label(self, text="Comments Folder Path:")
        self.comments_folder_label.grid(row=2, column=0, sticky="e")
        self.comments_folder_entry = tk.Entry(self)
        self.comments_folder_entry.grid(row=2, column=1, padx=5, pady=5)
        
        self.images_folder_label = tk.Label(self, text="Images Folder Path:")
        self.images_folder_label.grid(row=3, column=0, sticky="e")
        self.images_folder_entry = tk.Entry(self)
        self.images_folder_entry.grid(row=3, column=1, padx=5, pady=5)
        
        self.comment_total_label = tk.Label(self, text="Comment Total:")
        self.comment_total_label.grid(row=4, column=0, sticky="e")
        self.comment_total_entry = tk.Entry(self)
        self.comment_total_entry.grid(row=4, column=1, padx=5, pady=5)
        
        # Create the buttons
        self.save_button = tk.Button(self, text="Save", command=self.save_config)
        self.save_button.grid(row=5, column=0, padx=5, pady=10)
        
        self.load_button = tk.Button(self, text="Load", command=self.load_config)
        self.load_button.grid(row=5, column=1, padx=5, pady=10)
        
    def save_config(self):
        config = configparser.ConfigParser()
        
        config['DEFAULT'] = {
            'file_path': self.file_path_entry.get(),
            'groups': self.groups_entry.get(),
            'comments_folder_path': self.comments_folder_entry.get(),
            'images_folder_path': self.images_folder_entry.get(),
            'comment_total': self.comment_total_entry.get()
        }
        
        file_path = filedialog.asksaveasfilename(defaultextension=".ini")
        if file_path:
            with open(file_path, 'w') as config_file:
                config.write(config_file)
            print("Config file saved.")
    
    def load_config(self):
        file_path = filedialog.askopenfilename(filetypes=[('INI Files', '*.ini')])
        if file_path:
            config = configparser.ConfigParser()
            config.read(file_path)
            
            self.file_path_entry.delete(0, tk.END)
            self.file_path_entry.insert(tk.END, config['DEFAULT']['file_path'])
            
            self.groups_entry.delete(0, tk.END)
            self.groups_entry.insert(tk.END, config['DEFAULT']['groups'])
            
            self.comments_folder_entry.delete(0, tk.END)
            self.comments_folder_entry.insert(tk.END, config['DEFAULT']['comments_folder_path'])

import tkinter as tk
from tkinter import ttk

from main import functionality

class SimpleOutputInterface:
    def __init__(self, master):
        self.master = master
        master.title("Simple Output Interface")
        master.geometry("2560x1600")
        master.configure(bg='#f0f0f0')

        self.create_widgets()

    def create_widgets(self):
        # Input frame
        input_frame = ttk.Frame(self.master, padding="10 10 10 0")
        input_frame.pack(fill=tk.X)

        input_label = ttk.Label(input_frame, text="Enter input:")
        input_label.pack(anchor=tk.W)

        self.input_entry = ttk.Entry(input_frame, width=50)
        self.input_entry.pack(side=tk.LEFT, expand=True, fill=tk.X)

        submit_button = ttk.Button(input_frame, text="Submit", command=self.on_submit)
        submit_button.pack(side=tk.RIGHT, padx=(10, 0))

        # Output frame
        output_frame = ttk.Frame(self.master, padding="10")
        output_frame.pack(expand=True, fill=tk.BOTH)

        output_label = ttk.Label(output_frame, text="Output:")
        output_label.pack(anchor=tk.W)

        self.output_text = tk.Text(output_frame, wrap=tk.WORD, state="disabled", height=15)
        self.output_text.pack(expand=True, fill=tk.BOTH)

        # Scrollbar for output
        scrollbar = ttk.Scrollbar(output_frame, orient="vertical", command=self.output_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.output_text.configure(yscrollcommand=scrollbar.set)

    def on_submit(self):
        input_text = self.input_entry.get()
        if input_text:
            output = functionality(input_text)
            self.update_output(output)
            self.input_entry.delete(0, tk.END)
        else:
            self.update_output("Please enter some input.")

    def update_output(self, text):
        self.output_text.configure(state="normal")
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, text)
        self.output_text.configure(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleOutputInterface(root)
    root.mainloop()
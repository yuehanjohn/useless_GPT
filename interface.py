import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont

#from main import functionality

def alternate_capitalization(text):
    result = []
    for i, char in enumerate(text):
        if i % 2 == 0:
            result.append(char.upper())
        else:
            result.append(char.lower())
    return ''.join(result)

class EnhancedOutputInterface:
    def __init__(self, master):
        self.master = master
        master.title("Enhanced Output Interface")
        master.geometry("2560x1600")
        master.configure(bg='#f0f0f0')

        self.create_widgets()

    def create_widgets(self):
        # Customize font sizes here
        label_font_size = 18     # Size for labels
        input_font_size = 20     # Size for input text area
        output_font_size = 20    # Size for output text area

        # Set up fonts
        label_font = tkfont.Font(family="TkDefaultFont", size=label_font_size)
        input_font = tkfont.Font(family="TkTextFont", size=input_font_size)
        output_font = tkfont.Font(family="TkTextFont", size=output_font_size)

        # Input frame (15% of screen height)
        input_frame = ttk.Frame(self.master, padding="10")
        input_frame.pack(fill=tk.X, pady=(0, 10))

        input_label = ttk.Label(input_frame, text="Enter input:", font=label_font)
        input_label.pack(anchor=tk.W)

        self.input_entry = tk.Text(input_frame, wrap=tk.WORD, height=int(0.15 * 1600 / input_font.metrics()['linespace']), font=input_font)
        self.input_entry.pack(fill=tk.X, expand=True)

        submit_button = ttk.Button(input_frame, text="Submit", command=self.on_submit)
        submit_button.pack(pady=(10, 0))

        # Output frame
        output_frame = ttk.Frame(self.master, padding="10")
        output_frame.pack(expand=True, fill=tk.BOTH)

        output_label = ttk.Label(output_frame, text="Output:", font=label_font)
        output_label.pack(anchor=tk.W)

        self.output_text = tk.Text(output_frame, wrap=tk.WORD, state="disabled", font=output_font)
        self.output_text.pack(expand=True, fill=tk.BOTH)

        # Scrollbar for output
        scrollbar = ttk.Scrollbar(output_frame, orient="vertical", command=self.output_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.output_text.configure(yscrollcommand=scrollbar.set)

    def on_submit(self):
        input_text = self.input_entry.get("1.0", tk.END).strip()
        if input_text:
            output = input_text  # Replace this with functionality(input_text) when ready
            #output = functionality(input_text)
            self.update_output(f"{output}\n\n")  # Only output text is added
            self.input_entry.delete("1.0", tk.END)
        else:
            self.update_output("Please enter some input.\n\n")

    def update_output(self, text):
        text = alternate_capitalization(text)
        self.output_text.configure(state="normal")
        self.output_text.insert("1.0", text)  # Insert at the beginning
        self.output_text.configure(state="disabled")
        self.output_text.see("1.0")  # Scroll to the top

if __name__ == "__main__":
    root = tk.Tk()
    app = EnhancedOutputInterface(root)
    root.mainloop()
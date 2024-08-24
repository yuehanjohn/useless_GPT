import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
import io

from main import functionality, opposite_text

def alternate_capitalization(text):
    return ''.join(char.upper() if i % 2 == 0 else char.lower() for i, char in enumerate(text))

def generate_image(prompt):
    url = f"https://image.pollinations.ai/prompt/{prompt}"
    response = requests.get(url)
    
    if response.status_code == 200:
        image_data = io.BytesIO(response.content)
        pil_image = Image.open(image_data)
        pil_image = pil_image.resize((800, 600), Image.LANCZOS)
        tk_image = ImageTk.PhotoImage(pil_image)
        return tk_image
    else:
        print(f"Failed to retrieve image. Status code: {response.status_code}")
        return None

class EnhancedOutputInterface:
    def __init__(self, master):
        self.master = master
        master.title("Enhanced Output Interface")
        master.geometry("1920x1080")
        master.configure(bg='#f0f0f0')

        self.create_widgets()

    def create_widgets(self):
        label_font_size = 18
        input_font_size = 20
        output_font_size = 20

        label_font = tkfont.Font(family="TkDefaultFont", size=label_font_size)
        input_font = tkfont.Font(family="TkTextFont", size=input_font_size)
        output_font = tkfont.Font(family="TkTextFont", size=output_font_size)

        input_frame = ttk.Frame(self.master, padding="10")
        input_frame.pack(fill=tk.X, pady=(0, 10))

        input_label = ttk.Label(input_frame, text="Enter input:", font=label_font)
        input_label.pack(anchor=tk.W)

        self.input_entry = tk.Text(input_frame, wrap=tk.WORD, height=int(0.15 * 1600 / input_font.metrics()['linespace']), font=input_font)
        self.input_entry.pack(fill=tk.X, expand=True)

        submit_button = ttk.Button(input_frame, text="Submit", command=self.on_submit)
        submit_button.pack(pady=(10, 0))

        self.output_frame = ttk.Frame(self.master, padding="10")
        self.output_frame.pack(expand=True, fill=tk.BOTH)

        self.text_output_frame = ttk.Frame(self.output_frame)
        self.text_output_frame.grid(row=0, column=0, sticky="nsew")

        output_label = ttk.Label(self.text_output_frame, text="Output:", font=label_font)
        output_label.pack(anchor=tk.W)

        self.output_text = tk.Text(self.text_output_frame, wrap=tk.WORD, state="disabled", font=output_font)
        self.output_text.pack(expand=True, fill=tk.BOTH)

        text_scrollbar = ttk.Scrollbar(self.text_output_frame, orient="vertical", command=self.output_text.yview)
        text_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.output_text.configure(yscrollcommand=text_scrollbar.set)

        self.image_output_frame = ttk.Frame(self.output_frame)
        self.image_output_frame.grid(row=0, column=1, sticky="nsew")

        image_label = ttk.Label(self.image_output_frame, text="Image Output:", font=label_font)
        image_label.pack(anchor=tk.W)

        self.image_canvas = tk.Canvas(self.image_output_frame, bg="white", width=800, height=600)
        self.image_canvas.pack(expand=True, fill=tk.BOTH)

        self.set_frame_widths(text_width=70, image_width=30)

        adjust_button = ttk.Button(self.master, text="Adjust Frame Widths", command=self.adjust_frame_widths)
        adjust_button.pack(pady=10)

        self.output_frame.rowconfigure(0, weight=1)
        self.output_frame.columnconfigure(0, weight=70)
        self.output_frame.columnconfigure(1, weight=30)

    def set_frame_widths(self, text_width, image_width):
        self.output_frame.columnconfigure(0, weight=text_width)
        self.output_frame.columnconfigure(1, weight=image_width)

    def adjust_frame_widths(self):
        dialog = tk.Toplevel(self.master)
        dialog.title("Adjust Frame Widths")

        tk.Label(dialog, text="Text Frame Width (%):").grid(row=0, column=0)
        text_entry = tk.Entry(dialog)
        text_entry.grid(row=0, column=1)
        text_entry.insert(0, str(self.output_frame.grid_columnconfigure(0)['weight']))

        tk.Label(dialog, text="Image Frame Width (%):").grid(row=1, column=0)
        image_entry = tk.Entry(dialog)
        image_entry.grid(row=1, column=1)
        image_entry.insert(0, str(self.output_frame.grid_columnconfigure(1)['weight']))

        def apply_widths():
            try:
                text_width = int(text_entry.get())
                image_width = int(image_entry.get())
                if text_width + image_width != 100:
                    raise ValueError("Widths must sum to 100")
                self.set_frame_widths(text_width, image_width)
                dialog.destroy()
            except ValueError as e:
                messagebox.showerror("Error", str(e))

        tk.Button(dialog, text="Apply", command=apply_widths).grid(row=2, column=0, columnspan=2)

    def on_submit(self):
        input_text = self.input_entry.get("1.0", tk.END).strip()
        if input_text:
            output = functionality(input_text)  # Replace this with functionality(input_text) when ready
            self.update_output(f"{output}\n\n")
            self.input_entry.delete("1.0", tk.END)
            
            img = generate_image(output)
            if img:
                self.display_image(img)
            else:
                self.display_placeholder_image()
        else:
            self.update_output("Please enter some input.\n\n")

    def update_output(self, text):
        text = alternate_capitalization(text)
        self.output_text.configure(state="normal")
        self.output_text.insert("1.0", text)  # Insert at the beginning
        self.output_text.configure(state="disabled")
        self.output_text.see("1.0")  # Scroll to the top

    def display_image(self, img):
        self.image_canvas.delete("all")  # Clear previous image
        
        # Get the dimensions of the canvas and image
        canvas_width = self.image_canvas.winfo_width()
        canvas_height = self.image_canvas.winfo_height()
        img_width = img.width()
        img_height = img.height()
        
        # Calculate the position to center the image
        x = (canvas_width - img_width) // 2
        y = (canvas_height - img_height) // 2
        
        # Create the image on the canvas at the calculated position
        self.image_canvas.create_image(x, y, anchor=tk.NW, image=img)
        self.image_canvas.image = img  # Keep a reference to prevent garbage collection

    def display_placeholder_image(self):
        image = Image.new('RGB', (800, 600), color='lightgray')
        photo = ImageTk.PhotoImage(image)
        
        # Get the dimensions of the canvas and image
        canvas_width = self.image_canvas.winfo_width()
        canvas_height = self.image_canvas.winfo_height()
        img_width = photo.width()
        img_height = photo.height()
        
        # Calculate the position to center the image
        x = (canvas_width - img_width) // 2
        y = (canvas_height - img_height) // 2
        
        self.image_canvas.delete("all")  # Clear previous image
        self.image_canvas.create_image(x, y, anchor=tk.NW, image=photo)
        self.image_canvas.image = photo  # Keep a reference to prevent garbage collection


if __name__ == "__main__":
    root = tk.Tk()
    app = EnhancedOutputInterface(root)
    root.mainloop()
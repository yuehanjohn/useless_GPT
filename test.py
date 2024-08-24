import requests
from tkinter import Tk, Label, PhotoImage
from PIL import Image, ImageTk
import io

# Function to fetch and display the image
def fetch_and_display_image(prompt):
    # Construct the URL with the prompt
    url = f"https://image.pollinations.ai/prompt/{prompt}"
    
    # Request the image
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Open the image from the response content
        image_data = io.BytesIO(response.content)
        image = Image.open(image_data)

        # Create a Tkinter window
        root = Tk()
        root.title("Text to Image")

        # Convert the image to a format Tkinter can use
        tk_image = ImageTk.PhotoImage(image)

        # Create a label to display the image
        label = Label(root, image=tk_image)
        label.pack()

        # Start the Tkinter event loop
        root.mainloop()
    else:
        print(f"Failed to retrieve image. Status code: {response.status_code}")

# Example usage
fetch_and_display_image("a mountain")
import requests
from PIL import Image, ImageTk
import io

def generate_image(prompt):
    # Construct the URL with the prompt
    url = f"https://image.pollinations.ai/prompt/{prompt}"
    
    # Request the image
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Open the image from the response content
        image_data = io.BytesIO(response.content)
        pil_image = Image.open(image_data)
        
        # Resize the image to fit the canvas (adjust size as needed)
        pil_image = pil_image.resize((800, 600), Image.LANCZOS)
        
        # Convert PIL Image to Tkinter-compatible PhotoImage
        tk_image = ImageTk.PhotoImage(pil_image)
        
        return tk_image
    else:
        print(f"Failed to retrieve image. Status code: {response.status_code}")
        return None
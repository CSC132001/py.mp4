import openai
import pytesseract
from PIL import Image
import tkinter as tk
from tkinter import filedialog, Text, Label, Button
import cv2  # For camera capture

# Set up Tesseract command path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Set up OpenAI API Key
openai.api_key = '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'  # Make sure to replace this with your API key

# OCR Function to extract text from an image
def extract_text_from_image(image_path):
    try:
        image = Image.open(image_path)
        return pytesseract.image_to_string(image)
    except Exception as e:
        return str(e)

# OpenAI function for generating replacements
def get_ai_replacement(ingredient, recipe):
    messages = [
        {"role": "user", "content": f"I have a recipe that uses {ingredient}. What is an optimal replacement, how much should I use, and how will it affect the recipe? Limit the answer to under 700 characters, includeing spaces."}
    ]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=150
        )
        ai_response = response.choices[0].message['content'].strip()

        # Truncate the response to 700 characters
        if len(ai_response) > 700:
            ai_response = ai_response[:700] + "..."
        return ai_response
    except Exception as e:
        return f"Error calling OpenAI API: {str(e)}"

# Tkinter App for input and interaction
class RecipeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Recipe Ingredient Replacement")
        self.recipe_text = ""

        # UI Elements
        self.label = Label(root, text="Upload a Recipe or Enter the Text")
        self.label.pack()

        self.text_box = Text(root, height=12, width=50)
        self.text_box.pack()

        self.upload_button = Button(root, text="Upload Recipe Image", command=self.upload_image)
        self.upload_button.pack()

        self.camera_button = Button(root, text="Capture Recipe via Camera", command=self.capture_image)
        self.camera_button.pack()

        self.label2 = Label(root, text="Enter Ingredient to Replace")
        self.label2.pack()

        self.ingredient_entry = Text(root, height=1, width=20)
        self.ingredient_entry.pack()

        self.submit_button = Button(root, text="Get Replacement", command=self.get_replacement)
        self.submit_button.pack()

        self.result_label = Label(root, text="", wraplength=400)
        self.result_label.pack()

    def upload_image(self):
        # Open a file dialog to choose an image
        file_path = filedialog.askopenfilename()
        if file_path:
            self.recipe_text = extract_text_from_image(file_path)
            self.text_box.delete("1.0", tk.END)  # Clear previous text
            self.text_box.insert(tk.END, self.recipe_text)

    def capture_image(self):
        # Try to use the external USB camera (index 1)
        cap = cv2.VideoCapture(1)  # Change this index if needed (1 is for external cameras)

        if not cap.isOpened():
            self.result_label.config(text="Could not open USB webcam.")
            return

        # Read a frame from the camera
        ret, frame = cap.read()
        if not ret:
            self.result_label.config(text="Failed to capture image.")
            cap.release()
            return

        # Save the captured image to a file
        img_path = "captured_image.png"
        cv2.imwrite(img_path, frame)

        # Release the camera
        cap.release()

        # Process the captured image with Tesseract and display the text
        self.recipe_text = extract_text_from_image(img_path)
        self.text_box.delete("1.0", tk.END)  # Clear previous text
        self.text_box.insert(tk.END, self.recipe_text)

    def get_replacement(self):
        # Get the ingredient input and recipe
        ingredient = self.ingredient_entry.get("1.0", tk.END).strip()
        recipe = self.text_box.get("1.0", tk.END).strip()

        if ingredient and recipe:
            replacement_info = get_ai_replacement(ingredient, recipe)
            self.result_label.config(text=replacement_info)  # Display replacement info in UI
        else:
            self.result_label.config(text="Please enter a valid recipe and ingredient.")

# Run the Tkinter app
root = tk.Tk()
app = RecipeApp(root)
root.mainloop()

import openai
import pytesseract
from PIL import Image
import tkinter as tk
from tkinter import filedialog, Text, Label, Button, Checkbutton, IntVar, Scrollbar, Canvas, Frame
from tkinter.font import Font
import cv2

# Set up Tesseract command path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Set up OpenAI API Key


# OCR Function to extract text from an image
def extract_text_from_image(image_path):
    try:
        image = Image.open(image_path)
        return pytesseract.image_to_string(image)
    except Exception as e:
        return str(e)

# OpenAI function for generating replacements
def get_ai_replacement(ingredient):
    messages = [
        {"role": "user", "content": f"I have a recipe that uses {ingredient}. What is an optimal replacement, how much should I use, and how will it affect the recipe? Limit the answer to 350 characters per ingredient, including spaces."}
    ]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=350
        )
        ai_response = response.choices[0].message['content'].strip()
        return ai_response[:350] if len(ai_response) > 350 else ai_response
    except Exception as e:
        return f"Error calling OpenAI API: {str(e)}"

# Tkinter App for input and interaction
class RecipeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Recipe Ingredient Replacement")
        self.root.geometry("900x600")

        self.recipe_text = ""
        self.default_font = Font(family="Arial", size=14)

        # Main frame for content and results side by side
        self.main_frame = Frame(root)
        self.main_frame.pack(fill="both", expand=True)

        # Left frame for text input and checkboxes
        self.left_frame = Frame(self.main_frame)
        self.left_frame.pack(side="left", fill="both", expand=True, padx=(10, 5), pady=10)

        # Right frame for results display
        self.right_frame = Frame(self.main_frame, width=300)
        self.right_frame.pack(side="right", fill="y", padx=(5, 10), pady=10)

        # UI Elements
        self.label = Label(self.left_frame, text="Upload a Recipe or Enter Ingredients (one per line)", font=self.default_font)
        self.label.pack(pady=5)

        # Create a canvas with scrollbar for ingredients and checkboxes
        self.canvas = Canvas(self.left_frame)
        self.canvas.pack(fill="both", expand=True, pady=(0, 10))

        self.scrollbar = Scrollbar(self.left_frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Frame inside canvas for content
        self.frame = Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")

        # Ingredients and checkboxes setup
        self.ingredients_text = Text(self.frame, height=12, width=40, font=self.default_font)
        self.ingredients_text.grid(row=0, column=1, sticky="n")

        # Buttons for image upload and camera capture
        self.upload_button = Button(self.frame, text="Upload Recipe Image", command=self.upload_image, font=self.default_font)
        self.upload_button.grid(row=1, column=0, columnspan=2, pady=5)

        self.camera_button = Button(self.frame, text="Capture Recipe via Camera", command=self.capture_image, font=self.default_font)
        self.camera_button.grid(row=2, column=0, columnspan=2, pady=5)

        # Get Replacement button
        self.submit_button = Button(self.frame, text="Get Replacement", command=self.get_replacement, font=self.default_font)
        self.submit_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Update checkboxes as user types
        self.ingredients_text.bind("<KeyRelease>", self.update_checkboxes)

        # Update scroll region when window resizes
        self.frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Right-side label and text area for displaying replacements
        self.result_label = Label(self.right_frame, text="Replacement Suggestions", font=self.default_font)
        self.result_label.pack(pady=5)

        self.result_text = Text(self.right_frame, wrap="word", font=self.default_font, height=30, width=35)
        self.result_text.pack(fill="both", expand=True)

        # Track the checkbuttons and variables
        self.check_vars = {}

    def clear_checkboxes(self):
        # Clear existing checkboxes
        for line_index in list(self.check_vars.keys()):
            self.ingredients_text.delete(line_index)
            del self.check_vars[line_index]

    def add_checkboxes_for_ocr_text(self):
        # Add checkboxes for each line in OCR text
        lines = self.ingredients_text.get("1.0", tk.END).strip().split("\n")
        for i, line in enumerate(lines):
            line_index = f"{i + 1}.0"
            if line.strip() and line_index not in self.check_vars:
                var = IntVar()
                self.check_vars[line_index] = var
                self.ingredients_text.window_create(line_index, window=Checkbutton(self.ingredients_text, variable=var))

    def update_checkboxes(self, event=None):
        # Clear previous checkboxes and add new ones
        self.clear_checkboxes()
        self.add_checkboxes_for_ocr_text()

        # Prevent extra newlines when pressing Enter
        if event and event.keysym == "Return":
            return "break"

    def upload_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.recipe_text = extract_text_from_image(file_path)
            self.ingredients_text.delete("1.0", tk.END)
            self.ingredients_text.insert(tk.END, self.recipe_text)
            self.update_checkboxes()  # Update checkboxes after inserting text

    def capture_image(self):
        cap = cv2.VideoCapture(1)
        if not cap.isOpened():
            self.result_text.insert(tk.END, "Could not open USB webcam.\n")
            return

        ret, frame = cap.read()
        if not ret:
            self.result_text.insert(tk.END, "Failed to capture image.\n")
            cap.release()
            return

        img_path = "captured_image.png"
        cv2.imwrite(img_path, frame)
        cap.release()

        self.recipe_text = extract_text_from_image(img_path)
        self.ingredients_text.delete("1.0", tk.END)
        self.ingredients_text.insert(tk.END, self.recipe_text)
        self.update_checkboxes()  # Update checkboxes after inserting text

    def get_replacement(self):
        # Clear the result text box before displaying new results
        self.result_text.delete("1.0", tk.END)
        
        # Get all lines of ingredients text and loop through each one
        lines = self.ingredients_text.get("1.0", tk.END).strip().split("\n")
        replacements = []

        for i, line in enumerate(lines):
            line_index = f"{i + 1}.0"  # Line index in Text widget starts from 1
            if self.check_vars.get(line_index) and self.check_vars[line_index].get() == 1:
                # Checkbox is selected, call OpenAI for replacement
                replacement = get_ai_replacement(line.strip())
                replacements.append(f"{line}: {replacement}\n")

        if replacements:
            self.result_text.insert(tk.END, "\n\n".join(replacements))
        else:
            self.result_text.insert(tk.END, "No ingredients selected for replacement.")

# Run the Tkinter app
root = tk.Tk()
app = RecipeApp(root)
root.mainloop()

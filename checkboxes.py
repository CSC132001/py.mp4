import tkinter as tk
from tkinter import filedialog, Label, Button, Checkbutton, IntVar, Scrollbar, Canvas, Frame
from tkinter.font import Font

# Tkinter App for input and interaction
class RecipeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Recipe Ingredient Replacement")
        self.root.geometry("900x600")  # Expanded width to make room for right-side replacements

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
        self.ingredients_text = tk.Text(self.frame, height=12, width=40, font=self.default_font)
        self.ingredients_text.grid(row=0, column=1, sticky="n")

        self.checkbox_frame = Frame(self.frame)
        self.checkbox_frame.grid(row=0, column=0, padx=5, sticky="n")

        # Buttons for image upload and camera capture
        self.upload_button = Button(self.frame, text="Upload Recipe Image", command=self.upload_image, font=self.default_font)
        self.upload_button.grid(row=1, column=0, columnspan=2, pady=5)

        self.camera_button = Button(self.frame, text="Capture Recipe via Camera", command=self.capture_image, font=self.default_font)
        self.camera_button.grid(row=2, column=0, columnspan=2, pady=5)

        # Get Replacement button
        self.submit_button = Button(self.frame, text="Get Replacement", command=self.get_replacement, font=self.default_font)
        self.submit_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Update scroll region when window resizes
        self.frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Right-side label and text area for displaying results
        self.result_label = Label(self.right_frame, text="Replacement Suggestions", font=self.default_font)
        self.result_label.pack(pady=5)

        self.result_text = tk.Text(self.right_frame, wrap="word", font=self.default_font, height=30, width=35)
        self.result_text.pack(fill="both", expand=True)

        # Track the checkbuttons and variables
        self.check_vars = {}

        # Bind event only for Enter key to update checkboxes
        self.ingredients_text.bind("<Return>", self.update_checkboxes)
        self.ingredients_text.bind("<Tab>", self.insert_indent)

    def insert_indent(self, event=None):
        """Inserts a tab when Tab is pressed in the text widget."""
        self.ingredients_text.insert(tk.INSERT, "\t")
        return "break"  # Prevents default behavior

    def update_checkboxes(self, event=None):
        # Prevent default newline behavior on Enter key
        self.ingredients_text.insert(tk.INSERT, "\n")
        
        # Get current ingredients, split by line
        ingredients = self.ingredients_text.get("1.0", tk.END).strip().split("\n")

        # Clear existing checkboxes to avoid duplicates
        for widget in self.ingredients_text.window_names():
            self.ingredients_text.window_configure(widget, window="")

        # Add checkboxes for each line in the text box
        self.check_vars.clear()  # Reset checkbox variables
        for idx, ingredient in enumerate(ingredients):
            if ingredient.strip():  # Skip empty lines
                var = IntVar()
                self.check_vars[ingredient] = var
                # Insert checkbox at the start of each line
                self.ingredients_text.window_create(f"{idx + 1}.0", window=tk.Checkbutton(self.ingredients_text, variable=var))
        
        # Return "break" to prevent adding an extra newline
        return "break"

    def get_replacement(self):
        # Get ingredients from the text box and replacements for selected ones
        replacements = []
        for ingredient, var in self.check_vars.items():
            if var.get() == 1:
                replacement = get_ai_replacement(ingredient)
                replacements.append(f"{ingredient}: {replacement}")

        # Display the replacements below the button
        self.result_label.config(text="\n".join(replacements) if replacements else "No ingredients selected for replacement.")
    def upload_image(self):
        # Placeholder for image upload functionality
        pass

    def capture_image(self):
        # Placeholder for camera capture functionality
        pass

    def get_replacement(self):
        # Placeholder for getting replacements functionality
        pass

# Run the Tkinter app
root = tk.Tk()
app = RecipeApp(root)
root.mainloop()
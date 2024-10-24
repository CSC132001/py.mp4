import tkinter as tk
from tkinter import Label, Button, Text, Checkbutton, IntVar, Scrollbar, Canvas
from tkinter.font import Font

# Function to generate replacements (using OpenAI API if needed)
def get_ai_replacement(ingredient):
    # Placeholder function for ingredient replacement
    return f"Replacement for {ingredient}"

# Tkinter App for input and interaction
class RecipeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Recipe Ingredient Replacement")

        # Set default font to size 14
        self.default_font = Font(family="Arial", size=14)

        # UI Elements
        self.label = Label(root, text="Enter Ingredients (one per line)", font=self.default_font)
        self.label.pack(pady=10)

        # Create a canvas to manage scrolling and dynamic sizing
        self.canvas = Canvas(root)
        self.canvas.pack(side="top", fill="both", expand=True, pady=10)

        # Scrollbar for the canvas
        self.scrollbar = Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Create a frame inside the canvas to hold the content
        self.frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame, anchor="n")

        # Frame for checkboxes and text box side by side, centered
        self.main_frame = tk.Frame(self.frame)
        self.main_frame.pack(pady=20)

        # Frame for checkboxes (left side)
        self.checkbox_frame = tk.Frame(self.main_frame)
        self.checkbox_frame.grid(row=0, column=0, padx=5, sticky="n")

        # Text box for ingredients (right side) with double spacing
        self.text_frame = tk.Frame(self.main_frame)
        self.text_frame.grid(row=0, column=1, sticky="n")

        # Text box with larger size, double spacing, and font
        self.ingredients_text = Text(self.text_frame, height=12, width=40, font=self.default_font, spacing3=10)
        self.ingredients_text.pack(side="left", fill="y")

        # Configure double spacing for text in the text box using a tag
        self.ingredients_text.tag_configure("double_space", spacing3=10)

        self.label2 = Label(self.frame, text="Select Ingredients to Replace", font=self.default_font)
        self.label2.pack(pady=10)

        self.submit_button = Button(self.frame, text="Get Replacement", command=self.get_replacement, font=self.default_font)
        self.submit_button.pack(pady=10)

        self.result_label = Label(self.frame, text="", wraplength=400, font=self.default_font)
        self.result_label.pack(pady=10)

        # Track the checkbuttons and variables
        self.check_vars = {}

        # Bind the key release event to update checkboxes as user types
        self.ingredients_text.bind("<KeyRelease>", self.update_checkboxes)

        # Update canvas scroll region when window resizes
        self.frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

    def update_checkboxes(self, event=None):
        # Get all the current text from the text box
        ingredients = self.ingredients_text.get("1.0", tk.END).strip().split("\n")

        # Clear the existing checkboxes
        for widget in self.checkbox_frame.winfo_children():
            widget.destroy()

        # Adjust the height of the text box based on the number of lines (ingredients)
        new_height = len(ingredients) if len(ingredients) > 12 else 12
        self.ingredients_text.config(height=new_height)

        # Apply double spacing tag to the text box content
        self.ingredients_text.tag_add("double_space", "1.0", tk.END)

        # Add checkboxes next to each ingredient in perfect alignment
        self.check_vars.clear()  # Clear previous variables
        for index, ingredient in enumerate(ingredients):
            var = IntVar()
            self.check_vars[ingredient] = var
            cb = Checkbutton(self.checkbox_frame, variable=var, text="", font=self.default_font)
            cb.grid(row=index, column=0, sticky="w")

    def get_replacement(self):
        # Get the current ingredients from the text box
        ingredients = self.ingredients_text.get("1.0", tk.END).strip().split("\n")

        # Check which ingredients are selected and replace them
        replacements = []
        for ingredient in ingredients:
            if self.check_vars.get(ingredient, IntVar()).get() == 1:
                # Replace the ingredient with its AI-generated replacement
                replacement = get_ai_replacement(ingredient)
                replacements.append(f"{ingredient}: {replacement}")

        # Display the replacements below the button
        if replacements:
            self.result_label.config(text="\n".join(replacements))
        else:
            self.result_label.config(text="No ingredients selected for replacement.")

# Run the Tkinter app
root = tk.Tk()
app = RecipeApp(root)
root.mainloop()




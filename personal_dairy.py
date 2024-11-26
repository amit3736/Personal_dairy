import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import os

# Function to save diary entry
def save_entry():
    text = text_area.get("1.0", tk.END).strip()  # Get all text from the Text widget
    if not text:
        messagebox.showwarning("Warning", "The diary entry is empty!")
        return
    
    # Create a "diary_entries" folder if it doesn't exist
    if not os.path.exists("diary_entries"):
        os.makedirs("diary_entries")
    
    # Generate filename using the current date
    filename = datetime.now().strftime("diary_%Y-%m-%d.txt")
    filepath = os.path.join("diary_entries", filename)
    
    # Save the text to the file
    with open(filepath, "w") as file:
        file.write(text)
    
    messagebox.showinfo("Saved", f"Diary entry saved to {filepath}")
    text_area.delete("1.0", tk.END)  # Clear the text area

# Function to view previous entries
def view_entries():
    if not os.path.exists("diary_entries"):
        messagebox.showinfo("No Entries", "No diary entries found.")
        return
    
    entries = os.listdir("diary_entries")
    if not entries:
        messagebox.showinfo("No Entries", "No diary entries found.")
        return
    
    # Display all available entries in a new window
    view_window = tk.Toplevel(window)
    view_window.title("View Entries")
    view_window.geometry("400x400")
    
    tk.Label(view_window, text="Diary Entries", font=("Arial", 16)).pack(pady=10)
    listbox = tk.Listbox(view_window, width=50, height=20)
    listbox.pack(pady=10)

    # Populate the listbox with filenames
    for entry in sorted(entries):
        listbox.insert(tk.END, entry)
    
    # Function to display the content of a selected entry
    def open_entry():
        selected = listbox.curselection()
        if not selected:
            messagebox.showwarning("Warning", "No entry selected!")
            return
        
        filename = listbox.get(selected[0])
        filepath = os.path.join("diary_entries", filename)
        
        with open(filepath, "r") as file:
            content = file.read()
        
        content_window = tk.Toplevel(view_window)
        content_window.title(filename)
        content_window.geometry("400x400")
        tk.Label(content_window, text=filename, font=("Arial", 16)).pack(pady=10)
        tk.Text(content_window, wrap=tk.WORD, height=20, width=50).insert(tk.END, content)
    
    tk.Button(view_window, text="Open Entry", command=open_entry).pack(pady=10)

# Main application window
window = tk.Tk()
window.title("Personal Diary")
window.geometry("500x500")

# Label and Text area for writing entries
tk.Label(window, text="Write Your Diary Entry", font=("Arial", 16)).pack(pady=10)
text_area = tk.Text(window, wrap=tk.WORD, width=50, height=15)
text_area.pack(pady=10)

# Save and View buttons
save_button = tk.Button(window, text="Save Entry", command=save_entry, width=15, bg="green", fg="white")
save_button.pack(pady=5)

view_button = tk.Button(window, text="View Entries", command=view_entries, width=15, bg="blue", fg="white")
view_button.pack(pady=5)

# Run the Tkinter event loop
window.mainloop()

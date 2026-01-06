import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from doctomood.main import process_single_file


class DoctomoodGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Doctomood - Question Processor")
        self.root.geometry("700x320")
        self.root.resizable(False, False)

        # Get default directory (home)
        self.default_dir = str(Path.home())

        # Configure modern styling
        self.setup_styles()

        # Variables
        self.input_file = tk.StringVar()
        self.output_dir = tk.StringVar()

        # Create UI
        self.create_widgets()

    def setup_styles(self):
        """Configure modern button and widget styles."""
        style = ttk.Style()

        # Try to use a modern theme if available
        available_themes = style.theme_names()
        if "clam" in available_themes:
            style.theme_use("clam")
        elif "alt" in available_themes:
            style.theme_use("alt")

        # Configure Entry style for consistent height - match button height
        style.configure(
            "TEntry",
            padding=(8, 4),
            font=("Helvetica", 10),
        )

        # Configure Label style
        style.configure(
            "TLabel",
            font=("Helvetica", 10),
            padding=2,
        )

    def create_widgets(self):
        # Main container with padding
        main_container = ttk.Frame(self.root, padding="20")
        main_container.pack(fill=tk.BOTH, expand=True)

        # Input file selection section
        input_section = ttk.LabelFrame(main_container, text="Input File", padding="15")
        input_section.pack(fill=tk.X, pady=(0, 15))

        input_inner = ttk.Frame(input_section)
        input_inner.pack(fill=tk.X)

        ttk.Label(input_inner, text="File:", font=("Helvetica", 10, "bold")).pack(
            side=tk.LEFT, padx=(0, 10)
        )
        input_entry = ttk.Entry(
            input_inner, textvariable=self.input_file, state="readonly"
        )
        input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10), ipady=2)

        # Use regular Button for better customization - match entry height
        self.input_button = tk.Button(
            input_inner,
            text="📁 Browse",
            command=self.select_input_file,
            font=("Helvetica", 10, "bold"),
            bg="#4A90E2",
            fg="white",
            activebackground="#357ABD",
            activeforeground="white",
            relief=tk.RAISED,
            bd=2,
            padx=15,
            pady=4,
            cursor="hand2",
        )
        self.input_button.pack(side=tk.LEFT)

        # Output directory selection section
        output_section = ttk.LabelFrame(
            main_container, text="Output Directory", padding="15"
        )
        output_section.pack(fill=tk.X, pady=(0, 20))

        output_inner = ttk.Frame(output_section)
        output_inner.pack(fill=tk.X)

        ttk.Label(output_inner, text="Folder:", font=("Helvetica", 10, "bold")).pack(
            side=tk.LEFT, padx=(0, 10)
        )
        output_entry = ttk.Entry(
            output_inner, textvariable=self.output_dir, state="readonly"
        )
        output_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10), ipady=2)

        # Use regular Button for better customization - match entry height
        self.output_button = tk.Button(
            output_inner,
            text="📂 Browse",
            command=self.select_output_dir,
            font=("Helvetica", 10, "bold"),
            bg="#4A90E2",
            fg="white",
            activebackground="#357ABD",
            activeforeground="white",
            relief=tk.RAISED,
            bd=2,
            padx=15,
            pady=4,
            cursor="hand2",
        )
        self.output_button.pack(side=tk.LEFT)

        # Process button section - centered and prominent
        process_section = ttk.Frame(main_container)
        process_section.pack(fill=tk.X, pady=(10, 0))

        # Center the process button
        process_button_container = ttk.Frame(process_section)
        process_button_container.pack(expand=True)

        # Use regular Button for better customization and visibility - larger and centered
        self.process_button = tk.Button(
            process_button_container,
            text="▶ Process Questions",
            command=self.process_file,
            state=tk.DISABLED,
            font=("Helvetica", 12, "bold"),
            bg="#CCCCCC",
            fg="#666666",
            activebackground="#218838",
            activeforeground="white",
            relief=tk.RAISED,
            bd=2,
            padx=35,
            pady=12,
            cursor="hand2",
        )
        self.process_button.pack(pady=5)

        # Status label with better visibility - centered below button
        self.status_label = ttk.Label(
            process_button_container, text="", font=("Helvetica", 10), foreground="gray"
        )
        self.status_label.pack(pady=(5, 0))

        # Update button state when variables change
        self.input_file.trace_add("write", self.update_button_state)
        self.output_dir.trace_add("write", self.update_button_state)

    def select_input_file(self):
        # Note: tkinter file dialogs don't support custom sizes, but they remember
        # their last size on most systems. We can only set initialdir.
        filename = filedialog.askopenfilename(
            title="Select Input File",
            initialdir=self.default_dir,
            filetypes=[
                ("Document files (*.docx, *.odt)", "*.docx *.odt"),
                ("Word documents (*.docx)", "*.docx"),
                ("OpenDocument (*.odt)", "*.odt"),
                ("All files", "*.*"),
            ],
        )
        if filename:
            self.input_file.set(filename)

    def select_output_dir(self):
        # Note: tkinter file dialogs don't support custom sizes, but they remember
        # their last size on most systems. We can only set initialdir.
        dirname = filedialog.askdirectory(
            title="Select Output Directory", initialdir=self.default_dir
        )
        if dirname:
            self.output_dir.set(dirname)

    def update_button_state(self, *args):
        if self.input_file.get() and self.output_dir.get():
            self.process_button.config(state=tk.NORMAL, bg="#28A745", fg="white")
        else:
            self.process_button.config(state=tk.DISABLED, bg="#CCCCCC", fg="#666666")

    def process_file(self):
        input_path = self.input_file.get()
        output_path = self.output_dir.get()

        if not input_path or not output_path:
            messagebox.showerror(
                "Error", "Please select both input file and output directory."
            )
            return

        try:
            self.process_button.config(state=tk.DISABLED)
            self.status_label.config(text="Processing...", foreground="blue")

            # Process the file with respect_name=True
            docs_output, xml_output, df = process_single_file(
                input_path, output_path, respect_name=True, write=True
            )

            self.status_label.config(text="Success!", foreground="green")
            messagebox.showinfo(
                "Success",
                f"Files processed successfully!\n\n"
                f"DOCX: {docs_output}\n"
                f"XML: {xml_output}\n\n"
                f"Processed {len(df)} questions.",
            )
        except Exception as e:
            self.status_label.config(text="Error", foreground="red")
            messagebox.showerror("Error", f"An error occurred:\n\n{str(e)}")
        finally:
            # Restore button state and colors
            if self.input_file.get() and self.output_dir.get():
                self.process_button.config(state=tk.NORMAL, bg="#28A745", fg="white")
            else:
                self.process_button.config(
                    state=tk.DISABLED, bg="#CCCCCC", fg="#666666"
                )


def main():
    root = tk.Tk()
    app = DoctomoodGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

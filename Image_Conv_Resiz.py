import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from PIL import Image, ImageTk
import threading
from pathlib import Path
try:
    from pillow_heif import register_heif_opener
    register_heif_opener()
    HEIC_SUPPORT = True
except ImportError:
    HEIC_SUPPORT = False

class ImageConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Bulk Image Converter")
        self.root.geometry("655x700")
        self.root.configure(bg='#f0f0f0')
        
        self.selected_files = []
        self.output_dir = ""
        self.individual_quality_settings = {}
        self.is_converting = False
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame with scrolling capability
        main_canvas = tk.Canvas(self.root, bg='#f0f0f0')
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=main_canvas.yview)
        scrollable_frame = ttk.Frame(main_canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all"))
        )
        
        main_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        main_canvas.configure(yscrollcommand=scrollbar.set)
        
        # Main frame
        main_frame = ttk.Frame(scrollable_frame, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(4, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Bulk Image Converter", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # File selection section
        file_frame = ttk.LabelFrame(main_frame, text="Select Images", padding="10")
        file_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        file_frame.columnconfigure(1, weight=1)
        
        ttk.Button(file_frame, text="Browse Files", 
                  command=self.browse_files).grid(row=0, column=0, padx=(0, 10))
        
        self.files_label = ttk.Label(file_frame, text="No files selected")
        self.files_label.grid(row=0, column=1, sticky=(tk.W, tk.E))
        
        ttk.Button(file_frame, text="Clear", 
                  command=self.clear_files).grid(row=0, column=2)
        
        # Output directory section
        output_frame = ttk.LabelFrame(main_frame, text="Output Directory", padding="10")
        output_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        output_frame.columnconfigure(1, weight=1)
        
        ttk.Button(output_frame, text="Browse Folder", 
                  command=self.browse_output_dir).grid(row=0, column=0, padx=(0, 10))
        
        self.output_label = ttk.Label(output_frame, text="Same as source directory")
        self.output_label.grid(row=0, column=1, sticky=(tk.W, tk.E))
        
        # Conversion settings
        settings_frame = ttk.LabelFrame(main_frame, text="Conversion Settings", padding="10")
        settings_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Conversion mode selection
        ttk.Label(settings_frame, text="Conversion Mode:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        
        self.conversion_mode = tk.StringVar(value="all_to_one")
        mode_frame = ttk.Frame(settings_frame)
        mode_frame.grid(row=0, column=1, columnspan=4, sticky=tk.W, pady=(0, 10))
        
        ttk.Radiobutton(mode_frame, text="All files to one format", 
                       variable=self.conversion_mode, value="all_to_one",
                       command=self.toggle_conversion_mode).grid(row=0, column=0, sticky=tk.W)
        ttk.Radiobutton(mode_frame, text="Individual format selection", 
                       variable=self.conversion_mode, value="individual",
                       command=self.toggle_conversion_mode).grid(row=0, column=1, sticky=tk.W, padx=(20, 0))
        
        # Single format selection (for all_to_one mode)
        self.single_format_frame = ttk.Frame(settings_frame)
        self.single_format_frame.grid(row=1, column=0, columnspan=5, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(self.single_format_frame, text="Convert to:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        
        self.format_var = tk.StringVar(value="JPEG")
        format_values = ["JPEG", "PNG", "WEBP", "BMP", "TIFF", "GIF"]
        if HEIC_SUPPORT:
            format_values.append("HEIC")
        
        self.format_combo = ttk.Combobox(self.single_format_frame, textvariable=self.format_var,
                                        values=format_values, state="readonly", width=10)
        self.format_combo.grid(row=0, column=1, sticky=tk.W, padx=(0, 20))
        self.format_combo.bind("<<ComboboxSelected>>", self.on_format_change)
        
        # Quality setting (for JPEG/WEBP/HEIC)
        self.quality_label = ttk.Label(self.single_format_frame, text="Quality:")
        self.quality_label.grid(row=0, column=2, sticky=tk.W, padx=(0, 10))
        
        self.quality_var = tk.StringVar(value="85")
        self.quality_spin = ttk.Spinbox(self.single_format_frame, from_=1, to=100, 
                                       textvariable=self.quality_var, width=5)
        self.quality_spin.grid(row=0, column=3, sticky=tk.W, padx=(0, 20))
        
        # Size settings
        size_frame = ttk.LabelFrame(settings_frame, text="Size Settings", padding="5")
        size_frame.grid(row=2, column=0, columnspan=5, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.size_mode = tk.StringVar(value="keep_original")
        
        ttk.Radiobutton(size_frame, text="Keep original size", 
                       variable=self.size_mode, value="keep_original",
                       command=self.toggle_size_mode).grid(row=0, column=0, sticky=tk.W)
        ttk.Radiobutton(size_frame, text="Resize to specific dimensions", 
                       variable=self.size_mode, value="custom_size",
                       command=self.toggle_size_mode).grid(row=0, column=1, sticky=tk.W, padx=(20, 0))
        ttk.Radiobutton(size_frame, text="Resize by percentage", 
                       variable=self.size_mode, value="percentage",
                       command=self.toggle_size_mode).grid(row=0, column=2, sticky=tk.W, padx=(20, 0))
        
        # Custom size controls
        self.custom_size_frame = ttk.Frame(size_frame)
        self.custom_size_frame.grid(row=1, column=0, columnspan=3, sticky=tk.W, pady=(10, 0))
        
        self.width_var = tk.StringVar(value="800")
        self.height_var = tk.StringVar(value="600")
        self.percentage_var = tk.StringVar(value="50")
        
        self.width_label = ttk.Label(self.custom_size_frame, text="Width:")
        self.width_entry = ttk.Entry(self.custom_size_frame, textvariable=self.width_var, width=8)
        self.height_label = ttk.Label(self.custom_size_frame, text="Height:")
        self.height_entry = ttk.Entry(self.custom_size_frame, textvariable=self.height_var, width=8)
        self.percentage_label = ttk.Label(self.custom_size_frame, text="Scale:")
        self.percentage_entry = ttk.Entry(self.custom_size_frame, textvariable=self.percentage_var, width=6)
        self.percentage_percent = ttk.Label(self.custom_size_frame, text="%")
        
        self.maintain_ratio_var = tk.BooleanVar(value=True)
        self.ratio_check = ttk.Checkbutton(self.custom_size_frame, text="Maintain aspect ratio", 
                                          variable=self.maintain_ratio_var)
        
        # File list with format selection
        list_frame = ttk.LabelFrame(main_frame, text="Selected Files", padding="10")
        list_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # Treeview with scrollbar
        tree_frame = ttk.Frame(list_frame)
        tree_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)
        
        self.file_tree = ttk.Treeview(tree_frame, columns=("size", "format", "target_format"), show="tree headings", height="5")
        self.file_tree.heading("#0", text="File Name")
        self.file_tree.heading("size", text="Size")
        self.file_tree.heading("format", text="Current Format")
        self.file_tree.heading("target_format", text="Convert To")
        
        self.file_tree.column("#0", width=300)
        self.file_tree.column("size", width=100)
        self.file_tree.column("format", width=80)
        self.file_tree.column("target_format", width=100)
        
        # Bind double-click for individual format selection
        self.file_tree.bind("<Double-1>", self.on_item_double_click)
        
        tree_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.file_tree.yview)
        self.file_tree.configure(yscrollcommand=tree_scrollbar.set)
        
        self.file_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        tree_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Individual format selection controls
        self.individual_controls_frame = ttk.Frame(list_frame)
        self.individual_controls_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
        ttk.Label(self.individual_controls_frame, 
                 text="Double-click files to set individual target formats").grid(row=0, column=0, sticky=tk.W)
        
        # Progress section
        progress_frame = ttk.Frame(main_frame)
        progress_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        progress_frame.columnconfigure(0, weight=1)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, 
                                           maximum=100)
        self.progress_bar.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        self.status_label = ttk.Label(progress_frame, text="Ready")
        self.status_label.grid(row=1, column=0, sticky=tk.W)
        
        # Convert button
        self.convert_btn = ttk.Button(main_frame, text="Convert Images", 
                                     command=self.start_conversion)
        self.convert_btn.grid(row=6, column=0, columnspan=3, pady=10)
        
        # Initially set up the UI state
        self.toggle_conversion_mode()
        self.toggle_size_mode()
        self.on_format_change()
        
        # Pack the scrollable area
        main_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mousewheel to canvas
        def _on_mousewheel(event):
            main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        main_canvas.bind("<MouseWheel>", _on_mousewheel)
    
    def on_format_change(self, event=None):
        """Show/hide quality setting based on selected format"""
        format_name = self.format_var.get()
        if format_name in ["JPEG", "WEBP", "HEIC"]:
            self.quality_label.grid()
            self.quality_spin.grid()
        else:
            self.quality_label.grid_remove()
            self.quality_spin.grid_remove()
        
    def toggle_conversion_mode(self):
        """Toggle between single format and individual format selection modes"""
        if self.conversion_mode.get() == "all_to_one":
            self.single_format_frame.grid()
            self.individual_controls_frame.grid_remove()
        else:
            self.single_format_frame.grid_remove()
            self.individual_controls_frame.grid()
        self.update_file_list()
    
    def toggle_size_mode(self):
        """Toggle size control visibility based on selected mode"""
        # Hide all controls first
        for widget in [self.width_label, self.width_entry, self.height_label, 
                      self.height_entry, self.percentage_label, self.percentage_entry, 
                      self.percentage_percent, self.ratio_check]:
            widget.grid_remove()
        
        if self.size_mode.get() == "custom_size":
            self.width_label.grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
            self.width_entry.grid(row=0, column=1, sticky=tk.W, padx=(0, 10))
            self.height_label.grid(row=0, column=2, sticky=tk.W, padx=(0, 5))
            self.height_entry.grid(row=0, column=3, sticky=tk.W, padx=(0, 20))
            self.ratio_check.grid(row=0, column=4, sticky=tk.W)
        elif self.size_mode.get() == "percentage":
            self.percentage_label.grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
            self.percentage_entry.grid(row=0, column=1, sticky=tk.W)
            self.percentage_percent.grid(row=0, column=2, sticky=tk.W, padx=(0, 20))
            self.ratio_check.grid(row=0, column=3, sticky=tk.W)
    
    def on_item_double_click(self, event):
        """Handle double-click on file list item for individual format selection"""
        if self.conversion_mode.get() != "individual":
            return
        
        selection = self.file_tree.selection()
        if not selection:
            return
        
        item = selection[0]
        self.show_format_dialog(item)
    
    def show_format_dialog(self, item):
        """Show dialog for selecting individual file format"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Select Target Format")
        dialog.geometry("300x250")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.geometry("+%d+%d" % (self.root.winfo_rootx() + 50, self.root.winfo_rooty() + 50))
        
        # Get current values
        current_values = self.file_tree.item(item, "values")
        current_target = current_values[2] if len(current_values) > 2 else "JPEG"
        
        # Format selection
        ttk.Label(dialog, text="Convert to format:").pack(pady=10)
        format_var = tk.StringVar(value=current_target)
        
        format_values = ["JPEG", "PNG", "WEBP", "BMP", "TIFF", "GIF"]
        if HEIC_SUPPORT:
            format_values.append("HEIC")
            
        format_combo = ttk.Combobox(dialog, textvariable=format_var,
                                   values=format_values, state="readonly")
        format_combo.pack(pady=5)
        
        # Quality for certain formats
        quality_frame = ttk.Frame(dialog)
        quality_frame.pack(pady=10)
        
        quality_label = ttk.Label(quality_frame, text="Quality (for JPEG/WEBP/HEIC):")
        quality_label.pack()
        quality_var = tk.StringVar(value="85")
        quality_spin = ttk.Spinbox(quality_frame, from_=1, to=100, textvariable=quality_var, width=5)
        quality_spin.pack(pady=5)
        
        def update_quality_visibility(*args):
            if format_var.get() in ["JPEG", "WEBP", "HEIC"]:
                quality_label.pack()
                quality_spin.pack(pady=5)
            else:
                quality_label.pack_forget()
                quality_spin.pack_forget()
        
        format_var.trace('w', update_quality_visibility)
        update_quality_visibility()
        
        # Buttons
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=20)
        
        def apply_format():
            new_format = format_var.get()
            # Update the item in tree
            values = list(self.file_tree.item(item, "values"))
            if len(values) >= 3:
                values[2] = new_format
            else:
                values.extend([""] * (3 - len(values)))
                values[2] = new_format
            self.file_tree.item(item, values=values)
            
            # Store quality setting if applicable
            if new_format in ["JPEG", "WEBP", "HEIC"]:
                self.individual_quality_settings[item] = quality_var.get()
            
            dialog.destroy()
        
        ttk.Button(button_frame, text="Apply", command=apply_format).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
    
    def browse_files(self):
        file_types = [
            ("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff *.tif *.webp *.gif"),
            ("JPEG files", "*.jpg *.jpeg"),
            ("PNG files", "*.png"),
            ("All files", "*.*")
        ]
        
        if HEIC_SUPPORT:
            file_types.insert(0, ("All image files", "*.jpg *.jpeg *.png *.bmp *.tiff *.tif *.webp *.gif *.heic *.heif"))
            file_types.append(("HEIC files", "*.heic *.heif"))
        
        files = filedialog.askopenfilenames(
            title="Select Image Files",
            filetypes=file_types
        )
        
        if files:
            self.selected_files = list(files)
            self.update_file_list()
            self.files_label.config(text=f"{len(files)} files selected")
            
            # Show HEIC warning if HEIC files selected but no support
            if not HEIC_SUPPORT and any(f.lower().endswith(('.heic', '.heif')) for f in files):
                messagebox.showwarning("HEIC Support", 
                    "HEIC files detected but pillow-heif is not installed.\n" +
                    "Install it with: pip install pillow-heif\n" +
                    "HEIC files will be skipped during conversion.")
    
    def clear_files(self):
        self.selected_files = []
        self.individual_quality_settings = {}
        self.update_file_list()
        self.files_label.config(text="No files selected")
    
    def browse_output_dir(self):
        directory = filedialog.askdirectory(title="Select Output Directory")
        if directory:
            self.output_dir = directory
            self.output_label.config(text=directory)
    
    def update_file_list(self):
        # Clear existing items
        for item in self.file_tree.get_children():
            self.file_tree.delete(item)
        
        # Add selected files
        for file_path in self.selected_files:
            try:
                path = Path(file_path)
                if path.exists():
                    size = path.stat().st_size
                    size_str = self.format_file_size(size)
                    format_str = path.suffix.upper().lstrip('.')
                    
                    # Determine target format
                    if self.conversion_mode.get() == "all_to_one":
                        target_format = self.format_var.get()
                    else:
                        target_format = "JPEG"  # Default for individual mode
                    
                    self.file_tree.insert("", "end", text=path.name, 
                                         values=(size_str, format_str, target_format))
                else:
                    self.file_tree.insert("", "end", text=path.name, 
                                         values=("File not found", "Unknown", "JPEG"))
            except Exception as e:
                self.file_tree.insert("", "end", text=Path(file_path).name, 
                                     values=("Error", "Unknown", "JPEG"))
    
    def format_file_size(self, size_bytes):
        """Convert bytes to human readable format"""
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024**2:
            return f"{size_bytes/1024:.1f} KB"
        elif size_bytes < 1024**3:
            return f"{size_bytes/(1024**2):.1f} MB"
        else:
            return f"{size_bytes/(1024**3):.1f} GB"
    
    def validate_inputs(self):
        """Validate user inputs before conversion"""
        if not self.selected_files:
            messagebox.showwarning("No Files", "Please select image files to convert.")
            return False
        
        # Validate size inputs if custom sizing is selected
        if self.size_mode.get() == "custom_size":
            try:
                width = int(self.width_var.get())
                height = int(self.height_var.get())
                if width <= 0 or height <= 0:
                    raise ValueError("Dimensions must be positive")
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter valid positive numbers for width and height.")
                return False
        
        elif self.size_mode.get() == "percentage":
            try:
                percentage = float(self.percentage_var.get())
                if percentage <= 0:
                    raise ValueError("Percentage must be positive")
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter a valid positive number for percentage.")
                return False
        
        # Validate quality input
        if self.conversion_mode.get() == "all_to_one":
            target_format = self.format_var.get()
            if target_format in ["JPEG", "WEBP", "HEIC"]:
                try:
                    quality = int(self.quality_var.get())
                    if not 1 <= quality <= 100:
                        raise ValueError("Quality must be between 1 and 100")
                except ValueError:
                    messagebox.showerror("Invalid Input", "Please enter a valid quality value (1-100).")
                    return False
        
        return True
    
    def start_conversion(self):
        if not self.validate_inputs():
            return
        
        if self.is_converting:
            messagebox.showinfo("Conversion in Progress", "A conversion is already in progress.")
            return
        
        # Disable convert button during conversion
        self.convert_btn.config(state="disabled")
        self.is_converting = True
        
        # Start conversion in separate thread
        thread = threading.Thread(target=self.convert_images, daemon=True)
        thread.start()
    
    def convert_images(self):
        try:
            if self.conversion_mode.get() == "all_to_one":
                target_format = self.format_var.get()
                quality = int(self.quality_var.get()) if self.quality_var.get().isdigit() else 85
            
            total_files = len(self.selected_files)
            successful = 0
            failed = 0
            failed_files = []
            
            for i, file_path in enumerate(self.selected_files):
                try:
                    path = Path(file_path)
                    
                    # Skip HEIC files if no support
                    if not HEIC_SUPPORT and path.suffix.lower() in ['.heic', '.heif']:
                        failed += 1
                        failed_files.append(f"{path.name}: HEIC not supported")
                        continue
                    
                    # Update progress
                    progress = (i / total_files) * 100
                    self.root.after(0, lambda p=progress: self.progress_var.set(p))
                    
                    self.root.after(0, lambda name=path.name: self.status_label.config(text=f"Converting: {name}"))
                    
                    # Get target format for this file
                    if self.conversion_mode.get() == "individual":
                        # Find the corresponding tree item to get target format
                        target_format = "JPEG"  # Default
                        quality = 85  # Default
                        for item in self.file_tree.get_children():
                            if self.file_tree.item(item, "text") == path.name:
                                values = self.file_tree.item(item, "values")
                                if len(values) >= 3:
                                    target_format = values[2]
                                # Get individual quality setting if available
                                if item in self.individual_quality_settings:
                                    try:
                                        quality = int(self.individual_quality_settings[item])
                                    except (ValueError, TypeError):
                                        quality = 85
                                break
                    
                    # Open and process image
                    with Image.open(file_path) as img:
                        # Convert mode if necessary
                        if target_format == "JPEG" and img.mode in ("RGBA", "P", "LA"):
                            # Convert to RGB for JPEG
                            if img.mode == "P":
                                img = img.convert("RGBA")
                            if img.mode in ("RGBA", "LA"):
                                background = Image.new("RGB", img.size, (255, 255, 255))
                                if img.mode == "RGBA":
                                    background.paste(img, mask=img.split()[-1])
                                else:  # LA mode
                                    background.paste(img.convert("RGB"))
                                img = background
                        elif target_format == "PNG" and img.mode not in ("RGBA", "RGB", "P", "L", "LA"):
                            img = img.convert("RGBA")
                        elif target_format == "HEIC":
                            # HEIC supports RGB and RGBA
                            if img.mode not in ("RGB", "RGBA"):
                                img = img.convert("RGB")
                        
                        # Handle resizing based on mode
                        if self.size_mode.get() == "custom_size":
                            try:
                                new_width = int(self.width_var.get())
                                new_height = int(self.height_var.get())
                                
                                if self.maintain_ratio_var.get():
                                    img.thumbnail((new_width, new_height), Image.Resampling.LANCZOS)
                                else:
                                    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                            except (ValueError, AttributeError):
                                pass  # Skip resize if invalid dimensions
                        elif self.size_mode.get() == "percentage":
                            try:
                                scale = float(self.percentage_var.get()) / 100.0
                                new_width = int(img.width * scale)
                                new_height = int(img.height * scale)
                                if new_width > 0 and new_height > 0:
                                    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                            except (ValueError, ZeroDivisionError, AttributeError):
                                pass  # Skip resize if invalid percentage
                        
                        # Determine output path
                        if self.output_dir:
                            output_dir = Path(self.output_dir)
                        else:
                            output_dir = path.parent
                        
                        # Create output directory if it doesn't exist
                        output_dir.mkdir(parents=True, exist_ok=True)
                        
                        if target_format == "HEIC":
                            output_path = output_dir / f"{path.stem}.heic"
                        else:
                            output_path = output_dir / f"{path.stem}.{target_format.lower()}"
                        
                        # Check if output file already exists and create unique name if needed
                        counter = 1
                        original_output_path = output_path
                        while output_path.exists():
                            if target_format == "HEIC":
                                output_path = output_dir / f"{path.stem}_{counter}.heic"
                            else:
                                output_path = output_dir / f"{path.stem}_{counter}.{target_format.lower()}"
                            counter += 1
                        
                        # Save with appropriate parameters
                        save_kwargs = {}
                        if target_format in ["JPEG", "WEBP", "HEIC"]:
                            save_kwargs["quality"] = quality
                            if target_format != "HEIC":
                                save_kwargs["optimize"] = True
                        elif target_format == "PNG":
                            save_kwargs["optimize"] = True
                        
                        img.save(output_path, format=target_format, **save_kwargs)
                        successful += 1
                        
                except Exception as e:
                    failed += 1
                    error_msg = f"{Path(file_path).name}: {str(e)}"
                    failed_files.append(error_msg)
                    print(f"Error converting {file_path}: {e}")
            
            # Update progress to 100%
            self.root.after(0, lambda: self.progress_var.set(100))
            
            # Show completion message
            self.root.after(0, lambda: self.conversion_complete(successful, failed, failed_files))
            
        except Exception as e:
            self.root.after(0, lambda: self.conversion_error(str(e)))
        finally:
            self.is_converting = False
    
    def conversion_complete(self, successful, failed, failed_files):
        """Handle conversion completion"""
        self.status_label.config(text=f"Complete: {successful} converted, {failed} failed")
        self.convert_btn.config(state="normal")
        
        if failed == 0:
            messagebox.showinfo("Conversion Complete", 
                              f"Successfully converted {successful} images!")
        else:
            # Create detailed error message
            error_msg = f"Converted {successful} images.\n{failed} files failed to convert.\n\n"
            if failed_files:
                error_msg += "Failed files:\n" + "\n".join(failed_files[:5])  # Show first 5 errors
                if len(failed_files) > 5:
                    error_msg += f"\n... and {len(failed_files) - 5} more"
            
            messagebox.showwarning("Conversion Complete", error_msg)
    
    def conversion_error(self, error_message):
        """Handle conversion error"""
        self.status_label.config(text="Error during conversion")
        self.convert_btn.config(state="normal")
        messagebox.showerror("Conversion Error", f"An error occurred during conversion:\n{error_message}")

def main():
    root = tk.Tk()
    
    # Set application icon if available
    try:
        root.iconbitmap("icon.ico")  # Optional: add an icon file
    except:
        pass
    
    # Improve appearance on Windows
    try:
        from tkinter import ttk
        style = ttk.Style()
        style.theme_use('clam')  # Use a modern theme
    except:
        pass
    
    app = ImageConverter(root)
    
    # Handle window closing
    def on_closing():
        if app.is_converting:
            if messagebox.askokcancel("Quit", "Conversion is in progress. Do you want to quit anyway?"):
                root.destroy()
        else:
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()

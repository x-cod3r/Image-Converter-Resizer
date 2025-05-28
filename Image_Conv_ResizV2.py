import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from PIL import Image, ImageTk # Ensure ImageTk is imported if you plan to use it, though not used in current snippet
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
        self.root.geometry("655x700") # Consider making this more dynamic or larger if needed
        self.root.configure(bg='#f0f0f0')
        
        self.selected_files = []
        self.output_dir = ""
        self.individual_quality_settings = {}
        self.is_converting = False
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame with scrolling capability
        main_canvas = tk.Canvas(self.root, bg='#f0f0f0', highlightthickness=0) # Added highlightthickness=0
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=main_canvas.yview)
        scrollable_frame = ttk.Frame(main_canvas) # Use ttk.Frame for consistency
        
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
        scrollable_frame.columnconfigure(0, weight=1) # Allow scrollable_frame to expand
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(4, weight=1) # This allows the file list (row 4) to expand
        
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
        # --- MODIFIED: Added ICO ---
        format_values = ["JPEG", "PNG", "WEBP", "BMP", "TIFF", "GIF", "ICO"]
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
        
        self.file_tree = ttk.Treeview(tree_frame, columns=("size", "format", "target_format"), show="tree headings", height=8) # Set desired number of rows
        self.file_tree.heading("#0", text="File Name")
        self.file_tree.heading("size", text="Size")
        self.file_tree.heading("format", text="Current Format")
        self.file_tree.heading("target_format", text="Convert To")
        
        self.file_tree.column("#0", width=280, stretch=tk.YES) # Allow name column to stretch
        self.file_tree.column("size", width=100, stretch=tk.NO)
        self.file_tree.column("format", width=80, stretch=tk.NO)
        self.file_tree.column("target_format", width=100, stretch=tk.NO)
        
        self.file_tree.bind("<Double-1>", self.on_item_double_click)
        
        tree_scrollbar_y = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.file_tree.yview)
        tree_scrollbar_x = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.file_tree.xview) # Added horizontal scrollbar
        self.file_tree.configure(yscrollcommand=tree_scrollbar_y.set, xscrollcommand=tree_scrollbar_x.set)
        
        self.file_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        tree_scrollbar_y.grid(row=0, column=1, sticky=(tk.N, tk.S))
        tree_scrollbar_x.grid(row=1, column=0, sticky=(tk.W, tk.E)) # Grid for horizontal scrollbar
        
        tree_frame.rowconfigure(0, weight=1) # Make treeview expand vertically
        tree_frame.columnconfigure(0, weight=1) # Make treeview expand horizontally


        # Individual format selection controls
        self.individual_controls_frame = ttk.Frame(list_frame)
        self.individual_controls_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(10, 0)) # Changed from tree_frame to list_frame
        
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
        
        def _on_mousewheel(event, canvas=main_canvas): # Pass canvas as default arg
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")

        # Bind mousewheel to main_canvas and scrollable_frame and its children
        # This helps ensure scrolling works more consistently
        main_canvas.bind_all("<MouseWheel>", _on_mousewheel)
    
    def on_format_change(self, event=None):
        format_name = self.format_var.get()
        if format_name in ["JPEG", "WEBP", "HEIC"]:
            self.quality_label.grid()
            self.quality_spin.grid()
        else:
            self.quality_label.grid_remove()
            self.quality_spin.grid_remove()
        
    def toggle_conversion_mode(self):
        if self.conversion_mode.get() == "all_to_one":
            self.single_format_frame.grid()
            self.individual_controls_frame.grid_remove()
            # Update target format column for all items if switching to "all_to_one"
            if self.file_tree.get_children():
                new_target_format = self.format_var.get()
                for item_id in self.file_tree.get_children():
                    values = list(self.file_tree.item(item_id, "values"))
                    if len(values) >= 3:
                        values[2] = new_target_format
                        self.file_tree.item(item_id, values=values)

        else: # "individual" mode
            self.single_format_frame.grid_remove()
            self.individual_controls_frame.grid()
            # In individual mode, the target format column is set per item
            # We could reset them to a default or keep their last setting from "all_to_one"
            # For now, let's keep them, user can double click to change
        self.update_file_list() # Refresh list to reflect mode changes
    
    def toggle_size_mode(self):
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
            self.ratio_check.grid(row=0, column=3, sticky=tk.W) # Ratio check also for percentage
    
    def on_item_double_click(self, event):
        if self.conversion_mode.get() != "individual":
            return
        
        selection = self.file_tree.selection()
        if not selection:
            return
        
        item = selection[0]
        self.show_format_dialog(item)
    
    def show_format_dialog(self, item):
        dialog = tk.Toplevel(self.root)
        dialog.title("Select Target Format")
        dialog.geometry("300x250") # Adjusted for potential quality spinbox
        dialog.transient(self.root)
        dialog.grab_set()
        
        dialog.geometry("+%d+%d" % (self.root.winfo_rootx() + 50, self.root.winfo_rooty() + 50))
        
        current_values = self.file_tree.item(item, "values")
        current_target = current_values[2] if len(current_values) > 2 and current_values[2] else "JPEG"
        
        ttk.Label(dialog, text=f"File: {self.file_tree.item(item, 'text')}").pack(pady=(10,0))
        ttk.Label(dialog, text="Convert to format:").pack(pady=(5,0))
        format_var = tk.StringVar(value=current_target)
        
        # --- MODIFIED: Added ICO ---
        format_values = ["JPEG", "PNG", "WEBP", "BMP", "TIFF", "GIF", "ICO"]
        if HEIC_SUPPORT:
            format_values.append("HEIC")
            
        format_combo = ttk.Combobox(dialog, textvariable=format_var,
                                   values=format_values, state="readonly")
        format_combo.pack(pady=5)
        
        quality_frame = ttk.Frame(dialog)
        quality_frame.pack(pady=10)
        
        quality_label = ttk.Label(quality_frame, text="Quality (for JPEG/WEBP/HEIC):")
        # quality_label.pack() # Pack conditionally
        
        # Get stored quality or default
        stored_quality = self.individual_quality_settings.get(item, "85")
        quality_var = tk.StringVar(value=str(stored_quality)) # Ensure it's a string
        quality_spin = ttk.Spinbox(quality_frame, from_=1, to=100, textvariable=quality_var, width=5)
        # quality_spin.pack(pady=5) # Pack conditionally

        def update_quality_visibility(*args):
            selected_format = format_var.get()
            if selected_format in ["JPEG", "WEBP", "HEIC"]:
                quality_label.pack(pady=(5,0))
                quality_spin.pack(pady=5)
            else:
                quality_label.pack_forget()
                quality_spin.pack_forget()
        
        format_var.trace_add('write', update_quality_visibility) # Use trace_add for modern Tk
        update_quality_visibility() # Initial call
        
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=20)
        
        def apply_format():
            new_format = format_var.get()
            values = list(self.file_tree.item(item, "values"))
            if len(values) >= 3:
                values[2] = new_format
            else: # Should not happen if list is populated correctly
                values.extend([""] * (3 - len(values))) # Pad if necessary
                values[2] = new_format
            self.file_tree.item(item, values=values)
            
            if new_format in ["JPEG", "WEBP", "HEIC"]:
                self.individual_quality_settings[item] = quality_var.get()
            elif item in self.individual_quality_settings: # Remove quality if not applicable
                del self.individual_quality_settings[item]
            
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
            # Add HEIC to the "Image files" and a specific HEIC entry
            file_types.insert(0, ("All image files", "*.jpg *.jpeg *.png *.bmp *.tiff *.tif *.webp *.gif *.heic *.heif"))
            file_types.append(("HEIC files", "*.heic *.heif"))
        else:
             file_types.insert(0, ("All image files", "*.jpg *.jpeg *.png *.bmp *.tiff *.tif *.webp *.gif"))


        files = filedialog.askopenfilenames(
            title="Select Image Files",
            filetypes=file_types
        )
        
        if files:
            # Add new files, avoid duplicates if browsing multiple times
            new_files = [f for f in files if f not in self.selected_files]
            self.selected_files.extend(new_files)
            self.update_file_list()
            self.files_label.config(text=f"{len(self.selected_files)} files selected")
            
            if not HEIC_SUPPORT and any(f.lower().endswith(('.heic', '.heif')) for f in new_files):
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
        # Store current selection and scroll position if needed (more advanced)
        # For now, just rebuild
        
        # Get all current item IDs from the tree
        tree_items_map = {self.file_tree.item(item_id, "text"): item_id for item_id in self.file_tree.get_children()}
        
        new_file_paths_set = set(self.selected_files)
        existing_filenames_in_tree = set(tree_items_map.keys())

        # Remove items from tree that are no longer in selected_files
        for filename, item_id in list(tree_items_map.items()): # Iterate over a copy
            file_path_found = False
            for f_path in self.selected_files:
                if Path(f_path).name == filename:
                    file_path_found = True
                    break
            if not file_path_found:
                if self.file_tree.exists(item_id):
                    self.file_tree.delete(item_id)
                if item_id in self.individual_quality_settings:
                    del self.individual_quality_settings[item_id] # Clean up quality settings

        # Add new files or update existing ones
        for file_path in self.selected_files:
            path_obj = Path(file_path)
            filename = path_obj.name
            
            try:
                target_format_val = "JPEG" # Default for new items
                if self.conversion_mode.get() == "all_to_one":
                    target_format_val = self.format_var.get()
                
                item_id = tree_items_map.get(filename)

                if path_obj.exists():
                    size = path_obj.stat().st_size
                    size_str = self.format_file_size(size)
                    format_str = path_obj.suffix.upper().lstrip('.')
                    
                    # If in individual mode and item exists, try to keep its target format
                    if item_id and self.conversion_mode.get() == "individual":
                        current_item_values = self.file_tree.item(item_id, "values")
                        if len(current_item_values) >= 3 and current_item_values[2]:
                            target_format_val = current_item_values[2]
                    
                    values_tuple = (size_str, format_str, target_format_val)

                    if item_id and self.file_tree.exists(item_id): # File is already in tree, update it
                        self.file_tree.item(item_id, values=values_tuple)
                    else: # New file, insert it
                        self.file_tree.insert("", "end", iid=file_path, text=filename, # Use file_path as iid for uniqueness
                                             values=values_tuple)
                else: # File not found
                    if item_id and self.file_tree.exists(item_id):
                        self.file_tree.item(item_id, values=("File not found", "Unknown", target_format_val))
                    else:
                        self.file_tree.insert("", "end", iid=file_path, text=filename,
                                             values=("File not found", "Unknown", target_format_val))
            except Exception as e:
                print(f"Error updating file list for {filename}: {e}")
                if item_id and self.file_tree.exists(item_id):
                     self.file_tree.item(item_id, values=("Error", "Unknown", target_format_val))
                else:
                    self.file_tree.insert("", "end", iid=file_path, text=filename,
                                         values=("Error", "Unknown", target_format_val))
    
    def format_file_size(self, size_bytes):
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024**2:
            return f"{size_bytes/1024:.1f} KB"
        elif size_bytes < 1024**3:
            return f"{size_bytes/(1024**2):.1f} MB"
        else:
            return f"{size_bytes/(1024**3):.1f} GB"
    
    def validate_inputs(self):
        if not self.selected_files:
            messagebox.showwarning("No Files", "Please select image files to convert.")
            return False
        
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
        
        # For individual mode, quality is validated when set in the dialog implicitly by Spinbox.
        # Or, could add validation here by iterating through self.individual_quality_settings
        
        return True
    
    def start_conversion(self):
        if not self.validate_inputs():
            return
        
        if self.is_converting:
            messagebox.showinfo("Conversion in Progress", "A conversion is already in progress.")
            return
        
        self.convert_btn.config(state="disabled")
        self.is_converting = True
        
        thread = threading.Thread(target=self.convert_images, daemon=True)
        thread.start()
    
    def convert_images(self):
        try:
            default_quality = 85
            if self.conversion_mode.get() == "all_to_one":
                global_target_format = self.format_var.get()
                if global_target_format in ["JPEG", "WEBP", "HEIC"]:
                    try:
                        default_quality = int(self.quality_var.get())
                    except ValueError:
                        default_quality = 85
            
            total_files = len(self.selected_files)
            successful = 0
            failed = 0
            failed_files_details = [] # Store tuples of (filename, error_message)
            
            for i, file_path_str in enumerate(self.selected_files):
                current_path = Path(file_path_str)
                filename_for_status = current_path.name
                
                # Update progress
                progress_val = ((i + 1) / total_files) * 100 # Use i+1 for 1-based progress
                self.root.after(0, lambda p=progress_val: self.progress_var.set(p))
                self.root.after(0, lambda name=filename_for_status: self.status_label.config(text=f"Converting: {name}"))

                try:
                    if not HEIC_SUPPORT and current_path.suffix.lower() in ['.heic', '.heif']:
                        raise Exception("HEIC not supported (pillow-heif not installed)")

                    # Determine target format and quality for this specific file
                    item_target_format = "JPEG" # Default
                    item_quality = default_quality

                    if self.conversion_mode.get() == "individual":
                        # Find the item in the tree by its path (used as iid)
                        item_id = file_path_str # We used file_path as iid
                        if self.file_tree.exists(item_id):
                            values = self.file_tree.item(item_id, "values")
                            if len(values) >= 3 and values[2]:
                                item_target_format = values[2]
                            
                            if item_target_format in ["JPEG", "WEBP", "HEIC"]:
                                stored_q = self.individual_quality_settings.get(item_id)
                                if stored_q is not None:
                                    try:
                                        item_quality = int(stored_q)
                                    except ValueError:
                                        pass # Keep default_quality
                        else: # Should not happen if list is synced
                            print(f"Warning: File {filename_for_status} not found in tree for individual settings.")
                    else: # all_to_one mode
                        item_target_format = global_target_format
                        # item_quality is already default_quality (which was set from global settings)

                    with Image.open(current_path) as img:
                        # Apply resizing
                        resized_img = img
                        if self.size_mode.get() == "custom_size":
                            new_w = int(self.width_var.get())
                            new_h = int(self.height_var.get())
                            if self.maintain_ratio_var.get():
                                temp_img = resized_img.copy()
                                temp_img.thumbnail((new_w, new_h), Image.Resampling.LANCZOS)
                                resized_img = temp_img
                            else:
                                resized_img = resized_img.resize((new_w, new_h), Image.Resampling.LANCZOS)
                        elif self.size_mode.get() == "percentage":
                            scale = float(self.percentage_var.get()) / 100.0
                            new_w = int(resized_img.width * scale)
                            new_h = int(resized_img.height * scale)
                            if new_w > 0 and new_h > 0:
                                if self.maintain_ratio_var.get(): # Percentage inherently maintains ratio if applied to both w/h
                                    resized_img = resized_img.resize((new_w, new_h), Image.Resampling.LANCZOS)
                                else: # This case for percentage without maintaining ratio is a bit odd, but let's implement as direct scale
                                     resized_img = resized_img.resize((new_w, new_h), Image.Resampling.LANCZOS)


                        # Handle mode conversion after resizing
                        img_to_save = resized_img
                        if item_target_format == "JPEG":
                            if img_to_save.mode in ("RGBA", "P", "LA"):
                                if img_to_save.mode == "P":
                                    img_to_save = img_to_save.convert("RGBA")
                                if img_to_save.mode == "LA":
                                     img_to_save = img_to_save.convert("RGBA") # Simplify: LA to RGBA
                                
                                # Now img_to_save is RGBA if it had alpha
                                background = Image.new("RGB", img_to_save.size, (255, 255, 255))
                                background.paste(img_to_save, mask=img_to_save.split()[-1])
                                img_to_save = background
                            elif img_to_save.mode != "RGB": # Ensure it's RGB if not already handled by alpha
                                img_to_save = img_to_save.convert("RGB")

                        elif item_target_format == "PNG":
                            if img_to_save.mode not in ("RGBA", "RGB", "P", "L", "LA"):
                                img_to_save = img_to_save.convert("RGBA") # Prefer RGBA for PNG to keep transparency
                        elif item_target_format == "HEIC":
                            if img_to_save.mode not in ("RGB", "RGBA"):
                                img_to_save = img_to_save.convert("RGB") # Default to RGB
                        # --- MODIFIED: ICO mode conversion ---
                        elif item_target_format == "ICO":
                            if img_to_save.mode != "RGBA":
                                img_to_save = img_to_save.convert("RGBA") # ICOs benefit from RGBA for transparency

                        # Determine output path
                        output_base_dir = Path(self.output_dir) if self.output_dir else current_path.parent
                        output_base_dir.mkdir(parents=True, exist_ok=True)
                        
                        # --- MODIFIED: ICO extension ---
                        file_extension = item_target_format.lower()
                        if item_target_format == "ICO":
                            file_extension = "ico"
                        
                        output_filename = f"{current_path.stem}.{file_extension}"
                        final_output_path = output_base_dir / output_filename
                        
                        counter = 1
                        while final_output_path.exists():
                            output_filename = f"{current_path.stem}_{counter}.{file_extension}"
                            final_output_path = output_base_dir / output_filename
                            counter += 1
                        
                        save_kwargs = {}
                        if item_target_format in ["JPEG", "WEBP", "HEIC"]:
                            save_kwargs["quality"] = item_quality
                            if item_target_format != "HEIC": # pillow-heif doesn't use 'optimize'
                                save_kwargs["optimize"] = True
                        elif item_target_format == "PNG":
                            save_kwargs["optimize"] = True
                        # --- MODIFIED: ICO save options ---
                        elif item_target_format == "ICO":
                            # Standard sizes for ICO. Pillow will resize `img_to_save` for each.
                            save_kwargs["sizes"] = [(16,16), (32,32), (48,48), (64,64), (128,128), (256,256)]
                            # If img_to_save is smaller than 256x256, Pillow will upscale for larger icon sizes.
                            # If img_to_save is very large, it will be downscaled.
                        
                        img_to_save.save(final_output_path, format=item_target_format, **save_kwargs)
                        successful += 1
                        
                except Exception as e_inner:
                    failed += 1
                    failed_files_details.append((filename_for_status, str(e_inner)))
                    print(f"Error converting {current_path}: {e_inner}")
            
            self.root.after(0, lambda: self.progress_var.set(100)) # Ensure 100% at the end
            self.root.after(0, lambda: self.conversion_complete(successful, failed, failed_files_details))
            
        except Exception as e_outer: # Should ideally not be reached if inner try-except is robust
            self.root.after(0, lambda: self.conversion_error(f"An unexpected error occurred: {str(e_outer)}"))
        finally:
            self.is_converting = False
            self.root.after(0, lambda: self.convert_btn.config(state="normal")) # Re-enable button
    
    def conversion_complete(self, successful, failed, failed_files_details):
        final_status_msg = f"Conversion Complete: {successful} succeeded, {failed} failed."
        self.status_label.config(text=final_status_msg)
        
        if failed == 0:
            messagebox.showinfo("Conversion Complete", f"Successfully converted {successful} images!")
        else:
            error_summary = f"{final_status_msg}\n\nFailed files:\n"
            for i, (name, err) in enumerate(failed_files_details):
                if i < 10: # Show details for up to 10 failed files
                    error_summary += f"- {name}: {err}\n"
                else:
                    error_summary += f"...and {len(failed_files_details) - 10} more.\n"
                    break
            messagebox.showwarning("Conversion Issues", error_summary)
    
    def conversion_error(self, error_message):
        self.status_label.config(text="Error during conversion!")
        self.convert_btn.config(state="normal")
        messagebox.showerror("Conversion Error", f"An error occurred:\n{error_message}")

def main():
    root = tk.Tk()
    
    # Attempt to set a more modern theme if available (e.g., on Windows)
    try:
        style = ttk.Style(root)
        # Available themes can be checked with style.theme_names()
        # 'clam', 'alt', 'default', 'classic' are common.
        # 'vista' on Windows, 'aqua' on macOS.
        if 'clam' in style.theme_names():
            style.theme_use('clam')
        elif 'vista' in style.theme_names(): # For a more native Windows look
             style.theme_use('vista')
    except tk.TclError:
        pass # If theming fails, use default
    
    app = ImageConverter(root)
    
    def on_closing():
        if app.is_converting:
            if messagebox.askokcancel("Quit", "Conversion is in progress. Do you want to quit anyway? This may leave partial files."):
                # Optionally, add logic here to try and stop the thread gracefully if possible
                root.destroy()
        else:
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()

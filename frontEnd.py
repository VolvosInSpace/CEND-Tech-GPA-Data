import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import os

from backEnd import GPAProcessor

class GPAAnalysisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GPA Analysis")
        self.root.geometry("1000x700")
        self.root.configure(bg="#121212")
        
        self.processor = GPAProcessor()
        self.file_directory = None

        # Main layout
        self.main_frame = tk.Frame(self.root, bg="#1E1E1E")
        self.main_frame.pack(fill="both", expand=True)

        # Sidebar
        self.sidebar = tk.Frame(self.main_frame, width=250, bg="#252525")
        self.sidebar.pack(side="left", fill="y", padx=10, pady=10)
        tk.Label(self.sidebar, text="GPA Analysis", font=("Arial", 20, "bold"),
                 fg="white", bg="#252525").pack(pady=20)

        # Navigation Buttons
        self.buttons = {}
        self.create_nav_button("Dashboard", self.show_dashboard)
        self.create_nav_button("Section Data", self.show_section)
        self.create_nav_button("Group Data", self.show_group)
        self.create_nav_button("Good List", self.show_good_list)
        self.create_nav_button("Work List", self.show_bad_list)
        self.create_nav_button("History", self.show_history)  # Add new history button
        
        # Content Area
        self.content_area = tk.Frame(self.main_frame, bg="#2A2A2A")
        self.content_area.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Tabs
        self.tabs = {
            "Dashboard": tk.Frame(self.content_area, bg="#2A2A2A"),
            "Section Data": tk.Frame(self.content_area, bg="#2A2A2A"),
            "Group Data": tk.Frame(self.content_area, bg="#2A2A2A"),
            "Good List": tk.Frame(self.content_area, bg="#2A2A2A"),
            "Work List": tk.Frame(self.content_area, bg="#2A2A2A"),
            "History": tk.Frame(self.content_area, bg="#2A2A2A")  # Add history tab
        }

        self.setup_dashboard_tab()
        self.setup_section_tab()
        self.setup_group_tab()
        self.setup_good_list_tab()
        self.setup_bad_list_tab()
        self.setup_history_tab()  # Add this line
        self.show_dashboard()

    def create_nav_button(self, name, command):
        btn = tk.Button(self.sidebar, text=name, bg="#333333", fg="white",
                        activebackground="#444444", font=("Arial", 14),
                        height=2, command=lambda: self.switch_tab(name, command))
        btn.pack(pady=8, padx=15, fill="x")
        self.buttons[name] = btn

    def switch_tab(self, name, command):
        for btn in self.buttons.values():
            btn.configure(bg="#333333")
        self.buttons[name].configure(bg="#555555")
        command()

    def show_dashboard(self):
        self.show_tab("Dashboard")

    def show_section(self):
        self.show_tab("Section Data")
        self.update_section_data()

    def show_group(self):
        self.show_tab("Group Data")
        self.update_group_data()

    def show_good_list(self):
        self.show_tab("Good List")
        self.update_good_list()

    def show_bad_list(self):
        self.show_tab("Work List")
        self.update_work_list()

    def show_history(self):
        self.show_tab("History")
        self.update_history_data()  # Fix the method name

    def show_tab(self, tab_name):
        for tab in self.tabs.values():
            tab.pack_forget()
        self.tabs[tab_name].pack(fill="both", expand=True)

    def setup_dashboard_tab(self):
        dashboard = self.tabs["Dashboard"]
        tk.Label(dashboard, text="Teacher GPA Calculator", font=("Arial", 24, "bold"),
                 fg="white", bg="#2A2A2A").pack(pady=10)
        
        # Directory selection frame
        dir_frame = tk.Frame(dashboard, bg="#2A2A2A")
        dir_frame.pack(pady=20)
        tk.Label(dir_frame, text="Select Directory:", font=("Arial", 12),
                 fg="white", bg="#2A2A2A").pack(side="left", padx=5)
        self.dir_path_var = tk.StringVar()
        dir_entry = tk.Entry(dir_frame, textvariable=self.dir_path_var, width=50)
        dir_entry.pack(side="left", padx=5)
        browse_btn = tk.Button(dir_frame, text="Browse", command=self.select_directory)
        browse_btn.pack(side="left", padx=5)
        
        # Run file selection frame (populated after processing files)
        run_frame = tk.Frame(dashboard, bg="#2A2A2A")
        run_frame.pack(pady=10)
        tk.Label(run_frame, text="Select Run File:", font=("Arial", 12),
                 fg="white", bg="#2A2A2A").pack(side="left", padx=5)
        self.run_file_combobox = ttk.Combobox(run_frame, values=[])
        self.run_file_combobox.pack(side="left", padx=5)
        apply_run_btn = tk.Button(run_frame, text="Apply Run", command=self.apply_run_selection)
        apply_run_btn.pack(side="left", padx=5)
        
        # Process button
        process_btn = tk.Button(dashboard, text="Process Files", command=self.process_files,
                                bg="#4CAF50", fg="white", font=("Arial", 12, "bold"),
                                padx=20, pady=10)
        process_btn.pack(pady=20)
        
        # Status frame
        self.status_frame = tk.Frame(dashboard, bg="#2A2A2A")
        self.status_frame.pack(fill="x", padx=20, pady=10)
        self.status_label = tk.Label(self.status_frame, text="Ready to process files.",
                                     font=("Arial", 12), fg="white", bg="#2A2A2A")
        self.status_label.pack(pady=5)
        
        # Summary statistics frame
        self.summary_frame = tk.Frame(dashboard, bg="#2A2A2A")
        self.summary_frame.pack(fill="both", expand=True, padx=20, pady=10)

    def select_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.file_directory = directory
            self.dir_path_var.set(directory)
            self.status_label.config(text=f"Selected directory: {directory}")

    def process_files(self):
        if not self.file_directory:
            messagebox.showerror("Error", "Please select a directory first")
            return
        try:
            self.status_label.config(text="Processing files...")
            self.root.update()
            file_count = self.processor.load_files_to_dataframes(self.file_directory)
            self.processor.calculate_all_gpas()
            self.processor.populate_good_work_lists()
            self.update_summary()
            self.update_section_data()
            self.update_group_data()
            self.update_good_list()
            self.update_work_list()
            self.update_history_data()  # Add this line
            
            # Populate the run file combobox with keys from run_dfs
            run_files = list(self.processor.run_dfs.keys())
            print("DEBUG: Run files loaded:", run_files)
            self.run_file_combobox['values'] = ["ALLFILES"] + run_files  
            self.run_file_combobox.current(0)  
            self.status_label.config(text=f"Processed {file_count} files successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Error processing files: {str(e)}")
            self.status_label.config(text=f"Error: {str(e)}")

    def apply_run_selection(self):
        selected_run = self.run_file_combobox.get()
        if not selected_run:
            messagebox.showwarning("Warning", "Please select a run file from the dropdown.")
            return
        try:
            if selected_run == "ALLFILES":
                # Reset to include all data
                self.processor.section_dfs = self.processor.all_section_dfs.copy()
                self.processor.group_dfs = self.processor.all_group_dfs.copy()
            else:
                self.processor.select_run(selected_run)
            
            self.processor.calculate_all_gpas()
            # Add this line to rebuild good_list and work_list after selection
            self.processor.populate_good_work_lists()
            
            # Update all relevant pages with filtered data
            self.update_section_data()
            self.update_group_data()
            self.update_good_list()
            self.update_work_list()
            self.update_history_data()
            self.update_summary()
            self.status_label.config(text=f"Run file '{selected_run}' applied successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_summary(self):
        for widget in self.summary_frame.winfo_children():
            widget.destroy()
        stats = self.processor.get_summary_statistics()
        if not stats or stats['section_count'] == 0:
            tk.Label(self.summary_frame, text="No data loaded", font=("Arial", 14),
                     fg="white", bg="#2A2A2A").pack(pady=10)
            return
        tk.Label(self.summary_frame, text="Summary Statistics", font=("Arial", 16, "bold"),
                 fg="white", bg="#2A2A2A").pack(pady=10)
        info_frame = tk.Frame(self.summary_frame, bg="#2A2A2A")
        info_frame.pack(fill="x", pady=5)
        info_list = [
            f"Number of Groups: {stats['group_count']}",
            f"Number of Sections: {stats['section_count']}",
            f"Total Unique Students: {stats['student_count']}",
            f"Students on Good List: {stats['good_list_count']}",
            f"Students on Work List: {stats['work_list_count']}",
            f"Overall GPA: {stats['overall_gpa']:.2f}" if stats['overall_gpa'] else "Overall GPA: N/A"
        ]
        for info in info_list:
            tk.Label(info_frame, text=info, font=("Arial", 12),
                     fg="white", bg="#2A2A2A", anchor="w").pack(fill="x", pady=2)
        chart_frame = tk.Frame(self.summary_frame, bg="#2A2A2A")
        chart_frame.pack(fill="both", expand=True, pady=10)
        

    def setup_section_tab(self):
        tab = self.tabs["Section Data"]
        header_frame = tk.Frame(tab, bg="#2A2A2A")
        header_frame.pack(fill="x", pady=10)
        
        tk.Label(header_frame, text="Section GPA Data", font=("Arial", 18, "bold"),
                 fg="white", bg="#2A2A2A").pack(side="left", padx=20)
                 
        export_btn = tk.Button(header_frame, text="Export to CSV", 
                              command=lambda: self.export_to_csv("Section Data"),
                              bg="#4CAF50", fg="white", font=("Arial", 10))
        export_btn.pack(side="right", padx=20)
        
        # Create a container frame for the table and scrollbars
        table_frame = tk.Frame(tab, bg="#2A2A2A")
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Detailed grade distribution columns with Z-Score added
        columns = ["Section Name", "GPA", "Z-Score", "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "D-", "F"]
        self.section_table = ttk.Treeview(table_frame, columns=columns, show="headings", height=20)
        for col in columns:
            self.section_table.heading(col, text=col)
            self.section_table.column(col, width=80, anchor="center")
        self.section_table.column("Section Name", width=150, anchor="w")
        self.section_table.column("Z-Score", width=80, anchor="center")
        
        # Create vertical scrollbar
        y_scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.section_table.yview)
        self.section_table.configure(yscrollcommand=y_scrollbar.set)
        
        # Create horizontal scrollbar
        x_scrollbar = ttk.Scrollbar(table_frame, orient="horizontal", command=self.section_table.xview)
        self.section_table.configure(xscrollcommand=x_scrollbar.set)
        
        # Place the treeview and scrollbars in the frame using grid
        self.section_table.grid(row=0, column=0, sticky='nsew')
        y_scrollbar.grid(row=0, column=1, sticky='ns')
        x_scrollbar.grid(row=1, column=0, sticky='ew')
        
        # Configure the table_frame grid
        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

    def update_section_data(self):
        for item in self.section_table.get_children():
            self.section_table.delete(item)
        sections_data = self.processor.get_all_sections_data()
        if not sections_data:
            return
        for section in sections_data:
            gpa_text = f"{section['gpa']:.2f}" if section['gpa'] is not None else "N/A"
            z_score_text = f"{section['z_score']:.2f}" if section['z_score'] is not None else "N/A"
            dist = section['distribution']
            row_data = [
                section['name'],
                gpa_text,
                z_score_text,
                dist.get("A", 0),
                dist.get("A-", 0),
                dist.get("B+", 0),
                dist.get("B", 0),
                dist.get("B-", 0),
                dist.get("C+", 0),
                dist.get("C", 0),
                dist.get("C-", 0),
                dist.get("D+", 0),
                dist.get("D", 0),
                dist.get("D-", 0),
                dist.get("F", 0)
            ]
            self.section_table.insert("", "end", values=row_data)

    def setup_group_tab(self):
        frame = self.tabs["Group Data"]
        header_frame = tk.Frame(frame, bg="#2A2A2A")
        header_frame.pack(fill="x", pady=(10, 5))
        
        self.group_overall_label = tk.Label(header_frame, text="All groups combined GPA: N/A",
                                            font=("Arial", 16, "bold"), fg="white", bg="#2A2A2A")
        self.group_overall_label.pack(side="left", padx=20)
        
        export_btn = tk.Button(header_frame, text="Export to CSV", 
                        command=lambda: self.export_to_csv("Group Data"),
                        bg="#4CAF50", fg="white", font=("Arial", 10))
        export_btn.pack(side="right", padx=20)
        
        # Create a container frame for the table and scrollbars
        table_frame = tk.Frame(frame, bg="#2A2A2A")
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.group_table = ttk.Treeview(table_frame, columns=["Group Name", "GPA", "Z-Score", "Sections"],
                                        show="headings", height=10)
        self.group_table.heading("Group Name", text="Group Name")
        self.group_table.heading("GPA", text="GPA")
        self.group_table.heading("Z-Score", text="Z-Score")
        self.group_table.heading("Sections", text="Sections")
        self.group_table.column("Group Name", width=200, anchor="w")
        self.group_table.column("GPA", width=100, anchor="center")
        self.group_table.column("Z-Score", width=100, anchor="center")
        self.group_table.column("Sections", width=400, anchor="w")
        
        # Create vertical scrollbar
        y_scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.group_table.yview)
        self.group_table.configure(yscrollcommand=y_scrollbar.set)
        
        # Create horizontal scrollbar
        x_scrollbar = ttk.Scrollbar(table_frame, orient="horizontal", command=self.group_table.xview)
        self.group_table.configure(xscrollcommand=x_scrollbar.set)
        
        # Place the treeview and scrollbars in the frame using grid
        self.group_table.grid(row=0, column=0, sticky='nsew')
        y_scrollbar.grid(row=0, column=1, sticky='ns')
        x_scrollbar.grid(row=1, column=0, sticky='ew')
        
        # Configure the table_frame grid
        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

    def update_group_data(self):
        for item in self.group_table.get_children():
            self.group_table.delete(item)
        overall_gpa = self.processor.get_overall_gpa()
        if overall_gpa is not None:
            self.group_overall_label.config(text=f"All groups combined GPA: {overall_gpa:.2f}")
        else:
            self.group_overall_label.config(text="All groups combined GPA: N/A")
        groups_data = self.processor.get_all_groups_data()
        if not groups_data:
            return
        max_len = 0
        for group in groups_data:
            gpa_text = f"{group['gpa']:.2f}" if group['gpa'] is not None else "N/A"
            z_score_text = f"{group['z_score']:.2f}" if group['z_score'] is not None else "N/A"
            sections_str = ", ".join(group['sections'])
            if len(sections_str) > max_len:
                max_len = len(sections_str)
            row_data = [
                group['name'],
                gpa_text,
                z_score_text,
                sections_str
            ]
            self.group_table.insert("", "end", values=row_data)
        min_width = 400
        new_width = max(min_width, min(2000, max_len * 7))
        self.group_table.column("Sections", width=new_width)

    def setup_good_list_tab(self):
        self.create_student_list_tab(self.tabs["Good List"], "Students with A Grades",
                                ["Student Name", "ID", "GPA", "Sections"])

    def setup_bad_list_tab(self):
        self.create_student_list_tab(self.tabs["Work List"], "Students Needing Support",
                                ["Student Name", "ID", "GPA", "Sections"])

    def create_student_list_tab(self, tab, title, columns):
        header_frame = tk.Frame(tab, bg="#2A2A2A")
        header_frame.pack(fill="x", pady=10)
        
        tk.Label(header_frame, text=title, font=("Arial", 18, "bold"),
                 fg="white", bg="#2A2A2A").pack(side="left", padx=20)
                 
        # Determine list type from title
        list_type = "Good List" if "A Grades" in title else "Work List"
        export_btn = tk.Button(header_frame, text="Export to CSV", 
                              command=lambda: self.export_to_csv(list_type),
                              bg="#4CAF50", fg="white", font=("Arial", 10))
        export_btn.pack(side="right", padx=20)
        
        table = ttk.Treeview(tab, columns=columns, show="headings", height=20)
        for col in columns:
            table.heading(col, text=col)
        table.column(columns[0], width=200, anchor="w")
        table.column(columns[1], width=100, anchor="center")
        table.column(columns[2], width=100, anchor="center")  # GPA column
        table.column(columns[3], width=400, anchor="w")       # Sections column
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=table.yview)
        table.configure(yscrollcommand=scrollbar.set)
        table.pack(side="left", fill="both", expand=True, padx=(20, 0), pady=10)
        scrollbar.pack(side="right", fill="y", padx=(0, 20), pady=10)
        if "A Grades" in title:
            self.good_list_table = table
        else:
            self.work_list_table = table

    def update_good_list(self):
        for item in self.good_list_table.get_children():
            self.good_list_table.delete(item)
        good_list = self.processor.good_list
        if not good_list:
            return
        max_len = 0
        for student_id, info in good_list.items():
            gpa = self.processor.get_student_gpa(student_id)
            gpa_text = f"{gpa:.2f}" if gpa is not None else "N/A"
            sections_str = ", ".join(info['classes'])
            if len(sections_str) > max_len:
                max_len = len(sections_str)
            row_data = [info['name'], student_id, gpa_text, sections_str]
            self.good_list_table.insert("", "end", values=row_data)
        min_width = 400
        new_width = max(min_width, min(2000, max_len * 7))
        self.good_list_table.column("Sections", width=new_width)

    def update_work_list(self):
        for item in self.work_list_table.get_children():
            self.work_list_table.delete(item)
        work_list = self.processor.work_list
        if not work_list:
            return
        max_len = 0
        for student_id, info in work_list.items():
            gpa = self.processor.get_student_gpa(student_id)
            gpa_text = f"{gpa:.2f}" if gpa is not None else "N/A"
            sections_str = ", ".join(info['classes'])
            if len(sections_str) > max_len:
                max_len = len(sections_str)
            row_data = [info['name'], student_id, gpa_text, sections_str]
            self.work_list_table.insert("", "end", values=row_data)
        min_width = 400
        new_width = max(min_width, min(2000, max_len * 7))
        self.work_list_table.column("Sections", width=new_width)

    def setup_history_tab(self):
        tab = self.tabs["History"]
        header_frame = tk.Frame(tab, bg="#2A2A2A")
        header_frame.pack(fill="x", pady=10)
        
        tk.Label(header_frame, text="Student History Analysis", font=("Arial", 18, "bold"),
                 fg="white", bg="#2A2A2A").pack(side="left", padx=20)
                 
        export_btn = tk.Button(header_frame, text="Export to CSV", 
                              command=lambda: self.export_to_csv("History"),
                              bg="#4CAF50", fg="white", font=("Arial", 10))
        export_btn.pack(side="right", padx=20)
        
        # Add warning banner frame (hidden by default)
        self.history_warning_frame = tk.Frame(tab, bg="#FFF3CD", padx=10, pady=10)
        self.history_warning_label = tk.Label(
            self.history_warning_frame,
            text="Please select 'ALLFILES' filter on the Dashboard to view student history data",
            font=("Arial", 12, "bold"),
            bg="#FFF3CD",
            fg="#856404"
        )
        self.history_warning_label.pack(fill="x", expand=True)
        # Don't pack the frame yet - we'll show/hide it as needed
        
        # Create a container frame for the table and scrollbars
        table_frame = tk.Frame(tab, bg="#2A2A2A")
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Create a single table with columns for name, ID, GPA, the three pattern types, and classes/grades
        columns = [
            "Student Name", 
            "ID",
            "GPA",  # Add GPA column
            "Good List Multiple Times", 
            "Work List Multiple Times", 
            "Both Lists",
            "Classes and Grades"
        ]
        
        self.history_table = ttk.Treeview(table_frame, columns=columns, show="headings", height=20)
        
        # Set up columns with appropriate widths
        self.history_table.heading("Student Name", text="Student Name")
        self.history_table.heading("ID", text="ID")
        self.history_table.heading("GPA", text="GPA")  # Add GPA heading
        self.history_table.heading("Good List Multiple Times", text="Good List Multiple Times")
        self.history_table.heading("Work List Multiple Times", text="Work List Multiple Times")
        self.history_table.heading("Both Lists", text="Both Lists")
        self.history_table.heading("Classes and Grades", text="Classes and Grades")
        
        self.history_table.column("Student Name", width=200, anchor="w")
        self.history_table.column("ID", width=100, anchor="center")
        self.history_table.column("GPA", width=80, anchor="center")  # Add GPA column
        self.history_table.column("Good List Multiple Times", width=150, anchor="center")
        self.history_table.column("Work List Multiple Times", width=150, anchor="center")
        self.history_table.column("Both Lists", width=150, anchor="center")
        self.history_table.column("Classes and Grades", width=500, anchor="w", stretch=tk.YES)
        
        # Create vertical scrollbar
        y_scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.history_table.yview)
        self.history_table.configure(yscrollcommand=y_scrollbar.set)
        
        # Create horizontal scrollbar
        x_scrollbar = ttk.Scrollbar(table_frame, orient="horizontal", command=self.history_table.xview)
        self.history_table.configure(xscrollcommand=x_scrollbar.set)
        
        # Place the treeview and scrollbars in the frame
        self.history_table.grid(row=0, column=0, sticky='nsew')
        y_scrollbar.grid(row=0, column=1, sticky='ns')
        x_scrollbar.grid(row=1, column=0, sticky='ew')
        
        # Configure the table_frame grid
        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

    def update_history_data(self):
        """Update the history table with student history patterns"""
        # Clear existing data
        for item in self.history_table.get_children():
            self.history_table.delete(item)
        
        # Check if a specific run filter is applied (not ALLFILES)
        current_run = self.run_file_combobox.get()
        if current_run != "ALLFILES" and current_run != "":
            # Show warning banner
            self.history_warning_frame.pack(fill="x", padx=20, pady=(0, 10), before=self.history_table.master)
        else:
            # Hide warning banner if it's visible
            self.history_warning_frame.pack_forget()
                
        # Get history data from processor
        history_data = self.processor.get_history_summary()
        if not history_data:
            return
                
        # Populate the table
        max_len = 0
        for student_id, info in history_data.items():
            # Get student's classes and grades
            classes_grades = self.get_student_classes_and_grades(student_id)
            if len(classes_grades) > max_len:
                max_len = len(classes_grades)
            # Calculate student GPA
            gpa = self.processor.get_student_gpa(student_id)
            gpa_text = f"{gpa:.2f}" if gpa is not None else "N/A"
            row_data = [
                info['name'],
                student_id,
                gpa_text,
                "✓" if info['repeat_good'] else "",
                "✓" if info['repeat_work'] else "",
                "✓" if info['mixed'] else "",
                classes_grades
            ]
            self.history_table.insert("", "end", values=row_data)

        # Dynamically set column width based on max content length (approximate)
        # 7 pixels per character is a rough estimate; adjust as needed
        min_width = 500
        new_width = max(min_width, min(2000, max_len * 7))
        self.history_table.column("Classes and Grades", width=new_width)

    def get_student_classes_and_grades(self, student_id):
        """Get a formatted string of classes and grades for a student"""
        classes_grades = []
        
        # Check good list
        if student_id in self.processor.good_list:
            for class_name in self.processor.good_list[student_id]['classes']:
                classes_grades.append(f"{class_name}: A")
        
        # Check work list
        if student_id in self.processor.work_list:
            for class_name in self.processor.work_list[student_id]['classes']:
                # Find the actual grade from section data
                grade = self.find_student_grade(student_id, class_name)
                classes_grades.append(f"{class_name}: {grade}")
        
        return ", ".join(classes_grades)

    def find_student_grade(self, student_id, class_name):
        """Find a student's grade in a specific class"""
        if class_name in self.processor.section_dfs:
            df = self.processor.section_dfs[class_name]
            student_row = df[df['ID'] == student_id]
            if not student_row.empty:
                return student_row['Grade'].iloc[0]
        return "?"  # Return ? if grade can't be found

    def export_to_csv(self, data_type):
        """General export function that handles file selection and calls appropriate export method"""
        file_types = [('CSV Files', '*.csv'), ('All Files', '*.*')]
        default_name = f"{data_type.lower().replace(' ', '_')}_export.csv"
        
        filepath = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=file_types,
            initialfile=default_name
        )
        
        if not filepath:  # User cancelled
            return
            
        try:
            if data_type == "Section Data":
                success = self.processor.export_section_data(filepath)
            elif data_type == "Group Data":
                success = self.processor.export_group_data(filepath)
            elif data_type == "Good List":
                success = self.processor.export_student_list(filepath, list_type='good')
            elif data_type == "Work List":
                success = self.processor.export_student_list(filepath, list_type='work')
            elif data_type == "History":
                success = self.processor.export_history_data(filepath)
            else:
                messagebox.showerror("Error", f"Unknown data type: {data_type}")
                return
                
            if success:
                messagebox.showinfo("Export Successful", f"{data_type} exported successfully to:\n{filepath}")
            else:
                messagebox.showwarning("No Data", f"No {data_type.lower()} available to export.")
        except Exception as e:
            messagebox.showerror("Export Error", f"Error exporting data: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = GPAAnalysisApp(root)
    root.mainloop()

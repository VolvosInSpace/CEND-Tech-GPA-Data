import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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

        # Content Area
        self.content_area = tk.Frame(self.main_frame, bg="#2A2A2A")
        self.content_area.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Tabs
        self.tabs = {
            "Dashboard": tk.Frame(self.content_area, bg="#2A2A2A"),
            "Section Data": tk.Frame(self.content_area, bg="#2A2A2A"),
            "Group Data": tk.Frame(self.content_area, bg="#2A2A2A"),
            "Good List": tk.Frame(self.content_area, bg="#2A2A2A"),
            "Work List": tk.Frame(self.content_area, bg="#2A2A2A")
        }

        self.setup_dashboard_tab()
        self.setup_section_tab()
        self.setup_group_tab()
        self.setup_good_list_tab()
        self.setup_bad_list_tab()
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
            
            # Populate the run file combobox with keys from run_dfs
            run_files = list(self.processor.run_dfs.keys())
            print("DEBUG: Run files loaded:", run_files)
            self.run_file_combobox['values'] = run_files
            if run_files:
                self.run_file_combobox.current(0)
            else:
                self.status_label.config(text="No run files found in directory.")
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
            self.processor.select_run(selected_run)
            self.processor.calculate_all_gpas()
            # Update all relevant pages with filtered data
            self.update_section_data()
            self.update_group_data()
            self.update_good_list()
            self.update_work_list()
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
        fig = self.processor.create_gpa_histogram()
        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def setup_section_tab(self):
        tab = self.tabs["Section Data"]
        tk.Label(tab, text="Section GPA Data", font=("Arial", 18, "bold"),
                 fg="white", bg="#2A2A2A").pack(pady=10)
        # Detailed grade distribution columns
        columns = ["Section Name", "GPA", "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "D-", "F"]
        self.section_table = ttk.Treeview(tab, columns=columns, show="headings", height=20)
        for col in columns:
            self.section_table.heading(col, text=col)
            self.section_table.column(col, width=80, anchor="center")
        self.section_table.column("Section Name", width=150, anchor="w")
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=self.section_table.yview)
        self.section_table.configure(yscrollcommand=scrollbar.set)
        self.section_table.pack(side="left", fill="both", expand=True, padx=(20, 0), pady=10)
        scrollbar.pack(side="right", fill="y", padx=(0, 20), pady=10)

    def update_section_data(self):
        for item in self.section_table.get_children():
            self.section_table.delete(item)
        sections_data = self.processor.get_all_sections_data()
        if not sections_data:
            return
        for section in sections_data:
            gpa_text = f"{section['gpa']:.2f}" if section['gpa'] is not None else "N/A"
            dist = section['distribution']
            row_data = [
                section['name'],
                gpa_text,
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
        self.group_overall_label = tk.Label(frame, text="All groups combined GPA: N/A",
                                             font=("Arial", 16, "bold"), fg="white", bg="#2A2A2A")
        self.group_overall_label.pack(pady=(10, 5))
        separator = tk.Frame(frame, height=2, bg="white")
        separator.pack(fill="x", padx=20, pady=5)
        self.group_table = ttk.Treeview(frame, columns=["Group Name", "GPA", "Sections"],
                                        show="headings", height=10)
        self.group_table.heading("Group Name", text="Group Name")
        self.group_table.heading("GPA", text="GPA")
        self.group_table.heading("Sections", text="Sections")
        self.group_table.column("Group Name", width=200, anchor="w")
        self.group_table.column("GPA", width=100, anchor="center")
        self.group_table.column("Sections", width=400, anchor="w")
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.group_table.yview)
        self.group_table.configure(yscrollcommand=scrollbar.set)
        self.group_table.pack(side="left", fill="both", expand=True, padx=(20, 0), pady=10)
        scrollbar.pack(side="right", fill="y", padx=(0, 20), pady=10)

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
        for group in groups_data:
            gpa_text = f"{group['gpa']:.2f}" if group['gpa'] is not None else "N/A"
            row_data = [
                group['name'],
                gpa_text,
                ", ".join(group['sections'])
            ]
            self.group_table.insert("", "end", values=row_data)

    def setup_good_list_tab(self):
        self.create_student_list_tab(self.tabs["Good List"], "Students with A Grades",
                                     ["Student Name", "ID", "Sections"])

    def setup_bad_list_tab(self):
        self.create_student_list_tab(self.tabs["Work List"], "Students Needing Support",
                                     ["Student Name", "ID", "Sections"])

    def create_student_list_tab(self, tab, title, columns):
        tk.Label(tab, text=title, font=("Arial", 18, "bold"),
                 fg="white", bg="#2A2A2A").pack(pady=10)
        table = ttk.Treeview(tab, columns=columns, show="headings", height=20)
        for col in columns:
            table.heading(col, text=col)
        table.column(columns[0], width=200, anchor="w")
        table.column(columns[1], width=100, anchor="center")
        table.column(columns[2], width=400, anchor="w")
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=table.yview)
        table.configure(yscrollcommand=scrollbar.set)
        table.pack(side="left", fill="both", expand=True, padx=(20, 0), pady=10)
        scrollbar.pack(side="right", fill="y", padx=(0, 20), pady=10)
        if title.startswith("Students with A"):
            self.good_list_table = table
        else:
            self.work_list_table = table

    def update_good_list(self):
        for item in self.good_list_table.get_children():
            self.good_list_table.delete(item)
        good_list = self.processor.good_list
        if not good_list:
            return
        for student_id, info in good_list.items():
            row_data = [info['name'], student_id, ", ".join(info['classes'])]
            self.good_list_table.insert("", "end", values=row_data)

    def update_work_list(self):
        for item in self.work_list_table.get_children():
            self.work_list_table.delete(item)
        work_list = self.processor.work_list
        if not work_list:
            return
        for student_id, info in work_list.items():
            row_data = [info['name'], student_id, ", ".join(info['classes'])]
            self.work_list_table.insert("", "end", values=row_data)

if __name__ == "__main__":
    root = tk.Tk()
    app = GPAAnalysisApp(root)
    root.mainloop()

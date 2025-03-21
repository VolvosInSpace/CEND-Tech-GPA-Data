import tkinter as tk
from tkinter import ttk, filedialog

class GPAAnalysisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GPA Analysis")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")
        
        # Create Notebook (Tabs)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Tabs
        self.dashboard_tab = ttk.Frame(self.notebook, padding=10)
        self.section_tab = ttk.Frame(self.notebook, padding=10)
        self.group_tab = ttk.Frame(self.notebook, padding=10)
        self.good_list_tab = ttk.Frame(self.notebook, padding=10)
        self.bad_list_tab = ttk.Frame(self.notebook, padding=10)
        
        self.notebook.add(self.dashboard_tab, text="Dashboard")
        self.notebook.add(self.section_tab, text="Based on Section")
        self.notebook.add(self.group_tab, text="Based on Group")
        self.notebook.add(self.good_list_tab, text="Good List")
        self.notebook.add(self.bad_list_tab, text="Work List")
        
        # Data storage
        self.good_list = []  # List of students with high grades
        self.work_list = []  # List of students with low grades
        self.uploaded_file = None
        
        # Setup each tab
        self.setup_dashboard_tab()
        self.setup_section_tab()
        self.setup_group_tab()
        self.setup_good_bad_tabs()
        
    def setup_dashboard_tab(self):
        ttk.Label(self.dashboard_tab, text="CEND Tech", font=("Arial", 18, "bold")).pack(pady=5)
        ttk.Label(self.dashboard_tab, text="Te(a)ch(er) GPA Calc. APP", font=("Arial", 14)).pack(pady=5)
        
        # File upload button
        self.upload_button = ttk.Button(self.dashboard_tab, text="Select File", command=self.upload_file)
        self.upload_button.pack(pady=5)
        
        # Label to display file name
        self.file_label = ttk.Label(self.dashboard_tab, text="No file selected", font=("Arial", 12))
        self.file_label.pack(pady=5)
    
    def upload_file(self):
        file_path = filedialog.askopenfilename(title="Select a File", filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx")])
        if file_path:
            self.uploaded_file = file_path
            self.file_label.config(text=f"Selected: {file_path.split('/')[-1]}")
    
    def setup_section_tab(self):
        ttk.Label(self.section_tab, text="Section Data", font=("Arial", 16, "bold")).pack(pady=10)
        self.section_tree = ttk.Treeview(self.section_tab, columns=("Section", "GPA", "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "D-", "F"), show="headings")
        
        for col in ["Section", "GPA", "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "D-", "F"]:
            self.section_tree.heading(col, text=col, anchor="center")
            self.section_tree.column(col, width=75, anchor="center")
        
        self.section_tree.pack(fill="both", expand=True, padx=10, pady=10)
    
    def setup_group_tab(self):
        ttk.Label(self.group_tab, text="Group Data", font=("Arial", 16, "bold")).pack(pady=10)
        
    def setup_good_bad_tabs(self):
        # Good List
        ttk.Label(self.good_list_tab, text="Good List", font=("Arial", 16, "bold")).pack(pady=10)
        self.good_tree = ttk.Treeview(self.good_list_tab, columns=("Name", "Section"), show="headings")
        
        for col in ["Name", "Section"]:
            self.good_tree.heading(col, text=col, anchor="center")
            self.good_tree.column(col, width=150, anchor="center")
        
        self.good_tree.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Work List
        ttk.Label(self.bad_list_tab, text="Work List", font=("Arial", 16, "bold")).pack(pady=10)
        self.work_tree = ttk.Treeview(self.bad_list_tab, columns=("Name", "Section"), show="headings")
        
        for col in ["Name", "Section"]:
            self.work_tree.heading(col, text=col, anchor="center")
            self.work_tree.column(col, width=150, anchor="center")
        
        self.work_tree.pack(fill="both", expand=True, padx=10, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style()
    style.configure("Accent.TButton", font=("Arial", 12), padding=10)
    app = GPAAnalysisApp(root)
    root.mainloop()

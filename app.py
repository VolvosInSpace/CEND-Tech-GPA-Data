import tkinter as tk
from tkinter import filedialog, ttk

class GPAAnalysisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GPA Analysis")
        self.root.geometry("1000x700")
        self.root.configure(bg="#121212")

        # Main layout: Sidebar and Content Area
        self.main_frame = tk.Frame(self.root, bg="#1E1E1E")
        self.main_frame.pack(fill="both", expand=True)

        # Sidebar
        self.sidebar = tk.Frame(self.main_frame, width=250, bg="#252525")
        self.sidebar.pack(side="left", fill="y", padx=10, pady=10)

        tk.Label(self.sidebar, text="GPA Analysis", font=("Arial", 20, "bold"), fg="white", bg="#252525").pack(pady=20)

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

        # Initialize Tabs
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
        btn = tk.Button(
            self.sidebar,
            text=name,
            bg="#333333",
            fg="white",
            activebackground="#444444",
            font=("Arial", 14),
            height=2,
            command=lambda: self.switch_tab(name, command)
        )
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

    def show_group(self):
        self.show_tab("Group Data")

    def show_good_list(self):
        self.show_tab("Good List")

    def show_bad_list(self):
        self.show_tab("Work List")

    def show_tab(self, tab_name):
        for tab in self.tabs.values():
            tab.pack_forget()
        self.tabs[tab_name].pack(fill="both", expand=True)

    def setup_dashboard_tab(self):
        tk.Label(self.tabs["Dashboard"], text="Teacher GPA Calculator", font=("Arial", 24, "bold"), fg="white", bg="#2A2A2A").pack(pady=10)
        upload_button = tk.Button(self.tabs["Dashboard"], text="Upload File", command=self.upload_file)
        upload_button.pack(pady=20)

        # Load the .gif image (make sure the image is in the same directory as your Python script)
        try:
            logo_image = tk.PhotoImage(file="logo.gif")  # Replace "logo.gif" with your actual .gif image filename
            logo_label = tk.Label(self.tabs["Dashboard"], image=logo_image, bg="#2A2A2A")
            logo_label.image = logo_image  # Keep a reference to avoid garbage collection
            logo_label.pack(pady=10)
        except Exception as e:
            print(f"Error loading image: {e}")
            logo_label = tk.Label(self.tabs["Dashboard"], text="[Logo Placeholder]", fg="white", bg="#2A2A2A", font=("Arial", 16))
            logo_label.pack(pady=10)

    def upload_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            print(f"File uploaded: {file_path}")

    def setup_section_tab(self):
        self.create_table(self.tabs["Section Data"], ["Section Name", "GPA", "A", "B", "C", "D", "F"])

    def setup_group_tab(self):
        frame = self.tabs["Group Data"]
        # Label for overall group GPA
        self.group_gpa_label = tk.Label(frame, text="All groups combined GPA: N/A", 
                                        font=("Arial", 16, "bold"), fg="white", bg="#2A2A2A")
        self.group_gpa_label.pack(pady=(10, 5))

        # Separator Line
        separator = tk.Frame(frame, height=2, bg="white")
        separator.pack(fill="x", padx=20, pady=5)

        # Table for displaying individual group GPAs
        self.group_table = ttk.Treeview(frame, columns=["Group Name", "GPA"], show="headings", height=10)
        self.group_table.heading("Group Name", text="Group Name")
        self.group_table.heading("GPA", text="GPA")
        self.group_table.column("Group Name", width=200, anchor="center")
        self.group_table.column("GPA", width=100, anchor="center")
        self.group_table.pack(fill="both", expand=True, padx=20, pady=10)

    def setup_good_list_tab(self):
        self.create_table(self.tabs["Good List"], ["Student Name", "GPA", "History"])

    def setup_bad_list_tab(self):
        self.create_table(self.tabs["Work List"], ["Student Name", "GPA", "History"])

    def create_table(self, parent, columns):
        tree = ttk.Treeview(parent, columns=columns, show="headings", height=20)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor="center")
        tree.pack(fill="both", expand=True, padx=20, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = GPAAnalysisApp(root)
    root.mainloop()

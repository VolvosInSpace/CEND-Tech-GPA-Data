import customtkinter as ctk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class GPAAnalysisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GPA Analysis")
        self.root.geometry("900x650")
        self.root.configure(bg="#121212")

        # Main layout: Sidebar and Content Area
        self.main_frame = ctk.CTkFrame(self.root, fg_color="#1E1E1E")
        self.main_frame.pack(fill="both", expand=True)

        # Sidebar
        self.sidebar = ctk.CTkFrame(self.main_frame, width=220, fg_color="#252525")
        self.sidebar.pack(side="left", fill="y", padx=10, pady=10)

        ctk.CTkLabel(self.sidebar, text="GPA Analysis", font=("Arial", 18, "bold"), text_color="white").pack(pady=20)

        # Navigation Buttons
        self.buttons = {}
        self.create_nav_button("Dashboard", self.show_dashboard)
        self.create_nav_button("Section Data", self.show_section)
        self.create_nav_button("Group Data", self.show_group)
        self.create_nav_button("Good List", self.show_good_list)
        self.create_nav_button("Work List", self.show_bad_list)

        # Content Area
        self.content_area = ctk.CTkFrame(self.main_frame, fg_color="#2A2A2A")
        self.content_area.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Initialize Tabs
        self.tabs = {
            "Dashboard": ctk.CTkFrame(self.content_area, fg_color="#2A2A2A"),
            "Section Data": ctk.CTkFrame(self.content_area, fg_color="#2A2A2A"),
            "Group Data": ctk.CTkFrame(self.content_area, fg_color="#2A2A2A"),
            "Good List": ctk.CTkFrame(self.content_area, fg_color="#2A2A2A"),
            "Work List": ctk.CTkFrame(self.content_area, fg_color="#2A2A2A")
        }

        self.setup_dashboard_tab()
        self.setup_section_tab()
        self.setup_group_tab()
        self.setup_good_list_tab()
        self.setup_bad_list_tab()
        self.show_dashboard()

    def create_nav_button(self, name, command):
        btn = ctk.CTkButton(
            self.sidebar,
            text=name,
            fg_color="#333333",
            text_color="white",
            hover_color="#444444",
            font=("Arial", 14),
            height=40,
            command=lambda: self.switch_tab(name, command)
        )
        btn.pack(pady=8, padx=15, fill="x")
        self.buttons[name] = btn

    def switch_tab(self, name, command):
        for btn in self.buttons.values():
            btn.configure(fg_color="#333333")
        self.buttons[name].configure(fg_color="#555555")
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
        ctk.CTkLabel(self.tabs["Dashboard"], text="Teacher GPA Calculator", font=("Arial", 24, "bold"), text_color="white").pack(pady=10)
        upload_button = ctk.CTkButton(self.tabs["Dashboard"], text="Upload File", command=self.upload_file)
        upload_button.pack(pady=20)

        # Add the CEND Tech logo
        try:
            logo_image = ImageTk.PhotoImage(Image.open("logo.gif"))  # Replace "logo.gif" with your actual image filename
            logo_label = ctk.CTkLabel(self.tabs["Dashboard"], image=logo_image, text="")
            logo_label.image = logo_image  # Keep a reference to avoid garbage collection
            logo_label.pack(pady=10)
        except Exception as e:
            print(f"Error loading image: {e}")
            ctk.CTkLabel(self.tabs["Dashboard"], text="[Logo Placeholder]", text_color="white", font=("Arial", 16)).pack(pady=10)

    def upload_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            print(f"File uploaded: {file_path}")

    def setup_section_tab(self):
        self.create_table(self.tabs["Section Data"], ["Section Name", "GPA", "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "D-", "F"])
        
        # Example data for sections and their GPAs
        sections = []
        gpas = []
        
        # Create a bar chart for sections and GPAs
        figure = Figure(figsize=(6, 4), dpi=100)
        ax = figure.add_subplot(111)
        ax.bar(sections, gpas, color="lightgreen")
        ax.set_title("GPA by Section")
        ax.set_xlabel("Sections")
        ax.set_ylabel("GPA")
        ax.set_ylim(0, 4.0)  # GPA range is typically 0 to 4.0
        
        canvas = FigureCanvasTkAgg(figure, self.tabs["Section Data"])
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=20, pady=10)

    def setup_group_tab(self):
        self.create_table(self.tabs["Group Data"], ["Group Name", "GPA", "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "D-", "F"])
        
        # Example data for groups and their GPAs
        groups = []
        gpas = []
        
        # Create a bar chart for groups and GPAs
        figure = Figure(figsize=(6, 4), dpi=100)
        ax = figure.add_subplot(111)
        ax.bar(groups, gpas, color="skyblue")
        ax.set_title("GPA by Group")
        ax.set_xlabel("Groups")
        ax.set_ylabel("GPA")
        ax.set_ylim(0, 4.0)  # GPA range is typically 0 to 4.0
        
        canvas = FigureCanvasTkAgg(figure, self.tabs["Group Data"])
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=20, pady=10)

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
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    root = ctk.CTk()
    app = GPAAnalysisApp(root)
    root.mainloop()
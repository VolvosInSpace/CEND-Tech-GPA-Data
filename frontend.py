import customtkinter as ctk
from tkinter import filedialog
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class GPAAnalysisApp:
    def __init__(self, root):
        ctk.set_appearance_mode("System")  
        ctk.set_default_color_theme("blue")

        self.root = root
        self.root.title("GPA Analysis")
        self.root.geometry("900x650")

        # Main layout: Sidebar and Content Area
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True)

        # Sidebar
        self.sidebar = ctk.CTkFrame(self.main_frame, width=220, fg_color="#1F1F1F", corner_radius=0)
        self.sidebar.pack(side="left", fill="y")

        ctk.CTkLabel(self.sidebar, text="GPA Analysis", font=("Arial", 18, "bold"), text_color="white").pack(pady=20)

        # Navigation Buttons
        self.buttons = {}  # Track active button states
        self.create_nav_button("Dashboard", self.show_dashboard)
        self.create_nav_button("Section Data", self.show_section)
        self.create_nav_button("Group Data", self.show_group)
        self.create_nav_button("Good List", self.show_good_list)
        self.create_nav_button("Work List", self.show_bad_list)

        # Content Area
        self.content_area = ctk.CTkFrame(self.main_frame, fg_color="#282828", corner_radius=10)
        self.content_area.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Initialize Tabs
        self.tabs = {
            "Dashboard": ctk.CTkFrame(self.content_area),
            "Section Data": ctk.CTkFrame(self.content_area),
            "Group Data": ctk.CTkFrame(self.content_area),
            "Good List": ctk.CTkFrame(self.content_area),
            "Work List": ctk.CTkFrame(self.content_area)
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
            fg_color="transparent", 
            hover_color="#333333",  
            text_color="white",
            anchor="w",  
            font=("Arial", 14),
            height=40,
            command=lambda n=name: self.switch_tab(n, command)
        )
        btn.pack(pady=5, padx=10, fill="x")
        self.buttons[name] = btn

    # Switches the active tab and updates button colors
    def switch_tab(self, name, command):
        for btn_name, btn in self.buttons.items():
            if btn_name == name:
                btn.configure(fg_color="#444444")  # Highlight active button
            else:
                btn.configure(fg_color="transparent")

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

    # Shows selected tab and hides others
    def show_tab(self, tab_name):
        for tab in self.tabs.values():
            tab.pack_forget()
        self.tabs[tab_name].pack(fill="both", expand=True)

    # Dashboard UI
    def setup_dashboard_tab(self):
        ctk.CTkLabel(self.tabs["Dashboard"], text="TEaCHer GPA Calc. App", font=("Arial", 20, "bold")).pack(pady=10)
        upload_button = ctk.CTkButton(
            self.tabs["Dashboard"],
            text="Upload File",
            command=self.upload_file
        )
        upload_button.pack(pady=20)

        # Add the CEND Tech logo 
        logo_image = Image.open("./Images/CEND_TECH_Logo.jpg") 
        logo_image = logo_image.resize((500, 400))  
        logo_photo = ImageTk.PhotoImage(logo_image)

        logo_label = ctk.CTkLabel(self.tabs["Dashboard"], image=logo_photo, text="")
        logo_label.image = logo_photo 
        logo_label.pack(pady=10)

    # File Upload
    def upload_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            print(f"File uploaded: {file_path}")

    # Section Data tab setup
    def setup_section_tab(self):
        # Create a frame for the table and chart
        frame = ctk.CTkFrame(self.tabs["Section Data"])
        frame.pack(fill="both", expand=True)

        # Table area
        table_frame = ctk.CTkFrame(frame)
        table_frame.pack(side="top", fill="x", padx=10, pady=10)
        self.create_table(table_frame, ["Section Name", "GPA", "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "D-", "F"])

        # Chart area
        chart_frame = ctk.CTkFrame(frame)
        chart_frame.pack(side="top", fill="both", expand=True, padx=10, pady=10)

        # Example data for the bar chart
        sections = ["Section A", "Section B", "Section C"]
        gpas = [3.5, 3.2, 3.8]

        # Create the bar chart
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.bar(sections, gpas, color="skyblue")
        ax.set_title("GPA by Section")
        ax.set_ylabel("GPA")
        ax.set_xlabel("Sections")

        # Embed the chart in the Tkinter tab
        canvas = FigureCanvasTkAgg(fig, chart_frame)
        canvas.get_tk_widget().pack(fill="both", expand=True)
        canvas.draw()

    # Group Data tab setup
    def setup_group_tab(self):
        # Create a frame for the table and chart
        frame = ctk.CTkFrame(self.tabs["Group Data"])
        frame.pack(fill="both", expand=True)

        # Table area
        table_frame = ctk.CTkFrame(frame)
        table_frame.pack(side="top", fill="x", padx=10, pady=10)
        self.create_table(table_frame, ["Group Name", "GPA", "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "D-", "F"])

        # Chart area
        chart_frame = ctk.CTkFrame(frame)
        chart_frame.pack(side="top", fill="both", expand=True, padx=10, pady=10)

        # Example data for the bar chart
        groups = ["Group 1", "Group 2", "Group 3"]
        gpas = [3.4, 3.6, 3.1]

        # Create the bar chart
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.bar(groups, gpas, color="lightgreen")
        ax.set_title("GPA by Group")
        ax.set_ylabel("GPA")
        ax.set_xlabel("Groups")

        # Embed the chart in the Tkinter tab
        canvas = FigureCanvasTkAgg(fig, chart_frame)
        canvas.get_tk_widget().pack(fill="both", expand=True)
        canvas.draw()

    # Good List tab setup
    def setup_good_list_tab(self):
        self.create_table(self.tabs["Good List"], ["Student Name", "GPA", "History"])

    # Work List tab setup
    def setup_bad_list_tab(self):
        self.create_table(self.tabs["Work List"], ["Student Name", "GPA", "History"])

    # Creates a table view
    def create_table(self, parent, columns):
        """Creates a table view with the given columns."""
        tree = ttk.Treeview(parent, columns=columns, show="headings", height=20)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor="center")
        tree.pack(fill="both", expand=True)

if __name__ == "__main__":
    root = ctk.CTk()
    app = GPAAnalysisApp(root)
    root.mainloop()
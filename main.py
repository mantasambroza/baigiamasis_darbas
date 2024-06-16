import customtkinter as ctk
import pandas as pd
from sqlalchemy import create_engine
from matplotlib.lines import Line2D
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np
from PIL import Image


# Connect to the database and load data into pandas dataframe
database_path = "/Users/mantasambroza/PycharmProjects/baigiamasis_darbas/database.db"
engine = create_engine(f"sqlite:///{database_path}")
df = pd.read_sql_table("lazeriu_duomenys", engine)
df["Date"] = pd.to_datetime(df["Date"])


class StatsFrame(ctk.CTkFrame):
    def __init__(self, master, title):
        super().__init__(master, border_color="white", border_width=2)

        # self.grid_columnconfigure(0, weight=1)
        self.title = title
        self.title = ctk.CTkLabel(
            self, text=self.title, fg_color="gray30", corner_radius=6
        )
        self.title.grid(
            row=0, column=0, padx=10, pady=(10, 0), columnspan=2, sticky="ew"
        )

        # Define labels
        self.label_selected = ctk.CTkLabel(self, text="Selected laser:", padx=50)
        self.label_std = ctk.CTkLabel(self, text="Standard deviation:")
        self.label_mean = ctk.CTkLabel(self, text="Mean:")
        self.label_max_value = ctk.CTkLabel(self, text="Maximum value:")
        self.label_min_value = ctk.CTkLabel(self, text="Minimum value:")

        self.label_selected_result = ctk.CTkLabel(self, text="N/A", pady=10, padx=50)
        self.label_std_result = ctk.CTkLabel(self, text="0", pady=10)
        self.label_mean_result = ctk.CTkLabel(self, text="0", pady=10)
        self.label_max_value_result = ctk.CTkLabel(self, text="0", pady=10)
        self.label_min_value_result = ctk.CTkLabel(self, text="0", pady=10)

        # Grid column 0
        self.label_selected.grid(row=1, column=0, pady=5, padx=5)
        self.label_std.grid(row=2, column=0, pady=5, padx=5)
        self.label_mean.grid(row=3, column=0, pady=5, padx=5)
        self.label_max_value.grid(row=4, column=0, pady=5, padx=5)
        self.label_min_value.grid(row=5, column=0, pady=5, padx=5)

        # Grid column 1
        self.label_selected_result.grid(row=1, column=1, pady=5, padx=5)
        self.label_std_result.grid(row=2, column=1, pady=5, padx=5)
        self.label_mean_result.grid(row=3, column=1, pady=5, padx=5)
        self.label_max_value_result.grid(row=4, column=1, pady=5, padx=5)
        self.label_min_value_result.grid(row=5, column=1, pady=5, padx=5)


class PlotFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # Creating figure for the plot
        self.figure = Figure(figsize=(9, 5), dpi=100, facecolor="white")
        self.ax = self.figure.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(
            row=0, column=2, columnspan=3, rowspan=7, pady=20
        )

        # Create and place the toolbar within its own frame
        self.toolbar_frame = ctk.CTkFrame(self, height=20)
        self.toolbar_frame.grid(row=0, column=0, columnspan=3)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.toolbar_frame)
        self.toolbar.update()
        self.toolbar.pack(side="top", anchor="nw", fill="x")


class PlotUpdateFrame(ctk.CTkFrame):
    def __init__(self, master, plot_frame, statusbar_frame):
        super().__init__(master)
        self.plot_frame = plot_frame
        self.statusbar_frame = statusbar_frame

        # Create and configure check boxes
        self.check_mean_var = ctk.StringVar(self, value="off")
        self.check_mean = ctk.CTkCheckBox(
            self,
            text="Add Mean",
            variable=self.check_mean_var,
            onvalue="on",
            offvalue="off",
        )

        self.check_std_var = ctk.StringVar(value="off")
        self.check_std = ctk.CTkCheckBox(
            self,
            text="Standard Deviation (1σ)",
            variable=self.check_std_var,
            onvalue="on",
            offvalue="off",
        )

        self.check_2std_var = ctk.StringVar(value="off")
        self.check_2std = ctk.CTkCheckBox(
            self,
            text="Standard Deviation (2σ)",
            variable=self.check_2std_var,
            onvalue="on",
            offvalue="off",
        )

        self.button_update = ctk.CTkButton(
            self, text="Update plot", command=self.update_plot
        )

        # Grid checkboxes and button to the frame
        self.check_mean.grid(row=0, column=1, pady=10, padx=15)
        self.check_std.grid(row=0, column=2, pady=10, padx=15)
        self.check_2std.grid(row=0, column=3, pady=10, padx=15)
        self.button_update.grid(row=0, column=4, pady=10, padx=15)

    def update_plot(self):
        # Get required values
        serial = self.master.entry_sn.get()
        chosen_parameter = self.master.option_menu.get()
        stdd = df[chosen_parameter].std()
        mean = df[chosen_parameter].mean()

        # Get values from the checkboxes
        std_tick = self.check_std.get()
        std2_tick = self.check_2std.get()
        mean_tick = self.check_mean.get()

        # Plot selected parameters for the ticked checkboxes
        if mean_tick == "on":
            self.plot_frame.ax.axhline(y=mean, color="r", label="Mean")
        if std_tick == "on":
            self.plot_frame.ax.axhspan(
                mean - stdd,
                mean + stdd,
                facecolor="b",
                alpha=0.25,
                label="Standard Deviation (1σ)",
            )
        if std2_tick == "on":
            self.plot_frame.ax.axhspan(
                mean - stdd * 2,
                mean + stdd * 2,
                facecolor="b",
                alpha=0.15,
                label="Standard Deviation (2σ)",
            )

        # Generate a new legend, with a manually marked serial number (same as in the main app)
        handles, labels = self.plot_frame.ax.get_legend_handles_labels()
        selected_laser_point = Line2D(
            [0],
            [0],
            label=serial,
            marker="o",
            markersize=10,
            markerfacecolor="r",
            markeredgecolor="r",
            linestyle="",
        )
        handles.append(selected_laser_point)
        self.plot_frame.ax.legend(handles=handles)
        self.plot_frame.canvas.draw()

        self.master.statusbar_frame.status_bar.configure(
            text="Plot has been updated with the selected parameters"
        )


class LogoFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # Load image, create label widget and attach image to it
        self.codeacademy_logo = ctk.CTkImage(
            light_image=Image.open(
                "/Users/mantasambroza/PycharmProjects/baigiamasis_darbas/codeacademy.png"
            ),
            dark_image=Image.open(
                "/Users/mantasambroza/PycharmProjects/baigiamasis_darbas/codeacademy.png"
            ),
            size=(276, 87),
        )

        self.label_logo = ctk.CTkLabel(self, image=self.codeacademy_logo, text="")
        self.label_logo.pack(padx=10, pady=10)


class StatusBarFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, border_width=0, fg_color="#151515", bg_color="#151515")

        font = ctk.CTkFont("Windows", size=16)
        self.status_bar = ctk.CTkLabel(
            self,
            text="Program is ready! Enter a serial number to begin...",
            text_color="darkgrey",
            font=font,
            pady=15,
            padx=10,
        )

        self.status_bar.pack(side="left")


class MainApp(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Laser Data Plotter")
        self._set_appearance_mode("dark")

        # Initialize class frames
        self.stats_frame = StatsFrame(self, "STATISTICS")
        self.plot_frame = PlotFrame(self)
        self.logo_frame = LogoFrame(self)
        self.statusbar_frame = StatusBarFrame(self)
        self.plot_update_frame = PlotUpdateFrame(
            self, self.plot_frame, self.statusbar_frame
        )

        # Grid frames
        self.stats_frame.grid(
            row=4, column=0, rowspan=5, columnspan=2, padx=75, pady=10, sticky="nsw"
        )
        self.plot_frame.grid(
            row=0, column=2, rowspan=7, columnspan=3, padx=5, pady=5, sticky="nsew"
        )
        self.logo_frame.grid(row=0, column=0, columnspan=2)
        self.plot_update_frame.grid(row=7, column=2, columnspan=3)
        self.statusbar_frame.grid(row=9, column=0, columnspan=5, sticky="we")

        # Creating other UI items on the master frame
        self.label_sn = ctk.CTkLabel(self, text="Serial number:")
        self.entry_sn = ctk.CTkEntry(self, placeholder_text="SN005090")
        self.label_parameter = ctk.CTkLabel(self, text="Laser parameter:")
        self.options = ["Power", "Repetition rate", "Wavelength", "PER", "Threshold"]
        self.option_menu = ctk.CTkOptionMenu(self, values=self.options)
        self.button_plot = ctk.CTkButton(self, text="Plot", command=self.plot_button)
        self.button_clear = ctk.CTkButton(
            self, text="Clear", command=self.clear_data_plot
        )

        # Grid master frame items
        self.label_sn.grid(row=1, column=0, padx=5, pady=5)
        self.label_parameter.grid(row=2, column=0, padx=5, pady=5)
        self.button_plot.grid(row=3, column=0, padx=5, pady=5)
        self.button_clear.grid(row=3, column=1, padx=5, pady=5)
        self.entry_sn.grid(row=1, column=1, padx=5, pady=5)
        self.option_menu.grid(row=2, column=1, padx=5, pady=5)

    def plot_button(self):
        # Clear canvas before drawing a new plot
        self.plot_frame.ax.clear()
        self.plot_frame.canvas.draw()

        # Get values for the serial and chosen parameter
        serial = self.entry_sn.get()
        chosen_parameter = self.option_menu.get()

        # Check if the entered serial number is in the database
        try:
            selected_laser_result = df.loc[
                df["Serial"] == serial, chosen_parameter
            ].values[0]
            self.stats_frame.label_selected_result.configure(text=selected_laser_result)
            self.statusbar_frame.status_bar.configure(
                text=f"Data for the {serial} is ready"
            )
        except IndexError:
            self.statusbar_frame.status_bar.configure(
                text=f"{serial} is not in the database. Please enter a new serial number."
            )
            self.stats_frame.label_selected_result.configure(text="Not found")

        # Calculate statistics for the chosen parameter and display results in statistics frame
        self.stats_frame.label_std_result.configure(
            text=f"{round(df[chosen_parameter].std(), 2)}"
        )
        self.stats_frame.label_mean_result.configure(
            text=f"{round(df[chosen_parameter].mean(), 2)}"
        )
        self.stats_frame.label_max_value_result.configure(
            text=f"{round(df[chosen_parameter].max(), 2)}"
        )
        self.stats_frame.label_min_value_result.configure(
            text=f"{round(df[chosen_parameter].min(), 2)}"
        )

        # Change size and color of the marker of the selected serial number
        size = np.where(df["Serial"] == serial, 60, 30)
        color = np.where(df["Serial"] == serial, "tab:red", "tab:blue")
        self.plot_frame.ax.scatter(
            df["Date"],
            df[chosen_parameter],
            c=color,
            s=size,
            label=f"{chosen_parameter} data",
        )
        self.plot_frame.ax.set_title(
            f"Measured {chosen_parameter} of the lasers in the database"
        )

        # Create a list of possible y-axis labels (depends on a chosen parameter)
        ylabel_map = {
            "Power": "Power, [mW]",
            "Repetition rate": "Repetition rate, [MHz]",
            "Wavelength": "Wavelength, [nm]",
            "PER": "PER, [dB]",
            "Threshold": "Threshold, [mA]",
        }

        # Edit legend to manually add selected laser serial number, set labels for the axes
        handles, labels = self.plot_frame.ax.get_legend_handles_labels()
        selected_laser_point = Line2D(
            [0],
            [0],
            label=serial,
            marker="o",
            markersize=10,
            markerfacecolor="r",
            markeredgecolor="r",
            linestyle="",
        )
        handles.append(selected_laser_point)
        self.plot_frame.ax.legend(handles=handles)
        self.plot_frame.ax.set_ylabel(ylabel_map[chosen_parameter])
        self.plot_frame.ax.set_xlabel("Date")
        self.plot_frame.canvas.draw()

    def clear_data_plot(self):
        self.stats_frame.label_std_result.configure(text="0")
        self.stats_frame.label_mean_result.configure(text="0")
        self.stats_frame.label_max_value_result.configure(text="0")
        self.stats_frame.label_min_value_result.configure(text="0")
        self.plot_frame.ax.clear()
        self.plot_frame.canvas.draw()

        self.statusbar_frame.status_bar.configure(
            text="Plot has been cleared. Select a parameter to plot or enter a new serial number."
        )


# Create and run the app
if __name__ == "__main__":
    app = MainApp()
    app.mainloop()

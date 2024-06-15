import customtkinter as ctk
import pandas as pd
from sqlalchemy import create_engine
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np
from PIL import Image, ImageTk

engine = create_engine('sqlite:///lazeriu_duomenys.db')
df = pd.read_sql_table('lazeriu_duomenys', engine)
df['Date'] = pd.to_datetime(df['Date'])


class StatsFrame(ctk.CTkFrame):
    def __init__(self, master, title):
        super().__init__(master, border_color='white', border_width=2)

        # self.grid_columnconfigure(0, weight=1)
        self.title = title
        self.title = ctk.CTkLabel(self, text=self.title, fg_color="gray30", corner_radius=6)
        self.title.grid(row=0, column=0, padx=10, pady=(10, 0), columnspan=2, sticky="ew")

        # Define labels
        self.label_selected = ctk.CTkLabel(self, text='Selected laser:', padx=50)
        self.label_std = ctk.CTkLabel(self, text='Standard deviation:')
        self.label_mean = ctk.CTkLabel(self, text='Mean:')
        self.label_max_value = ctk.CTkLabel(self, text='Maximum value:')
        self.label_min_value = ctk.CTkLabel(self, text='Minimum value:')

        self.label_selected_result = ctk.CTkLabel(self, text='N/A', pady=10, padx=50)
        self.label_std_result = ctk.CTkLabel(self, text='0', pady=10)
        self.label_mean_result = ctk.CTkLabel(self, text='0', pady=10)
        self.label_max_value_result = ctk.CTkLabel(self, text='0', pady=10)
        self.label_min_value_result = ctk.CTkLabel(self, text='0', pady=10)

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
        self.figure = Figure(figsize=(9, 5), dpi=100, facecolor='white')
        self.ax = self.figure.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=2, columnspan=3, rowspan=7, pady=20)

        # Create and place the toolbar within its own frame
        self.toolbar_frame = ctk.CTkFrame(self, height=20)
        self.toolbar_frame.grid(row=0, column=0, columnspan=3)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.toolbar_frame)
        self.toolbar.update()
        self.toolbar.pack(side='top', anchor='nw', fill='x')

        print("PlotFrame initialized successfully")


class PlotUpdateFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

class LogoFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.codeacademy_logo = ctk.CTkImage(light_image=Image.open('codeacademy.png'),
                                             dark_image=Image.open('codeacademy.png'),
                                             size=(276, 87))

        self.label_logo = ctk.CTkLabel(self, image=self.codeacademy_logo, text='')
        self.label_logo.pack(padx=10, pady=10)

class MainApp(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Laser data")
        self._set_appearance_mode("dark")
        # self.geometry("900x600")

        # Initialize frames
        self.stats_frame = StatsFrame(self, 'STATISTICS')
        self.plot_frame = PlotFrame(self)
        self.logo_frame = LogoFrame(self)

        self.stats_frame.grid(row=4, column=0, rowspan=5, columnspan=2, padx=75, pady=10, sticky='nsw')
        self.plot_frame.grid(row=0, column=2, rowspan=7, columnspan=3, padx=5, pady=5, sticky='nsew')
        self.logo_frame.grid(row=0, column=0, columnspan=2)

        # Creating all items
        self.label_sn = ctk.CTkLabel(self, text="Serial number:")
        self.entry_sn = ctk.CTkEntry(self, placeholder_text="K0018000")
        self.label_parameter = ctk.CTkLabel(self, text="Laser parameter:")
        self.options = ['Power', 'Repetition rate', 'Wavelength', 'PER', 'Threshold']
        self.option_menu = ctk.CTkOptionMenu(self, values=self.options)
        self.button_plot = ctk.CTkButton(self, text="Plot", command=self.plot_button)
        self.button_clear = ctk.CTkButton(self, text='Clear', command=self.clear_data_plot)

        self.check_std_var = ctk.StringVar(value='off')
        self.check_std = ctk.CTkCheckBox(self, text='Add Standard Deviation', variable=self.check_std_var, onvalue='on',
                                         offvalue='off')
        self.check_mean_var = ctk.StringVar(self, value='off')
        self.check_mean = ctk.CTkCheckBox(self, text='Add Mean', variable=self.check_mean_var, onvalue='on',
                                          offvalue='off')
        self.button_update = ctk.CTkButton(self, text='Update plot', command=self.update_plot)

        # Adding all elements with the grid, column 0
        self.label_sn.grid(row=1, column=0, padx=5, pady=5)
        self.label_parameter.grid(row=2, column=0, padx=5, pady=5)
        self.button_plot.grid(row=3, column=0, padx=5, pady=5)
        self.button_clear.grid(row=3, column=1, padx=5, pady=5)

        # Adding all elements with the grid, column 1
        self.entry_sn.grid(row=1, column=1, padx=5, pady=5)
        self.option_menu.grid(row=2, column=1, padx=5, pady=5)

        self.check_std.grid(row=7, column=2, pady=10)
        self.check_mean.grid(row=7, column=3, pady=10)
        self.button_update.grid(row=7, column=4, pady=10)

    def plot_button(self):

        self.plot_frame.ax.clear()
        self.plot_frame.canvas.draw()

        serial = self.entry_sn.get()
        chosen_parameter = self.option_menu.get()
        selected_laser_result = df.loc[df['Serial'] == serial, chosen_parameter].values[0]

        self.stats_frame.label_selected_result.configure(text=selected_laser_result)
        self.stats_frame.label_std_result.configure(text=f'{round(df[chosen_parameter].std(), 2)}')
        self.stats_frame.label_mean_result.configure(text=f'{round(df[chosen_parameter].mean(), 2)}')
        self.stats_frame.label_max_value_result.configure(text=f'{round(df[chosen_parameter].max(), 2)}')
        self.stats_frame.label_min_value_result.configure(text=f'{round(df[chosen_parameter].min(), 2)}')

        size = np.where(df['Serial'] == serial, 60, 30)
        color = np.where(df['Serial'] == serial, 'tab:red', 'tab:blue')
        self.plot_frame.ax.scatter(df['Date'], df[chosen_parameter], c=color, s=size,
                                   label=f'{chosen_parameter} of lasers')
        self.plot_frame.ax.set_title('Selected laser comparison')

        ylabel_map = {
            'Power': 'Power, [mW]',
            'Repetition rate': 'Repetition rate, [MHz]',
            'Wavelength': 'Wavelength, [nm]',
            'PER': 'PER, [dB]',
            'Threshold': 'Threshold, [mA]'
        }

        self.plot_frame.ax.legend()
        self.plot_frame.ax.set_ylabel(ylabel_map[chosen_parameter])
        self.plot_frame.ax.set_xlabel('Measurement date')
        self.plot_frame.canvas.draw()

    def update_plot(self):
        chosen_parameter = self.option_menu.get()
        stdd = df[chosen_parameter].std()
        mean = df[chosen_parameter].mean()

        std_tick = self.check_std.get()
        mean_tick = self.check_mean.get()

        if std_tick == 'on':
            self.plot_frame.ax.axhspan(mean - stdd, mean + stdd, facecolor='b', alpha=0.25, label='Standard deviation')
        if mean_tick == 'on':
            self.plot_frame.ax.axhline(y=mean, color='r', label='Mean')
        self.plot_frame.ax.legend()
        self.plot_frame.canvas.draw()

    def clear_data_plot(self):
        self.stats_frame.label_std_result.configure(text='0')
        self.stats_frame.label_mean_result.configure(text='0')
        self.stats_frame.label_max_value_result.configure(text='0')
        self.stats_frame.label_min_value_result.configure(text='0')
        self.plot_frame.ax.clear()
        self.plot_frame.canvas.draw()


# Create and run the app
if __name__ == "__main__":
    app = MainApp()
    app.mainloop()

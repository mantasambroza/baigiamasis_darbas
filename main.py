import customtkinter as ctk
import matplotlib.pyplot as plt
import pandas as pd
from sqlalchemy import create_engine
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np

engine = create_engine('sqlite:///lazeriu_duomenys.db')
df = pd.read_sql_table('lazeriu_duomenys', engine)
df['Date'] = pd.to_datetime(df['Date'])


class MainApp(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Lazeriu testavimas")
        # self.geometry("900x600")

        # Creating all items
        self.label_sn = ctk.CTkLabel(self, text="Serial number:")
        self.entry_sn = ctk.CTkEntry(self, placeholder_text="K0018000")
        self.label_parameter = ctk.CTkLabel(self, text="Laser parameter:")
        self.options = ['Power', 'Repetition rate', 'Wavelength', 'PER', 'Threshold']
        self.option_menu = ctk.CTkOptionMenu(self, values=self.options)
        self.button_plot = ctk.CTkButton(self, text="Plot", command=self.plot_button)
        self.label_std = ctk.CTkLabel(self, text='Std:')
        self.label_mean = ctk.CTkLabel(self, text='Mean:')
        self.label_max_value = ctk.CTkLabel(self, text='Max:')
        self.label_min_value = ctk.CTkLabel(self, text='Min:')
        self.label_std_result = ctk.CTkLabel(self, text='0')
        self.label_mean_result = ctk.CTkLabel(self, text='0')
        self.label_max_value_result = ctk.CTkLabel(self, text='0')
        self.label_min_value_result = ctk.CTkLabel(self, text='0')
        self.button_clear = ctk.CTkButton(self, text='Clear', command=self.clear_data_plot)
        self.check_std_var = ctk.StringVar(value='off')
        self.check_std = ctk.CTkCheckBox(self, text='Add Std', variable=self.check_std_var, onvalue='on',
                                         offvalue='off')
        self.check_mean_var = ctk.StringVar(self, value='off')
        self.check_mean = ctk.CTkCheckBox(self, text='Add Mean', variable=self.check_mean_var, onvalue='on',
                                          offvalue='off')
        self.button_update = ctk.CTkButton(self, text='Upadate plot', command=self.update_plot)

        # Adding all elements with the grid, column 0
        self.label_sn.grid(row=0, column=0, padx=5, pady=5)
        self.label_parameter.grid(row=1, column=0, padx=5, pady=5)
        self.button_plot.grid(row=2, column=0, padx=5, pady=5)
        self.button_clear.grid(row=2, column=1, padx=5, pady=5)
        self.label_std.grid(row=3, column=0, pady=5, padx=5)
        self.label_mean.grid(row=4, column=0, pady=5, padx=5)
        self.label_max_value.grid(row=5, column=0, pady=5, padx=5)
        self.label_min_value.grid(row=6, column=0, pady=5, padx=5)

        # Adding all elements with the grid, column 1
        self.entry_sn.grid(row=0, column=1, padx=5, pady=5)
        self.option_menu.grid(row=1, column=1, padx=5, pady=5)
        self.label_std_result.grid(row=3, column=1, pady=5, padx=5)
        self.label_mean_result.grid(row=4, column=1, pady=5, padx=5)
        self.label_max_value_result.grid(row=5, column=1, pady=5, padx=5)
        self.label_min_value_result.grid(row=6, column=1, pady=5, padx=5)
        self.check_std.grid(row=7, column=2, pady=5)
        self.check_mean.grid(row=7, column=3, pady=5)
        self.button_update.grid(row=7, column=4, pady=5)

        # Creating figure for the plot
        self.figure = Figure(figsize=(9, 6), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.ax.plot()

        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=2, columnspan=3, rowspan=7, pady=20)

        self.toolbar_frame = ctk.CTkFrame(self, height=20)
        self.toolbar_frame.grid(row=8, column=2, columnspan=3, pady=10)

    def plot_button(self):
        serial = self.entry_sn.get()
        chosen_parameter = self.option_menu.get()

        self.label_std_result.configure(text=f'{round(df[chosen_parameter].std(), 2)}')
        self.label_mean_result.configure(text=f'{round(df[chosen_parameter].mean(), 2)}')
        self.label_max_value_result.configure(text=f'{round(df[chosen_parameter].max(), 2)}')
        self.label_min_value_result.configure(text=f'{round(df[chosen_parameter].min(), 2)}')

        size = np.where(df['Serial'] == serial, 60, 30)
        color = np.where(df['Serial'] == serial, 'tab:red', 'tab:blue')
        self.ax.scatter(df['Date'], df[chosen_parameter], c=color, s=size, label=f'{chosen_parameter} of lasers')
        self.ax.set_title('Selected laser comparison')

        ylabel_map = {
            'Power': 'Power, [mW]',
            'Repetition rate': 'Repetition rate, [MHz]',
            'Wavelength': 'Wavelength, [nm]',
            'PER': 'PER, [dB]',
            'Threshold': 'Threshold, [mA]'
        }

        self.ax.set_ylabel(ylabel_map[chosen_parameter])
        self.ax.set_xlabel('Measurement date')

        if hasattr(self, 'canvas'):
            self.canvas.get_tk_widget().grid_forget()
            self.canvas.get_tk_widget().destroy()
        if hasattr(self, 'toolbar'):
            self.toolbar.grid_forget()
            self.toolbar.destroy()

        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=2, columnspan=3, rowspan=7, pady=20)

        self.toolbar = NavigationToolbar2Tk(self.canvas, self.toolbar_frame)
        self.toolbar.update()
        self.toolbar.pack(side='bottom', fill='x')
        #self.toolbar.grid(row=7, column=2, columnspan=3, pady=10)

    def update_plot(self):
        chosen_parameter = self.option_menu.get()
        std = df[chosen_parameter].std()
        mean = df[chosen_parameter].mean()

        std_tick = self.check_std.get()
        mean_tick = self.check_mean.get()

        if std_tick == 'on':
            self.ax.axhspan(mean - std, mean + std, facecolor='b', alpha=0.25, label='Standard deviation')
        if mean_tick == 'on':
            self.ax.axhline(y=mean, color='r', label='Mean')
        self.ax.legend()

        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=2, columnspan=3, rowspan=7, pady=20)

    def clear_data_plot(self):
        self.label_std_result.configure(text='0')
        self.label_mean_result.configure(text='0')
        self.label_max_value_result.configure(text='0')
        self.label_min_value_result.configure(text='0')
        self.ax.clear()
        self.canvas.draw()


# Create and run the app
if __name__ == "__main__":
    app = MainApp()
    app.mainloop()

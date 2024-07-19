import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import geopandas as gpd
import matplotlib.pyplot as plt

class ChinaMapApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Interactive China Map")
        self.geometry("800x600")

        # Load the GeoJSON file
        geojson_path = "china.geojson"
        self.china = gpd.read_file(geojson_path)

        # Create a figure and axis
        self.fig, self.ax = plt.subplots()
        self.current_province = None
        self.default_color = '#FF003F'  # Default color
        self.clicked_color = '#007FFF'     # Color for clicked province
        self.border_color = 'black'      # Border color
        self.border_width = 1          # Border width

        # Set the background color for the figure and axis
        self.fig.patch.set_facecolor('#FFFF00')  # Light red background for figure
        self.ax.set_facecolor('#FFFF00')  # Light red background for axis

        # Initialize a color column in the GeoDataFrame
        self.china['color'] = self.default_color

        # Plot the GeoDataFrame with border and colors
        self.china.plot(ax=self.ax, color=self.china['color'], edgecolor=self.border_color, linewidth=self.border_width)

        # Remove axis labels and ticks
        self.ax.set_axis_off()

        # Create a canvas to embed the plot
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)

        # Connect the event handler
        self.canvas.mpl_connect("button_press_event", self.on_click)

    def on_click(self, event):
        # Get the clicked point coordinates
        x, y = event.xdata, event.ydata
        if x is not None and y is not None:
            # Find the province that contains the clicked point
            point = gpd.points_from_xy([x], [y])
            province = self.china[self.china.contains(point[0])]
            if not province.empty:
                province_index = province.index[0]
                # If there's a previously clicked province, revert its color
                if self.current_province is not None:
                    self.china.loc[self.current_province, 'color'] = self.default_color
                # Update the clicked province's color
                self.china.loc[province_index, 'color'] = self.clicked_color
                self.current_province = province_index

                # Clear the previous plot
                self.ax.clear()
                # Replot the GeoDataFrame with updated colors and borders
                self.china.plot(ax=self.ax, color=self.china['color'], edgecolor=self.border_color, linewidth=self.border_width)

                # Set the background color for the axis and figure again
                self.ax.set_facecolor('#FFFF00')  # Light red background for axis
                self.fig.patch.set_facecolor('#FFFF00')  # Light red background for figure

                # Remove axis labels and ticks
                self.ax.set_axis_off()

                # Redraw the canvas
                self.canvas.draw()

                # Get the name of the province
                province_name = province.iloc[0]['NAME_1']  # Adjust this to the correct column name
                print(f"Clicked on: {province_name}")
                messagebox.showinfo("Province", f"You clicked on: {province_name}")

if __name__ == "__main__":
    app = ChinaMapApp()
    app.mainloop()





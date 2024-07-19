import tkinter as tk
from tkinter import ttk
from tkinterweb import HtmlFrame
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import geopandas as gpd
import matplotlib.pyplot as plt

class WikipediaViewer(tk.Toplevel):
    def __init__(self, master, title):
        super().__init__(master)
        self.title("Wikipedia Viewer")

        # Make the window maximized
        self.maximize_window()

        # Create and pack HtmlFrame for web content
        self.html_frame = HtmlFrame(self, horizontal_scrollbar="auto", vertical_scrollbar="auto")
        self.html_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Load the Wikipedia page
        url = f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}"
        self.html_frame.load_url(url)

    def maximize_window(self):
        # Get screen dimensions
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        # Set window size to screen dimensions
        self.geometry(f"{width}x{height}+0+0")

class MapTab(tk.Frame):
    def __init__(self, parent, geojson_path, title, map_color, bg_color, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.geojson_path = geojson_path
        self.title = title
        self.map_color = map_color
        self.bg_color = bg_color

        # Create a figure and axis
        self.fig, self.ax = plt.subplots()
        self.current_province = None
        self.default_color = map_color  # Default color
        self.clicked_color = '#007FFF'  # Color for clicked province
        self.border_color = 'black'  # Border color
        self.border_width = 1  # Border width

        # Set the background color for the figure and axis
        self.fig.patch.set_facecolor(bg_color)  # Background color for figure
        self.ax.set_facecolor(bg_color)  # Background color for axis

        # Load the GeoJSON file
        self.data = gpd.read_file(self.geojson_path)
        self.data['color'] = self.default_color

        # Plot the GeoDataFrame with border and colors
        self.data.plot(ax=self.ax, color=self.data['color'], edgecolor=self.border_color, linewidth=self.border_width)

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
            province = self.data[self.data.contains(point[0])]
            if not province.empty:
                province_index = province.index[0]
                # If there's a previously clicked province, revert its color
                if self.current_province is not None:
                    self.data.loc[self.current_province, 'color'] = self.default_color
                # Update the clicked province's color
                self.data.loc[province_index, 'color'] = self.clicked_color
                self.current_province = province_index

                # Clear the previous plot
                self.ax.clear()
                # Replot the GeoDataFrame with updated colors and borders
                self.data.plot(ax=self.ax, color=self.data['color'], edgecolor=self.border_color, linewidth=self.border_width)

                # Set the background color for the axis and figure again
                self.ax.set_facecolor(self.bg_color)  # Background color for axis
                self.fig.patch.set_facecolor(self.bg_color)  # Background color for figure

                # Remove axis labels and ticks
                self.ax.set_axis_off()

                # Redraw the canvas
                self.canvas.draw()

                # Get the name of the province
                province_name = province.iloc[0]['NAME_1']  # Adjust this to the correct column name
                print(f"Clicked on: {province_name}")

                # Open the WikipediaViewer with the selected province
                WikipediaViewer(self, province_name)

class MapApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Interactive Map Viewer")
        self.geometry("1200x800")
        
        self.style = ttk.Style()
        self.style.configure('TNotebook.Tab', font=('Helvetica', 14, 'bold'), padding=[10, 5])

        # Create a notebook (tabbed interface)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)

        # Add tabs for China, India, and USA maps with specific colors
        self.china_tab = MapTab(self.notebook, "china.geojson", "China", '#FF003F', '#FFFF00')
        self.india_tab = MapTab(self.notebook, "india.geojson", "India", '#FF9933', '#009E49')
        self.usa_tab = MapTab(self.notebook, "usa.geojson", "USA", '#0033A0', '#FF003F')

        # Add tabs to the notebook
        self.notebook.add(self.china_tab, text="China")
        self.notebook.add(self.india_tab, text="India")
        self.notebook.add(self.usa_tab, text="USA")

if __name__ == "__main__":
    app = MapApp()
    app.mainloop()



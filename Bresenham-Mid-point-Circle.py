import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
import numpy as np


def dda_line(x1, y1, x2, y2):
    points = []
    dx = x2 - x1
    dy = y2 - y1
    steps = abs(dx) if abs(dx) > abs(dy) else abs(dy)

    if steps == 0:
        return [(x1, y1)]

    x_increment = dx / steps
    y_increment = dy / steps

    x = x1
    y = y1

    for _ in range(steps + 1):
        points.append((round(x), round(y)))
        x += x_increment
        y += y_increment

    return points


def bresenham_line(x1, y1, x2, y2):
    points = []
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)

    x, y = x1, y1

    step_x = 1 if x2 > x1 else -1
    step_y = 1 if y2 > y1 else -1

    if dx > dy:
        p = 2 * dy - dx
        for _ in range(dx + 1):
            points.append((x, y))
            if p >= 0:
                y += step_y
                p -= 2 * dx
            x += step_x
            p += 2 * dy
    else:
        p = 2 * dx - dy
        for _ in range(dy + 1):
            points.append((x, y))
            if p >= 0:
                x += step_x
                p -= 2 * dy
            y += step_y
            p += 2 * dx

    return points


def midpoint_line(x1, y1, x2, y2):
    points = []
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)

    x, y = x1, y1

    step_x = 1 if x2 > x1 else -1
    step_y = 1 if y2 > y1 else -1

    if dx > dy:
        d = dy - dx/2
        for _ in range(dx + 1):
            points.append((x, y))
            if d > 0:
                y += step_y
                d -= dx
            x += step_x
            d += dy
    else:
        d = dx - dy/2
        for _ in range(dy + 1):
            points.append((x, y))
            if d > 0:
                x += step_x
                d -= dy
            y += step_y
            d += dx

    return points


def bresenham_circle(xc, yc, r):
    points = []
    x = 0
    y = r
    d = 3 - 2 * r

    while x <= y:
        # Add points in all octants
        points.extend([
            (xc + x, yc + y), (xc - x, yc + y),
            (xc + x, yc - y), (xc - x, yc - y),
            (xc + y, yc + x), (xc - y, yc + x),
            (xc + y, yc - x), (xc - y, yc - x)
        ])

        if d < 0:
            d = d + 4 * x + 6
        else:
            d = d + 4 * (x - y) + 10
            y -= 1
        x += 1

    return points


def midpoint_circle(xc, yc, r):
    points = []
    x = 0
    y = r
    p = 1 - r

    while x <= y:
        # Add points in all octants
        points.extend([
            (xc + x, yc + y), (xc - x, yc + y),
            (xc + x, yc - y), (xc - x, yc - y),
            (xc + y, yc + x), (xc - y, yc + x),
            (xc + y, yc - x), (xc - y, yc - x)
        ])

        if p < 0:
            p = p + 2 * x + 3
        else:
            p = p + 2 * (x - y) + 5
            y -= 1
        x += 1

    return points


def analyze_line_algorithms(x1, y1, x2, y2):
    """Analyze performance and accuracy of line drawing algorithms."""
    # Calculate slope
    if x2 - x1 != 0:
        slope = (y2 - y1) / (x2 - x1)
    else:
        slope = float('inf')

    results = {}
    algorithms = {
        'DDA': dda_line,
        'Bresenham': bresenham_line,
        'Midpoint': midpoint_line
    }

    # Perfect line points for comparison
    num_points = max(abs(x2 - x1), abs(y2 - y1)) + 1
    if slope != float('inf'):
        perfect_x = np.linspace(x1, x2, num_points)
        perfect_y = y1 + slope * (perfect_x - x1)
    else:
        perfect_y = np.linspace(y1, y2, num_points)
        perfect_x = np.full_like(perfect_y, x1)

    for name, algo in algorithms.items():
        # Measure execution time
        start_time = time.perf_counter()
        points = algo(x1, y1, x2, y2)
        execution_time = (time.perf_counter() - start_time) * 1000  # ms

        # Calculate accuracy metrics
        errors = []
        for px, py in points:
            # Find closest point on perfect line
            if slope != float('inf'):
                perfect_y_at_x = y1 + slope * (px - x1)
                error = abs(py - perfect_y_at_x)
            else:
                error = abs(px - x1)
            errors.append(error)

        results[name] = {
            'execution_time': execution_time,
            'num_points': len(points),
            'avg_error': np.mean(errors),
            'max_error': max(errors),
            'points': points
        }

    return slope, results


class LineAnalyzer:
    def __init__(self, root):
        self.root = root
        self.setup_gui()

    def setup_gui(self):
        # Create test cases for different slopes
        self.test_cases = [
            # (x1, y1, x2, y2, description)
            (0, 0, 100, 50, "Slope < 1"),
            (0, 0, 50, 100, "Slope > 1"),
            (0, 0, 100, 0, "Slope = 0"),
            (0, 0, 0, 100, "Vertical line"),
            (0, 0, 100, 100, "Slope = 1")
        ]

        # Create buttons for each test case
        for i, (x1, y1, x2, y2, desc) in enumerate(self.test_cases):
            ttk.Button(
                self.root,
                text=f"Test {desc}",
                command=lambda x1=x1, y1=y1, x2=x2, y2=y2: self.run_analysis(
                    x1, y1, x2, y2)
            ).grid(row=i, column=0, pady=5)

        # Results display
        self.results_text = tk.Text(self.root, height=20, width=60)
        self.results_text.grid(row=0, column=1, rowspan=len(self.test_cases))

        # Plot area
        self.fig, self.ax = plt.subplots(figsize=(10, 10))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().grid(row=0, column=2, rowspan=len(self.test_cases))

    def run_analysis(self, x1, y1, x2, y2):
        self.results_text.delete(1.0, tk.END)
        self.ax.clear()

        slope, results = analyze_line_algorithms(x1, y1, x2, y2)

        # Display results
        self.results_text.insert(tk.END, f"Slope: {slope:.2f}\n\n")

        colors = {'DDA': 'red', 'Bresenham': 'blue', 'Midpoint': 'green'}

        for algo_name, data in results.items():
            # Plot points
            x_coords, y_coords = zip(*data['points'])
            self.ax.scatter(x_coords, y_coords, color=colors[algo_name],
                            label=f"{algo_name}", alpha=0.6, s=20)

            # Display metrics
            self.results_text.insert(tk.END, f"{algo_name} Algorithm:\n")
            self.results_text.insert(
                tk.END, f"Execution time: {data['execution_time']:.4f} ms\n")
            self.results_text.insert(
                tk.END, f"Points generated: {data['num_points']}\n")
            self.results_text.insert(
                tk.END, f"Average error: {data['avg_error']:.4f}\n")
            self.results_text.insert(
                tk.END, f"Maximum error: {data['max_error']:.4f}\n\n")

        self.ax.grid(True)
        self.ax.legend()
        self.ax.set_aspect('equal')
        self.canvas.draw()


class LineDrawerGUI:
    def __init__(self, root):
        self.root = root

        # Control frame on the left
        self.control_frame = ttk.Frame(root, padding="10")
        self.control_frame.grid(row=0, column=0, sticky='nsew')

        # Input fields
        ttk.Label(self.control_frame, text="Start X:").grid(row=0, column=0)
        self.x1 = tk.StringVar(value="0")
        ttk.Entry(self.control_frame, textvariable=self.x1).grid(
            row=0, column=1)

        ttk.Label(self.control_frame, text="Start Y:").grid(row=1, column=0)
        self.y1 = tk.StringVar(value="0")
        ttk.Entry(self.control_frame, textvariable=self.y1).grid(
            row=1, column=1)

        ttk.Label(self.control_frame, text="End X:").grid(row=2, column=0)
        self.x2 = tk.StringVar(value="10")
        ttk.Entry(self.control_frame, textvariable=self.x2).grid(
            row=2, column=1)

        ttk.Label(self.control_frame, text="End Y:").grid(row=3, column=0)
        self.y2 = tk.StringVar(value="10")
        ttk.Entry(self.control_frame, textvariable=self.y2).grid(
            row=3, column=1)

        # Algorithm selection
        self.algorithm = tk.StringVar(value="all")
        ttk.Radiobutton(self.control_frame, text="DDA", variable=self.algorithm,
                        value="dda").grid(row=4, column=0)
        ttk.Radiobutton(self.control_frame, text="Bresenham", variable=self.algorithm,
                        value="bresenham").grid(row=4, column=1)
        ttk.Radiobutton(self.control_frame, text="Midpoint", variable=self.algorithm,
                        value="midpoint").grid(row=5, column=0)
        ttk.Radiobutton(self.control_frame, text="Compare All", variable=self.algorithm,
                        value="all").grid(row=5, column=1)

        # Draw button
        ttk.Button(self.control_frame, text="Draw", command=self.draw_line).grid(
            row=6, column=0, columnspan=2)

        # Results text area
        self.results_text = tk.Text(self.control_frame, height=10, width=40)
        self.results_text.grid(row=7, column=0, columnspan=2)

        # Create main frame with scrollbars for the chart area
        self.main_frame = ttk.Frame(root)
        self.main_frame.grid(row=0, column=1, sticky='nsew')

        # Setup scrollbars for the chart area
        self.scroll_canvas = tk.Canvas(self.main_frame)
        self.vsb = ttk.Scrollbar(
            self.main_frame, orient="vertical", command=self.scroll_canvas.yview)
        self.hsb = ttk.Scrollbar(
            self.main_frame, orient="horizontal", command=self.scroll_canvas.xview)
        self.scroll_canvas.configure(
            yscrollcommand=self.vsb.set, xscrollcommand=self.hsb.set)

        # Grid scrollbars and canvas
        self.vsb.grid(row=0, column=1, sticky='ns')
        self.hsb.grid(row=1, column=0, sticky='ew')
        self.scroll_canvas.grid(row=0, column=0, sticky='nsew')

        # Create frame inside canvas for the matplotlib figure
        self.chart_frame = ttk.Frame(self.scroll_canvas)
        self.canvas_frame = self.scroll_canvas.create_window(
            (0, 0), window=self.chart_frame, anchor='nw')

        # Plot setup - Create a figure with subplots
        self.fig = plt.Figure(figsize=(15, 5))
        self.plots = {
            'dda': self.fig.add_subplot(131),
            'bresenham': self.fig.add_subplot(132),
            'midpoint': self.fig.add_subplot(133)
        }
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.chart_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Configure grid weights
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=1)
        root.grid_rowconfigure(0, weight=1)

        # Bind events for scrolling
        self.chart_frame.bind('<Configure>', self.on_frame_configure)
        self.scroll_canvas.bind('<Configure>', self.on_canvas_configure)

    def on_frame_configure(self, event=None):
        """Reset the scroll region to encompass the inner frame"""
        self.scroll_canvas.configure(
            scrollregion=self.scroll_canvas.bbox("all"))

    def on_canvas_configure(self, event):
        """Update the inner frame's width to fill the canvas"""
        canvas_width = event.width
        self.scroll_canvas.itemconfig(self.canvas_frame, width=canvas_width)

    def draw_line(self):
        try:
            x1 = int(self.x1.get())
            y1 = int(self.y1.get())
            x2 = int(self.x2.get())
            y2 = int(self.y2.get())

            self.results_text.delete(1.0, tk.END)

            algorithms = {
                'dda': (dda_line, 'red', 'DDA'),
                'bresenham': (bresenham_line, 'blue', 'Bresenham'),
                'midpoint': (midpoint_line, 'green', 'Midpoint')
            }

            # Clear all subplots
            for ax in self.plots.values():
                ax.clear()

            if self.algorithm.get() == 'all':
                selected_algorithms = algorithms
            else:
                selected_algorithms = {
                    self.algorithm.get(): algorithms[self.algorithm.get()]}

            for algo_name, (algo_func, color, label) in selected_algorithms.items():
                start_time = time.perf_counter()
                points = algo_func(x1, y1, x2, y2)
                execution_time = (time.perf_counter() - start_time) * 1000

                # Plot points and lines on respective subplot
                x_coords, y_coords = zip(*points)
                ax = self.plots[algo_name]
                ax.scatter(x_coords, y_coords, color=color, s=10)
                ax.plot(x_coords, y_coords, color=color,
                        linestyle='-', alpha=0.5)
                ax.set_title(f"{label} Algorithm")
                ax.grid(True)
                ax.set_aspect('equal')

                # Display metrics
                self.results_text.insert(tk.END,
                                         f"{label} Algorithm:\n"
                                         f"Points generated: {len(points)}\n"
                                         f"Execution time: {execution_time:.4f} ms\n\n"
                                         )

            self.fig.tight_layout()
            self.canvas.draw()

        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values")


class CircleDrawerGUI:
    def __init__(self, root):
        self.root = root

        # Control frame on the left
        self.control_frame = ttk.Frame(root, padding="10")
        self.control_frame.grid(row=0, column=0, sticky='nsew')

        # Input fields
        ttk.Label(self.control_frame, text="Center X:").grid(row=0, column=0)
        self.xc = tk.StringVar(value="0")
        ttk.Entry(self.control_frame, textvariable=self.xc).grid(
            row=0, column=1)

        ttk.Label(self.control_frame, text="Center Y:").grid(row=1, column=0)
        self.yc = tk.StringVar(value="0")
        ttk.Entry(self.control_frame, textvariable=self.yc).grid(
            row=1, column=1)

        ttk.Label(self.control_frame, text="Radius:").grid(row=2, column=0)
        self.radius = tk.StringVar(value="10")
        ttk.Entry(self.control_frame, textvariable=self.radius).grid(
            row=2, column=1)

        # Algorithm selection
        self.algorithm = tk.StringVar(value="all")
        ttk.Radiobutton(self.control_frame, text="Bresenham", variable=self.algorithm,
                        value="bresenham").grid(row=3, column=0)
        ttk.Radiobutton(self.control_frame, text="Midpoint", variable=self.algorithm,
                        value="midpoint").grid(row=3, column=1)
        ttk.Radiobutton(self.control_frame, text="Compare Both", variable=self.algorithm,
                        value="all").grid(row=4, column=0, columnspan=2)

        # Draw button
        ttk.Button(self.control_frame, text="Draw", command=self.draw_circle).grid(
            row=5, column=0, columnspan=2)

        # Results text area
        self.results_text = tk.Text(self.control_frame, height=10, width=40)
        self.results_text.grid(row=6, column=0, columnspan=2)

        # Create main frame with scrollbars for the chart area
        self.main_frame = ttk.Frame(root)
        self.main_frame.grid(row=0, column=1, sticky='nsew')

        # Setup scrollbars for the chart area
        self.scroll_canvas = tk.Canvas(self.main_frame)
        self.vsb = ttk.Scrollbar(
            self.main_frame, orient="vertical", command=self.scroll_canvas.yview)
        self.hsb = ttk.Scrollbar(
            self.main_frame, orient="horizontal", command=self.scroll_canvas.xview)
        self.scroll_canvas.configure(
            yscrollcommand=self.vsb.set, xscrollcommand=self.hsb.set)

        # Grid scrollbars and canvas
        self.vsb.grid(row=0, column=1, sticky='ns')
        self.hsb.grid(row=1, column=0, sticky='ew')
        self.scroll_canvas.grid(row=0, column=0, sticky='nsew')

        # Create frame inside canvas for the matplotlib figure
        self.chart_frame = ttk.Frame(self.scroll_canvas)
        self.canvas_frame = self.scroll_canvas.create_window(
            (0, 0), window=self.chart_frame, anchor='nw')

        # Plot setup - Create a figure with subplots
        self.fig = plt.Figure(figsize=(10, 5))
        self.plots = {
            'bresenham': self.fig.add_subplot(121),
            'midpoint': self.fig.add_subplot(122)
        }
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.chart_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Configure grid weights
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=1)
        root.grid_rowconfigure(0, weight=1)

        # Bind events for scrolling
        self.chart_frame.bind('<Configure>', self.on_frame_configure)
        self.scroll_canvas.bind('<Configure>', self.on_canvas_configure)

    def on_frame_configure(self, event=None):
        """Reset the scroll region to encompass the inner frame"""
        self.scroll_canvas.configure(
            scrollregion=self.scroll_canvas.bbox("all"))

    def on_canvas_configure(self, event):
        """Update the inner frame's width to fill the canvas"""
        canvas_width = event.width
        self.scroll_canvas.itemconfig(self.canvas_frame, width=canvas_width)

    def draw_circle(self):
        try:
            xc = int(self.xc.get())
            yc = int(self.yc.get())
            r = int(self.radius.get())

            self.results_text.delete(1.0, tk.END)

            algorithms = {
                'bresenham': (bresenham_circle, 'blue', 'Bresenham'),
                'midpoint': (midpoint_circle, 'green', 'Midpoint')
            }

            # Clear all subplots
            for ax in self.plots.values():
                ax.clear()

            if self.algorithm.get() == 'all':
                selected_algorithms = algorithms
            else:
                selected_algorithms = {
                    self.algorithm.get(): algorithms[self.algorithm.get()]}

            # Draw perfect circle for comparison on each subplot
            theta = np.linspace(0, 2*np.pi, 1000)
            perfect_x = xc + r * np.cos(theta)
            perfect_y = yc + r * np.sin(theta)

            for algo_name, (algo_func, color, label) in selected_algorithms.items():
                ax = self.plots[algo_name]
                # Draw perfect circle
                ax.plot(perfect_x, perfect_y, 'r--',
                        label='Perfect Circle', alpha=0.5)

                start_time = time.perf_counter()
                points = algo_func(xc, yc, r)
                execution_time = (time.perf_counter() - start_time) * 1000

                # Plot points
                x_coords, y_coords = zip(*points)
                ax.scatter(x_coords, y_coords, color=color, label=label, s=10)
                ax.set_title(f"{label} Algorithm")
                ax.grid(True)
                ax.set_aspect('equal')
                ax.legend()

                # Calculate and display metrics
                errors = [abs(np.sqrt((x - xc)**2 + (y - yc)**2) - r)
                          for x, y in points]
                avg_error = np.mean(errors)
                max_error = np.max(errors)

                self.results_text.insert(tk.END,
                                         f"{label} Algorithm:\n"
                                         f"Points generated: {len(points)}\n"
                                         f"Execution time: {execution_time:.4f} ms\n"
                                         f"Average error: {avg_error:.4f} pixels\n"
                                         f"Maximum error: {max_error:.4f} pixels\n\n"
                                         )

            self.fig.tight_layout()
            self.canvas.draw()

        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Drawing Algorithms Comparison")

    # Configure the root window to be resizable
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    # Set a reasonable starting size for the window
    root.geometry("1200x800")

    notebook = ttk.Notebook(root)
    notebook.pack(fill='both', expand=True, padx=5, pady=5)

    # Add the analysis tab
    analysis_frame = ttk.Frame(notebook)
    notebook.add(analysis_frame, text="Algorithm Analysis")

    # Create the analyzer
    analyzer = LineAnalyzer(analysis_frame)

    # Original tabs
    line_frame = ttk.Frame(notebook)
    circle_frame = ttk.Frame(notebook)
    notebook.add(line_frame, text="Line Drawing")
    notebook.add(circle_frame, text="Circle Drawing")

    line_app = LineDrawerGUI(line_frame)
    circle_app = CircleDrawerGUI(circle_frame)

    root.mainloop()
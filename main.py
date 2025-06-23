# Main Python application logic for the interactive web app.
# This file contains the core application class and plotting logic.

import numpy as np
import plotly.graph_objects as go
import plotly.offline as pyo
from js import document, console
import json
from plot_utils import DataGenerator, PlotStyler


class PlotApp:
    # """Main application class handling the interactive plotting."""

    def __init__(self):
        self.data_generator = DataGenerator()
        self.plot_styler = PlotStyler()
        self.current_color_is_red = False

    async def initialize(self):
        # """Initialize the application and create the first plot."""
        console.log("Initializing PlotApp...")
        await self.create_initial_plot()

    async def create_initial_plot(self):
        # """Create the initial plot with default settings."""
        try:
            # Generate data using our Python utilities
            x_data, y_data = self.data_generator.generate_linear_data(-10, 10, 0.5)

            # Create the plot
            fig = self.create_plotly_figure(x_data, y_data, is_red=False)

            # Convert to HTML and display
            plot_html = pyo.plot(fig, output_type="div", include_plotlyjs=False)

            # Inject Plotly.js if not already loaded
            await self.ensure_plotly_loaded()

            # Update the plot container
            plot_container = document.getElementById("plot-container")
            plot_container.innerHTML = plot_html

            console.log("Initial plot created successfully!")

        except Exception as e:
            console.error(f"Error creating initial plot: {e}")
            raise e

    def create_plotly_figure(self, x_data, y_data, is_red=False):
        # """Create a Plotly figure with the given data and color scheme."""

        # Use our Python styling utilities
        colors = self.plot_styler.get_color_scheme(is_red)

        trace = go.Scatter(
            x=x_data,
            y=y_data,
            mode="lines+markers",
            name="y = x",
            line=dict(color=colors["line"], width=3),
            marker=dict(color=colors["marker"], size=6, opacity=0.8),
        )

        # Create layout with Python-generated styling
        layout = self.plot_styler.create_layout(
            title=f"Linear Function: y = x {'(RED)' if is_red else '(BLUE)'}",
            is_red=is_red,
        )

        fig = go.Figure(data=[trace], layout=layout)
        return fig

    def update_plot_color(self, is_red):
        # """Update the plot color based on checkbox state."""
        try:
            console.log(f"Updating plot color: is_red = {is_red}")
            self.current_color_is_red = is_red

            # Regenerate data (in case we want to modify it based on color)
            x_data, y_data = self.data_generator.generate_linear_data(-10, 10, 0.5)

            # Create new figure with updated colors
            fig = self.create_plotly_figure(x_data, y_data, is_red)

            # Update the plot
            plot_html = pyo.plot(fig, output_type="div", include_plotlyjs=False)
            plot_container = document.getElementById("plot-container")
            plot_container.innerHTML = plot_html

            console.log("Plot color updated successfully!")

        except Exception as e:
            console.error(f"Error updating plot color: {e}")

    async def ensure_plotly_loaded(self):
        # """Ensure Plotly.js is loaded for rendering."""
        # Inject Plotly.js CDN if not already present
        script_exists = document.querySelector('script[src*="plotly"]')
        if not script_exists:
            console.log("Loading Plotly.js...")
            script = document.createElement("script")
            script.src = (
                "https://cdnjs.cloudflare.com/ajax/libs/plotly.js/2.26.0/plotly.min.js"
            )
            document.head.appendChild(script)

            # Wait for script to load
            await self.wait_for_plotly()

    async def wait_for_plotly(self):
        # """Wait for Plotly to be available."""
        import asyncio

        max_attempts = 50
        for attempt in range(max_attempts):
            try:
                # Check if Plotly is available in the global scope
                if hasattr(document.defaultView, "Plotly"):
                    console.log("Plotly.js loaded successfully!")
                    return
            except:
                pass
            await asyncio.sleep(0.1)

        console.log("Warning: Plotly.js may not have loaded properly")


# Helper functions for data processing
def calculate_polynomial(x_values, coefficients):
    # """Calculate polynomial values for given x values and coefficients."""
    return np.polyval(coefficients, x_values)


def generate_sample_data(func_type="linear", n_points=50):
    # """Generate sample data for different function types."""
    x = np.linspace(-10, 10, n_points)

    if func_type == "linear":
        y = x  # y = x
    else:
        y = x  # default to linear

    return x.tolist(), y.tolist()

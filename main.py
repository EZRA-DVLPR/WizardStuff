import matplotlib.pyplot as plt
import io
import base64
from js import document
from pyodide.ffi import create_proxy

# Update status
status_elem = document.getElementById("status")
status_elem.innerHTML = "Python loaded! Creating plot..."

# Simple data
x = [1, 2, 3]
y = [1, 2, 3]


def create_display_plot(is_red):
    """Create and display the plot with specified color"""
    # Clear any existing plot
    plt.clf()

    # Create the plot
    plt.figure(figsize=(8, 6))
    if is_red:
        plt.plot(x, y, "ro-", linewidth=2, markersize=8, label="Red Line")
    else:
        plt.plot(x, y, "bo-", linewidth=2, markersize=8, label="Blue Line")
    plt.xlabel("X values")
    plt.ylabel("Y values")
    plt.title(f'Simple Plot: x=[1,2,3], y=[1,2,3] {"(RED)" if is_red else "(BLUE)"}')
    plt.grid(True, alpha=0.3)
    plt.legend()

    # Convert plot to image
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png", dpi=100, bbox_inches="tight")
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode()
    plt.close()

    # Display the plot
    plot_container = document.getElementById("plot-container")
    plot_container.innerHTML = f'<img src="data:image/png;base64,{image_base64}" style="width:100%; height:auto;">'


def handle_color_change(event):
    """Called when checkbox state changes"""
    checkbox = document.getElementById("color-checkbox")
    is_red = checkbox.checked
    print(f"Checkbox changed: {is_red}")
    create_display_plot(is_red)

    # Update status
    status_elem = document.getElementById("status")
    status_elem.innerHTML = f"✅ Plot updated! Color: {'RED' if is_red else 'BLUE'}"


# Create a JavaScript-compatible proxy for the event handler
color_change_proxy = create_proxy(handle_color_change)

# Add event listener to checkbox
checkbox = document.getElementById("color-checkbox")
checkbox.addEventListener("change", color_change_proxy)

# Create initial plot (blue, since checkbox starts unchecked)
create_display_plot(False)

# Update status
status_elem.innerHTML = "✅ Plot created successfully! Use checkbox to change color."

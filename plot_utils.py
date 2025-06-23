# Python utilities for data generation and plot styling.
# This module contains reusable Python classes for creating interactive plots.

import numpy as np
from typing import Tuple, List, Dict, Any

class DataGenerator:
    """Handles all data generation logic in pure Python."""
    
    def __init__(self):
        self.default_range = (-10, 10)
        self.default_step = 0.5
    
    def generate_linear_data(self, start: float = -10, end: float = 10, step: float = 0.5) -> Tuple[List[float], List[float]]:
        """Generate data points for y = x function."""
        x_values = np.arange(start, end + step, step)
        y_values = x_values  # y = x
        return x_values.tolist(), y_values.tolist()
    
    def generate_quadratic_data(self, start: float = -10, end: float = 10, step: float = 0.5) -> Tuple[List[float], List[float]]:
        """Generate data points for y = x² function."""
        x_values = np.arange(start, end + step, step)
        y_values = x_values ** 2
        return x_values.tolist(), y_values.tolist()
    
    def generate_cubic_data(self, start: float = -10, end: float = 10, step: float = 0.5) -> Tuple[List[float], List[float]]:
        """Generate data points for y = x³ function."""
        x_values = np.arange(start, end + step, step)
        y_values = x_values ** 3
        return x_values.tolist(), y_values.tolist()
    
    def generate_sine_data(self, start: float = -10, end: float = 10, step: float = 0.1) -> Tuple[List[float], List[float]]:
        """Generate data points for y = sin(x) function."""
        x_values = np.arange(start, end + step, step)
        y_values = np.sin(x_values)
        return x_values.tolist(), y_values.tolist()
    
    def generate_custom_function(self, func, start: float = -10, end: float = 10, step: float = 0.5) -> Tuple[List[float], List[float]]:
        """Generate data points for a custom function."""
        x_values = np.arange(start, end + step, step)
        y_values = [func(x) for x in x_values]
        return x_values.tolist(), y_values

class PlotStyler:
    """Handles all plot styling and theming in pure Python."""
    
    def __init__(self):
        self.color_schemes = {
            'blue': {
                'line': '#3498db',
                'marker': '#2980b9',
                'background': '#f8f9fa'
            },
            'red': {
                'line': '#e74c3c',
                'marker': '#c0392b', 
                'background': '#fef5f5'
            }
        }
        
        self.default_layout_config = {
            'font_family': 'Segoe UI, sans-serif',
            'plot_bgcolor': '#fafafa',
            'paper_bgcolor': 'white',
            'grid_color': '#ddd',
            'zeroline_color': '#999'
        }
    
    def get_color_scheme(self, is_red: bool = False) -> Dict[str, str]:
        """Get color scheme based on the current state."""
        return self.color_schemes['red'] if is_red else self.color_schemes['blue']
    
    def create_layout(self, title: str, is_red: bool = False) -> Dict[str, Any]:
        """Create a Plotly layout configuration."""
        colors = self.get_color_scheme(is_red)
        
        layout = {
            'title': {
                'text': title,
                'font': {'size': 20, 'color': '#333'},
                'x': 0.5  # Center the title
            },
            'xaxis': {
                'title': 'X values',
                'gridcolor': self.default_layout_config['grid_color'],
                'zerolinecolor': self.default_layout_config['zeroline_color'],
                'showgrid': True,
                'zeroline': True
            },
            'yaxis': {
                'title': 'Y values',
                'gridcolor': self.default_layout_config['grid_color'],
                'zerolinecolor': self.default_layout_config['zeroline_color'],
                'showgrid': True,
                'zeroline': True
            },
            'plot_bgcolor': colors['background'],
            'paper_bgcolor': self.default_layout_config['paper_bgcolor'],
            'font': {'family': self.default_layout_config['font_family']},
            'margin': {'t': 60, 'r': 20, 'b': 60, 'l': 60},
            'hovermode': 'closest'
        }
        
        return layout
    
    def create_trace_config(self, name: str, is_red: bool = False) -> Dict[str, Any]:
        """Create trace configuration for Plotly."""
        colors = self.get_color_scheme(is_red)
        
        trace_config = {
            'mode': 'lines+markers',
            'name': name,
            'line': {
                'color': colors['line'],
                'width': 3
            },
            'marker': {
                'color': colors['marker'],
                'size': 6,
                'opacity': 0.8
            },
            'hovertemplate': '<b>%{fullData.name}</b><br>X: %{x}<br>Y: %{y}<extra></extra>'
        }
        
        return trace_config

class MathUtils:
    """Mathematical utility functions for data processing."""
    
    @staticmethod
    def linspace(start: float, stop: float, num: int = 50) -> np.ndarray:
        """Python equivalent of numpy linspace."""
        return np.linspace(start, stop, num)
    
    @staticmethod
    def arange(start: float, stop: float, step: float = 1.0) -> np.ndarray:
        """Python equivalent of numpy arange."""
        return np.arange(start, stop, step)
    
    @staticmethod
    def apply_function(x_values: List[float], func_name: str) -> List[float]:
        """Apply a mathematical function to x values."""
        x_array = np.array(x_values)
        
        functions = {
            'linear': lambda x: x,
            'quadratic': lambda x: x**2,
            'cubic': lambda x: x**3,
            'sine': lambda x: np.sin(x),
            'cosine': lambda x: np.cos(x),
            'exponential': lambda x: np.exp(x),
            'logarithmic': lambda x: np.log(np.abs(x) + 1e-10)  # Avoid log(0)
        }
        
        if func_name in functions:
            return functions[func_name](x_array).tolist()
        else:
            return x_values  # Return original if function not found

# Utility functions for statistical operations
def calculate_statistics(data: List[float]) -> Dict[str, float]:
    """Calculate basic statistics for a dataset."""
    np_data = np.array(data)
    return {
        'mean': float(np.mean(np_data)),
        'median': float(np.median(np_data)),
        'std': float(np.std(np_data)),
        'min': float(np.min(np_data)),
        'max': float(np.max(np_data))
    }

def smooth_data(x_data: List[float], y_data: List[float], window_size: int = 5) -> Tuple[List[float], List[float]]:
    """Apply smoothing to data using a moving average."""
    if len(y_data) < window_size:
        return x_data, y_data
    
    # Simple moving average
    smoothed_y = []
    for i in range(len(y_data)):
        start_idx = max(0, i - window_size // 2)
        end_idx = min(len(y_data), i + window_size // 2 + 1)
        smoothed_y.append(np.mean(y_data[start_idx:end_idx]))
    
    return x_data, smoothed_y

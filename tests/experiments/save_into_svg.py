import matplotlib.pyplot as plt
import numpy as np
import pltsave
import json
import zlib
import base64
import io


class NumpyEncoder(json.JSONEncoder):
    """Custom JSON encoder for numpy data types."""

    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.bool_):
            return bool(obj)
        return super().default(obj)


def create_sin_figure():
    """Create a simple matplotlib figure with sin oscillations."""
    fig, ax = plt.subplots(figsize=(10, 6))

    # Generate sin oscillation data
    x = np.linspace(0, 4 * np.pi, 200)
    y1 = np.sin(x)
    y2 = np.sin(2 * x) * 0.5
    y3 = np.sin(0.5 * x) * 1.5

    # Plot multiple sin waves
    ax.plot(x, y1, label="sin(x)", linewidth=2, color="blue")
    ax.plot(x, y2, label="0.5*sin(2x)", linewidth=2, color="red")
    ax.plot(x, y3, label="1.5*sin(0.5x)", linewidth=2, color="green")

    # Styling
    ax.set_title("Sin Oscillations", fontsize=16)
    ax.set_xlabel("x", fontsize=12)
    ax.set_ylabel("y", fontsize=12)
    ax.legend()
    ax.grid(True, alpha=0.3)

    return fig


def get_compressed_figure_data(fig):
    """
    Convert a matplotlib figure to a compressed string using pltsave and custom compression.

    Args:
        fig: matplotlib figure object

    Returns:
        str: Compressed string representation that looks like random symbols
    """
    # Use pltsave to dump the figure into a structured format
    figure_info = pltsave.dumps(fig)

    # Convert to dictionary
    figure_dict = figure_info.to_dict()

    # Convert dict to JSON string using custom encoder for numpy arrays
    json_string = json.dumps(figure_dict, separators=(",", ":"), cls=NumpyEncoder)

    # Compress the JSON string using zlib
    compressed_bytes = zlib.compress(json_string.encode("utf-8"))

    # Encode to base64 to get a string that looks like random symbols
    compressed_string = base64.b64encode(compressed_bytes).decode("ascii")

    return compressed_string


def save_figure_to_svg_with_metadata(fig, filename="figure_with_metadata.svg"):
    """
    Save a matplotlib figure as SVG with embedded compressed pltsave data as metadata.

    Args:
        fig: matplotlib figure object
        filename: output SVG filename

    Returns:
        str: Path to the saved SVG file
    """
    # Get compressed figure data
    compressed_data = get_compressed_figure_data(fig)

    # Save figure to SVG in memory first
    svg_buffer = io.StringIO()
    fig.savefig(svg_buffer, format="svg")
    svg_content = svg_buffer.getvalue()
    svg_buffer.close()

    # Find the closing </svg> tag and insert metadata before it
    closing_tag = "</svg>"
    closing_index = svg_content.rfind(closing_tag)

    if closing_index == -1:
        raise ValueError("Could not find closing </svg> tag in generated SVG")

    # Create metadata XML
    metadata = f"""
<metadata>
    <pltsave:data encoding="base64" compression="gzip">{compressed_data}</pltsave:data>
</metadata>
"""

    # Insert metadata before closing </svg> tag
    modified_svg = svg_content[:closing_index] + metadata + svg_content[closing_index:]

    # Write to file
    with open(filename, "w", encoding="utf-8") as f:
        f.write(modified_svg)

    return filename


if __name__ == "__main__":
    # Create the sin oscillation figure
    fig = create_sin_figure()

    # Save figure to SVG with embedded metadata
    svg_filename = save_figure_to_svg_with_metadata(
        fig, "sin_oscillations_with_metadata.svg"
    )

    # Output the compressed string for verification
    compressed_data = get_compressed_figure_data(fig)
    print("Compressed figure data:")
    print(compressed_data)
    print(f"\nSVG file saved as: {svg_filename}")

    # Close the figure to free memory
    plt.close(fig)

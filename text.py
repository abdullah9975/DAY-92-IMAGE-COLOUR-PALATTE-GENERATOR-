# Define a dictionary mapping hex values to color names
COLOR_NAMES = {
    "#FF0000": 'Red',
    "#00FF00": 'Green',
    "#0000FF": 'Blue',
    # Add more color mappings as needed
}


def get_color_name(hex_value):
    # Convert hex value to uppercase
    hex_value = hex_value.upper()

    # Check if the hex value is in the dictionary
    if hex_value in COLOR_NAMES:
        return COLOR_NAMES[hex_value]
    else:
        return "Unknown"  # Return "Unknown" if the color is not found in the dictionary


# Example usage:
hex_value = "#55493B"  # Red color
color_name = get_color_name(hex_value)
print(color_name)  # Output: 'Red'

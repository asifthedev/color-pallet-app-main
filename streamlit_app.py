import streamlit as st

# Path to the HTML file
html_file_path = "index.html"

# Load the HTML content
with open(html_file_path, "r") as file:
    html_content = file.read()

# Find the colors array in the HTML file
start_index = html_content.find("const colors = [")
end_index = html_content.find("];", start_index)

if start_index != -1:
    colors_array_str = html_content[start_index + len("const colors = ["):end_index].strip()
    colors_array = [color.strip().strip('"') for color in colors_array_str.split(",")]
else:
    colors_array_str = ""
    colors_array = []

# Streamlit interface
st.title("Color Palette Manager")

# Color input for adding
color_value = st.color_picker("Pick a color")
st.write(f"Selected color: {color_value}")

# Button to add color to the colors array
if st.button("Add Color to Palette"):
    # Update the colors array by adding the new color
    colors_array.append(color_value)

    # Convert the array back to a string
    new_colors_array_str = ', '.join(f'"{color}"' for color in colors_array)

    # Replace the old colors array in the HTML content
    updated_html_content = (
        html_content[:start_index + len("const colors = [")]
        + new_colors_array_str
        + html_content[end_index:]
    )

    # Write the updated content back to the HTML file
    with open(html_file_path, "w") as file:
        file.write(updated_html_content)

    st.success("Color added to the palette successfully!")

# Option to remove a color
st.subheader("Remove a Color from Palette")
color_to_remove = st.selectbox("Select a color to remove", colors_array)

confirm_removal = st.checkbox("Confirm removal")

if st.button("Remove Selected Color"):
    if confirm_removal:
        # Remove the color from the last occurrence in the array
        if color_to_remove in colors_array:
            colors_array.reverse()  # Reverse to find the last occurrence
            colors_array.remove(color_to_remove)
            colors_array.reverse()  # Reverse back to original order

            # Convert the array back to a string
            new_colors_array_str = ', '.join(f'"{color}"' for color in colors_array)

            # Replace the old colors array in the HTML content
            updated_html_content = (
                html_content[:start_index + len("const colors = [")]
                + new_colors_array_str
                + html_content[end_index:]
            )

            # Write the updated content back to the HTML file
            with open(html_file_path, "w") as file:
                file.write(updated_html_content)

            st.success("Color removed from the palette successfully!")
        else:
            st.error("Color not found in the array.")
    else:
        st.info("Please confirm removal before proceeding.")

# Display the current colors array (for reference)
st.subheader("Current Colors Array")
st.code(', '.join(f'"{color}"' for color in colors_array))

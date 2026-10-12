import os
import numpy as np
from flask import Flask, render_template, request, send_from_directory
from PIL import Image
from sklearn.cluster import KMeans
from matplotlib.colors import to_hex

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def get_most_common_colors(image_path, num_colors=10):
    img = Image.open(image_path)
    img = img.convert('RGB')
    np_img = np.array(img)
    height, width, _ = np_img.shape
    colors = np_img.reshape(-1, 3)

    # Perform K-means clustering to find dominant colors
    kmeans = KMeans(n_clusters=num_colors)
    kmeans.fit(colors)
    centroids = kmeans.cluster_centers_.astype(int)

    most_common = []
    for color_rgb in centroids:
        hex_color = rgb_to_hex(color_rgb)
        color_name = get_color_name(hex_color)
        most_common.append((color_name, hex_color, color_rgb, 0))  # Count not calculated in K-means

    return most_common

def rgb_to_hex(rgb):
    return to_hex(tuple(rgb / 255))

def get_color_name(hex_color):
    # Here you can implement a method to map the hex color to a color name
    color_name = "Unknown"
    return color_name

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('index.html', message='No file part')
        file = request.files['file']
        if file.filename == '':
            return render_template('index.html', message='No selected file')

        color_count = int(request.form['colorCount'])  # Get the selected number of colors
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        most_common_colors = get_most_common_colors(file_path, num_colors=color_count)
        return render_template('result.html', colors=most_common_colors, image_filename=file.filename)

    return render_template('index.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)

# import os
# import numpy as np
# import webcolors
# from colour import Color
# from flask import Flask, render_template, request, send_from_directory
# from PIL import Image
# from collections import Counter
# from sklearn.cluster import KMeans
# from colour import Color
# from colorthief import ColorNameLookup
#
#
# app = Flask(__name__)
#
# UPLOAD_FOLDER = 'uploads'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#
# # Define a dictionary to map RGB tuples to color names
# COLOR_NAMES = {
#     (255, 0, 0): 'Red',
#     (0, 255, 0): 'Green',
#     (0, 0, 255): 'Blue',
#     # Add more color mappings as needed
# }
#
# def get_most_common_colors(image_path, num_colors=10):
#     img = Image.open(image_path)
#     img = img.convert('RGB')
#     np_img = np.array(img)
#     height, width, _ = np_img.shape
#     colors = np_img.reshape(-1, 3)
#
#     # Perform K-means clustering to find dominant colors
#     kmeans = KMeans(n_clusters=num_colors)
#     kmeans.fit(colors)
#     centroids = kmeans.cluster_centers_.astype(int)
#
#     most_common = []
#     for color_rgb in centroids:
#         color_name = get_color_name(tuple(color_rgb))  # Convert NumPy array to tuple
#         hex_color = rgb_to_hex(tuple(color_rgb))  # Convert NumPy array to tuple
#         most_common.append((color_name, hex_color, color_rgb, 0))  # Count not calculated in K-means
#
#     return most_common
#
#
# def rgb_to_hex(rgb):
#     return '#{:02x}{:02x}{:02x}'.format(*rgb)
#
#
# # Create an instance of ColorNameLookup
# color_lookup = ColorNameLookup()
#
# def get_color_name(rgb_tuple):
#     # Convert RGB tuple to hex string
#     hex_color = '#{:02x}{:02x}{:02x}'.format(*rgb_tuple)
#
#     # Get color name using ColorNameLookup
#     color_name = color_lookup.lookup(hex_color)
#
#     return color_name
#
#
#
# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         if 'file' not in request.files:
#             return render_template('index.html', message='No file part')
#         file = request.files['file']
#         if file.filename == '':
#             return render_template('index.html', message='No selected file')
#
#         color_count = int(request.form['colorCount'])  # Get the selected number of colors
#         file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
#         file.save(file_path)
#         most_common_colors = get_most_common_colors(file_path, num_colors=color_count)
#         return render_template('result.html', colors=most_common_colors, image_filename=file.filename)
#
#     return render_template('index.html')
#
# @app.route('/uploads/<filename>')
# def uploaded_file(filename):
#     return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
#
# if __name__ == '__main__':
#     app.run(debug=True)

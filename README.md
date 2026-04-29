# 🌟 Image Processing Toolbox & GUI Dashboard

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green)
![NumPy](https://img.shields.io/badge/NumPy-Data%20Science-blueviolet)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-orange)

A comprehensive desktop application designed to perform a wide range of standard and advanced Image Processing operations. This project features a clean, user-friendly Graphical User Interface (GUI) and follows the "Separation of Concerns" architectural principle for clean and maintainable code.

## 🚀 Features & Implemented Tasks

The application allows users to upload images and apply the following operations, displaying both the input and the result side-by-side using `matplotlib` subplots:

1. **Point Operations:** Addition, Subtraction, Division, and Image Complement (Negative).
2. **Color Image Operations:** Lighting modification, Channel Swapping (R to G), and Channel Elimination (Removing Red).
3. **Image Histogram:** Histogram Stretching and Histogram Equalization (with histogram plots).
4. **Neighborhood Processing:** Linear filters (Average, Laplacian) and Non-linear filters (Maximum, Minimum, Median, Mode).
5. **Image Restoration:** Noise reduction for Salt & Pepper (using Average, Median, Outlier methods) and Gaussian Noise (using Image Averaging).
6. **Image Segmentation:** Basic Global Thresholding, Otsu's Automatic Thresholding, and Adaptive Thresholding.
7. **Edge Detection:** Sobel Operator (X and Y magnitude).
8. **Mathematical Morphology:** Dilation, Erosion, Opening, Internal/External Boundary Extraction, and Morphological Gradient.

## 🏗️ Project Architecture (Clean Code)

The project is heavily refactored to separate the User Interface from the core mathematical logic:

* `main.py`: The entry point that initializes the Tkinter dashboard, sidebar, and workspace.
* `image_processing.py`: The core logic file. Contains pure Python, OpenCV, and NumPy functions. No GUI code exists here.
* `tasks_gui.py`: Manages the state and specific UI components (buttons, upload logic) for each of the 8 tasks.
* `ui_helpers.py`: Utility functions for clearing the workspace and embedding Matplotlib figures into Tkinter.

## 🛠️ Technology Stack

* **Python:** Core programming language.
* **OpenCV (`cv2`):** Core computer vision library used for image manipulation.
* **NumPy:** Matrix operations and pixel-level mathematical calculations.
* **SciPy:** Used for complex statistical operations (e.g., Mode filter logic).
* **Matplotlib:** Used for generating scientific subplots and histograms.
* **Tkinter:** Native Python library used to build the dark-themed desktop dashboard.

## 💻 How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/Image-Processing-Toolbox.git
   cd Image-Processing-Toolbox
   ```

2. **Install the required dependencies:**
   ```bash
   pip install opencv-python numpy matplotlib scipy
   ```

3. **Run the application:**  
   ```bash
   python main.py
   ```

## 👩‍💻 Author
**Mariam Ahmed**

Software Engineer | Machine Learning & Computer Vision Developer

[LinkedIn](www.linkedin.com/in/mariam-ahmed-ai) | [GitHub](https://github.com/mariamahmed10395-boop)
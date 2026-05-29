import tkinter as tk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt
import cv2
import numpy as np
import image_processing as ip
import ui_helpers as ui
import os

# Global Application State
class AppState:
    current_paths = {"path1": "", "path2": ""}

def upload_image(key="path1", label=None, on_upload_callback=None):
    path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp")])
    if path:
        AppState.current_paths[key] = path
        if label:
            filename = os.path.basename(path)
            label.config(text=f"{filename} ✔️", fg="#2ecc71")
        if on_upload_callback:
            on_upload_callback()

def clear_images(labels=None, on_clear_callback=None):
    AppState.current_paths = {"path1": "", "path2": ""}
    if labels:
        for lbl in labels:
            lbl.config(text="No image selected", fg="#e74c3c")
    if on_clear_callback:
        on_clear_callback()

def draw_sources(workspace):
    ui.clear_workspace(workspace)
    p1 = AppState.current_paths["path1"]
    p2 = AppState.current_paths["path2"]
    
    if not p1 and not p2:
        # Streamlit inspired welcome layout
        frame = tk.Frame(workspace, bg="#121214")
        frame.pack(expand=True)
        tk.Label(frame, text="🔹 IMAGE PROCESSING STUDIO 🔹", bg="#121214", fg="#00E5FF", font=("Segoe UI", 26, "bold")).pack(pady=15)
        
        welcome_text = (
            "Welcome! Awaiting image processing...\n\n"
            "The parameters and second image visibility adjust dynamically.\n"
            "For Brightness, only one image is needed."
        )
        tk.Label(
            frame, 
            text=welcome_text, 
            bg="#121214", 
            fg="#8E9AA6", 
            font=("Segoe UI", 13), 
            justify="center",
            pady=10
        ).pack()
        return

    # Visualizing current active source images
    fig = plt.figure(figsize=(10, 5), facecolor="white")
    if p1 and p2:
        img1 = cv2.imread(p1)
        img2 = cv2.imread(p2)
        if img1 is not None:
            img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
            plt.subplot(1, 2, 1)
            plt.imshow(img1)
            plt.title("Primary Image (Image 1)", fontweight='bold')
            plt.axis('off')
        if img2 is not None:
            img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
            plt.subplot(1, 2, 2)
            plt.imshow(img2)
            plt.title("Secondary Image (Image 2)", fontweight='bold')
            plt.axis('off')
    elif p1:
        img1 = cv2.imread(p1)
        if img1 is not None:
            img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
            plt.imshow(img1)
            plt.title("Primary Image Active", fontweight='bold')
            plt.axis('off')
    elif p2:
        img2 = cv2.imread(p2)
        if img2 is not None:
            img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
            plt.imshow(img2)
            plt.title("Secondary Image Active", fontweight='bold')
            plt.axis('off')
            
    plt.tight_layout()
    ui.display_in_workspace(fig, workspace)

# --- Sub-Filter Functions & Logics ---
from scipy import stats

def mode_filter_logic(img, size=5):
    padded_img = np.pad(img, size//2, mode='edge')
    result = np.zeros_like(img)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            region = padded_img[i:i+size, j:j+size]
            result[i, j] = stats.mode(region, axis=None).mode
    return result

def run_operation(category, op_name, workspace, slider_val=0, back_callback=None):
    p1 = AppState.current_paths["path1"]
    p2 = AppState.current_paths["path2"]

    # Validations
    if not p1:
        messagebox.showerror("Error", "Please upload the Primary Image (Image 1) first!")
        return

    requires_second_img = (category == "Point Operations" and op_name in ["Addition", "Subtraction", "Division"])
    if requires_second_img and not p2:
        messagebox.showerror("Error", f"'{op_name}' requires both Image 1 and Image 2!")
        return

    try:
        if category == "Point Operations":
            if op_name == "Brightness":
                img = cv2.imread(p1)
                if img is None: raise ValueError("Failed to load image.")
                img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                res = cv2.convertScaleAbs(img_rgb, beta=slider_val)
                
                fig = plt.figure(figsize=(10, 5), facecolor="white")
                plt.subplot(1, 2, 1); plt.imshow(img_rgb); plt.title("Original Image"); plt.axis('off')
                plt.subplot(1, 2, 2); plt.imshow(res); plt.title(f"Brightness Adjusted ({slider_val})"); plt.axis('off')
                plt.tight_layout()
                
            elif op_name in ["Addition", "Subtraction", "Division"]:
                x1 = cv2.imread(p1, 0)
                x2 = cv2.imread(p2, 0)
                if x1 is None or x2 is None: raise ValueError("Failed to load images.")
                x1 = cv2.resize(x1, (400, 400))
                x2 = cv2.resize(x2, (400, 400))
                
                if op_name == "Addition":
                    y = cv2.add(x1, x2)
                    title = "Addition (x1 + x2)"
                elif op_name == "Subtraction":
                    y = cv2.subtract(x1, x2)
                    title = "Subtraction (x1 - x2)"
                else:
                    with np.errstate(divide='ignore', invalid='ignore'):
                        y = np.divide(x1, np.where(x2 == 0, 1, x2))
                    y = np.clip(y, 0, 255).astype(np.uint8)
                    title = "Division (x1 / x2)"
                
                fig = plt.figure(figsize=(12, 5), facecolor="white")
                plt.subplot(1, 3, 1); plt.imshow(x1, cmap='gray'); plt.title("Image 1"); plt.axis('off')
                plt.subplot(1, 3, 2); plt.imshow(x2, cmap='gray'); plt.title("Image 2"); plt.axis('off')
                plt.subplot(1, 3, 3); plt.imshow(y, cmap='gray'); plt.title(title); plt.axis('off')
                plt.tight_layout()
                
            elif op_name == "Complement":
                x1 = cv2.imread(p1, 0)
                if x1 is None: raise ValueError("Failed to load image.")
                y = 255 - x1
                fig = plt.figure(figsize=(10, 5), facecolor="white")
                plt.subplot(1, 2, 1); plt.imshow(x1, cmap='gray'); plt.title("Original"); plt.axis('off')
                plt.subplot(1, 2, 2); plt.imshow(y, cmap='gray'); plt.title("Complement (255 - x1)"); plt.axis('off')
                plt.tight_layout()

        elif category == "Color Operations":
            img = cv2.imread(p1)
            if img is None: raise ValueError("Failed to load color image.")
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            r, g, b = cv2.split(img_rgb)
            
            if op_name == "Change Red Lighting":
                res = cv2.merge([cv2.add(r, 50), g, b])
                title = "Change Red Lighting (R + 50)"
            elif op_name == "Swap R to G":
                res = cv2.merge([g, r, b])
                title = "Swap R to G"
            else: # Eliminate Red
                res = img_rgb.copy()
                res[:, :, 0] = 0
                title = "Eliminate Red (R = 0)"
                
            fig = plt.figure(figsize=(10, 5), facecolor="white")
            plt.subplot(1, 2, 1); plt.imshow(img_rgb); plt.title("Original Image"); plt.axis('off')
            plt.subplot(1, 2, 2); plt.imshow(res); plt.title(title); plt.axis('off')
            plt.tight_layout()

        elif category == "Image Histogram":
            image = cv2.imread(p1, 0)
            if image is None: raise ValueError("Failed to load image.")
            
            if "Stretching" in op_name:
                min_val, max_val = np.min(image), np.max(image)
                processed = (((image - min_val) / (max_val - min_val)) * 255).astype(np.uint8)
                titles = ['Original', 'Original Hist', 'Stretched', 'Stretched Hist']
            else:
                processed = cv2.equalizeHist(image)
                titles = ['Original', 'Original Hist', 'Equalized', 'Equalized Hist']
                
            fig = plt.figure(figsize=(10, 5), facecolor="white")
            plt.subplot(2, 2, 1); plt.imshow(image, cmap='gray'); plt.title(titles[0]); plt.axis('off')
            plt.subplot(2, 2, 2); plt.hist(image.ravel(), 256, [0, 256]); plt.title(titles[1])
            plt.subplot(2, 2, 3); plt.imshow(processed, cmap='gray'); plt.title(titles[2]); plt.axis('off')
            plt.subplot(2, 2, 4); plt.hist(processed.ravel(), 256, [0, 256]); plt.title(titles[3])
            plt.tight_layout()

        elif category == "Neighborhood Processing":
            img = cv2.imread(p1, 0)
            if img is None: raise ValueError("Failed to load image.")
            
            # Make sure kernel size is odd
            k_size = int(slider_val)
            if k_size % 2 == 0:
                k_size += 1
            
            if op_name == "Average Filter":
                res = cv2.blur(img, (k_size, k_size))
            elif op_name == "Laplacian Filter":
                res = cv2.Laplacian(img, cv2.CV_64F).astype(np.uint8)
            elif op_name == "Maximum Filter":
                res = cv2.dilate(img, np.ones((k_size, k_size), np.uint8))
            elif op_name == "Minimum Filter":
                res = cv2.erode(img, np.ones((k_size, k_size), np.uint8))
            elif op_name == "Median Filter":
                res = cv2.medianBlur(img, k_size)
            else: # Mode Filter
                res = mode_filter_logic(img, k_size)
                
            fig = plt.figure(figsize=(10, 5), facecolor="white")
            plt.subplot(1, 2, 1); plt.imshow(img, cmap='gray'); plt.title("Original"); plt.axis('off')
            plt.subplot(1, 2, 2); plt.imshow(res, cmap='gray'); plt.title(f"{op_name} (Size {k_size}x{k_size})"); plt.axis('off')
            plt.tight_layout()

        elif category == "Image Restoration":
            img = cv2.imread(p1, 0)
            if img is None: raise ValueError("Failed to load image.")
            img = cv2.resize(img, (300, 300))
            
            if "Salt & Pepper" in op_name:
                res = ip.get_salt_pepper_restoration(p1)
                titles = ['Original', 'Salt & Pepper Noise', 'Average Filter', 'Median Filter', 'Outlier Method']
                fig = plt.figure(figsize=(12, 7), facecolor="white")
                for i in range(5):
                    plt.subplot(2, 3, i + 1); plt.imshow(res[i], cmap='gray'); plt.title(titles[i]); plt.axis('off')
            else: # Gaussian Restoration
                res = ip.get_gaussian_restoration(p1)
                titles = ['Original', 'Gaussian Noise', 'Image Averaging', 'Average Filter']
                fig = plt.figure(figsize=(15, 5), facecolor="white")
                for i in range(4):
                    plt.subplot(1, 4, i + 1); plt.imshow(res[i], cmap='gray'); plt.title(titles[i]); plt.axis('off')
            plt.tight_layout()

        elif category == "Image Segmentation":
            img = cv2.imread(p1, 0)
            if img is None: raise ValueError("Failed to load image.")
            
            if "Basic Global" in op_name:
                _, res = cv2.threshold(img, int(slider_val), 255, cv2.THRESH_BINARY)
                title = f"Basic Global Threshold ({int(slider_val)})"
            elif "Otsu" in op_name:
                _, res = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                title = "Otsu's Thresholding"
            else: # Adaptive
                res = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
                title = "Adaptive Thresholding"
                
            fig = plt.figure(figsize=(10, 5), facecolor="white")
            plt.subplot(1, 2, 1); plt.imshow(img, cmap='gray'); plt.title("Original"); plt.axis('off')
            plt.subplot(1, 2, 2); plt.imshow(res, cmap='gray'); plt.title(title); plt.axis('off')
            plt.tight_layout()

        elif category == "Edge Detection":
            gray_image = cv2.imread(p1, 0)
            if gray_image is None: raise ValueError("Failed to load image.")
            kernelx = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
            kernely = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
            img_x = cv2.filter2D(gray_image, cv2.CV_64F, kernelx)
            img_y = cv2.filter2D(gray_image, cv2.CV_64F, kernely)
            res = cv2.convertScaleAbs(cv2.magnitude(img_x, img_y))

            fig = plt.figure(figsize=(10, 5), facecolor="white")
            plt.subplot(1, 2, 1); plt.imshow(gray_image, cmap='gray'); plt.title('Original Image'); plt.axis('off')
            plt.subplot(1, 2, 2); plt.imshow(res, cmap='gray'); plt.title('Sobel Edge Detection'); plt.axis('off')
            plt.tight_layout()

        elif category == "Mathematical Morphology":
            img = cv2.imread(p1, 0)
            if img is None: raise ValueError("Failed to load image.")
            _, img_bin = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
            kernel = np.ones((5, 5), np.uint8)
            iterations = int(slider_val) if op_name in ["Erosion", "Dilation"] else 1
            
            if op_name == "Dilation":
                res = cv2.dilate(img_bin, kernel, iterations=iterations)
                title = f"Dilation ({iterations} iterations)"
            elif op_name == "Erosion":
                res = cv2.erode(img_bin, kernel, iterations=iterations)
                title = f"Erosion ({iterations} iterations)"
            elif op_name == "Opening":
                res = cv2.morphologyEx(img_bin, cv2.MORPH_OPEN, kernel)
                title = "Opening Operation"
            elif op_name == "Internal Boundary":
                res = cv2.subtract(img_bin, cv2.erode(img_bin, kernel, iterations=1))
                title = "Internal Boundary"
            elif op_name == "External Boundary":
                res = cv2.subtract(cv2.dilate(img_bin, kernel, iterations=1), img_bin)
                title = "External Boundary"
            else: # Morphological Gradient
                res = cv2.morphologyEx(img_bin, cv2.MORPH_GRADIENT, kernel)
                title = "Morphological Gradient"
                
            fig = plt.figure(figsize=(10, 5), facecolor="white")
            plt.subplot(1, 2, 1); plt.imshow(img_bin, cmap='gray'); plt.title("Original Binary"); plt.axis('off')
            plt.subplot(1, 2, 2); plt.imshow(res, cmap='gray'); plt.title(title); plt.axis('off')
            plt.tight_layout()
            
        else:
            messagebox.showerror("Error", f"Unknown Category: {category}")
            return

        ui.display_in_workspace(fig, workspace, back_callback)

    except Exception as e:
        messagebox.showerror("Execution Error", f"An error occurred while running operation:\n{str(e)}")
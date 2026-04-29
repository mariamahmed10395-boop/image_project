import tkinter as tk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt
import image_processing as ip
import ui_helpers as ui

# فئة لحفظ مسارات الصور بشكل منظم بعيداً عن المتغيرات العامة (Global)
class AppState:
    current_paths = {"path1": "", "path2": ""}

def reset_paths():
    AppState.current_paths = {"path1": "", "path2": ""}

def upload_image(key="path1", label=None):
    path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp")])
    if path:
        AppState.current_paths[key] = path
        if label:
            label.config(text="Image Uploaded Successfully ✔️", fg="#2ecc71")

def create_ui_header(frame, title):
    tk.Label(frame, text=title, bg="#121212", fg="#ffd700", font=("Arial", 18, "bold")).pack(pady=20)

# --- Task 1 UI ---
def open_task1_options(workspace):
    ui.clear_workspace(workspace)
    reset_paths()
    frame = tk.Frame(workspace, bg="#121212")
    frame.pack(expand=True)
    create_ui_header(frame, "Point Operations")

    lbl1 = tk.Label(frame, text="No image 1 selected", bg="#121212", fg="#e74c3c", font=("Arial", 11))
    lbl2 = tk.Label(frame, text="No image 2 selected", bg="#121212", fg="#e74c3c", font=("Arial", 11))

    tk.Button(frame, text="Upload Image 1 ", command=lambda: upload_image("path1", lbl1), bg="#3498db", fg="white", font=("Arial", 12, "bold"), width=25).pack(pady=5)
    lbl1.pack(pady=5)
    tk.Button(frame, text="Upload Image 2 ", command=lambda: upload_image("path2", lbl2), bg="#3498db", fg="white", font=("Arial", 12, "bold"), width=25).pack(pady=5)
    lbl2.pack(pady=5)

    def apply():
        if not AppState.current_paths["path1"] or not AppState.current_paths["path2"]:
            messagebox.showerror("Error", "Please upload BOTH images first!")
            return
        res = ip.get_point_ops(AppState.current_paths["path1"], AppState.current_paths["path2"])
        fig = plt.figure(figsize=(12, 10), facecolor="white")
        titles = ['Addition', 'Subtraction', 'Division', 'Complement']
        for i in range(4):
            plt.subplot(1, 4, i+1); plt.imshow(res[i], cmap='gray'); plt.title(titles[i]); plt.axis('off')
        plt.tight_layout()
        ui.display_in_workspace(fig, workspace, lambda: open_task1_options(workspace))

    tk.Button(frame, text="Apply All Operations", command=apply, bg="#e67e22", fg="white", font=("Arial", 12, "bold"), width=25).pack(pady=20)

# --- Task 2 UI ---
def open_task2_options(workspace):
    ui.clear_workspace(workspace)
    reset_paths()
    frame = tk.Frame(workspace, bg="#121212")
    frame.pack(expand=True)
    create_ui_header(frame, "Color Operations")
    
    lbl = tk.Label(frame, text="No image selected", bg="#121212", fg="#e74c3c", font=("Arial", 11))
    tk.Button(frame, text="Upload Image", command=lambda: upload_image("path1", lbl), bg="#3498db", fg="white", font=("Arial", 12, "bold"), width=25).pack(pady=10)
    lbl.pack(pady=5)

    def apply():
        if not AppState.current_paths["path1"]:
            messagebox.showerror("Error", "Please upload an image first!")
            return
        res = ip.get_color_ops(AppState.current_paths["path1"])
        fig = plt.figure(figsize=(15, 5), facecolor="white")
        titles = ['Original Image', 'Change Red Lighting', 'Swap R to G', 'Eliminate Red']
        for i in range(4):
            plt.subplot(1, 4, i+1); plt.imshow(res[i]); plt.title(titles[i], fontweight='bold'); plt.axis('off')
        plt.tight_layout()
        ui.display_in_workspace(fig, workspace, lambda: open_task2_options(workspace))

    tk.Button(frame, text="Apply Color Operations", command=apply, bg="#e67e22", fg="white", font=("Arial", 12, "bold"), width=25).pack(pady=20)

# --- Task 3 UI ---
def open_task3_options(workspace):
    ui.clear_workspace(workspace)
    reset_paths()
    frame = tk.Frame(workspace, bg="#121212")
    frame.pack(expand=True)
    create_ui_header(frame, "Histogram Operations")
    
    lbl = tk.Label(frame, text="No image selected", bg="#121212", fg="#e74c3c", font=("Arial", 11))
    tk.Button(frame, text="Upload Image", command=lambda: upload_image("path1", lbl), bg="#3498db", fg="white", font=("Arial", 12, "bold"), width=25).pack(pady=10)
    lbl.pack(pady=5)

    def apply(mode):
        if not AppState.current_paths["path1"]:
            messagebox.showerror("Error", "Please upload an image first!")
            return
        if mode == 'stretch':
            orig, processed = ip.get_histogram_stretching(AppState.current_paths["path1"])
            titles = ['Original', 'Original Hist', 'Stretched', 'Stretched Hist']
        else:
            orig, processed = ip.get_histogram_equalization(AppState.current_paths["path1"])
            titles = ['Original', 'Original Hist', 'Equalized', 'Equalized Hist']
            
        fig = plt.figure(figsize=(10, 5), facecolor="white")
        plt.subplot(2, 2, 1); plt.imshow(orig, cmap='gray'); plt.title(titles[0]); plt.axis('off')
        plt.subplot(2, 2, 2); plt.hist(orig.ravel(), 256, [0, 256]); plt.title(titles[1])
        plt.subplot(2, 2, 3); plt.imshow(processed, cmap='gray'); plt.title(titles[2]); plt.axis('off')
        plt.subplot(2, 2, 4); plt.hist(processed.ravel(), 256, [0, 256]); plt.title(titles[3])
        plt.tight_layout()
        ui.display_in_workspace(fig, workspace, lambda: open_task3_options(workspace))

    tk.Button(frame, text="1. Apply Stretching", command=lambda: apply('stretch'), bg="#2ecc71", fg="white", font=("Arial", 12, "bold"), width=25).pack(pady=10)
    tk.Button(frame, text="2. Apply Equalization", command=lambda: apply('equal'), bg="#9b59b6", fg="white", font=("Arial", 12, "bold"), width=25).pack(pady=10)

# --- Task 4 UI ---
def open_task4_options(workspace):
    ui.clear_workspace(workspace)
    reset_paths()
    frame = tk.Frame(workspace, bg="#121212")
    frame.pack(expand=True)
    create_ui_header(frame, "Neighborhood Processing")
    
    lbl = tk.Label(frame, text="No image selected", bg="#121212", fg="#e74c3c", font=("Arial", 11))
    tk.Button(frame, text="Upload Image", command=lambda: upload_image("path1", lbl), bg="#3498db", fg="white", font=("Arial", 12, "bold"), width=25).pack(pady=10)
    lbl.pack(pady=5)

    def apply():
        if not AppState.current_paths["path1"]:
            messagebox.showerror("Error", "Please upload an image first!")
            return
        res = ip.get_neighborhood_ops(AppState.current_paths["path1"])
        fig = plt.figure(figsize=(18, 10), facecolor="white")
        titles = ['Original', 'Average', 'Laplacian', 'Maximum', 'Minimum', 'Median', 'Mode']
        for i in range(7):
            plt.subplot(2, 4, i+1); plt.imshow(res[i], cmap='gray'); plt.title(titles[i], fontweight='bold'); plt.axis('off')
        plt.tight_layout()
        ui.display_in_workspace(fig, workspace, lambda: open_task4_options(workspace))

    tk.Button(frame, text="Apply All Filters", command=apply, bg="#e67e22", fg="white", font=("Arial", 12, "bold"), width=25).pack(pady=20)

# --- Task 5 UI ---
def open_task5_options(workspace):
    ui.clear_workspace(workspace)
    reset_paths()
    frame = tk.Frame(workspace, bg="#121212")
    frame.pack(expand=True)
    create_ui_header(frame, "Image Restoration")
    
    lbl = tk.Label(frame, text="No image selected", bg="#121212", fg="#e74c3c", font=("Arial", 11))
    tk.Button(frame, text="Upload Image", command=lambda: upload_image("path1", lbl), bg="#3498db", fg="white", font=("Arial", 12, "bold"), width=30).pack(pady=10)
    lbl.pack(pady=5)

    def apply(mode):
        if not AppState.current_paths["path1"]:
            messagebox.showerror("Error", "Please upload an image first!")
            return
        if mode == 'sp':
            res = ip.get_salt_pepper_restoration(AppState.current_paths["path1"])
            titles = ['Original', 'Salt & Pepper', 'Average', 'Median', 'Outlier']
            fig = plt.figure(figsize=(12, 7), facecolor="white")
            for i in range(5):
                plt.subplot(2, 3, i + 1); plt.imshow(res[i], cmap='gray'); plt.title(titles[i]); plt.axis('off')
        else:
            res = ip.get_gaussian_restoration(AppState.current_paths["path1"])
            titles = ['Original', 'Gaussian Noise', 'Image Averaging', 'Average Filter']
            fig = plt.figure(figsize=(15, 5), facecolor="white")
            for i in range(4):
                plt.subplot(1, 4, i + 1); plt.imshow(res[i], cmap='gray'); plt.title(titles[i]); plt.axis('off')
        
        plt.tight_layout()
        ui.display_in_workspace(fig, workspace, lambda: open_task5_options(workspace))

    tk.Button(frame, text="1. Salt & Pepper Restoration", command=lambda: apply('sp'), bg="#2ecc71", fg="white", font=("Arial", 12, "bold"), width=30).pack(pady=10)
    tk.Button(frame, text="2. Gaussian Restoration", command=lambda: apply('gauss'), bg="#9b59b6", fg="white", font=("Arial", 12, "bold"), width=30).pack(pady=10)

# --- Task 6 UI ---
def open_task6_options(workspace):
    ui.clear_workspace(workspace)
    reset_paths()
    frame = tk.Frame(workspace, bg="#121212")
    frame.pack(expand=True)
    create_ui_header(frame, "Image Segmentation")
    
    lbl = tk.Label(frame, text="No image selected", bg="#121212", fg="#e74c3c", font=("Arial", 11))
    tk.Button(frame, text="Upload Image", command=lambda: upload_image("path1", lbl), bg="#3498db", fg="white", font=("Arial", 12, "bold"), width=25).pack(pady=10)
    lbl.pack(pady=5)

    def apply():
        if not AppState.current_paths["path1"]:
            messagebox.showerror("Error", "Please upload an image first!")
            return
        res = ip.get_segmentation_ops(AppState.current_paths["path1"])
        fig = plt.figure(figsize=(18, 5), facecolor="white")
        titles = ['Original Image', 'Basic Global', 'Otsu Threshold', 'Adaptive Threshold']
        for i in range(4):
            plt.subplot(1, 4, i+1); plt.imshow(res[i], cmap='gray'); plt.title(titles[i], fontweight='bold'); plt.axis('off')
        plt.tight_layout()
        ui.display_in_workspace(fig, workspace, lambda: open_task6_options(workspace))

    tk.Button(frame, text="Apply Thresholding", command=apply, bg="#e67e22", fg="white", font=("Arial", 12, "bold"), width=25).pack(pady=20)

# --- Task 7 UI ---
def open_task7_options(workspace):
    ui.clear_workspace(workspace)
    reset_paths()
    frame = tk.Frame(workspace, bg="#121212")
    frame.pack(expand=True)
    create_ui_header(frame, "Edge Detection")
    
    lbl = tk.Label(frame, text="No image selected", bg="#121212", fg="#e74c3c", font=("Arial", 11))
    tk.Button(frame, text="Upload Image", command=lambda: upload_image("path1", lbl), bg="#3498db", fg="white", font=("Arial", 12, "bold"), width=25).pack(pady=10)
    lbl.pack(pady=5)

    def apply():
        if not AppState.current_paths["path1"]:
            messagebox.showerror("Error", "Please upload an image first!")
            return
        res = ip.get_edge_detection(AppState.current_paths["path1"])
        fig = plt.figure(figsize=(10, 5), facecolor="white")
        titles = ['Original Image', 'Sobel Edge Detection']
        for i in range(2):
            plt.subplot(1, 2, i+1); plt.imshow(res[i], cmap='gray'); plt.title(titles[i]); plt.axis('off')
        plt.tight_layout()
        ui.display_in_workspace(fig, workspace, lambda: open_task7_options(workspace))

    tk.Button(frame, text="Apply Sobel Edge", command=apply, bg="#e67e22", fg="white", font=("Arial", 12, "bold"), width=25).pack(pady=10)

# --- Task 8 UI ---
def open_task8_options(workspace):
    ui.clear_workspace(workspace)
    reset_paths()
    frame = tk.Frame(workspace, bg="#121212")
    frame.pack(expand=True)
    create_ui_header(frame, "Mathematical Morphology")
    
    lbl = tk.Label(frame, text="No image selected", bg="#121212", fg="#e74c3c", font=("Arial", 11))
    tk.Button(frame, text="Upload Image", command=lambda: upload_image("path1", lbl), bg="#3498db", fg="white", font=("Arial", 12, "bold"), width=25).pack(pady=10)
    lbl.pack(pady=5)

    def apply():
        if not AppState.current_paths["path1"]:
            messagebox.showerror("Error", "Please upload an image first!")
            return
        res = ip.get_morphology_ops(AppState.current_paths["path1"])
        fig = plt.figure(figsize=(18, 10), facecolor="white")
        titles = ['Original Binary', 'Dilation', 'Erosion', 'Opening', 'Internal Boundary', 'External Boundary', 'Gradient']
        for i in range(7):
            plt.subplot(2, 4, i+1); plt.imshow(res[i], cmap='gray'); plt.title(titles[i], fontweight='bold'); plt.axis('off')
        plt.tight_layout()
        ui.display_in_workspace(fig, workspace, lambda: open_task8_options(workspace))

    tk.Button(frame, text="Apply All Morphological Ops", command=apply, bg="#e67e22", fg="white", font=("Arial", 12, "bold"), width=25).pack(pady=20)
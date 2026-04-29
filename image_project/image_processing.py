import cv2
import numpy as np
from scipy import stats

# --- Task 1: Point Operations ---
def get_point_ops(path1, path2):
    x1 = cv2.imread(path1, 0)
    x2 = cv2.imread(path2, 0)
    if x1 is None or x2 is None: return None
    x1 = cv2.resize(x1, (400, 400))
    x2 = cv2.resize(x2, (400, 400))
    
    y1 = cv2.add(x1, x2)
    y2 = cv2.subtract(x1, x2)
    with np.errstate(divide='ignore', invalid='ignore'):
        y3 = np.divide(x1, np.where(x2 == 0, 1, x2))
    y3 = np.clip(y3, 0, 255).astype(np.uint8)
    y4 = 255 - x1
    return [y1, y2, y3, y4]

# --- Task 2: Color Operations ---
def get_color_ops(path):
    img = cv2.imread(path)
    if img is None: return None
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    r, g, b = cv2.split(img_rgb)
    change_red_image = cv2.merge([cv2.add(r, 50), g, b])
    swapped_image = cv2.merge([g, r, b])
    
    no_red_image = img_rgb.copy()
    no_red_image[:, :, 0] = 0
    return [img_rgb, change_red_image, swapped_image, no_red_image]

# --- Task 3: Histogram ---
def get_histogram_stretching(path):
    img = cv2.imread(path, 0)
    if img is None: return None
    min_val, max_val = np.min(img), np.max(img)
    stretched = (((img - min_val) / (max_val - min_val)) * 255).astype(np.uint8)
    return img, stretched

def get_histogram_equalization(path):
    img = cv2.imread(path, 0)
    if img is None: return None
    return img, cv2.equalizeHist(img)

# --- Task 4: Neighborhood Operations ---
def mode_filter_logic(img, size):
    padded_img = np.pad(img, size//2, mode='edge')
    result = np.zeros_like(img)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            region = padded_img[i:i+size, j:j+size]
            result[i, j] = stats.mode(region, axis=None).mode
    return result

def get_neighborhood_ops(path):
    img = cv2.imread(path, 0)
    if img is None: return None
    k_size = 5
    kernel = np.ones((k_size, k_size), np.uint8)
    
    return [
        img, 
        cv2.blur(img, (k_size, k_size)), 
        cv2.Laplacian(img, cv2.CV_64F).astype(np.uint8),
        cv2.dilate(img, kernel), 
        cv2.erode(img, kernel), 
        cv2.medianBlur(img, k_size),
        mode_filter_logic(img, k_size)
    ]

# --- Task 5: Restoration ---
def get_salt_pepper_restoration(path):
    img = cv2.imread(path, 0)
    if img is None: return None
    img = cv2.resize(img, (300, 300))
    
    noise_img = np.copy(img)
    row, col = noise_img.shape
    num_pixels = np.random.randint(3000, 10000)
    for _ in range(num_pixels):
        y, x = np.random.randint(0, row-1), np.random.randint(0, col-1)
        noise_img[y][x] = 255
    for _ in range(num_pixels):
        y, x = np.random.randint(0, row-1), np.random.randint(0, col-1)
        noise_img[y][x] = 0

    avg_res = cv2.blur(noise_img, (5, 5))
    med_res = cv2.medianBlur(noise_img, 5)
    
    outlier_res = np.copy(noise_img).astype(np.float32)
    mean_f = cv2.blur(noise_img, (3, 3)).astype(np.float32)
    diff = np.abs(outlier_res - mean_f)
    outlier_res[diff > 50] = mean_f[diff > 50]
    outlier_res = np.clip(outlier_res, 0, 255).astype(np.uint8)
    
    return [img, noise_img, avg_res, med_res, outlier_res]

def get_gaussian_restoration(path):
    img = cv2.imread(path, 0)
    if img is None: return None
    img = cv2.resize(img, (300, 300))

    num_images = 10
    noisy_images = []
    for _ in range(num_images):
        gauss_noise = np.random.normal(0, 25, img.shape).astype(np.float32)
        noisy = cv2.add(img.astype(np.float32), gauss_noise)
        noisy_images.append(noisy)

    single_noisy = np.clip(noisy_images[0], 0, 255).astype(np.uint8)
    
    sum_imgs = np.zeros_like(img, dtype=np.float32)
    for n_img in noisy_images:
        sum_imgs += n_img
    averaged_res = np.clip((sum_imgs / num_images), 0, 255).astype(np.uint8)
    avg_filter_res = cv2.blur(single_noisy, (5, 5))
    
    return [img, single_noisy, averaged_res, avg_filter_res]

# --- Task 6: Segmentation ---
def get_segmentation_ops(path):
    img = cv2.imread(path, 0)
    if img is None: return None
    _, th1 = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    _, th2 = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    th3 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    return [img, th1, th2, th3]

# --- Task 7: Edge Detection ---
def get_edge_detection(path):
    img = cv2.imread(path, 0)
    if img is None: return None
    kernelx = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    kernely = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
    img_x = cv2.filter2D(img, cv2.CV_64F, kernelx)
    img_y = cv2.filter2D(img, cv2.CV_64F, kernely)
    res = cv2.convertScaleAbs(cv2.magnitude(img_x, img_y))
    return [img, res]

# --- Task 8: Morphology ---
def get_morphology_ops(path):
    img = cv2.imread(path, 0)
    if img is None: return None
    _, img_bin = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    kernel = np.ones((5, 5), np.uint8)
    
    dilation = cv2.dilate(img_bin, kernel, iterations=1)
    erosion = cv2.erode(img_bin, kernel, iterations=1)
    opening = cv2.morphologyEx(img_bin, cv2.MORPH_OPEN, kernel)
    internal_bound = cv2.subtract(img_bin, erosion)
    external_bound = cv2.subtract(dilation, img_bin)
    gradient = cv2.morphologyEx(img_bin, cv2.MORPH_GRADIENT, kernel)
    
    return [img_bin, dilation, erosion, opening, internal_bound, external_bound, gradient]
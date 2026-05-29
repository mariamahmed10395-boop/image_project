import tkinter as tk
from tkinter import ttk, messagebox
import tasks_gui as tg
import ui_helpers as ui
import time

# Main Dashboard Setup
root = tk.Tk()
root.title("✨ Advanced Image Processing Dashboard ✨")
root.geometry("1200x820")
root.minsize(800, 600)
root.configure(bg="#121214")

# Centered Bandicam watermark at the top header area
watermark_lbl = tk.Label(
    root, 
    text="www.BANDICAM.com", 
    bg="#121214", 
    fg="#252528", 
    font=("Arial", 9, "bold")
)
watermark_lbl.pack(side="top", fill="x", pady=(2, 0))

# Custom ttk Styles
style = ttk.Style()
style.theme_use("clam")
style.configure(".", background="#121214", foreground="#ffffff")
style.configure("TCombobox", fieldbackground="#2A2A30", background="#1E1E22", foreground="#ffffff", bordercolor="#3A3A40", arrowcolor="#00E5FF")
style.map("TCombobox", fieldbackground=[("readonly", "#2A2A30")], foreground=[("readonly", "#ffffff")])

# Layout mode
current_layout_mode = None

# Operations mapping database for Comboboxes
operations_db = {
    "Point Operations": [
        "Brightness",
        "Addition",
        "Subtraction",
        "Division",
        "Complement"
    ],
    "Color Operations": [
        "Change Red Lighting",
        "Swap R to G",
        "Eliminate Red"
    ],
    "Image Histogram": [
        "Histogram Stretching",
        "Histogram Equalization"
    ],
    "Neighborhood Processing": [
        "Average Filter",
        "Laplacian Filter",
        "Maximum Filter",
        "Minimum Filter",
        "Median Filter",
        "Mode Filter"
    ],
    "Image Restoration": [
        "Salt & Pepper Noise Restoration",
        "Gaussian Noise Restoration (Averaging)"
    ],
    "Image Segmentation": [
        "Basic Global Thresholding",
        "Otsu's Thresholding",
        "Adaptive Thresholding"
    ],
    "Edge Detection": [
        "Sobel Edge Detection"
    ],
    "Mathematical Morphology": [
        "Erosion",
        "Dilation",
        "Opening",
        "Internal Boundary",
        "External Boundary",
        "Gradient"
    ]
}

# --- Event Triggers & Conditional Logic ---
def on_category_change(event=None):
    category = category_combo.get()
    op_combo.configure(state="readonly")
    if category in operations_db:
        op_combo['values'] = operations_db[category]
        op_combo.set(operations_db[category][0])
    update_conditional_ui()

def update_conditional_ui(event=None):
    category = category_combo.get()
    op = op_combo.get()
    
    # 1. Conditional Second Image Upload Frame
    requires_second_img = (category == "Point Operations" and op in ["Addition", "Subtraction", "Division"])
    
    if requires_second_img:
        btn_clear.pack_forget()
        sec_upload_frame.pack(fill="x", pady=(5, 5))
        btn_clear.pack(fill="x", pady=(10, 2))
        
        lbl_status2.configure(
            text="No image selected" if not tg.AppState.current_paths["path2"] else "Uploaded ✔️", 
            fg="#e74c3c" if not tg.AppState.current_paths["path2"] else "#2ecc71"
        )
        lbl_tooltip2.configure(text=f"Required for {op}", fg="#00E5FF")
    else:
        sec_upload_frame.pack_forget()
        
    # 2. Dynamic Parameter Slider Configuration
    show_slider = False
    slider_label = ""
    min_val, max_val, default_val, resolution = 0, 100, 0, 1
    
    if category == "Point Operations" and op == "Brightness":
        show_slider = True
        slider_label = "Brightness Adjustment:"
        min_val, max_val, default_val = -100, 100, -20
    elif category == "Image Segmentation" and op == "Basic Global Thresholding":
        show_slider = True
        slider_label = "Threshold Level:"
        min_val, max_val, default_val = 0, 255, 127
    elif category == "Neighborhood Processing" and op in ["Average Filter", "Median Filter", "Mode Filter", "Maximum Filter", "Minimum Filter"]:
        show_slider = True
        slider_label = "Kernel Size (Odd Only):"
        min_val, max_val, default_val, resolution = 3, 21, 5, 2
    elif category == "Mathematical Morphology" and op in ["Erosion", "Dilation"]:
        show_slider = True
        slider_label = "Iterations:"
        min_val, max_val, default_val = 1, 10, 1
        
    # Unpack both first to handle order/grid reconfig cleanly and prevent TclErrors
    param_card.pack_forget()
    param_card.grid_forget()
    actions_card.pack_forget()
    actions_card.grid_forget()
    
    if current_layout_mode == "horizontal":
        if show_slider:
            lbl_slider_title.config(text=slider_label)
            brightness_slider.configure(from_=min_val, to=max_val, resolution=resolution)
            brightness_slider.set(default_val)
            brightness_slider.pack(fill="x", pady=5)
            lbl_slider_val.pack()
            
            param_card.pack(fill="x", pady=10)
            
        actions_card.pack(fill="x", pady=(10, 0))
    else:
        # Vertical Gridding (Column 2)
        if show_slider:
            lbl_slider_title.config(text=slider_label)
            brightness_slider.configure(from_=min_val, to=max_val, resolution=resolution)
            brightness_slider.set(default_val)
            brightness_slider.pack(fill="x", pady=5)
            lbl_slider_val.pack()
            
            param_card.grid(row=0, column=2, sticky="nsew", padx=5, pady=0)
            actions_card.grid(row=1, column=2, sticky="nsew", padx=5, pady=(5, 0))
        else:
            actions_card.grid(row=0, column=2, rowspan=2, sticky="nsew", padx=5, pady=0)

def on_slider_move(val):
    lbl_slider_val.config(text=f"Value: {int(float(val))}")

def trigger_apply():
    category = category_combo.get()
    op = op_combo.get()
    s_val = int(brightness_slider.get())
    
    tg.run_operation(category, op, workspace, slider_val=s_val, back_callback=lambda: tg.draw_sources(workspace))

# --- Widget Creation ---

# Top Bar (Slim dark web title bar)
top_bar = tk.Frame(root, bg="#0C0C0E", height=45)
top_bar.pack(side="top", fill="x")

# Cyber cyan glowing separator line
glow_line = tk.Frame(root, bg="#00E5FF", height=2)
glow_line.pack(side="top", fill="x")

# Top Bar Elements
tb_title_left = tk.Label(
    top_bar, 
    text="ADVANCED IMAGE PROCESSING DASHBOARD", 
    bg="#0C0C0E", 
    fg="#8E9AA6", 
    font=("Segoe UI", 10, "bold")
)
tb_title_left.pack(side="left", padx=15, pady=8)

tb_title_center = tk.Label(
    top_bar, 
    text="🔹 IMAGE PROCESSING TOOLBOX 🔹", 
    bg="#0C0C0E", 
    fg="#00E5FF", 
    font=("Segoe UI", 12, "bold")
)
tb_title_center.pack(side="left", expand=True, pady=8)

tb_deployed = tk.Label(
    top_bar, 
    text="🟢 Deployed", 
    bg="#0C0C0E", 
    fg="#2ECC71", 
    font=("Segoe UI", 9, "bold")
)
tb_deployed.pack(side="right", padx=(0, 15), pady=8)

tb_chat = tk.Button(
    top_bar, 
    text="💬 Chat", 
    bg="#2D2D30", 
    fg="#ffffff", 
    font=("Segoe UI", 9), 
    relief="flat", 
    cursor="hand2"
)
tb_chat.pack(side="right", padx=10, pady=6)

# Main Container
main_container = tk.Frame(root, bg="#121214")
main_container.pack(fill="both", expand=True)

# Control Panel Sidebar
control_panel = tk.Frame(main_container, bg="#1E1E22", padx=15, pady=15)

# Workspace Studio Canvas
workspace = tk.Frame(main_container, bg="#121214", bd=0)

# Card 1: Active Images
img_card = tk.LabelFrame(
    control_panel, 
    text=" 📁 ACTIVE IMAGES ", 
    bg="#1E1E22", 
    fg="#00E5FF", 
    font=("Segoe UI", 11, "bold"),
    bd=1,
    relief="solid",
    padx=10,
    pady=10
)

btn_upload1 = tk.Button(
    img_card, 
    text="Upload Primary Image", 
    command=lambda: tg.upload_image("path1", lbl_status1, lambda: tg.draw_sources(workspace)), 
    bg="#00E5FF", 
    fg="#000000", 
    font=("Segoe UI", 10, "bold"), 
    relief="flat",
    cursor="hand2"
)
lbl_status1 = tk.Label(img_card, text="No image selected", bg="#1E1E22", fg="#e74c3c", font=("Segoe UI", 10))

# Modular Secondary Image Frame (packed conditionally)
sec_upload_frame = tk.Frame(img_card, bg="#1E1E22")

btn_upload2 = tk.Button(
    sec_upload_frame, 
    text="Upload Secondary Image", 
    command=lambda: tg.upload_image("path2", lbl_status2, lambda: tg.draw_sources(workspace)), 
    bg="#2d2d30", 
    fg="#ffffff", 
    font=("Segoe UI", 10, "bold"), 
    relief="flat",
    cursor="hand2"
)
lbl_status2 = tk.Label(sec_upload_frame, text="No image selected", bg="#1E1E22", fg="#e74c3c", font=("Segoe UI", 10))
lbl_tooltip2 = tk.Label(sec_upload_frame, text="Required for Addition", bg="#1E1E22", fg="#00E5FF", font=("Segoe UI", 9, "italic"))

btn_upload2.pack(fill="x", pady=(2, 2))
lbl_status2.pack()
lbl_tooltip2.pack()

btn_clear = tk.Button(
    img_card, 
    text="Reset All State", 
    command=lambda: tg.clear_images([lbl_status1, lbl_status2], lambda: tg.draw_sources(workspace)), 
    bg="#e74c3c", 
    fg="white", 
    font=("Segoe UI", 9, "bold"), 
    relief="flat",
    cursor="hand2"
)

# Card 2: Operation Selector
op_card = tk.LabelFrame(
    control_panel, 
    text=" ⚙️ OPERATION SELECTOR ", 
    bg="#1E1E22", 
    fg="#00E5FF", 
    font=("Segoe UI", 11, "bold"),
    bd=1,
    relief="solid",
    padx=10,
    pady=10
)

tk.Label(op_card, text="Category Selection:", bg="#1E1E22", fg="#aaaaaa", font=("Segoe UI", 10)).pack(anchor="w", pady=(0,5))
category_combo = ttk.Combobox(
    op_card, 
    values=list(operations_db.keys()), 
    state="readonly", 
    font=("Segoe UI", 10)
)
category_combo.pack(fill="x", pady=(0, 10))
category_combo.bind("<<ComboboxSelected>>", on_category_change)

tk.Label(op_card, text="Operation Method:", bg="#1E1E22", fg="#aaaaaa", font=("Segoe UI", 10)).pack(anchor="w", pady=(5,5))
op_combo = ttk.Combobox(
    op_card, 
    state="readonly", 
    font=("Segoe UI", 10)
)
op_combo.pack(fill="x", pady=(0, 5))
op_combo.bind("<<ComboboxSelected>>", update_conditional_ui)

# Card 3: Parameters Card (Shown dynamically)
param_card = tk.LabelFrame(
    control_panel, 
    text=" 🛠️ PARAMETERS ", 
    bg="#1E1E22", 
    fg="#00E5FF", 
    font=("Segoe UI", 11, "bold"),
    bd=1,
    relief="solid",
    padx=10,
    pady=8
)
lbl_slider_title = tk.Label(param_card, text="Brightness Adjustment:", bg="#1E1E22", fg="#aaaaaa", font=("Segoe UI", 10))
lbl_slider_title.pack(anchor="w")

brightness_slider = tk.Scale(
    param_card, 
    from_=-100, 
    to=100, 
    orient="horizontal", 
    bg="#1E1E22", 
    fg="#ffffff", 
    highlightthickness=0, 
    troughcolor="#2A2A30", 
    activebackground="#00E5FF",
    command=on_slider_move
)
brightness_slider.set(-20)
lbl_slider_val = tk.Label(param_card, text="Value: -20", bg="#1E1E22", fg="#00E5FF", font=("Segoe UI", 9, "bold"))

# Card 4: Actions (explicitly parented to control_panel to prevent TclErrors)
actions_card = tk.LabelFrame(
    control_panel, 
    text=" 🚀 ACTIONS ", 
    bg="#1E1E22", 
    fg="#00E5FF", 
    font=("Segoe UI", 11, "bold"),
    bd=1,
    relief="solid",
    padx=10,
    pady=10
)

btn_apply = tk.Button(
    actions_card, 
    text="Apply Operation", 
    command=trigger_apply, 
    bg="#FF7A00", 
    fg="white", 
    font=("Segoe UI", 11, "bold"), 
    relief="flat",
    cursor="hand2",
    activebackground="#d35400",
    activeforeground="white"
)

btn_reset_view = tk.Button(
    actions_card, 
    text="Original Image Preview", 
    command=lambda: tg.draw_sources(workspace), 
    bg="#00E5FF", 
    fg="#000000", 
    font=("Segoe UI", 10, "bold"), 
    relief="flat",
    cursor="hand2"
)

# Button Hover Animations
def on_enter(btn, hover_color, text_color=None):
    btn['background'] = hover_color
    if text_color:
        btn['foreground'] = text_color

def on_leave(btn, orig_color, text_color=None):
    btn['background'] = orig_color
    if text_color:
        btn['foreground'] = text_color

btn_upload1.bind("<Enter>", lambda e: on_enter(btn_upload1, "#00B5CC", "#000000"))
btn_upload1.bind("<Leave>", lambda e: on_leave(btn_upload1, "#00E5FF", "#000000"))
btn_upload2.bind("<Enter>", lambda e: on_enter(btn_upload2, "#404040", "#ffffff") if btn_upload2['state']=="normal" else None)
btn_upload2.bind("<Leave>", lambda e: on_leave(btn_upload2, "#2d2d30", "#ffffff") if btn_upload2['state']=="normal" else None)
btn_clear.bind("<Enter>", lambda e: on_enter(btn_clear, "#c0392b"))
btn_clear.bind("<Leave>", lambda e: on_leave(btn_clear, "#e74c3c"))
btn_apply.bind("<Enter>", lambda e: on_enter(btn_apply, "#e05a00"))
btn_apply.bind("<Leave>", lambda e: on_leave(btn_apply, "#FF7A00"))
btn_reset_view.bind("<Enter>", lambda e: on_enter(btn_reset_view, "#00B5CC", "#000000"))
btn_reset_view.bind("<Leave>", lambda e: on_leave(btn_reset_view, "#00E5FF", "#000000"))

# --- WINDOWS 11 STYLED TASKBAR ---
taskbar_frame = tk.Frame(root, bg="#1F1F24", height=48)
taskbar_frame.pack(side="bottom", fill="x")

taskbar_center_container = tk.Frame(taskbar_frame, bg="#1F1F24")
taskbar_center_container.pack(expand=True)

tb_search = tk.Entry(taskbar_center_container, bg="#2A2A30", fg="#888888", font=("Segoe UI", 9), width=18, bd=0, highlightthickness=1, highlightcolor="#00E5FF", highlightbackground="#3A3A40")
tb_search.insert(0, " 🔍 Search...")
tb_search.pack(side="left", padx=(0, 20), ipady=3)

tb_start = tk.Label(taskbar_center_container, text="❖", bg="#1F1F24", fg="#00E5FF", font=("Segoe UI", 16, "bold"), cursor="hand2")
tb_start.pack(side="left", padx=8)

taskbar_shortcuts = [("🔍", "Search"), ("📁", "TaskView"), ("📁", "Widgets"), ("📂", "Explorer"), ("🌐", "Edge"), ("🐍", "Python")]
for icon, tooltip in taskbar_shortcuts:
    tk.Label(taskbar_center_container, text=icon, bg="#1F1F24", fg="#ffffff", font=("Segoe UI", 13), cursor="hand2").pack(side="left", padx=8)

# Tray clock + weather
tb_tray = tk.Frame(taskbar_frame, bg="#1F1F24")
tb_tray.pack(side="right", padx=15, fill="y")

current_date = time.strftime("%m/%d/%Y")
current_time = time.strftime("%I:%M %p")
tb_weather = tk.Label(tb_tray, text="☀️ 24°C", bg="#1F1F24", fg="#ffffff", font=("Segoe UI", 9, "bold"))
tb_weather.pack(side="left", padx=8)

tb_clock = tk.Label(tb_tray, text=f"{current_time}\n{current_date}", bg="#1F1F24", fg="#dddddd", font=("Segoe UI", 8), justify="right")
tb_clock.pack(side="left", padx=5)

def update_taskbar_clock():
    new_date = time.strftime("%m/%d/%Y")
    new_time = time.strftime("%I:%M %p")
    tb_clock.config(text=f"{new_time}\n{new_date}")
    root.after(15000, update_taskbar_clock)
update_taskbar_clock()

# --- Responsive Dynamic Layout ---
def rearrange_layout(event=None):
    global current_layout_mode
    if event and event.widget != root:
        return
        
    width = root.winfo_width()
    
    if width >= 850:
        if current_layout_mode != "horizontal":
            current_layout_mode = "horizontal"
            
            workspace.pack_forget()
            control_panel.pack_forget()
            
            # Sidebar Layout Configuration
            control_panel.configure(width=330)
            control_panel.pack_propagate(False)
            control_panel.pack(side="left", fill="y", padx=(10, 5), pady=10)
            workspace.pack(side="right", fill="both", expand=True, padx=(5, 10), pady=10)
            
            img_card.grid_forget()
            op_card.grid_forget()
            param_card.grid_forget()
            actions_card.grid_forget()
            
            img_card.pack(fill="x", pady=(0, 10))
            op_card.pack(fill="x", pady=10)
            
            update_conditional_ui()
            
            # Primary upload packing
            btn_upload1.pack_forget()
            lbl_status1.pack_forget()
            sec_upload_frame.pack_forget()
            btn_clear.pack_forget()
            
            btn_upload1.pack(fill="x", pady=(5, 2))
            lbl_status1.pack(pady=(0, 5))
            
            # Manage conditional frames & sliders
            update_conditional_ui()
            btn_clear.pack(fill="x", pady=(10, 2))
            
            btn_apply.pack_forget()
            btn_reset_view.pack_forget()
            btn_apply.pack(fill="x", ipady=8, pady=(0, 10))
            btn_reset_view.pack(fill="x", ipady=5)
            
    else:  # Vertical Mode Reflow
        if current_layout_mode != "vertical":
            current_layout_mode = "vertical"
            
            workspace.pack_forget()
            control_panel.pack_forget()
            
            control_panel.pack_propagate(True)
            control_panel.pack(side="top", fill="x", padx=10, pady=(10, 5))
            workspace.pack(side="bottom", fill="both", expand=True, padx=10, pady=(5, 10))
            
            img_card.pack_forget()
            op_card.pack_forget()
            param_card.pack_forget()
            actions_card.grid_forget()
            
            control_panel.columnconfigure(0, weight=1)
            control_panel.columnconfigure(1, weight=1)
            control_panel.columnconfigure(2, weight=1)
            
            img_card.grid(row=0, column=0, sticky="nsew", padx=5, pady=0)
            op_card.grid(row=0, column=1, sticky="nsew", padx=5, pady=0)
            
            # Repack image widgets inside vertical layout
            btn_upload1.pack_forget()
            lbl_status1.pack_forget()
            sec_upload_frame.pack_forget()
            btn_clear.pack_forget()
            
            btn_upload1.pack(fill="x", pady=2)
            lbl_status1.pack()
            
            # Manage conditional states gridding
            update_conditional_ui()
            btn_clear.pack(fill="x", pady=(5, 2))
            
            btn_apply.pack_forget()
            btn_reset_view.pack_forget()
            btn_apply.pack(fill="x", ipady=4, pady=(0, 6))
            btn_reset_view.pack(fill="x", ipady=3)

# Configure layout resizing trigger
root.bind("<Configure>", rearrange_layout)

# Initialize Comboboxes
category_combo.set("Point Operations")
on_category_change()

# Draw visual welcome greetings
tg.draw_sources(workspace)

if __name__ == "__main__":
    root.after(100, rearrange_layout)
    root.mainloop()
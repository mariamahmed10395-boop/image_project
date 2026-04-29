import tkinter as tk
import tasks_gui as tg

# Main Dashboard UI setup
root = tk.Tk()
root.title("Image Processing Dashboard")
root.geometry("1100x700")
root.configure(bg="#121212")

# Header
header_frame = tk.Frame(root, bg="#000000", height=80)
header_frame.pack(side="top", fill="x")
tk.Label(header_frame, text="✨ Image Processing Final Project ✨", bg="#000000", fg="white", font=("Arial", 22, "bold")).pack(pady=20)

# Sidebar
sidebar = tk.Frame(root, bg="#1e1e1e", width=250)
sidebar.pack(side="left", fill="y")
tk.Label(sidebar, text="Control Panel", bg="#1e1e1e", fg="#ffffff", font=("Arial", 16, "bold")).pack(pady=20)

# Workspace
workspace = tk.Frame(root, bg="#121212", bd=0)
workspace.pack(side="right", fill="both", expand=True, padx=20, pady=20)

welcome_lbl = tk.Label(workspace, text="Welcome to Our Image Processing App\n\n👈 Please select a task from the menu", 
                       bg="#121212", fg="#aaaaaa", font=("Arial", 16), justify="center")
welcome_lbl.pack(expand=True)

# Sidebar Tasks Mapping
tasks = [
    ("➕ Task 1: Point Operations", lambda: tg.open_task1_options(workspace), "#3498db"), 
    ("🎨 Task 2: Color Operations", lambda: tg.open_task2_options(workspace), "#e74c3c"), 
    ("📊 Task 3: Image Histogram", lambda: tg.open_task3_options(workspace), "#2ecc71"),  
    ("🔲 Task 4: Neighborhood Ops", lambda: tg.open_task4_options(workspace), "#f1c40f"),  
    ("🪄 Task 5: Restoration", lambda: tg.open_task5_options(workspace), "#9b59b6"),      
    ("✂️ Task 6: Segmentation", lambda: tg.open_task6_options(workspace), "#1abc9c"),     
    ("📏 Task 7: Edge Detection", lambda: tg.open_task7_options(workspace), "#e67e22"),   
    ("🦠 Task 8: Morphology", lambda: tg.open_task8_options(workspace), "#ff9ff3")        
]

for text, cmd, color in tasks:
    tk.Button(sidebar, text=text, font=("Arial", 12, "bold"), bg="#2d2d2d", fg=color, 
              activebackground="#404040", activeforeground=color, relief="flat", cursor="hand2", command=cmd).pack(pady=8, padx=15, fill="x", ipady=5)

if __name__ == "__main__":
    root.mainloop()
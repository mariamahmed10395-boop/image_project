import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

def clear_workspace(workspace):
    for widget in workspace.winfo_children():
        widget.destroy()

def display_in_workspace(fig, workspace, back_command=None):
    clear_workspace(workspace)
    
    if back_command:
        top_frame = tk.Frame(workspace, bg="#121212")
        top_frame.pack(side="top", fill="x", pady=5)
        btn_back = tk.Button(top_frame, text="⬅ Back ", command=back_command, 
                             bg="#e74c3c", fg="white", font=("Arial", 12, "bold"), cursor="hand2")
        btn_back.pack(side="left", padx=10)

    canvas = FigureCanvasTkAgg(fig, master=workspace)
    canvas.draw()
    
    toolbar = NavigationToolbar2Tk(canvas, workspace)
    toolbar.update()
    
    canvas.get_tk_widget().pack(side="top", fill="both", expand=True)
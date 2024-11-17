import os
import tkinter as tk
from tkinter import filedialog, messagebox

def process_files():
    # Get user inputs
    folder_path = input_folder_var.get()
    output_folder_path = output_folder_var.get()
    base_texture_path = texture_path_var.get()

    if not folder_path or not output_folder_path or not base_texture_path:
        messagebox.showerror("Error", "Please fill in all fields!")
        return

    # Get all files in the folder and group pairs
    try:
        files = os.listdir(folder_path)
        pairs = {}

        for file in files:
            if file.endswith(".paa"):
                key = "_".join(file.split("_")[:2])  # Key for the file pair
                if key not in pairs:
                    pairs[key] = []
                pairs[key].append(file)

        # Create .rvmat files for each pair
        for key, textures in pairs.items():
            if len(textures) == 2:
                nopx_file = next((f for f in textures if "nopx" in f), None)
                co_file = next((f for f in textures if "co" in f), None)

                if nopx_file and co_file:
                    rvmat_content = f"""
ambient[]={{{0.89999998,0.89999998,0.89999998,1}}};
diffuse[]={{{0.89999998,0.89999998,0.89999998,1}}};
forcedDiffuse[]={{{0.02,0.02,0.02,1}}};
specular[]={{{0,0,0,0}}};
specularPower=1;
emmisive[]={{{0,0,0,0}}};
PixelShaderID="NormalMapDiffuse";
VertexShaderID="NormalMapDiffuseAlpha";
class Stage1
{{
    texture="{base_texture_path}{nopx_file}";
    uvSource="tex";
    class uvTransform
    {{
        aside[]={{{10,0,0}}};
        up[]={{{0,10,0}}};
        dir[]={{{0,0,10}}};
        pos[]={{{0,0,0}}};
    }};
}};
class Stage2
{{
    texture="{base_texture_path}{co_file}";
    uvSource="tex";
    class uvTransform
    {{
        aside[]={{{10,0,0}}};
        up[]={{{0,10,0}}};
        dir[]={{{0,0,10}}};
        pos[]={{{0,0,0}}};
    }};
}};
"""
                    # Create new .rvmat file
                    rvmat_file_name = f"{key}.rvmat"
                    rvmat_file_path = os.path.join(output_folder_path, rvmat_file_name)
                    
                    # Write to the file
                    with open(rvmat_file_path, "w", encoding="utf-8") as rvmat_file:
                        rvmat_file.write(rvmat_content)

        messagebox.showinfo("Success", "All RVmat files have been successfully created!")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred:\n{e}")

# Tkinter GUI
root = tk.Tk()
root.title("RVmat File Generator")

# Input folder selection
tk.Label(root, text="Folder Containing PAA Files:").grid(row=0, column=0, sticky="w")
input_folder_var = tk.StringVar()
tk.Entry(root, textvariable=input_folder_var, width=50).grid(row=0, column=1)
tk.Button(root, text="Browse", command=lambda: input_folder_var.set(filedialog.askdirectory())).grid(row=0, column=2)

# Output folder selection
tk.Label(root, text="Folder to Save RVmat Files:").grid(row=1, column=0, sticky="w")
output_folder_var = tk.StringVar()
tk.Entry(root, textvariable=output_folder_var, width=50).grid(row=1, column=1)
tk.Button(root, text="Browse", command=lambda: output_folder_var.set(filedialog.askdirectory())).grid(row=1, column=2)

# Base texture path input
tk.Label(root, text="Base Path for Textures:").grid(row=2, column=0, sticky="w")
texture_path_var = tk.StringVar()
tk.Entry(root, textvariable=texture_path_var, width=50).grid(row=2, column=1)

# Start processing button
tk.Button(root, text="Generate RVmat Files", command=process_files).grid(row=3, column=0, columnspan=3, pady=10)

# Run the application
root.mainloop()

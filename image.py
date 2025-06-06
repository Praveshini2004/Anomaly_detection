import matplotlib.pyplot as plt
import numpy as np
import os
import zipfile
import random

# === Configuration ===
base_dir = "cpu_usage_images"
normal_dir = os.path.join(base_dir, "normal")
high_dir = os.path.join(base_dir, "high")
zip_filename = "cpu_usage_graphs.zip"
num_images = 1000

# === Step 1: Create required directories ===
os.makedirs(normal_dir, exist_ok=True)
os.makedirs(high_dir, exist_ok=True)

# === Step 2: Generate synthetic CPU utilization data ===
def generate_cpu_series(high_usage=False):
    base = np.random.uniform(70, 100) if high_usage else np.random.uniform(30, 70)
    noise = np.random.normal(0, 5, 30)
    return np.clip(base + noise, 0, 100)

# === Step 3: Save plot with axes and labels ===
def save_plot(index, series, label):
    plt.figure(figsize=(5, 2))
    plt.plot(series, color='blue', linewidth=1)
    plt.ylim(0, 110)

    # More Y-axis ticks
    plt.yticks(np.arange(0, 111, 20))  # Shows 0, 10, 20, ..., 100

    plt.xlabel("Time")
    plt.ylabel("CPU Utilization (%)")
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()

    folder = high_dir if label == "high" else normal_dir
    filename = os.path.join(folder, f"{label}_{index:04d}.png")
    plt.savefig(filename)
    plt.close()


# === Step 4: Generate and save all plots ===
for i in range(num_images):
    is_high = random.random() < 0.5
    label = "high" if is_high else "normal"
    cpu_data = generate_cpu_series(high_usage=is_high)
    save_plot(i, cpu_data, label)

# === Step 5: Create ZIP file with folder structure ===
with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for label in ["normal", "high"]:
        folder_path = os.path.join(base_dir, label)
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            arcname = os.path.join(label, file_name)  # Preserve subfolder in ZIP
            zipf.write(file_path, arcname)

print(f"✅ ZIP file created: {zip_filename}")

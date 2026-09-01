import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Initialize camera
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise RuntimeError("Camera not accessible")

# CALIBRATION
known_pixel = 300     # Pixel position of reference 1
known_lambda = 546.1  # Reference 1 wavelength (nm)
ref_pixel = 100       # Pixel position of reference 2
ref_lambda = 380.0    # Reference 2 wavelength (nm)
pixel_scale = (known_lambda - ref_lambda) / (known_pixel - ref_pixel)

def pixel_to_wavelength(pixel):
    return ref_lambda + (pixel - ref_pixel) * pixel_scale

vibgyor = {
    'Violet': (380, 450, '#8F00FF'),
    'Indigo': (450, 485, '#4B0082'),
    'Blue':   (485, 500, '#0000FF'),
    'Green':  (500, 565, '#00FF00'),
    'Yellow': (565, 590, '#FFFF00'),
    'Orange': (590, 625, '#FF7F00'),
    'Red':    (625, 700, '#FF0000')
}

fig, axes = plt.subplots(7, 1, figsize=(10, 12))
plt.subplots_adjust(hspace=0.6)
fig.suptitle('Live VIBGYOR Spectrum Analysis', fontsize=14)

lines = []
for idx, (color, (low, high, hex_color)) in enumerate(vibgyor.items()):
    ax = axes[idx]
    line, = ax.plot([], [], color=hex_color, linewidth=2)
    ax.set_xlim(low, high)
    ax.set_ylim(0, 255)
    ax.set_ylabel('Intensity', fontsize=8)
    ax.set_title(color, color=hex_color, fontweight='bold', fontsize=10)
    if idx == 6:
        ax.set_xlabel('Wavelength (nm)', fontsize=10)
    ax.grid(alpha=0.3)
    lines.append(line)

def update(frame):
    ret, frame_img = cap.read()
    if not ret:
        return lines
    
    # Convert to grayscale for true spatial intensity measurement
    gray = cv2.cvtColor(frame_img, cv2.COLOR_BGR2GRAY)
    
    # Vertical spatial averaging over a 40-pixel band (reduces noise)
    h, w = gray.shape
    roi = gray[h // 2 - 20 : h // 2 + 20, :]
    intensity_row = np.mean(roi, axis=0)
    
    pixels = np.arange(w)
    wavelengths = pixel_to_wavelength(pixels)
    
    for idx, (color, (low, high, _)) in enumerate(vibgyor.items()):
        mask = (wavelengths >= low) & (wavelengths <= high)
        if np.any(mask):
            lines[idx].set_data(wavelengths[mask], intensity_row[mask])
    
    return lines

def on_close(event):
    cap.release()
    cv2.destroyAllWindows()

fig.canvas.mpl_connect('close_event', on_close)

ani = FuncAnimation(fig, update, blit=True, interval=30, cache_frame_data=False)

try:
    plt.show()
finally:
    if cap.isOpened():
        cap.release()
        cv2.destroyAllWindows()
# visual-spectrometer-graphing
An easy to set up, rudrimentary visualisation of spectrometer software.
Live VIBGYOR Spectrum Analysis

A real-time VIBGYOR spectrum analyzer built with Python, OpenCV, NumPy, and Matplotlib. The project captures live video from a webcam, converts the image into a spatial intensity profile, maps camera pixels to approximate wavelengths, and displays the resulting spectrum across the visible VIBGYOR range.


Features
Real-time webcam capture using OpenCV
VIBGYOR wavelength classification from 380–700 nm
Live intensity plots for Violet, Indigo, Blue, Green, Yellow, Orange, and Red
Pixel-to-wavelength calibration using two reference points
Vertical spatial averaging to reduce image noise
Real-time visualization using Matplotlib animation
Automatic camera cleanup when the application closes
Technologies Used
Python 3
OpenCV — webcam capture and image processing
NumPy — numerical calculations and spatial averaging
Matplotlib — real-time spectrum visualization
Project Structure
live-vibgyor-spectrum/
│
├── spectrum.py
├── README.md
└── requirements.txt

Getting Started
1. Clone the Repository
git clone https://github.com/your-username/live-vibgyor-spectrum.git
cd live-vibgyor-spectrum

2. Create a Virtual Environment
python -m venv venv


Activate it:

Windows:

venv\Scripts\activate


Linux/macOS:

source venv/bin/activate

3. Install Dependencies
pip install opencv-python numpy matplotlib


Or, if using requirements.txt:

pip install -r requirements.txt

4. Run the Program
python spectrum.py


The program will access the webcam and display the live VIBGYOR spectrum using Matplotlib.

How It Works

The application follows this processing pipeline:

Webcam
   ↓
Capture Frame
   ↓
Convert to Grayscale
   ↓
Select Horizontal ROI
   ↓
Average Pixel Intensity
   ↓
Pixel-to-Wavelength Conversion
   ↓
Separate VIBGYOR Bands
   ↓
Live Matplotlib Plots

1. Camera Capture

The webcam is initialized using OpenCV:

cap = cv2.VideoCapture(0)


The program continuously captures frames from the camera.

2. Grayscale Conversion

Each frame is converted from BGR to grayscale:

gray = cv2.cvtColor(frame_img, cv2.COLOR_BGR2GRAY)


This provides a single intensity value for each pixel.

3. Spatial Averaging

A 40-pixel-high horizontal region around the center of the frame is selected:

roi = gray[h // 2 - 20 : h // 2 + 20, :]


The intensity is averaged vertically:

intensity_row = np.mean(roi, axis=0)


This reduces random noise and produces a one-dimensional spatial intensity profile.

4. Pixel-to-Wavelength Calibration

Two reference points are used to establish a linear relationship between camera pixels and wavelength.

Current calibration values:

Reference	Pixel	Wavelength
Reference 1	300	546.1 nm
Reference 2	100	380.0 nm

The pixel scale is calculated as:

pixel_scale = (known_lambda - ref_lambda) / (known_pixel - ref_pixel)


The wavelength corresponding to a pixel is then calculated using:

wavelength = ref_lambda + (pixel - ref_pixel) * pixel_scale

5. VIBGYOR Classification

The visible spectrum is divided into approximate wavelength ranges:

Color	Wavelength Range
Violet	380–450 nm
Indigo	450–485 nm
Blue	485–500 nm
Green	500–565 nm
Yellow	565–590 nm
Orange	590–625 nm
Red	625–700 nm

Each range is plotted independently using its corresponding color.

Calibration

Calibration is one of the most important parts of this project.

The default code assumes two known spectral reference points:

known_pixel = 300
known_lambda = 546.1

ref_pixel = 100
ref_lambda = 380.0


To improve accuracy, replace these values with measurements from your own optical setup.

For example:

known_pixel = 320
known_lambda = 546.1

ref_pixel = 110
ref_lambda = 404.7


The two reference wavelengths should correspond to known spectral lines whose pixel positions can be identified in the camera image.

Important: The pixel-to-wavelength relationship is assumed to be linear. Real camera and spectrometer systems may exhibit optical distortion and nonlinear dispersion, so higher-order calibration may be required for accurate spectroscopy.

Output

The application generates seven live plots:

Violet
  ↓
Indigo
  ↓
Blue
  ↓
Green
  ↓
Yellow
  ↓
Orange
  ↓
Red


Each graph shows:

X-axis: Wavelength in nanometers
Y-axis: Grayscale intensity
Line color: Corresponding VIBGYOR color
Experimental Setup

For best results, the camera should observe a spatially separated spectrum rather than an ordinary white-light source.

A typical setup could include:

Light Source
     ↓
   Slit
     ↓
Diffraction Grating
     ↓
Dispersed Spectrum
     ↓
   Webcam
     ↓
Python Analyzer


The spectrum should be aligned horizontally so that different wavelengths appear at different horizontal pixel positions.

Limitations

This project is intended primarily as an educational and experimental spectrum visualization tool, not as a laboratory-grade spectrometer.

Important limitations include:

Webcam sensors are not calibrated scientific detectors.
Grayscale intensity does not directly represent physical optical power.
The wavelength calibration assumes a linear relationship.
Camera lens and optical geometry can introduce distortion.
Automatic exposure and white balance can affect measured intensity.
The wavelength ranges used for color classification are approximate.
Accuracy depends heavily on the optical setup and calibration quality.
The webcam's RGB response is not used; the current implementation measures grayscale intensity.
Possible Improvements
Automatic spectral-line detection
Polynomial wavelength calibration
Dark-frame and background subtraction
Automatic exposure control
Peak wavelength detection
Intensity normalization
RGB-based spectral analysis
Saving spectrum data as CSV
Exporting spectrum plots as images
GUI controls for calibration
Multiple-point calibration
Full-screen spectrum visualization
Camera selection support
Real-time wavelength peak labels
Requirements

A requirements.txt file can contain:

opencv-python
numpy
matplotlib


Install the dependencies with:

pip install -r requirements.txt

Applications

This project can be used for educational demonstrations and experiments involving:

Diffraction gratings
Visible-light spectra
Optical experiments
Spectral calibration
Physics laboratory projects
Computer vision experiments
Real-time scientific visualization
Contributing

Contributions are welcome.

Fork the repository.
Create a new branch:
git checkout -b feature/my-feature

Make your changes.
Commit your changes:
git commit -m "Add my feature"

Push the branch:
git push origin feature/my-feature

Open a Pull Request.
License

This project is open-source. You can add a license such as MIT if you want others to freely use, modify, and distribute the project.

Acknowledgements

This project uses:

OpenCV
NumPy
Matplotlib
Project Goal

The goal of this project is to demonstrate how a simple webcam and optical setup can be combined with Python-based image processing to create a real-time visualization of the visible light spectrum.

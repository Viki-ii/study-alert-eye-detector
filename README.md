# 👁️ Laptop-Based Eye Drowsiness Detection and Alert System

A real-time drowsiness detection system that monitors user's eyes using a laptop webcam and triggers an alarm when signs of drowsiness are detected. Perfect for students, drivers in simulation training, and anyone who needs to stay alert while working on a computer.

## 🎯 Features

- **Real-time Eye Detection**: Uses MediaPipe Face Mesh for accurate eye landmark detection
- **Eye Aspect Ratio (EAR) Calculation**: Scientifically proven method for drowsiness detection
- **Three-Level Status System**:
  - ✅ **Awake**: EAR > 0.25
  - ⚠️ **Drowsy**: EAR between 0.20 and 0.25
  - 🚨 **Sleeping**: EAR < 0.20 for more than 2 seconds
- **Audio Alarm**: Automatic alarm when sleeping is detected
- **Visual Feedback**: Live webcam feed with eye landmarks and status display
- **FPS Counter**: Monitor system performance
- **Clean Exit**: Press 'Q' to quit safely

## 🏗️ Project Structure

```
DDAS/
│
├── main.py                  # Main application entry point
├── eye_detector.py          # Eye detection and EAR calculation module
├── alarm.py                 # Alarm system for audio alerts
├── utils.py                 # Utility functions (EAR calculation, drawing)
├── requirements.txt         # Python dependencies
├── alarm.wav               # Alarm sound file (auto-generated if missing)
├── face_landmarker.task    # MediaPipe face detection model (required)
└── README.md               # Project documentation
```

## 📋 Requirements

- **Python**: 3.10 or higher
- **Operating System**: Windows, Linux, or macOS
- **Hardware**: Laptop with working webcam
- **Dependencies**: See `requirements.txt`

## 🚀 Installation

### Step 1: Clone or Download the Project

```bash
cd DDAS
```

### Step 2: Create Virtual Environment (Recommended)

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Verify Installation

```bash
python -c "import cv2, mediapipe, pygame; print('All dependencies installed successfully!')"
```

> Note: `face_landmarker.task` is auto-downloaded by the app on first run if missing.

## 🎮 How to Run

Simply run the main application:

```bash
python main.py
```

The system will:
1. Initialize the camera
2. Start detecting your face and eyes
3. Calculate Eye Aspect Ratio (EAR) in real-time
4. Display status on screen
5. Trigger alarm if you fall asleep for more than 2 seconds

## 📊 How It Works

### Eye Aspect Ratio (EAR) Formula

The system uses the Eye Aspect Ratio algorithm:

```
EAR = (|p2-p6| + |p3-p5|) / (2 * |p1-p4|)
```

Where p1-p6 are the six eye landmark points detected by MediaPipe.

### Detection Logic

1. **Face Detection**: MediaPipe Face Mesh detects face and 468 facial landmarks
2. **Eye Extraction**: Extract 6 landmarks for each eye (12 total)
3. **EAR Calculation**: Calculate EAR for both left and right eyes
4. **Average EAR**: Take average of both eyes
5. **Status Determination**:
   - If EAR > 0.25 → Awake
   - If 0.20 < EAR ≤ 0.25 → Drowsy
   - If EAR ≤ 0.20 → Sleeping candidate
6. **Time Threshold**: If EAR ≤ 0.20 for 2+ seconds → Trigger alarm

### Key Components

#### 1. `utils.py`
- `calculate_ear()`: Computes Eye Aspect Ratio
- `get_eye_landmarks()`: Extracts eye landmarks from face mesh
- `draw_eye_landmarks()`: Visualizes eye landmarks on frame
- `get_status_color()`: Returns color based on status

#### 2. `eye_detector.py`
- `EyeDetector` class: Main eye detection engine
- Uses MediaPipe Face Mesh for landmark detection
- Processes frames and calculates EAR
- Determines drowsiness status

#### 3. `alarm.py`
- `AlarmSystem` class: Manages audio alerts
- Plays alarm sound in loop when sleeping detected
- Auto-generates default beep sound if alarm.wav missing
- Thread-safe alarm control

#### 4. `main.py`
- `DrowsinessDetectionSystem` class: Integrates all components
- Manages webcam capture
- Handles UI rendering
- Controls program flow

## 🎨 User Interface

The system displays:

- **Status**: Current state (Awake/Drowsy/Sleeping)
- **EAR Value**: Current Eye Aspect Ratio
- **FPS**: Frames per second
- **Timer**: Duration of eye closure (when drowsy/sleeping)
- **Alarm Indicator**: Shows when alarm is active
- **Eye Landmarks**: Green dots showing detected eye points
- **Instructions**: Keyboard controls

## ⚙️ Configuration

You can adjust these parameters in the code:

**In `eye_detector.py`:**
```python
EAR_THRESHOLD_AWAKE = 0.25    # Threshold for awake state
EAR_THRESHOLD_DROWSY = 0.20   # Threshold for drowsy state
```

**In `main.py`:**
```python
SLEEP_TIME_THRESHOLD = 2.0    # Seconds before alarm (default: 2)
```

## 🛠️ Technologies Used

| Technology | Purpose |
|------------|---------|
| **Python** | Core programming language |
| **OpenCV** | Video capture and image processing |
| **MediaPipe** | Face and eye landmark detection (Tasks API) |
| **NumPy** | Numerical computations |
| **SciPy** | Euclidean distance calculations |
| **Pygame** | Audio playback |

**Note:** This project uses the new MediaPipe Tasks API (v0.10+) which requires the `face_landmarker.task` model file.

## 📸 Screenshots

### System in Action
*Add your screenshots here after running the application*

**Awake State:**
- Green status indicator
- EAR value > 0.25
- Eye landmarks visible

**Drowsy State:**
- Yellow status indicator
- EAR value between 0.20-0.25
- Timer counting up

**Sleeping State:**
- Red status indicator
- EAR value < 0.20
- Alarm triggered
- Warning message displayed

## 🔧 Troubleshooting

### Camera Not Working
```python
# Try different camera index in main.py
system.start_camera(camera_index=1)  # Try 0, 1, 2...
```

### No Face Detected
- Ensure adequate lighting
- Position face directly in front of camera
- Remove objects obstructing face
- Adjust camera angle

### Alarm Not Playing
- Check if `alarm.wav` exists
- System auto-generates default if missing
- Verify pygame installation: `pip install --upgrade pygame`

### Low FPS
- Close other applications
- Reduce camera resolution in `main.py`:
```python
self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
```

### Import Errors
```bash
# Reinstall all dependencies
pip install --force-reinstall -r requirements.txt
```

## ☁️ Upload to GitHub (Best Practice)

### Additional Requirements Before Upload
- Install Git: https://git-scm.com/downloads
- Create a GitHub account and a new empty repository
- (Optional) Install GitHub CLI: https://cli.github.com/

### Step-by-Step Instructions

1. Open terminal in project folder:
```bash
cd "E:\vishnu\s6\course project\DDAS"
```

2. Initialize Git and create first commit:
```bash
git init
git add .
git commit -m "Initial commit: eye drowsiness detection system"
```

3. Rename default branch to `main`:
```bash
git branch -M main
```

4. Connect your GitHub repository:
```bash
git remote add origin https://github.com/<your-username>/<your-repo-name>.git
```

5. Push project:
```bash
git push -u origin main
```

### What Was Added for a Better GitHub Repo
- `.gitignore` to avoid uploading local env/cache files
- `.github/workflows/ci.yml` to auto-check imports on every push/PR
- Auto-download of `face_landmarker.task` (so large model file is not required in repo)

### Recommended Next Improvements
- Add screenshots/gif in the Screenshots section
- Add LICENSE (MIT recommended)
- Add repository topics: `python`, `opencv`, `mediapipe`, `drowsiness-detection`

## 🎓 Use Cases

- **Students**: Stay alert during long study sessions
- **Remote Workers**: Prevent fatigue during work-from-home
- **Researchers**: Study sleep patterns and drowsiness
- **Drivers**: Training simulation for drowsy driving prevention
- **Healthcare**: Monitor patient alertness

## 🔬 Research Background

The Eye Aspect Ratio (EAR) method was introduced in the paper:
> "Real-Time Eye Blink Detection using Facial Landmarks" by Tereza Soukupová and Jan Čech

It's a simple yet effective algorithm that:
- Operates in real-time
- Works with standard webcams
- Requires no specialized hardware
- Has high accuracy (>95% in good conditions)

## 📝 License

This project is open source and available for educational and personal use.

## 🤝 Contributing

Suggestions and improvements are welcome! Potential enhancements:
- Add yawn detection
- Head pose estimation
- Multiple face detection
- Mobile app version
- Cloud logging and analytics
- Customizable alarm sounds

## 📧 Support

If you encounter issues:
1. Check the Troubleshooting section
2. Verify all dependencies are installed
3. Ensure Python version is 3.10+
4. Check camera permissions in your OS

## 🎉 Acknowledgments

- MediaPipe team for the amazing Face Mesh model
- OpenCV community for computer vision tools
- Original EAR research by Soukupová & Čech

---

**Made with ❤️ for safer and more alert computing**

*Last Updated: February 2026*

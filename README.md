Gesture-Based Smart Presentation Assistant
Overview
The Gesture-Based Smart Presentation Assistant is an advanced Python application designed to control PowerPoint or Google Slides presentations through hand gestures and facial authentication. Utilizing computer vision and machine learning, the system authenticates presenters, enables gesture-based slide navigation, and provides real-time feedback. Additional features include webcam calibration for accuracy and an optional emotion-based pause mechanism, enhancing the interactivity and accessibility of presentations.
Key Features

Facial Authentication: Verifies presenter identity using DeepFace or MediaPipe Face Mesh, ensuring secure control access.
Gesture-Based Control: Supports four hand gestures (Next Slide, Previous Slide, Start Presentation, End Presentation) via MediaPipe Hands.
Real-Time Feedback: Displays presenter name and gesture status (e.g., "Next Slide ✔") on-screen for seamless interaction.
Camera Calibration: Employs OpenCV with a chessboard pattern to calibrate the webcam, minimizing distortion and enhancing gesture detection.
Emotion-Based Pause (Optional): Detects presenter confusion through facial emotion analysis, pausing the presentation with a "Paused due to confusion" message until expression change.
Bonus Features (Planned):
Voice feedback for gesture actions (e.g., "Next slide activated").
Integration with PowerPoint API or browser automation tools.
Customizable gesture training mode.



Prerequisites

Python 3.8 or higher
Webcam (built-in or external)
PowerPoint or Google Slides installed
Chessboard pattern image for calibration

Installation

Clone the Repository:
git clone https://github.com/rewaaalaa7/Gesture-Based-Smart-Presentation-Assistant.git
cd Gesture-Based-Smart-Presentation-Assistant


Create a Virtual Environment:
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


Install Dependencies:
pip install -r requirements.txt

Required libraries:

opencv-python
mediapipe
deepface
numpy
pyautogui


Prepare Assets:

Place a chessboard pattern image in the Resources directory for calibration.
Ensure PowerPoint or Google Slides is set up for presentation control.



Usage

Calibrate the Webcam:
python calibrate_camera.py


Follow prompts to use a chessboard pattern for calibration.


Launch the Application:
python main.py


Operation:

Authentication: Position your face in front of the webcam for identity verification.
Gestures:
Next Slide: Extend index and middle fingers (others folded).
Previous Slide: Extend little finger (others folded).
Start Presentation: Open palm facing camera.
End Presentation: Closed fist.


Feedback: Presenter name and gesture status appear on-screen.
Emotion-Pause (Optional): Presentation pauses if confusion is detected, resuming upon expression change.
Press q to exit.


Configuration:

Modify gesture thresholds or webcam settings in main.py for optimal performance.
Ensure adequate lighting and clear webcam view.



Project Structure

main.py: Core script for authentication, gesture recognition, and presentation control.
calibrate_camera.py: Script for webcam calibration.
Resources/: Directory for calibration images and optional presentation assets.
requirements.txt: List of Python dependencies.

Dependencies

opencv-python: Handles webcam access, image processing, and calibration.
mediapipe: Enables hand gesture and face mesh detection.
deepface: Supports facial authentication and optional emotion detection.
numpy: Facilitates efficient data processing.
pyautogui: Simulates keyboard inputs for slide control.

Contributing
Contributions are encouraged! To contribute:

Fork the repository.
Create a feature branch (git checkout -b feature-branch).
Submit a pull request with a detailed description of your changes.

License
This project is licensed under the MIT License. See the LICENSE file for details.
Contact
For inquiries or feedback, please use GitHub Issues or connect via LinkedIn.

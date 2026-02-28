"""
Eye detection module using MediaPipe Face Landmarker
"""

import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import os
import urllib.request
from utils import calculate_ear, get_eye_landmarks_new, draw_eye_landmarks


class EyeDetector:
    """
    Eye detector class for detecting drowsiness using Eye Aspect Ratio
    """
    
    # EAR thresholds
    EAR_THRESHOLD_AWAKE = 0.25
    EAR_THRESHOLD_DROWSY = 0.20
    MODEL_PATH = "face_landmarker.task"
    MODEL_URL = "https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task"
    
    def __init__(self):
        """Initialize MediaPipe Face Landmarker"""
        self._ensure_model_exists()

        # Set up Face Landmarker options
        base_options = python.BaseOptions(model_asset_path=self.MODEL_PATH)
        options = vision.FaceLandmarkerOptions(
            base_options=base_options,
            output_face_blendshapes=False,
            output_facial_transformation_matrixes=False,
            num_faces=1
        )
        
        self.detector = vision.FaceLandmarker.create_from_options(options)
        
        # State variables
        self.current_ear = 0.0
        self.current_status = "Awake"

    def _ensure_model_exists(self):
        """Download MediaPipe face landmarker model automatically if missing."""
        if os.path.exists(self.MODEL_PATH):
            return

        print("Model file not found. Downloading face_landmarker.task...")
        try:
            urllib.request.urlretrieve(self.MODEL_URL, self.MODEL_PATH)
            print("Model downloaded successfully.")
        except Exception as error:
            raise RuntimeError(
                "Failed to download face_landmarker.task. "
                "Please check internet connection and rerun."
            ) from error
        
    def detect_eyes(self, frame):
        """
        Detect eyes in the frame and calculate EAR
        
        Args:
            frame: OpenCV image frame (BGR)
            
        Returns:
            tuple: (success, left_ear, right_ear, face_landmarks)
        """
        # Convert BGR to RGB for MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Create MediaPipe Image object
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        
        # Detect face landmarks
        detection_result = self.detector.detect(mp_image)
        
        # Check if face detected
        if not detection_result.face_landmarks:
            return False, 0.0, 0.0, None
        
        # Get the first face landmarks
        face_landmarks = detection_result.face_landmarks[0]
        
        # Extract left and right eye landmarks
        left_eye = get_eye_landmarks_new(face_landmarks, 'left')
        right_eye = get_eye_landmarks_new(face_landmarks, 'right')
        
        # Calculate EAR for both eyes
        left_ear = calculate_ear(left_eye)
        right_ear = calculate_ear(right_eye)
        
        return True, left_ear, right_ear, face_landmarks
    
    def get_average_ear(self, left_ear, right_ear):
        """
        Calculate average EAR from both eyes
        
        Args:
            left_ear: Left eye EAR
            right_ear: Right eye EAR
            
        Returns:
            float: Average EAR
        """
        return (left_ear + right_ear) / 2.0
    
    def determine_status(self, ear):
        """
        Determine eye status based on EAR value
        
        Args:
            ear: Eye Aspect Ratio value
            
        Returns:
            str: Status ('Awake', 'Drowsy', or 'Sleeping')
        """
        if ear > self.EAR_THRESHOLD_AWAKE:
            return "Awake"
        elif ear > self.EAR_THRESHOLD_DROWSY:
            return "Drowsy"
        else:
            return "Sleeping"
    
    def draw_landmarks(self, frame, face_landmarks):
        """
        Draw face landmarks on frame
        
        Args:
            frame: OpenCV image frame
            face_landmarks: MediaPipe face landmarks
            
        Returns:
            frame: Frame with drawn landmarks
        """
        # Extract and draw left eye landmarks
        left_eye = get_eye_landmarks_new(face_landmarks, 'left')
        frame = draw_eye_landmarks(frame, left_eye, (0, 255, 0))
        
        # Extract and draw right eye landmarks
        right_eye = get_eye_landmarks_new(face_landmarks, 'right')
        frame = draw_eye_landmarks(frame, right_eye, (0, 255, 0))
        
        return frame
    
    def process_frame(self, frame):
        """
        Process frame and return detection results
        
        Args:
            frame: OpenCV image frame
            
        Returns:
            tuple: (processed_frame, ear_value, status, face_detected)
        """
        # Detect eyes
        success, left_ear, right_ear, face_landmarks = self.detect_eyes(frame)
        
        if not success:
            # No face detected
            cv2.putText(frame, "No face detected", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            return frame, 0.0, "No Face", False
        
        # Calculate average EAR
        avg_ear = self.get_average_ear(left_ear, right_ear)
        self.current_ear = avg_ear
        
        # Determine status
        status = self.determine_status(avg_ear)
        self.current_status = status
        
        # Draw eye landmarks
        frame = self.draw_landmarks(frame, face_landmarks)
        
        return frame, avg_ear, status, True
    
    def release(self):
        """Release resources"""
        pass  # New API handles cleanup automatically

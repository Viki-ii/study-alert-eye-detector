"""
Utility functions for eye drowsiness detection
"""

import numpy as np
from scipy.spatial import distance


def calculate_ear(eye_landmarks):
    """
    Calculate Eye Aspect Ratio (EAR) for drowsiness detection
    
    EAR Formula:
    EAR = (|p2-p6| + |p3-p5|) / (2 * |p1-p4|)
    
    Where p1-p6 are the eye landmark points
    
    Args:
        eye_landmarks: Array of 6 eye landmark points [(x1,y1), (x2,y2), ...]
        
    Returns:
        float: Eye Aspect Ratio value
    """
    # Compute the euclidean distances between the vertical eye landmarks
    vertical_1 = distance.euclidean(eye_landmarks[1], eye_landmarks[5])
    vertical_2 = distance.euclidean(eye_landmarks[2], eye_landmarks[4])
    
    # Compute the euclidean distance between the horizontal eye landmarks
    horizontal = distance.euclidean(eye_landmarks[0], eye_landmarks[3])
    
    # Calculate the eye aspect ratio
    ear = (vertical_1 + vertical_2) / (2.0 * horizontal)
    
    return ear


def get_eye_landmarks(face_landmarks, eye_type='left'):
    """
    Extract eye landmarks from face landmarks (Old MediaPipe API)
    
    Args:
        face_landmarks: MediaPipe face landmarks object
        eye_type: 'left' or 'right' eye
        
    Returns:
        list: List of 6 eye landmark coordinates
    """
    # MediaPipe face mesh indices for eyes
    LEFT_EYE_INDICES = [33, 160, 158, 133, 153, 144]
    RIGHT_EYE_INDICES = [362, 385, 387, 263, 373, 380]
    
    if eye_type == 'left':
        indices = LEFT_EYE_INDICES
    else:
        indices = RIGHT_EYE_INDICES
    
    eye_points = []
    for idx in indices:
        landmark = face_landmarks.landmark[idx]
        eye_points.append((landmark.x, landmark.y))
    
    return eye_points


def get_eye_landmarks_new(face_landmarks, eye_type='left'):
    """
    Extract eye landmarks from face landmarks (New MediaPipe Tasks API)
    
    Args:
        face_landmarks: List of MediaPipe NormalizedLandmark objects
        eye_type: 'left' or 'right' eye
        
    Returns:
        list: List of 6 eye landmark coordinates
    """
    # MediaPipe face mesh indices for eyes
    LEFT_EYE_INDICES = [33, 160, 158, 133, 153, 144]
    RIGHT_EYE_INDICES = [362, 385, 387, 263, 373, 380]
    
    if eye_type == 'left':
        indices = LEFT_EYE_INDICES
    else:
        indices = RIGHT_EYE_INDICES
    
    eye_points = []
    for idx in indices:
        landmark = face_landmarks[idx]
        eye_points.append((landmark.x, landmark.y))
    
    return eye_points


def draw_eye_landmarks(frame, eye_landmarks, color=(0, 255, 0)):
    """
    Draw eye landmarks on the frame
    
    Args:
        frame: OpenCV image frame
        eye_landmarks: List of eye landmark coordinates (normalized 0-1)
        color: BGR color tuple
        
    Returns:
        frame: Frame with drawn landmarks
    """
    import cv2
    
    h, w = frame.shape[:2]
    
    # Draw circles at each landmark point
    for (x, y) in eye_landmarks:
        # Convert normalized coordinates to pixel coordinates
        cx = int(x * w)
        cy = int(y * h)
        cv2.circle(frame, (cx, cy), 2, color, -1)
    
    # Draw lines connecting the landmarks
    points = [(int(x * w), int(y * h)) for (x, y) in eye_landmarks]
    for i in range(len(points)):
        if i == 0:
            cv2.line(frame, points[i], points[3], color, 1)
        elif i < 3:
            cv2.line(frame, points[i], points[i+3], color, 1)
    
    return frame


def get_status_color(status):
    """
    Get color for different status states
    
    Args:
        status: Status string ('Awake', 'Drowsy', 'Sleeping')
        
    Returns:
        tuple: BGR color tuple
    """
    colors = {
        'Awake': (0, 255, 0),      # Green
        'Drowsy': (0, 255, 255),   # Yellow
        'Sleeping': (0, 0, 255)    # Red
    }
    return colors.get(status, (255, 255, 255))

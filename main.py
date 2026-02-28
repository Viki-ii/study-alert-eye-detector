"""
Laptop-Based Eye Drowsiness Detection and Alert System

Main application that detects drowsiness by monitoring eye closure
and triggers an alarm when the user falls asleep.
"""

import cv2
import time
from eye_detector import EyeDetector
from alarm import AlarmSystem
from utils import get_status_color


class DrowsinessDetectionSystem:
    """
    Main drowsiness detection system
    """
    
    # Time threshold for detecting sleep (in seconds)
    SLEEP_TIME_THRESHOLD = 2.0
    
    def __init__(self):
        """Initialize the drowsiness detection system"""
        print("Initializing Drowsiness Detection System...")
        
        # Initialize components
        self.eye_detector = EyeDetector()
        self.alarm = AlarmSystem()
        self.cap = None
        
        # State variables
        self.sleeping_start_time = None
        self.is_sleeping = False
        self.frame_count = 0
        self.fps = 0
        self.fps_start_time = time.time()
        
        print("System initialized successfully!")
    
    def start_camera(self, camera_index=0):
        """
        Start the webcam
        
        Args:
            camera_index: Index of the camera (default: 0)
            
        Returns:
            bool: True if camera started successfully
        """
        print(f"Starting camera {camera_index}...")
        self.cap = cv2.VideoCapture(camera_index)
        
        if not self.cap.isOpened():
            print("Error: Could not open camera!")
            return False
        
        # Set camera properties for better performance
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        print("Camera started successfully!")
        return True
    
    def calculate_fps(self):
        """Calculate and update FPS"""
        self.frame_count += 1
        
        if self.frame_count >= 30:
            end_time = time.time()
            self.fps = self.frame_count / (end_time - self.fps_start_time)
            self.fps_start_time = end_time
            self.frame_count = 0
    
    def check_drowsiness(self, status):
        """
        Check if user is sleeping and manage alarm
        
        Args:
            status: Current eye status ('Awake', 'Drowsy', 'Sleeping')
        """
        current_time = time.time()
        
        if status == "Sleeping":
            # User's eyes are closed
            if self.sleeping_start_time is None:
                # Start tracking sleep time
                self.sleeping_start_time = current_time
            else:
                # Check how long eyes have been closed
                sleep_duration = current_time - self.sleeping_start_time
                
                if sleep_duration >= self.SLEEP_TIME_THRESHOLD:
                    # User has been sleeping for more than threshold
                    if not self.is_sleeping:
                        self.is_sleeping = True
                        print(f"\n⚠️  SLEEPING DETECTED! (Duration: {sleep_duration:.1f}s)")
                    
                    # Start alarm
                    if not self.alarm.is_alarm_playing():
                        self.alarm.start_alarm()
        else:
            # User is awake or drowsy - reset sleep tracking
            if self.sleeping_start_time is not None or self.is_sleeping:
                # User woke up
                if self.is_sleeping:
                    print("\n✓ User is awake now")
                
                self.sleeping_start_time = None
                self.is_sleeping = False
                
                # Stop alarm
                if self.alarm.is_alarm_playing():
                    self.alarm.stop_alarm()
    
    def draw_ui(self, frame, ear, status, face_detected):
        """
        Draw user interface elements on frame
        
        Args:
            frame: OpenCV image frame
            ear: Eye Aspect Ratio value
            status: Current status string
            face_detected: Whether face was detected
            
        Returns:
            frame: Frame with UI elements
        """
        h, w = frame.shape[:2]
        
        # Semi-transparent overlay for text background
        overlay = frame.copy()
        
        # Status box at top
        status_color = get_status_color(status)
        cv2.rectangle(overlay, (0, 0), (w, 100), (0, 0, 0), -1)
        frame = cv2.addWeighted(frame, 0.7, overlay, 0.3, 0)
        
        # Display status text
        cv2.putText(frame, f"Status: {status}", (10, 35),
                   cv2.FONT_HERSHEY_SIMPLEX, 1.0, status_color, 2)
        
        # Display EAR value
        if face_detected:
            ear_text = f"EAR: {ear:.3f}"
            cv2.putText(frame, ear_text, (10, 70),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Display FPS
        fps_text = f"FPS: {self.fps:.1f}"
        cv2.putText(frame, fps_text, (w - 120, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # Display sleep timer if drowsy/sleeping
        if self.sleeping_start_time is not None:
            sleep_duration = time.time() - self.sleeping_start_time
            timer_text = f"Closed: {sleep_duration:.1f}s"
            timer_color = (0, 165, 255) if sleep_duration < self.SLEEP_TIME_THRESHOLD else (0, 0, 255)
            cv2.putText(frame, timer_text, (w - 180, 70),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, timer_color, 2)
        
        # Alarm indicator
        if self.alarm.is_alarm_playing():
            cv2.putText(frame, "🚨 ALARM ON", (w // 2 - 100, h - 20),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        
        # Instructions at bottom
        cv2.putText(frame, "Press 'Q' to quit", (10, h - 20),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
        
        return frame
    
    def run(self):
        """
        Main loop for drowsiness detection
        """
        if not self.start_camera():
            return
        
        print("\n" + "="*60)
        print("DROWSINESS DETECTION SYSTEM RUNNING")
        print("="*60)
        print("Instructions:")
        print("  - Look at the camera")
        print("  - Press 'Q' to quit")
        print("  - Alarm will sound if you close your eyes for 2+ seconds")
        print("="*60 + "\n")
        
        try:
            while True:
                # Read frame from camera
                ret, frame = self.cap.read()
                
                if not ret:
                    print("Error: Failed to read frame from camera")
                    break
                
                # Flip frame horizontally for mirror effect
                frame = cv2.flip(frame, 1)
                
                # Process frame and detect eyes
                processed_frame, ear, status, face_detected = self.eye_detector.process_frame(frame)
                
                # Check for drowsiness and manage alarm
                if face_detected:
                    self.check_drowsiness(status)
                
                # Calculate FPS
                self.calculate_fps()
                
                # Draw UI elements
                display_frame = self.draw_ui(processed_frame, ear, status, face_detected)
                
                # Display the frame
                cv2.imshow('Drowsiness Detection System', display_frame)
                
                # Check for quit key
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q') or key == ord('Q'):
                    print("\nQuitting...")
                    break
                
        except KeyboardInterrupt:
            print("\n\nInterrupted by user")
        
        except Exception as e:
            print(f"\nError occurred: {e}")
            import traceback
            traceback.print_exc()
        
        finally:
            self.cleanup()
    
    def cleanup(self):
        """
        Clean up resources
        """
        print("\nCleaning up resources...")
        
        # Stop alarm
        if self.alarm:
            self.alarm.cleanup()
        
        # Release camera
        if self.cap:
            self.cap.release()
        
        # Close windows
        cv2.destroyAllWindows()
        
        # Release eye detector
        if self.eye_detector:
            self.eye_detector.release()
        
        print("Cleanup complete. Goodbye!")


def main():
    """
    Entry point of the application
    """
    print("\n" + "="*60)
    print("  LAPTOP-BASED EYE DROWSINESS DETECTION AND ALERT SYSTEM")
    print("="*60 + "\n")
    
    # Create and run the system
    system = DrowsinessDetectionSystem()
    system.run()


if __name__ == "__main__":
    main()

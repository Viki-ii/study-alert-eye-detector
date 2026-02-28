"""
Alarm module for playing alert sounds
"""

import os
import threading
import pygame


class AlarmSystem:
    """
    Alarm system class for playing and stopping alarm sounds
    """
    
    def __init__(self, alarm_file='alarm.wav'):
        """
        Initialize the alarm system
        
        Args:
            alarm_file: Path to the alarm sound file
        """
        self.alarm_file = alarm_file
        self.is_playing = False
        self.alarm_thread = None
        
        # Initialize pygame mixer
        pygame.mixer.init()
        
        # Check if alarm file exists
        if not os.path.exists(self.alarm_file):
            print(f"Warning: Alarm file '{self.alarm_file}' not found!")
            print("Creating a default beep sound...")
            self._create_default_alarm()
    
    def _create_default_alarm(self):
        """
        Create a default beep sound if alarm file doesn't exist
        """
        try:
            import numpy as np
            from scipy.io import wavfile
            
            # Generate a simple beep sound
            sample_rate = 44100
            duration = 1.0  # seconds
            frequency = 1000  # Hz
            
            # Generate sine wave
            t = np.linspace(0, duration, int(sample_rate * duration))
            # Create a beep pattern (on for 0.2s, off for 0.2s)
            beep = np.sin(2 * np.pi * frequency * t)
            
            # Apply amplitude envelope for beeping effect
            for i in range(len(beep)):
                cycle_pos = (i / sample_rate) % 0.4
                if cycle_pos > 0.2:
                    beep[i] = 0
            
            # Normalize and convert to 16-bit
            beep = beep * 32767
            beep = beep.astype(np.int16)
            
            # Save as WAV file
            wavfile.write(self.alarm_file, sample_rate, beep)
            print(f"Created default alarm file: {self.alarm_file}")
            
        except Exception as e:
            print(f"Error creating default alarm: {e}")
    
    def _play_alarm_loop(self):
        """
        Internal method to play alarm in a loop
        """
        try:
            # Load and play the sound
            pygame.mixer.music.load(self.alarm_file)
            pygame.mixer.music.play(-1)  # -1 means loop indefinitely
            
            # Keep the thread alive while alarm is playing
            while self.is_playing:
                pygame.time.wait(100)
                
        except Exception as e:
            print(f"Error playing alarm: {e}")
    
    def start_alarm(self):
        """
        Start playing the alarm sound
        """
        if not self.is_playing:
            self.is_playing = True
            
            # Start alarm in a separate thread
            self.alarm_thread = threading.Thread(target=self._play_alarm_loop, daemon=True)
            self.alarm_thread.start()
            
            print("🚨 ALARM STARTED!")
    
    def stop_alarm(self):
        """
        Stop playing the alarm sound
        """
        if self.is_playing:
            self.is_playing = False
            
            # Stop the music
            pygame.mixer.music.stop()
            
            # Wait for thread to finish
            if self.alarm_thread and self.alarm_thread.is_alive():
                self.alarm_thread.join(timeout=1.0)
            
            print("✓ Alarm stopped")
    
    def is_alarm_playing(self):
        """
        Check if alarm is currently playing
        
        Returns:
            bool: True if alarm is playing, False otherwise
        """
        return self.is_playing
    
    def cleanup(self):
        """
        Clean up resources
        """
        self.stop_alarm()
        pygame.mixer.quit()


# Simple test function
if __name__ == "__main__":
    import time
    
    print("Testing alarm system...")
    
    alarm = AlarmSystem()
    
    print("Playing alarm for 3 seconds...")
    alarm.start_alarm()
    time.sleep(3)
    
    print("Stopping alarm...")
    alarm.stop_alarm()
    time.sleep(1)
    
    print("Playing alarm again for 2 seconds...")
    alarm.start_alarm()
    time.sleep(2)
    
    alarm.cleanup()
    print("Test complete!")

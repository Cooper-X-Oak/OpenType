import pyaudio
import wave
import threading
import numpy as np
from PySide6.QtCore import QObject, Signal
from src.utils.logger import logger

class AudioRecorder(QObject):
    audio_level_changed = Signal(float)

    def __init__(self, sample_rate=16000, channels=1, bits_per_sample=16, device_index=None):
        super().__init__()
        self.sample_rate = sample_rate
        self.channels = channels
        self.bits_per_sample = bits_per_sample
        self.chunk_size = 1024
        self.device_index = device_index
        
        self.p = pyaudio.PyAudio()
        self.stream = None
        self.recording = False
        self.audio_data = bytearray()
        self.lock = threading.Lock()
        
        # Audio format mapping
        self.format_map = {
            8: pyaudio.paInt8,
            16: pyaudio.paInt16,
            24: pyaudio.paInt24,
            32: pyaudio.paInt32
        }
        
        if self.bits_per_sample not in self.format_map:
             raise ValueError(f"Unsupported bits per sample: {self.bits_per_sample}")
        
        self.pa_format = self.format_map[self.bits_per_sample]

        # Log available input devices
        logger.info("Available Audio Input Devices:")
        try:
            for i in range(self.p.get_device_count()):
                dev = self.p.get_device_info_by_index(i)
                if dev['maxInputChannels'] > 0:
                    logger.info(f"  [{i}] {dev['name']}")
        except Exception as e:
            logger.error(f"Failed to list audio devices: {e}")

    def _callback(self, in_data, frame_count, time_info, status):
        if self.recording:
            # Calculate audio level
            try:
                if self.bits_per_sample == 16:
                    audio_array = np.frombuffer(in_data, dtype=np.int16)
                    # Calculate RMS
                    rms = np.sqrt(np.mean(audio_array.astype(np.float32)**2))
                    # Normalize (adjust divisor based on sensitivity needs)
                    # 3000 is a reasonable baseline for speech detection threshold, 
                    # 15000 is loud speech.
                    level = min(1.0, rms / 10000.0)
                    self.audio_level_changed.emit(level)
            except Exception as e:
                # Don't log every frame to avoid spam, but good to know
                pass

            with self.lock:
                self.audio_data.extend(in_data)
            return (in_data, pyaudio.paContinue)
        else:
            return (None, pyaudio.paComplete)

    def start(self):
        if self.recording:
            return
            
        logger.info("Starting recording...")
        self.audio_data = bytearray()
        self.recording = True
        
        try:
            self.stream = self.p.open(
                format=self.pa_format,
                channels=self.channels,
                rate=self.sample_rate,
                input=True,
                input_device_index=self.device_index,
                frames_per_buffer=self.chunk_size,
                stream_callback=self._callback
            )
            self.stream.start_stream()
        except Exception as e:
            logger.error(f"Error starting recording: {e}")
            self.stop()
            raise

    def stop(self):
        if not self.recording:
            return

        logger.info("Stopping recording...")
        self.recording = False
        
        if self.stream:
            if self.stream.is_active():
                self.stream.stop_stream()
            self.stream.close()
            self.stream = None

    def get_audio_data(self):
        with self.lock:
            return bytes(self.audio_data)

    def save_wav(self, filename):
        data = self.get_audio_data()
        if not data:
            logger.warning("No audio data to save.")
            return

        logger.info(f"Saving {len(data)} bytes to {filename}")
        try:
            with wave.open(filename, 'wb') as wf:
                wf.setnchannels(self.channels)
                wf.setsampwidth(self.p.get_sample_size(self.pa_format))
                wf.setframerate(self.sample_rate)
                wf.writeframes(data)
        except Exception as e:
            logger.error(f"Error saving WAV file: {e}")
            
    def close(self):
        self.stop()
        self.p.terminate()

if __name__ == "__main__":
    # Simple test
    recorder = AudioRecorder()
    print("Press Enter to start recording...")
    input()
    recorder.start()
    print("Recording... Press Enter to stop.")
    input()
    recorder.stop()
    recorder.save_wav("test_recording.wav")
    print("Saved to test_recording.wav")
    recorder.close()

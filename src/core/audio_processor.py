import numpy as np
import audioop

def normalize_audio(audio_data, target_dBFS=-20.0):
    """
    对音频数据进行归一化处理
    """
    if not audio_data:
        return audio_data

    # Convert to numpy array for easier calculation if needed, 
    # but audioop is sufficient for PCM
    
    # Calculate current RMS
    # 2 means 16-bit (2 bytes)
    rms = audioop.rms(audio_data, 2)
    
    if rms == 0:
        return audio_data

    # Calculate current dBFS
    # Max possible RMS for 16-bit is 32767
    max_possible_rms = 32767
    current_dBFS = 20 * np.log10(rms / max_possible_rms)
    
    # Calculate gain needed
    gain = target_dBFS - current_dBFS
    factor = 10 ** (gain / 20)
    
    # Apply gain using audioop.mul
    # audioop.mul takes a factor, but it's not exactly float multiplication
    # It's better to use numpy for precise float multiplication then convert back
    
    # Convert bytes to numpy array
    audio_array = np.frombuffer(audio_data, dtype=np.int16)
    
    # Apply gain
    audio_array = audio_array * factor
    
    # Clip to avoid overflow
    audio_array = np.clip(audio_array, -32768, 32767)
    
    # Convert back to bytes
    normalized_data = audio_array.astype(np.int16).tobytes()
    
    return normalized_data

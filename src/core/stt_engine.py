import os
import dashscope
from dashscope.audio.asr import Recognition
from http import HTTPStatus
from src.utils.logger import logger

class STTEngine:
    def __init__(self, api_key=None):
        self.api_key = api_key
        # Use paraformer-v1 (offline/file mode) for faster one-shot recognition
        # paraformer-realtime-v1 is better for streaming but might be slower for file upload due to connection overhead
        self.model = 'paraformer-v1' 
        
    def set_api_key(self, api_key):
        self.api_key = api_key
        dashscope.api_key = api_key

    def recognize(self, audio_data, format='pcm', sample_rate=16000):
        """
        Recognize speech from audio data (bytes)
        """
        if not self.api_key:
            logger.error("API Key not set for STTEngine")
            return None, "API Key not set"

        try:
            logger.info(f"Sending audio to DashScope ({len(audio_data)} bytes)...")
            
            # Create a temporary file or use bytes directly if supported?
            # DashScope Python SDK supports file path or url.
            # Let's check if it supports bytes.
            # It seems Recognition.call takes 'file' argument which can be a path.
            # It might not take bytes directly in 'file'.
            # However, for 'paraformer-realtime-v1', it supports stream.
            # For 'paraformer-v1', let's use a temp file to be safe.
            
            # Actually, let's try to pass bytes if possible, but temp file is safer.
            import tempfile
            
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_audio:
                import wave
                with wave.open(temp_audio.name, 'wb') as wf:
                    wf.setnchannels(1)
                    wf.setsampwidth(2) # 16-bit
                    wf.setframerate(sample_rate)
                    wf.writeframes(audio_data)
                temp_path = temp_audio.name

            try:
                # Use Recognition class correctly: instantiate with callback=None, then call with file
                # This works for paraformer-realtime-v1 in recent SDKs
                recognition = Recognition(model=self.model, format='wav', sample_rate=sample_rate, callback=None)
                response = recognition.call(temp_path)
                
                if response.status_code == HTTPStatus.OK:
                    logger.info("Recognition successful")
                    logger.info(f"Response output type: {type(response.output)}")
                    logger.debug(f"Response output: {response.output}")
                    
                    if response.output:
                        text = ""
                        try:
                            # Handle 'sentence' field
                            if 'sentence' in response.output:
                                sent = response.output['sentence']
                                if isinstance(sent, list):
                                    text = "".join([s.get('text', '') for s in sent if isinstance(s, dict)])
                                elif isinstance(sent, dict):
                                    text = sent.get('text', '')
                                else:
                                    text = str(sent)
                            
                            # Handle 'sentences' field
                            elif 'sentences' in response.output:
                                sents = response.output['sentences']
                                if isinstance(sents, list):
                                    text = "".join([s.get('text', '') for s in sents if isinstance(s, dict)])
                                elif isinstance(sents, dict):
                                    text = sents.get('text', '')
                                else:
                                    text = str(sents)
                                    
                            # Handle 'text' field
                            elif 'text' in response.output:
                                text = response.output['text']
                            
                            else:
                                # Log structure if unknown
                                logger.warning(f"Unknown output structure: {response.output}")
                                text = str(response.output)
                        except Exception as parse_error:
                            logger.error(f"Error parsing response: {parse_error}")
                            text = str(response.output)
                        
                        return text, None
                    else:
                        return "", None # Empty output
                else:
                    logger.error(f"Recognition failed: {response.code} - {response.message}")
                    return None, f"{response.code}: {response.message}"
            finally:
                if os.path.exists(temp_path):
                    os.remove(temp_path)

        except Exception as e:
            logger.error(f"Error during recognition: {e}")
            return None, str(e)

if __name__ == "__main__":
    # Test
    api_key = os.getenv("DASHSCOPE_API_KEY")
    if api_key:
        engine = STTEngine(api_key)
        # Load a test wav if exists
        if os.path.exists("test_recording.wav"):
            with open("test_recording.wav", "rb") as f:
                # Read PCM data (skip header for wav if treating as pcm, but we send as wav)
                # Actually we can just read the whole file and pass it if we handle it right.
                # But here recognize takes raw PCM bytes usually if format='pcm'.
                # My implementation writes a WAV file from bytes.
                # So I should pass PCM bytes (without header).
                import wave
                with wave.open("test_recording.wav", 'rb') as wf:
                    frames = wf.readframes(wf.getnframes())
                
                text, error = engine.recognize(frames)
                if text:
                    print(f"Recognized: {text}")
                else:
                    print(f"Error: {error}")
        else:
            print("No test_recording.wav found. Run audio_recorder.py first.")
    else:
        print("Set DASHSCOPE_API_KEY env var to test.")

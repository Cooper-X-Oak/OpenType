
import logging

# Mock Logger
class Logger:
    def info(self, msg): print(f"INFO: {msg}")
    def debug(self, msg): print(f"DEBUG: {msg}")
    def warning(self, msg): print(f"WARNING: {msg}")
    def error(self, msg): print(f"ERROR: {msg}")

logger = Logger()

# The logic from stt_engine.py
def parse_response(output):
    text = ""
    try:
        # Handle 'sentence' field
        if 'sentence' in output:
            sent = output['sentence']
            if isinstance(sent, list):
                print(f"Detected 'sentence' is a LIST. Processing items...")
                text = "".join([s.get('text', '') for s in sent if isinstance(s, dict)])
            elif isinstance(sent, dict):
                print(f"Detected 'sentence' is a DICT.")
                text = sent.get('text', '')
            else:
                text = str(sent)
        
        # Handle 'sentences' field
        elif 'sentences' in output:
            sents = output['sentences']
            if isinstance(sents, list):
                print(f"Detected 'sentences' is a LIST. Processing items...")
                text = "".join([s.get('text', '') for s in sents if isinstance(s, dict)])
            elif isinstance(sents, dict):
                print(f"Detected 'sentences' is a DICT.")
                text = sents.get('text', '')
            else:
                text = str(sents)
                
        # Handle 'text' field
        elif 'text' in output:
            text = output['text']
        
        else:
            # Log structure if unknown
            logger.warning(f"Unknown output structure: {output}")
            text = str(output)
    except Exception as parse_error:
        logger.error(f"Error parsing response: {parse_error}")
        text = str(output)
    
    return text

def test_fix():
    print("=== Verifying Fix for 'list indices must be integers' ===")
    
    # Case 1: The likely cause of the error (sentence is a list)
    mock_output_error_case = {
        'sentence': [
            {'text': 'Hello world', 'begin_time': 0, 'end_time': 1000}
        ]
    }
    print(f"\nCase 1 Input: {mock_output_error_case}")
    result = parse_response(mock_output_error_case)
    print(f"Case 1 Result: '{result}'")
    assert result == "Hello world"
    
    # Case 2: Standard dict structure (what we expected before)
    mock_output_standard = {
        'sentence': {'text': 'Normal dict structure', 'begin_time': 0}
    }
    print(f"\nCase 2 Input: {mock_output_standard}")
    result = parse_response(mock_output_standard)
    print(f"Case 2 Result: '{result}'")
    assert result == "Normal dict structure"

    # Case 3: 'sentences' list (another common format)
    mock_output_sentences = {
        'sentences': [
            {'text': 'Sentence one. '},
            {'text': 'Sentence two.'}
        ]
    }
    print(f"\nCase 3 Input: {mock_output_sentences}")
    result = parse_response(mock_output_sentences)
    print(f"Case 3 Result: '{result}'")
    assert result == "Sentence one. Sentence two."

    print("\n=== Verification Passed: Code now handles List structures correctly! ===")

if __name__ == "__main__":
    test_fix()

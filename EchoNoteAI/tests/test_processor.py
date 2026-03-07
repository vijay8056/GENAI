import os
import pytest
from unittest.mock import MagicMock, patch
from processor import EchoProcessor

@pytest.fixture
def processor():
    with patch('google.generativeai.configure'), \
         patch('google.generativeai.GenerativeModel'):
        return EchoProcessor()

def test_initialization(processor):
    assert processor.recognizer is not None
    # Assuming GEMINI_API_KEY is not set in test environment, model might be None
    # or Mocked if patch is applied correctly.
    pass

def test_process_notes_no_model(processor):
    processor.model = None
    transcript = "This is a test transcript."
    result = processor.process_notes(transcript)
    assert "Raw Transcript (No AI configured):" in result
    assert transcript in result

@patch('google.generativeai.GenerativeModel')
def test_process_notes_with_model(mock_model_class, processor):
    mock_model = MagicMock()
    mock_model.generate_content.return_value.text = "Summarized Note"
    processor.model = mock_model
    
    result = processor.process_notes("Some raw text")
    assert result == "Summarized Note"
    mock_model.generate_content.assert_called_once()

def test_save_note(processor, tmp_path):
    # Mocking os.path.exists and open to avoid actual file creation in local dir
    # or using tmp_path to test file system interaction
    test_notes_dir = tmp_path / "notes"
    with patch('os.path.exists', return_value=True), \
         patch('builtins.open', create=True) as mock_open:
        
        content = "Test content"
        filename = processor.save_note(content)
        
        assert "notes/note_" in filename
        assert filename.endswith(".md")
        mock_open.assert_called_once()

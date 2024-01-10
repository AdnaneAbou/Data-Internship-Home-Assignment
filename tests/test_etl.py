import unittest
from unittest.mock import MagicMock
from src.dags.tasks import extract, transform, load
import os
import pandas as pd
import pytest
from unittest.mock import patch, mock_open

class TestExtractFunction:

    @pytest.fixture
    def mock_load_and_clean(self):
        with patch('your_module.load_and_clean') as mock:
            yield mock

    @pytest.fixture
    def mock_logging_info(self):
        with patch('builtins.logging.info') as mock:
            yield mock

    @pytest.fixture
    def mock_open_function(self):
        with patch('builtins.open', mock_open()) as mock:
            yield mock

    def test_extract(self, mock_load_and_clean, mock_logging_info, mock_open_function):
        # Arrange
        mock_load_and_clean.return_value = pd.DataFrame({
            'context': ['Text1', 'Text2', 'Text3'],
            # Add other columns as needed based on the structure of your CSV
        })

        # Act
        extract()

        # Assert
        # Add assertions based on the expected behavior of your function
        mock_load_and_clean.assert_called_once_with(os.path.join('source', 'jobs.csv'))

        expected_open_calls = [
            # Add expected open calls based on your function's behavior
            ((os.path.join('staging', 'extracted', '0.txt'), 'w'),),
            # Add more open calls as needed
        ]
        mock_open_function.assert_has_calls(expected_open_calls, any_order=True)

        expected_write_calls = [
            # Add expected write calls based on your function's behavior
            (mock_open_function.return_value.__enter__.return_value, ['Text1']),
            # Add more write calls as needed
        ]
        mock_open_function.return_value.__enter__.return_value.write.assert_has_calls(expected_write_calls, any_order=True)

        mock_logging_info.assert_called_with('Extraction of data done successfully')

if __name__ == '__main__':
    pytest.main()

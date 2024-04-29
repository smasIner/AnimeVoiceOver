import os
from unittest.mock import patch, MagicMock

import pandas as pd

from app.backend.auth import authenticate_sheets
from app.backend.requests import get_anime_dataframe


class TestAuth:

    @patch.dict(os.environ, {'SPREADSHEETS_API_KEY': 'test_api_key'})
    def test_authenticate_sheets(self):
        sheets_service = authenticate_sheets()
        assert sheets_service is not None


class TestRequests:

    @patch('app.backend.requests.authenticate_sheets')
    def test_get_anime_dataframe(self, mock_authenticate_sheets):
        # Mock the authenticate_sheets function
        mock_service = MagicMock()
        mock_authenticate_sheets.return_value = mock_service

        # Mock the Google Sheets API response
        mock_service.values().get.return_value.execute.return_value = {
            'values': [
                ['Character', 'Type', 'Status'],
                ['Character 1', 'Main', 'Recorded'],
                ['Character 2', 'Supporting', 'Not recorded'],
            ]
        }
        dataframe = get_anime_dataframe()
        assert isinstance(dataframe, pd.DataFrame)

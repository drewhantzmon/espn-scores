"""Base HTTP client for ESPN API interactions."""

from typing import Dict, Any, Optional
import requests
from espn_scores.core.exceptions import APIException


class ESPNClient:
    """
    Base client for making requests to ESPN APIs.
    Handles common functionality like request formatting, error handling, etc.
    """
    
    BASE_URL = "https://site.api.espn.com/apis/site/v2/sports"
    
    def __init__(self, timeout: int = 30):
        """
        Initialize the ESPN API client.
        
        Args:
            timeout: Request timeout in seconds
        """
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "espn-scores-python-package"
        })
    
    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Make a GET request to the ESPN API.
        
        Args:
            endpoint: API endpoint path
            params: Query parameters
            
        Returns:
            JSON response as dictionary
            
        Raises:
            APIException: If the request fails
        """
        url = f"{self.BASE_URL}/{endpoint}"
        
        try:
            response = self.session.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            raise APIException(
                f"ESPN API request failed: {str(e)}",
                status_code=response.status_code if hasattr(e, 'response') else None
            )
        except requests.exceptions.RequestException as e:
            raise APIException(f"Network error occurred: {str(e)}")
        except ValueError as e:
            raise APIException(f"Invalid JSON response: {str(e)}")
    
    def close(self):
        """Close the HTTP session."""
        self.session.close()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()

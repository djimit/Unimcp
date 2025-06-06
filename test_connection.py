#!/usr/bin/env python3
"""
Test script for Unifi API connection
"""
import os
import sys
import httpx
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("unifi-connection-test")

# Load environment variables from .env file if it exists
load_dotenv()


def test_connection():
    """Test connection to Unifi API"""
    api_key = os.environ.get("UNIFI_API_KEY")
    if not api_key:
        logger.error("UNIFI_API_KEY environment variable not set")
        logger.info("Please set the UNIFI_API_KEY environment variable or "
                    "create a .env file")
        sys.exit(1)
    
    base_url = os.environ.get(
        "UNIFI_API_URL",
        "https://sitemanager.ui.com/api"
    )
    logger.info(f"Testing connection to Unifi API at {base_url}")
    
    # Create headers with API key
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    
    try:
        # Make a simple request to test the connection
        with httpx.Client(headers=headers, timeout=10.0) as client:
            response = client.get(f"{base_url}/sites")
            
            if response.status_code == 200:
                logger.info("Connection successful!")
                sites = response.json()
                logger.info(f"Found {len(sites)} sites")
                for site in sites:
                    logger.info(
                        f"Site: {site.get('name', 'Unknown')} "
                        f"(ID: {site.get('id', 'Unknown')})"
                    )
                return True
            else:
                logger.error(
                    f"Connection failed with status code: "
                    f"{response.status_code}"
                )
                logger.error(f"Response: {response.text}")
                return False
    except Exception as e:
        logger.error(f"Error connecting to Unifi API: {e}")
        return False


if __name__ == "__main__":
    logger.info("Starting Unifi API connection test")
    success = test_connection()
    if success:
        logger.info("Test completed successfully")
        sys.exit(0)
    else:
        logger.error("Test failed")
        sys.exit(1)
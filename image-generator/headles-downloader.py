# this script is used to take a screenshot of a webpage using Playwright
# and it is then putted into final weather screen

from playwright.sync_api import sync_playwright
from PIL import Image
import os

def capture_screenshot_playwright(url, output_file='screenshot.png'):
    """
    Capture a screenshot using Playwright
    
    Args:
        url (str): URL of the webpage to capture
        output_file (str): Path where the screenshot will be saved
    """
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1920, "height": 1080})
        
        # Navigate to the page
        print(f"Navigating to {url}")
        page.goto(url, wait_until="networkidle")

        # page.click("a.leaflet-control-fullscreen-button")
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        # Take screenshot
        page.screenshot(path=output_file, full_page=True)
        print(f"Screenshot saved to {output_file}")
        
        # Close browser
        browser.close()


capture_screenshot_playwright("https://www.ventusky.com/?p=48.58;19.53;7&l=radar", "export/text.png")
    
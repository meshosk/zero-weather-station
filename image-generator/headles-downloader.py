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

def convert_image_to_16_gray(input_image_path, output_image_path):
    """
    Convert an image to 16 shades of gray and save it
    
    Args:
        input_image_path (str): Path to the source image
        output_image_path (str): Where to save the converted image
    """
    # Open the image
    with Image.open(input_image_path).convert("L") as img:
        # Reduce to 16 shades of gray
        img_16_gray = img.point(lambda x: (x // 16) * 16)
        
        # Create output directory if needed
        os.makedirs(os.path.dirname(output_image_path), exist_ok=True)
        
        # Save the converted image
        img_16_gray.save(output_image_path)
        print(f"Image converted to 16 shades of gray and saved to {output_image_path}")
        return img_16_gray

def crop_image(input_image_path, output_image_path, coords):
    """
    Extract a portion of an image based on coordinates
    
    Args:
        input_image_path (str): Path to the source image
        output_image_path (str): Where to save the cropped image
        coords (tuple): Cropping coordinates as (left, top, right, bottom)
    """
    # Open the image
    with Image.open(input_image_path) as img:
        # Crop the image using coordinates
        cropped_img = img.crop(coords)
        
        # Create output directory if needed
        os.makedirs(os.path.dirname(output_image_path), exist_ok=True)
        
        # Save the cropped image
        cropped_img.save(output_image_path)
        print(f"Cropped image saved to {output_image_path}")
        return cropped_img




capture_screenshot_playwright("https://www.ventusky.com/?p=48.58;19.53;7&l=radar", "export/text.png")

convert_image_to_16_gray("export/text.png", "export/text_16_gray.png")    
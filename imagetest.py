import os
import shutil
import cv2
from time import sleep
import pyautogui
from detectImage import scanimage

class TestDetectImage(unittest.TestCase):
    def test_scanimage(self):
        # Load test image and expected results
        test_image = cv2.imread("test_image.jpg")
        expected_results = {"alert1": (10, 20), "alert2": (30, 40)}

        # Call the scanimage function from detectImage module
        results = detectImage.scanimage(test_image)

        # Check that the actual results match the expected results
        self.assertEqual(results, expected_results)
        print("Detected properly")
# Test setup
test_dir = 'test_dir'
os.mkdir(test_dir)
targets_dir = os.path.join(test_dir, 'targets')
os.mkdir(targets_dir)
screenshot_path = os.path.join(test_dir, 'screenshot.png')
config_path = os.path.join(test_dir, 'config.txt')

# Create a sample image to detect
img = cv2.imread('test_image.png')
cv2.imwrite(os.path.join(targets_dir, 'test_image.png'), img)

# Write sample config file
with open(config_path, 'w') as config_file:
    config_file.write('# Disable tracking for test_image\n')
    config_file.write('test_image=0\n')
    config_file.write('# Enable tracking for non_existent_image\n')
    config_file.write('non_existent_image=1\n')

# Run script and simulate user input
try:
    # Simulate user pressing 'g' to start the search
    input_func = input
    input = lambda _: 'g'
    # Take a sample screenshot
    pyautogui.screenshot(screenshot_path)
    # Call the function with the test image path
    img_path = os.path.join(targets_dir, 'test_image.png')
    scanimage(img_path)
    # Simulate user closing the image window
    sleep(1)
    pyautogui.press('esc')
    # Simulate user pressing 's' to stop the search
    input = lambda _: 's'
    scanimage(img_path)
finally:
    input = input_func
    # Clean up test files
    os.remove(screenshot_path)
    shutil.rmtree(test_dir)

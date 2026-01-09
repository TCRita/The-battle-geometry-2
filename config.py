import os

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (200, 200, 200)
LIGHT_BLUE = (173, 216, 230)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

# Calculate BASE_DIR relative to this file
current_dir = os.path.dirname(os.path.abspath(__file__))
if os.path.exists(os.path.join(current_dir, 'image')):
    BASE_DIR = current_dir
elif os.path.exists(os.path.join(current_dir, '最終課題', 'image')):
    BASE_DIR = os.path.join(current_dir, '最終課題')
else:
    BASE_DIR = current_dir

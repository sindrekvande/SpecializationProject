import os
import sys

absolute_path = os.path.dirname(__file__)
relative_path = ".."
full_path = os.path.join(absolute_path, relative_path)
sys.path.insert(0, full_path)
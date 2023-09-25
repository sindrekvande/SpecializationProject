import os
import sys

absolutePath = os.path.dirname(__file__)
relativePath = ".."
fullPath = os.path.join(absolutePath, relativePath)
sys.path.insert(0, fullPath)
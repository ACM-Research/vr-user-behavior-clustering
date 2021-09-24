from app.DataParser import DataParser
import os
from pathlib import Path
from pathlib import PureWindowsPath

parser = DataParser(os.getcwd(), 1, 20, 10)

path = r"D:\Users\Thinh Nguyen\OneDrive\_1_Fall2021\ACM\Research\vr-user-behavior\main\resources\UserTracesByVideo\1"
DataParser.csvDictReader(path, "0Z4VWJ")

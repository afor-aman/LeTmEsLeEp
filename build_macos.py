#!/usr/bin/env python3
import os
import subprocess
import shutil
import sys

print("Building LetMeSleep macOS app bundle...")

# Ensure the resources directory exists
if not os.path.exists("resources/icons"):
    print("Error: resources/icons directory not found.")
    print("Make sure you run this script from the project root directory.")
    sys.exit(1)

# Clean previous build
print("Cleaning previous build artifacts...")
if os.path.exists("dist"):
    shutil.rmtree("dist")
if os.path.exists("build"):
    shutil.rmtree("build")

# Build using py2app - directly build the final version
print("Building app bundle...")
try:
    result = subprocess.call([sys.executable, "setup.py", "py2app"])
    if result != 0:
        print("Error: py2app build failed with exit code: {}".format(result))
        sys.exit(1)
    
    print("\nBuild completed successfully!")
    print("Application bundle created at: {}".format(os.path.abspath("dist/LetMeSleep.app")))
    print("Note: On macOS, you may need to right-click the app and select 'Open' the first time.")
    
    # Provide instructions for sharing
    print("\nTo share this application:")
    print("1. Create a ZIP file of dist/LetMeSleep.app:")
    print("   zip -r LetMeSleep.zip dist/LetMeSleep.app")
    print("2. Share the ZIP file")
    print("3. Recipients will need to extract the ZIP and may need to approve the app in")
    print("   System Preferences > Security & Privacy")
except Exception as e:
    print("Error building application: {}".format(e))
    sys.exit(1) 
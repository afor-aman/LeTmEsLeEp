"""
This is a setup.py script to build LetMeSleep as a macOS application
using py2app.

Usage:
    python setup.py py2app
"""

from setuptools import setup

APP = ['main.py']
DATA_FILES = [
    ('resources/icons', ['resources/icons/bot.svg'])
]
OPTIONS = {
    'argv_emulation': False,
    'packages': ['PyQt5', 'pyautogui', 'qdarktheme'],
    'includes': ['PyQt5.QtCore', 'PyQt5.QtGui', 'PyQt5.QtWidgets', 'qdarktheme'],
    'excludes': ['PyInstaller', 'numpy.random.tests', 'matplotlib', 'wx', 'tkinter', 'PySide2'],
    'iconfile': 'resources/icons/bot.svg',
    'plist': {
        'CFBundleName': 'LetMeSleep',
        'CFBundleDisplayName': 'LetMeSleep',
        'CFBundleIdentifier': 'com.letmesleep.app',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'NSHumanReadableCopyright': 'Copyright © 2023',
        'NSHighResolutionCapable': True,
        'NSPrincipalClass': 'NSApplication',
        'NSRequiresAquaSystemAppearance': False,
    },
}

setup(
    name='LetMeSleep',
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
) 
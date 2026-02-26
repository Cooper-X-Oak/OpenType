import PyInstaller.__main__
import os
import shutil

def build():
    print("Building OpenType...")
    
    # Clean previous build
    if os.path.exists("build"):
        shutil.rmtree("build")
    if os.path.exists("dist"):
        shutil.rmtree("dist")
    
    # PyInstaller arguments
    args = [
        'src/main.py',
        '--name=OpenType',
        '--onefile',
        '--noconsole',
        '--clean',
        '--add-data=src;src', # Include source if needed? No, PyInstaller analyzes imports.
        # But we might need data files. None for now except maybe icon.
        # Hidden imports often needed for dynamic imports
        '--hidden-import=pyaudio',
        '--hidden-import=dashscope',
        '--hidden-import=keyboard',
        '--hidden-import=pyperclip',
        '--hidden-import=PySide6',
        '--exclude-module=PyQt5',
        '--exclude-module=PyQt6',
    ]
    
    # Run PyInstaller
    PyInstaller.__main__.run(args)
    
    print("Build complete. Executable is in dist/OpenType.exe")

if __name__ == "__main__":
    build()

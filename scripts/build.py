import PyInstaller.__main__
import os
import shutil
import zipfile
import sys

# Add project root to path to import version
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.core.version import __version__

def build():
    print(f"Building OpenType v{__version__}...")
    
    # Clean previous build
    if os.path.exists("build"):
        shutil.rmtree("build")
    if os.path.exists("dist"):
        try:
            shutil.rmtree("dist")
        except Exception as e:
            print(f"Warning: Could not clean dist folder: {e}")
    
    # PyInstaller arguments
    args = [
        'src/main.py',
        '--name=OpenType',
        '--onefile',
        '--noconsole',
        '--clean',
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
    
    # Package for release
    package_release()

def package_release():
    print("Packaging release...")
    
    release_dir = "releases"
    if not os.path.exists(release_dir):
        os.makedirs(release_dir)
        
    release_name = f"OpenType-v{__version__}"
    zip_filename = os.path.join(release_dir, f"{release_name}.zip")
    
    # Files to include
    files_to_package = {
        "dist/OpenType.exe": "OpenType.exe",
        "config.json": "config.json"
    }
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for src, dst in files_to_package.items():
            if os.path.exists(src):
                print(f"Adding {src} as {dst}")
                zipf.write(src, dst)
            else:
                print(f"Warning: {src} not found!")
    
    print(f"Release packaged: {zip_filename}")

if __name__ == "__main__":
    build()

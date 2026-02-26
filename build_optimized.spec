# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# Exclude unnecessary modules to reduce size
# Note: PySide6 is large by default. We try to exclude submodules we don't use.
excludes = [
    'tkinter',
    'unittest',
    # 'email', # Often used for parsing headers
    # 'http',  # Required for networking (DashScope)
    # 'xml',   # Safer to keep
    'pydoc',
    'pdb',
    # 'distutils', # Required by PyInstaller hooks
    # 'multiprocessing', # Sometimes required
    # PySide6 modules we likely don't need
    'PySide6.QtQml',
    'PySide6.QtQuick',
    'PySide6.QtQuickWidgets',
    'PySide6.QtBluetooth',
    'PySide6.QtNfc',
    'PySide6.QtSql',
    'PySide6.QtXml',
    'PySide6.QtXmlPatterns',
    'PySide6.QtWebEngine',
    'PySide6.QtWebEngineCore',
    'PySide6.QtWebEngineWidgets',
    'PySide6.Qt3DCore',
    'PySide6.Qt3DInput',
    'PySide6.Qt3DLogic',
    'PySide6.Qt3DRender',
    'PySide6.Qt3DExtras',
    'PySide6.QtCharts',
    'PySide6.QtDataVisualization',
    'PySide6.QtMultimedia',
    'PySide6.QtMultimediaWidgets',
    'PySide6.QtPositioning',
    'PySide6.QtLocation',
    'PySide6.QtSensors',
    'PySide6.QtSerialPort',
    'PySide6.QtTest',
    'PySide6.QtWebChannel',
    'PySide6.QtWebSockets',
    'PySide6.QtDesigner',
    'PySide6.QtHelp',
    'PySide6.QtPrintSupport',
    'PySide6.QtSvg',
    'PySide6.QtSvgWidgets',
    # Other libraries
    'cv2',
    'matplotlib',
    'scipy',
    'pandas',
    'PIL',
]

a = Analysis(
    ['src/main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['keyboard', 'pyaudio', 'dashscope', 'pyperclip', 'win32api', 'win32gui', 'win32con'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=excludes,
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Manually filter binaries to reduce size
# 1. Remove Scipy/OpenBLAS if not needed (we excluded scipy module)
# 2. Remove Qt Quick/QML/PDF DLLs that might have slipped in
exclude_patterns = [
    'Qt6Quick', 'Qt6Qml', 'Qt6Pdf', 'Qt6VirtualKeyboard', 'Qt6DBus', 
    'Qt63D', 'Qt6Charts', 'Qt6DataVisualization', 'Qt6Multimedia', 
    'Qt6Positioning', 'Qt6Sensors', 'Qt6SerialPort', 'Qt6Web',
    # 'scipy', 'libscipy', # NumPy might need OpenBLAS which might be named similarly or shared
    'opengl32sw.dll'
]

def is_excluded(name):
    name_lower = name.lower()
    for pattern in exclude_patterns:
        if pattern.lower() in name_lower:
            return True
    return False

a.binaries = TOC([x for x in a.binaries if not is_excluded(x[0])])

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='OpenType',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='OpenType',
)

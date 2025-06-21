# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['qr_code_scanner.py'],
    pathex=[],
    binaries=[
        (r'C:\Users\ayush\AppData\Roaming\Python\Python312\site-packages\pyzbar\libiconv.dll', 'pyzbar'),
        (r'C:\Users\ayush\AppData\Roaming\Python\Python312\site-packages\pyzbar\libzbar-64.dll', 'pyzbar')
    ],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [('v', None, 'OPTION')],
    name='qr_code_scanner',
    debug=True,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

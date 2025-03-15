# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['src/main.py'],
    pathex=[],
    binaries=[],
    datas=[('icons','icons'),('src/latex.*.json','.'),('src/assets','assets')],
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
    [],
    exclude_binaries=True,
    name='tomino',
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
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='tomino',
)

v = open('VERSION','r').read()

if os.uname().sysname == 'Darwin':
    app = BUNDLE(
        coll,
        name='tomino.app',
        icon='icons/icon.icns',
        bundle_identifier=None,
        version=v,
        info_plist={
            'NSPrincipalClass': 'NSApplication',
            'NSAppleScriptEnabled': False,
            'CFBundleDocumentTypes': [{
                'CFBundleTypeName': 'tex',
                'CFBundleTypeIconFile': 'icons/icon.icns',
                'LSItemContentTypes': ['com.tomino.tex'],
                'LSHandlerRank': 'Mattia Bruno'
            }]
        },
    )
if os.uname().sysname == 'Linux':
    app = BUNDLE(
        coll,
        name='tomino',
        icon='icons/icon.icns',
        bundle_identifier=None,
        version=v,
    )

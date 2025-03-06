# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['src\\main.py'],
    pathex=['C:\\Users\\ilkaa\\Desktop\\Logan-study-style\\src'],
    binaries=[],
    datas=[('src/config', 'config'), ('src/img', 'img')],
    hiddenimports=['plyer.platforms.win.notification', 'google.auth.transport.requests', 'google_auth_oauthlib.flow', 'googleapiclient.discovery', 'sqlalchemy.sql.default_comparator', 'bcrypt', 'typing', 'collections.abc'],
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
    [],
    name='AnimeProductivity',
    debug=False,
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
    icon=['C:\\Users\\ilkaa\\Desktop\\Logan-study-style\\app.ico'],
)

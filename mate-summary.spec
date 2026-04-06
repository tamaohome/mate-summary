# -*- mode: python ; coding: utf-8 -*-

import shutil
from pathlib import Path

from app.config import APP_VERSION


project_root = Path.cwd()
block_cipher = None


a = Analysis(
    [str(project_root / "app" / "__main__.py")],
    pathex=[str(project_root)],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="MateSummary",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
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
    upx=False,
    upx_exclude=[],
    name="MateSummary",
)

bundle_dir = project_root / "dist" / coll.name
zip_base_name = project_root / "dist" / f"{coll.name}_v{APP_VERSION}"
zip_path = zip_base_name.with_suffix(".zip")
if zip_path.exists():
    zip_path.unlink()
shutil.make_archive(str(zip_base_name), "zip", root_dir=bundle_dir)

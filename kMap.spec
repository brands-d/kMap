# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['cli.py'],
             pathex=['C:\\Users\\Dominik Brandstetter\\Desktop\\kMap'],
             binaries=[],
             datas=[('./kmap/config/*.ini', 'kmap/config'), ('./kmap/resources/images/icon.png', 'kmap/resources/images'), ('./kmap/resources/misc/*', 'kmap/resources/misc'), ('./kmap/resources/texts/*', 'kmap/resources/texts'), ('./kmap/ui/*.ui', 'kmap/ui'), ('./example/scripts/*.py', 'example/scripts'), ('./example/data/*.hdf5', 'example/data'), ('./example/data/*.cube', 'example/data')],
             hiddenimports=['kmap.controller.realplotoptions', 'kmap.controller.miniplots', 'kmap.controller.tabwidget', 'kmap.controller.profileplot', 'kmap.controller.lmfitplot'],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=['.\\add_lib.py'],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts, 
          [],
          exclude_binaries=True,
          name='kMap',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas, 
               strip=False,
               upx=True,
               upx_exclude=[],
               name='kMap')

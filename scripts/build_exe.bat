@echo off
cd /d "%~dp0.."
rem Pick a Python that can actually run HaloBattery: some 3.14 builds fail to load
rem _ctypes, and PyInstaller must be installed for the very interpreter that runs
rem the app. "python" first, then the 3.12 launcher as a fallback.
set "PY=python"
%PY% -c "import ctypes" >nul 2>nul || set "PY=py -3.12"
%PY% -c "import ctypes" >nul 2>nul
if errorlevel 1 (
  echo No usable Python found: HaloBattery needs Python 3.10 or newer with a working _ctypes.
  pause
  exit /b 1
)
echo Using: %PY%
%PY% -m pip install -r requirements.txt pyinstaller
%PY% tools\make_icon.py halo.ico
%PY% tools\make_version.py version_info.txt
%PY% -m PyInstaller --noconfirm --onedir --windowed --noupx --name HaloBattery --icon halo.ico --version-file version_info.txt --add-data "lang;lang" --hidden-import hid --hidden-import pystray._win32 halo_battery.pyw
if errorlevel 1 (
  echo.
  echo Build failed. The lines above say why.
  pause
  exit /b 1
)
echo.
echo Done: dist\HaloBattery\HaloBattery.exe
echo Run THAT one, and keep the whole dist\HaloBattery folder together.
echo (build\ is PyInstaller's scratch space: the .exe in there cannot start)
pause

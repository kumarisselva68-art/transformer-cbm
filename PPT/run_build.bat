@echo off
REM =========================================================================
REM  Transformer Condition Monitoring - Presentation Build Automation
REM  Executes JS slide deck generation and PowerShell COM export to PDF & PNG
REM =========================================================================

echo [1/2] Generating Presentation (.pptx) via Node.js and PptxGenJS...
node "%~dp0build_presentation.js"
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Presentation generation failed!
    pause
    exit /b %ERRORLEVEL%
)

echo [2/2] Exporting to PDF and 1080p PNG Thumbnails via PowerPoint COM...
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0export_presentation.ps1"
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Export to PDF / PNG failed!
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo =========================================================================
echo  Build Completed Successfully!
echo  - PPTX: "%~dp0Transformer_CBM_Presentation.pptx"
echo  - PDF:  "%~dp0Transformer_CBM_Presentation.pdf"
echo  - PNGs: "%~dp0thumbnails\" (21 slides at 1920x1080)
echo  - Grid: "%~dp0contact_sheet.png"
echo =========================================================================
pause

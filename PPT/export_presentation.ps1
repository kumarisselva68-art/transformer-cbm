# export_presentation.ps1
# Automates PowerPoint COM to export PPTX to PDF and high-res PNG thumbnails,
# then compiles a contact sheet of all 21 slides in the Green/Black/White theme.

$ErrorActionPreference = "Stop"

$pptDir = "E:\Client\Transformer_CBM\PPT"
$pptxPath = Join-Path $pptDir "Transformer_CBM_Presentation.pptx"
$pdfPath = Join-Path $pptDir "Transformer_CBM_Presentation.pdf"
$thumbDir = Join-Path $pptDir "thumbnails"
$contactSheetPath = Join-Path $pptDir "contact_sheet.png"

if (-not (Test-Path $thumbDir)) {
    New-Item -ItemType Directory -Path $thumbDir | Out-Null
}

Write-Output "Starting PowerPoint COM automation..."
$ppt = New-Object -ComObject PowerPoint.Application

try {
    Write-Output "Opening presentation: $pptxPath"
    $pres = $ppt.Presentations.Open($pptxPath, $true, $false, $false)

    Write-Output "Exporting to PDF: $pdfPath"
    # 32 = ppSaveAsPDF
    $pres.SaveAs($pdfPath, 32)
    Write-Output "PDF export completed."

    $slideCount = $pres.Slides.Count
    Write-Output "Exporting $slideCount slides to PNG (1920x1080)..."
    for ($i = 1; $i -le $slideCount; $i++) {
        $padNum = if ($i -lt 10) { "0$i" } else { "$i" }
        $outImg = Join-Path $thumbDir "slide_$padNum.png"
        $pres.Slides.Item($i).Export($outImg, "PNG", 1920, 1080)
        Write-Output "  Exported slide $padNum -> $outImg"
    }

    $pres.Close()
    Write-Output "Presentation closed."
}
finally {
    $ppt.Quit()
    [System.GC]::Collect()
    [System.GC]::WaitForPendingFinalizers()
    Write-Output "PowerPoint COM released."
}

# Now generate a contact sheet (7x3 grid = 21 slides)
Add-Type -AssemblyName System.Drawing

Write-Output "Generating 7x3 contact sheet for 21 slides..."
$cols = 7
$rows = 3
$slideW = 384
$slideH = 216
$margin = 16
$headerH = 80

$sheetW = ($cols * $slideW) + (($cols + 1) * $margin)
$sheetH = $headerH + ($rows * $slideH) + (($rows + 1) * $margin)

$bmp = New-Object System.Drawing.Bitmap($sheetW, $sheetH)
$gfx = [System.Drawing.Graphics]::FromImage($bmp)
$gfx.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
$gfx.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::HighQuality
$gfx.Clear([System.Drawing.ColorTranslator]::FromHtml("#F8FAFC"))

# Header banner
$headerFont = New-Object System.Drawing.Font("Calibri", 18, [System.Drawing.FontStyle]::Bold)
$subFont = New-Object System.Drawing.Font("Calibri", 11, [System.Drawing.FontStyle]::Regular)
$brushDark = New-Object System.Drawing.SolidBrush([System.Drawing.ColorTranslator]::FromHtml("#111827"))
$brushGreen = New-Object System.Drawing.SolidBrush([System.Drawing.ColorTranslator]::FromHtml("#15803D"))

$titleStr = "IoT-Based Transformer Condition Monitoring with Predictive Adaptive Thermal Management Using ESP32"
$subStr = "Demonstration Platform Executed on an ATX SMPS | 21-Slide Complete Academic Deck Overview"

$gfx.DrawString($titleStr, $headerFont, $brushDark, [float]$margin, [float]15)
$gfx.DrawString($subStr, $subFont, $brushGreen, [float]$margin, [float]48)

$borderPen = New-Object System.Drawing.Pen([System.Drawing.ColorTranslator]::FromHtml("#CBD5E1"), [float]1)
$numFont = New-Object System.Drawing.Font("Calibri", 9, [System.Drawing.FontStyle]::Bold)
$badgeBgBrush = New-Object System.Drawing.SolidBrush([System.Drawing.ColorTranslator]::FromHtml("#15803D"))
$badgeTextBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::White)

for ($i = 1; $i -le $slideCount; $i++) {
    $padNum = if ($i -lt 10) { "0$i" } else { "$i" }
    $slideImgPath = Join-Path $thumbDir "slide_$padNum.png"
    if (Test-Path $slideImgPath) {
        $idx = $i - 1
        $c = $idx % $cols
        $r = [Math]::Floor($idx / $cols)
        
        $x = $margin + $c * ($slideW + $margin)
        $y = $headerH + $margin + $r * ($slideH + $margin)
        
        $sImg = [System.Drawing.Image]::FromFile($slideImgPath)
        $gfx.DrawImage($sImg, [float]$x, [float]$y, [float]$slideW, [float]$slideH)
        $sImg.Dispose()
        
        $gfx.DrawRectangle($borderPen, [float]$x, [float]$y, [float]$slideW, [float]$slideH)
        
        $gfx.FillRectangle($badgeBgBrush, [float]($x + 4), [float]($y + 4), [float]56, [float]18)
        $gfx.DrawString("Slide $padNum", $numFont, $badgeTextBrush, [float]($x + 7), [float]($y + 6))
    }
}

$bmp.Save($contactSheetPath, [System.Drawing.Imaging.ImageFormat]::Png)
$gfx.Dispose()
$bmp.Dispose()
$headerFont.Dispose()
$subFont.Dispose()
$brushDark.Dispose()
$brushGreen.Dispose()
$borderPen.Dispose()
$numFont.Dispose()
$badgeBgBrush.Dispose()
$badgeTextBrush.Dispose()

Write-Output "Contact sheet created at: $contactSheetPath"
Write-Output "All exports completed successfully!"

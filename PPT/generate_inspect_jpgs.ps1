Add-Type -AssemblyName System.Drawing

$inDir = 'E:\Client\Transformer_CBM\PPT\thumbnails'
$outDir = 'E:\Client\Transformer_CBM\PPT\preview_inspect'
if (-not (Test-Path $outDir)) {
    New-Item -ItemType Directory -Path $outDir | Out-Null
}

$jpegCodec = [System.Drawing.Imaging.ImageCodecInfo]::GetImageEncoders() | Where-Object { $_.FormatDescription -eq 'JPEG' }
$encParams = New-Object System.Drawing.Imaging.EncoderParameters(1)
$encParams.Param[0] = New-Object System.Drawing.Imaging.EncoderParameter([System.Drawing.Imaging.Encoder]::Quality, [long]55)

$files = Get-ChildItem -Path $inDir -Filter '*.png'
foreach ($f in $files) {
    $img = [System.Drawing.Image]::FromFile($f.FullName)
    $bmp = New-Object System.Drawing.Bitmap(960, 540)
    $g = [System.Drawing.Graphics]::FromImage($bmp)
    $g.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
    $g.DrawImage($img, 0, 0, 960, 540)
    $outPath = Join-Path $outDir ($f.BaseName + '.jpg')
    $bmp.Save($outPath, $jpegCodec, $encParams)
    $g.Dispose()
    $bmp.Dispose()
    $img.Dispose()
}

Get-ChildItem -Path $outDir | Select-Object Name, Length

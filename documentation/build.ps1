# =============================================================================
# Automated PDF Builder & Preview Generator for Typst
# =============================================================================
param(
    [switch]$Watch,
    [switch]$Preview,
    [string]$Target = "spec"  # "spec" or "showcase" or "all"
)

$PSScriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$TypstExe = Join-Path $PSScriptRoot "bin\typst.exe"

if (-not (Test-Path $TypstExe)) {
    Write-Error "Typst compiler binary not found at $TypstExe"
    exit 1
}

Write-Host "Using Typst: $(& $TypstExe --version)" -ForegroundColor Cyan

function Build-Doc($inputName, $outputName, $previewPrefix) {
    $inPath = Join-Path $PSScriptRoot $inputName
    $outPath = Join-Path $PSScriptRoot $outputName
    
    if ($Watch) {
        Write-Host "Starting continuous watch mode for $inputName..." -ForegroundColor Yellow
        & $TypstExe watch $inPath $outPath
    } else {
        Write-Host "Compiling $inputName -> $outputName..." -ForegroundColor Green
        & $TypstExe compile $inPath $outPath
        if ($LASTEXITCODE -eq 0) {
            Write-Host "Successfully compiled $outputName" -ForegroundColor Green
            if ($Preview) {
                Write-Host "Generating PNG page previews ($previewPrefix)..." -ForegroundColor Yellow
                $pattern = Join-Path $PSScriptRoot "$($previewPrefix)_{p}.png"
                & $TypstExe compile --format png --ppi 150 $inPath $pattern
                Write-Host "Previews generated." -ForegroundColor Green
            }
        } else {
            Write-Error "Compilation failed for $inputName."
        }
    }
}

if ($Target -eq "spec") {
    Build-Doc "transformer_cbm_spec.typ" "transformer_cbm_spec.pdf" "spec_page"
} elseif ($Target -eq "showcase") {
    Build-Doc "showcase.typ" "showcase.pdf" "preview"
} elseif ($Target -eq "all") {
    Build-Doc "transformer_cbm_spec.typ" "transformer_cbm_spec.pdf" "spec_page"
    Build-Doc "showcase.typ" "showcase.pdf" "preview"
} else {
    Build-Doc $Target "$($Target).pdf" "preview"
}

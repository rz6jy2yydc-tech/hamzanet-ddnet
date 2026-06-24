$ErrorActionPreference = "Stop"

Write-Host "== HamzaNet v0.1 Builder =="

if (!(Test-Path ddnet)) {
  Write-Host "Cloning DDNet source..."
  git clone --depth 1 --recursive --shallow-submodules https://github.com/ddnet/ddnet ddnet
}

Write-Host "Applying HamzaNet changes..."
python .\scripts\apply_hamzanet.py .\ddnet

Write-Host "Configuring CMake..."
cmake -S ddnet -B build -G "Visual Studio 17 2022" -A x64 -DPREFER_BUNDLED_LIBS=ON -DVULKAN=OFF -DVIDEORECORDER=OFF -DWEBSOCKETS=OFF

Write-Host "Building client..."
cmake --build build --config Release --target game-client --parallel 2
if ($LASTEXITCODE -ne 0) {
  Write-Host "Target game-client failed, trying full build..."
  cmake --build build --config Release --parallel 2
}

Write-Host "Collecting files..."
New-Item -ItemType Directory -Force out | Out-Null
Get-ChildItem -Path build -Recurse -Include *.exe,*.dll | Where-Object { $_.FullName -match "Release|release" } | Copy-Item -Destination out -Force
if (Test-Path ddnet\data) { Copy-Item -Path ddnet\data -Destination out\data -Recurse -Force }

Write-Host "Done. Check the out folder."

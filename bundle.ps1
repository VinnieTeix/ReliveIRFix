# Remove the 'dist' folder if it exists
if (Test-Path "dist") {
    Remove-Item -Recurse -Force "dist"
}

# Remove the 'build' folder if it exists
if (Test-Path "build") {
    Remove-Item -Recurse -Force "build"
}

# Delete the ReliveIRFix.spec file if it exists
if (Test-Path "ReliveIRFix.spec") {
    Remove-Item -Force "ReliveIRFix.spec"
}

# Run PyInstaller to build the executable
pyinstaller --onefile --noconsole --icon=icon.ico --uac-admin `
    --add-data "Fix_AMD_ReLive_Monitor.vbs;." `
    --add-data "ForceRefresh.bat;." `
    ReliveIRFix.py

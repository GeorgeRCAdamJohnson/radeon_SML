@echo off
echo Deploying Radeon AI to Netlify...

cd "C:\Users\biges\OneDrive\Desktop\amd_ai\radeon-ai\src\react"

echo Installing dependencies...
npm install

echo Building for production...
npm run build

if exist "out" (
    echo ✅ Build successful!
    echo 📁 Built files in: %CD%\out
    echo 🌐 Upload to: https://app.netlify.com/sites/wonderful-tanuki-bf8742/deploys
    echo.
    echo Opening Netlify deploy page...
    start https://app.netlify.com/sites/wonderful-tanuki-bf8742/deploys
    echo.
    echo Drag the 'out' folder to the deploy area
) else (
    echo ❌ Build failed
)

pause
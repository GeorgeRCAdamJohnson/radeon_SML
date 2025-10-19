@echo off
cd "C:\Users\biges\OneDrive\Desktop\amd_ai\radeon-ai\src\react"

echo Cleaning installation...
rmdir /s /q node_modules 2>nul
rmdir /s /q .next 2>nul
rmdir /s /q out 2>nul
del package-lock.json 2>nul

echo Installing fresh dependencies...
npm install

echo Building...
npm run build

if exist "out" (
    echo ✅ Build successful!
    echo Deploying...
    netlify deploy --prod --dir=out --site=3dd3a810-a18b-421b-81c2-fb538c3b368a
) else (
    echo ❌ Build failed
)

pause
@echo off
cd "C:\Users\biges\OneDrive\Desktop\amd_ai\radeon-ai\src\react"

echo Installing dependencies...
npm install

echo Building...
npm run build

if exist "out" (
    echo Deploying to Netlify...
    netlify deploy --prod --dir=out --site=3dd3a810-a18b-421b-81c2-fb538c3b368a
    echo ✅ Deployed to: https://wonderful-tanuki-bf8742.netlify.app
) else (
    echo ❌ Build failed - no out folder created
)

pause
@echo off
echo Setting up git repository for kaziranga-website-backend-2...

REM Change to the project directory
cd /d "c:\xampp\htdocs\kaziranga-Website-Backend-2"

REM Initialize git repository
if not exist .git (
    git init
    if %errorlevel% neq 0 (
        echo Git initialization failed. Make sure Git is installed and in your PATH.
        pause
        exit /b %errorlevel%
    )
    echo Git repository initialized.
) else (
    echo Git repository already exists.
)

REM Add all files to staging
git add .

REM Commit the files
git commit -m "first commit"

REM Set the main branch as default
git branch -M main

REM Add the remote origin
git remote add origin https://github.com/sachin75310/kaziranga-website-backend-2.git

REM Push to the remote repository
git push -u origin main

echo Repository setup complete!
pause
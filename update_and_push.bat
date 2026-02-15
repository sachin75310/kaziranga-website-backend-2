@echo off
echo Updating project for Render deployment...

REM Change to the project directory
cd /d "c:\xampp\htdocs\kaziranga-Website-Backend-2"

REM Add the new files to staging
git add .

REM Commit the changes
git commit -m "Add requirements.txt and update settings for Render deployment"

REM Push to the remote repository
git push origin main

echo Project updated and pushed to GitHub!
pause
@echo off
echo Updating project for Render deployment (v2)...

REM Change to the project directory
cd /d "c:\xampp\htdocs\kaziranga-Website-Backend-2"

REM Add the new files to staging
git add .

REM Commit the changes
git commit -m "Fix requirements.txt and update settings for python-decouple compatibility"

REM Push to the remote repository
git push origin main

echo Project updated and pushed to GitHub!
pause
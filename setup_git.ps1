Write-Host "Setting up git repository for kaziranga-website-backend-2..."

# Change to the project directory
Set-Location "c:\xampp\htdocs\kaziranga-Website-Backend-2"

# Check if .git folder already exists
if (!(Test-Path ".git")) {
    # Initialize git repository
    git init
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Git initialization failed. Make sure Git is installed and in your PATH." -ForegroundColor Red
        Read-Host "Press any key to continue..."
        exit $LASTEXITCODE
    }
    Write-Host "Git repository initialized." -ForegroundColor Green
} else {
    Write-Host "Git repository already exists." -ForegroundColor Yellow
}

# Add all files to staging
Write-Host "Adding files to staging..."
git add .

# Commit the files
Write-Host "Creating initial commit..."
git commit -m "first commit"

# Set the main branch as default
Write-Host "Setting main as default branch..."
git branch -M main

# Add the remote origin
Write-Host "Adding remote origin..."
git remote add origin https://github.com/sachin75310/kaziranga-website-backend-2.git

# Push to the remote repository
Write-Host "Pushing to remote repository..."
git push -u origin main

Write-Host "Repository setup complete!" -ForegroundColor Green
Read-Host "Press any key to continue..."
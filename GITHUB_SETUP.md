# GitHub Setup Guide

Follow these steps to push your Construction Contract Analyzer to GitHub.

## Prerequisites

1. **Install Git** (if not already installed):
   - Download from: https://git-scm.com/download/win
   - Or use winget: `winget install Git.Git`
   - Restart your terminal after installation

2. **Create a GitHub Account** (if you don't have one):
   - Go to: https://github.com
   - Sign up for a free account

## Steps to Push to GitHub

### Step 1: Initialize Git Repository

Open PowerShell in the project directory and run:

```powershell
cd "D:\Codeing Projects\AAA Contracts app"
git init
```

### Step 2: Configure Git (if first time)

```powershell
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### Step 3: Add All Files

```powershell
git add .
```

### Step 4: Make Initial Commit

```powershell
git commit -m "Initial commit: Construction Contract Analyzer web app"
```

### Step 5: Create Repository on GitHub

1. Go to https://github.com/new
2. Repository name: `construction-contract-analyzer` (or your preferred name)
3. Description: "A web application for analyzing construction contracts"
4. Choose **Public** or **Private**
5. **DO NOT** initialize with README, .gitignore, or license (we already have these)
6. Click **"Create repository"**

### Step 6: Connect Local Repository to GitHub

After creating the repository, GitHub will show you commands. Run these (replace `YOUR_USERNAME` with your GitHub username):

```powershell
git remote add origin https://github.com/YOUR_USERNAME/construction-contract-analyzer.git
git branch -M main
git push -u origin main
```

If you use SSH instead of HTTPS:

```powershell
git remote add origin git@github.com:YOUR_USERNAME/construction-contract-analyzer.git
git branch -M main
git push -u origin main
```

### Step 7: Authentication

If prompted:
- **HTTPS**: Enter your GitHub username and a Personal Access Token (not password)
  - Create token: https://github.com/settings/tokens
  - Select scope: `repo`
- **SSH**: Use your SSH key (if configured)

## Quick Command Summary

```powershell
# Navigate to project
cd "D:\Codeing Projects\AAA Contracts app"

# Initialize git
git init

# Add files
git add .

# Commit
git commit -m "Initial commit: Construction Contract Analyzer"

# Add remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/construction-contract-analyzer.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Future Updates

To push updates later:

```powershell
git add .
git commit -m "Description of changes"
git push
```

## Troubleshooting

**Problem**: "Git is not recognized"
- **Solution**: Install Git and restart terminal

**Problem**: "Authentication failed"
- **Solution**: Use Personal Access Token instead of password

**Problem**: "Repository not found"
- **Solution**: Check that you created the repository on GitHub and used the correct username/repo name

---

**Your code is ready! Just follow the steps above once Git is installed.**

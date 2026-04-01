#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Simple script to upload the 1DMaterialsAnalysisTool project to GitHub using subprocess
"""

import os
import sys
import subprocess
import time

def run_command(cmd, cwd=None):
    """Run a command and return output"""
    print(f"Running: {cmd}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd)
        if result.returncode != 0:
            print(f"  Error: {result.stderr}")
            return False, result.stderr
        print(f"  Success: {result.stdout[:100] if result.stdout else 'No output'}")
        return True, result.stdout
    except Exception as e:
        print(f"  Exception: {e}")
        return False, str(e)

def find_git():
    """Try to find git executable"""
    # Try common locations
    common_locations = [
        "git",  # Try in PATH first
        "C:\\Program Files\\Git\\bin\\git.exe",
        "C:\\Program Files (x86)\\Git\\bin\\git.exe",
        "C:\\msys64\\usr\\bin\\git.exe",
        "C:\\msys64\\git\\bin\\git.exe",
        os.path.join(os.environ.get('USERPROFILE', ''), "AppData", "Local", "Programs", "Git", "bin", "git.exe"),
    ]
    
    for git_path in common_locations:
        success, output = run_command(f'"{git_path}" --version')
        if success:
            print(f"Found git at: {git_path}")
            return git_path
    
    print("Could not find git executable!")
    return None

def main():
    """Main function"""
    repo_path = r"G:\doctorcode\1DMaterialsAnalysisTool"
    github_url = "https://github.com/dachuanx/cnt_raman_tool.git"
    
    print("=" * 60)
    print("1D Materials Analysis Tool - GitHub Upload")
    print("=" * 60)
    
    # Check if repository path exists
    if not os.path.exists(repo_path):
        print(f"Error: Repository path does not exist: {repo_path}")
        return
    
    # Find git
    git_path = find_git()
    if not git_path:
        print("\nGit not found. Please install git and add it to PATH.")
        print("Download from: https://git-scm.com/download/win")
        print("\nOr run these commands manually:")
        print(f"cd \"{repo_path}\"")
        print("git init")
        print("git add .")
        print("git commit -m \"Initial commit: 1D Materials Analysis Tool\"")
        print(f"git remote add origin {github_url}")
        print("git branch -M main")
        print("git push -u origin main")
        return
    
    # Change to repository directory
    original_dir = os.getcwd()
    try:
        os.chdir(repo_path)
        
        # Step 1: Initialize git repository
        print("\n1. Initializing git repository...")
        if os.path.exists(".git"):
            print("  .git directory already exists")
        else:
            success, output = run_command(f'"{git_path}" init')
            if not success:
                return
        
        # Step 2: Check git status
        print("\n2. Checking git status...")
        success, output = run_command(f'"{git_path}" status')
        if not success:
            return
        
        # Step 3: Add all files
        print("\n3. Adding files to git...")
        success, output = run_command(f'"{git_path}" add .')
        if not success:
            return
        
        # Step 4: Check if there are changes to commit
        print("\n4. Checking for changes to commit...")
        success, output = run_command(f'"{git_path}" status --porcelain')
        if success and output.strip():
            # Step 5: Commit changes
            print("\n5. Committing changes...")
            commit_message = "Initial commit: 1D Materials Analysis Tool with Raman and Absorption analysis"
            success, output = run_command(f'"{git_path}" commit -m "{commit_message}"')
            if not success:
                return
        else:
            print("  No changes to commit")
        
        # Step 6: Check remote
        print("\n6. Setting up GitHub remote...")
        success, output = run_command(f'"{git_path}" remote -v')
        if success:
            if "origin" in output:
                print("  Remote 'origin' already exists, updating URL...")
                success, output = run_command(f'"{git_path}" remote set-url origin {github_url}')
            else:
                print("  Adding remote 'origin'...")
                success, output = run_command(f'"{git_path}" remote add origin {github_url}')
        else:
            print("  Adding remote 'origin'...")
            success, output = run_command(f'"{git_path}" remote add origin {github_url}')
        
        if not success:
            return
        
        # Step 7: Push to GitHub
        print("\n7. Pushing to GitHub...")
        
        # Try main branch first
        print("  Trying to push to 'main' branch...")
        success, output = run_command(f'"{git_path}" push -u origin main')
        
        if not success:
            # Try master branch
            print("  Trying to push to 'master' branch...")
            success, output = run_command(f'"{git_path}" push -u origin master')
            
            if not success:
                # Create and push to main branch
                print("  Creating 'main' branch...")
                success, output = run_command(f'"{git_path}" branch -M main')
                if success:
                    success, output = run_command(f'"{git_path}" push -u origin main')
        
        if success:
            print("\n" + "=" * 60)
            print("✅ Successfully uploaded project to GitHub!")
            print("=" * 60)
            print(f"\nRepository URL: {github_url.replace('.git', '')}")
            print("\nFiles uploaded:")
            print("- README.md (Project documentation)")
            print("- requirements.txt (Dependencies)")
            print("- .gitignore (Git ignore file)")
            print("- 1Dtool.py (Main application)")
            print("- pages/ (Analysis modules)")
            print("  - page_raman.py (Raman spectroscopy analysis)")
            print("  - page_absorption.py (Absorption spectroscopy analysis)")
            print("  - page_transmittance.py (Transmittance analysis)")
            print("- dist/1D_Materials_Analysis_Tool.exe (Windows executable)")
        else:
            print("\n❌ Failed to push to GitHub")
            print("\nPossible reasons:")
            print("1. GitHub repository might not exist yet")
            print("2. Authentication issues (need GitHub credentials)")
            print("3. Network connectivity issues")
            print("\nYou may need to:")
            print(f"1. Create the repository at: {github_url.replace('.git', '')}")
            print("2. Set up SSH keys or personal access token")
            print("3. Run the commands manually")
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
    finally:
        os.chdir(original_dir)

if __name__ == "__main__":
    main()
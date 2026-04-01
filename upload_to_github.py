#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script to upload the 1DMaterialsAnalysisTool project to GitHub
"""

import os
import sys
from git import Repo, GitCommandError
import subprocess
import shutil

def find_git_executable():
    """Try to find git executable in common locations"""
    common_paths = [
        "C:\\Program Files\\Git\\bin\\git.exe",
        "C:\\Program Files (x86)\\Git\\bin\\git.exe",
        "C:\\msys64\\usr\\bin\\git.exe",
        "C:\\msys64\\git\\bin\\git.exe",
        os.path.join(os.environ.get('USERPROFILE', ''), "AppData", "Local", "Programs", "Git", "bin", "git.exe"),
        "git.exe",  # Try in PATH
    ]
    
    for path in common_paths:
        if os.path.exists(path):
            print(f"Found git at: {path}")
            return path
    
    # Try to find git using where command
    try:
        result = subprocess.run(["where", "git"], capture_output=True, text=True, shell=True)
        if result.returncode == 0 and result.stdout.strip():
            git_path = result.stdout.strip().split('\n')[0]
            print(f"Found git via where command: {git_path}")
            return git_path
    except:
        pass
    
    return None

def initialize_git_repo(repo_path, github_url):
    """Initialize git repository and push to GitHub"""
    print(f"Initializing git repository at: {repo_path}")
    print(f"GitHub URL: {github_url}")
    
    # Find git executable
    git_executable = find_git_executable()
    if not git_executable:
        print("ERROR: Could not find git executable!")
        print("Please make sure git is installed and in your PATH.")
        return False
    
    try:
        # Change to repository directory
        original_dir = os.getcwd()
        os.chdir(repo_path)
        
        # Initialize git repository
        print("\n1. Initializing git repository...")
        if os.path.exists(".git"):
            print("   .git directory already exists, skipping initialization")
        else:
            subprocess.run([git_executable, "init"], check=True)
            print("   ✓ Git repository initialized")
        
        # Add all files
        print("\n2. Adding files to git...")
        subprocess.run([git_executable, "add", "."], check=True)
        print("   ✓ Files added to staging area")
        
        # Check if there are any changes to commit
        status_result = subprocess.run([git_executable, "status", "--porcelain"], 
                                      capture_output=True, text=True, check=True)
        if not status_result.stdout.strip():
            print("   No changes to commit")
        else:
            # Commit changes
            print("\n3. Committing changes...")
            subprocess.run([git_executable, "commit", "-m", "Initial commit: 1D Materials Analysis Tool"], check=True)
            print("   ✓ Changes committed")
        
        # Check if remote already exists
        print("\n4. Setting up GitHub remote...")
        try:
            remote_result = subprocess.run([git_executable, "remote", "-v"], 
                                          capture_output=True, text=True, check=True)
            if "origin" in remote_result.stdout:
                print("   Remote 'origin' already exists")
                # Update remote URL
                subprocess.run([git_executable, "remote", "set-url", "origin", github_url], check=True)
                print(f"   ✓ Updated remote URL to: {github_url}")
            else:
                subprocess.run([git_executable, "remote", "add", "origin", github_url], check=True)
                print(f"   ✓ Added remote 'origin': {github_url}")
        except subprocess.CalledProcessError:
            subprocess.run([git_executable, "remote", "add", "origin", github_url], check=True)
            print(f"   ✓ Added remote 'origin': {github_url}")
        
        # Push to GitHub
        print("\n5. Pushing to GitHub...")
        try:
            subprocess.run([git_executable, "push", "-u", "origin", "main"], check=True)
            print("   ✓ Pushed to 'main' branch")
        except subprocess.CalledProcessError:
            # Try master branch if main doesn't exist
            try:
                subprocess.run([git_executable, "push", "-u", "origin", "master"], check=True)
                print("   ✓ Pushed to 'master' branch")
            except subprocess.CalledProcessError as e:
                print(f"   ✗ Failed to push: {e}")
                print("   Trying to create and push to main branch...")
                subprocess.run([git_executable, "branch", "-M", "main"], check=True)
                subprocess.run([git_executable, "push", "-u", "origin", "main"], check=True)
                print("   ✓ Created and pushed to 'main' branch")
        
        print("\n✅ Successfully uploaded project to GitHub!")
        print(f"📁 Repository: {github_url}")
        
        # Return to original directory
        os.chdir(original_dir)
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error during git operation: {e}")
        print(f"Command output: {e.output if hasattr(e, 'output') else 'No output'}")
        return False
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return False
    finally:
        # Ensure we return to original directory
        if 'original_dir' in locals():
            os.chdir(original_dir)

def main():
    """Main function"""
    repo_path = r"G:\doctorcode\1DMaterialsAnalysisTool"
    github_url = "https://github.com/dachuanx/cnt_raman_tool.git"
    
    print("=" * 60)
    print("1D Materials Analysis Tool - GitHub Upload Script")
    print("=" * 60)
    
    # Check if repository path exists
    if not os.path.exists(repo_path):
        print(f"❌ Repository path does not exist: {repo_path}")
        return
    
    print(f"Repository path: {repo_path}")
    print(f"GitHub URL: {github_url}")
    print()
    
    # Initialize and push to GitHub
    success = initialize_git_repo(repo_path, github_url)
    
    if success:
        print("\n" + "=" * 60)
        print("🎉 Upload completed successfully!")
        print("=" * 60)
        print("\nNext steps:")
        print("1. Visit https://github.com/dachuanx/cnt_raman_tool")
        print("2. Verify that all files are uploaded correctly")
        print("3. Update repository description if needed")
        print("4. Consider adding tags/releases for versioning")
    else:
        print("\n" + "=" * 60)
        print("❌ Upload failed!")
        print("=" * 60)
        print("\nTroubleshooting steps:")
        print("1. Make sure git is installed and in PATH")
        print("2. Check your GitHub credentials")
        print("3. Verify the repository URL is correct")
        print("4. Ensure you have write access to the repository")
        
        # Manual instructions
        print("\n📝 Manual upload instructions:")
        print(f"cd \"{repo_path}\"")
        print("git init")
        print("git add .")
        print("git commit -m \"Initial commit: 1D Materials Analysis Tool\"")
        print(f"git remote add origin {github_url}")
        print("git branch -M main")
        print("git push -u origin main")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
자동 Git 커밋 및 GitHub 푸시 스크립트
"""

import os
import sys
from git import Repo
from git.exc import InvalidGitRepositoryError

# 설정
REPO_PATH = r'c:\code'
GITHUB_REPO = 'https://github.com/cjs944666-gif/inspector1.git'
GIT_USER_NAME = 'Vision Inspector'
GIT_USER_EMAIL = 'inspector@example.com'
COMMIT_MESSAGE = 'Initial Vision Inspector project setup with UI and configuration modules'

def main():
    print(f"🔧 Working directory: {REPO_PATH}")
    
    # 레포지토리 초기화 또는 기존 레포 로드
    try:
        repo = Repo(REPO_PATH)
        print("✅ Git repository found")
    except InvalidGitRepositoryError:
        print("❌ No git repository found. Initializing...")
        repo = Repo.init(REPO_PATH)
        print("✅ Git repository initialized")
    
    # Git 설정
    with repo.config_writer() as git_config:
        git_config.set_value('user', 'name', GIT_USER_NAME)
        git_config.set_value('user', 'email', GIT_USER_EMAIL)
    
    print(f"✅ Git configured: {GIT_USER_NAME} <{GIT_USER_EMAIL}>")
    
    # 모든 파일 추가
    print("📁 Adding files...")
    repo.index.add('*')
    
    # 커밋
    print("💾 Creating commit...")
    try:
        repo.index.commit(COMMIT_MESSAGE)
        print(f"✅ Commit created: {COMMIT_MESSAGE}")
    except Exception as e:
        print(f"❌ Commit failed: {e}")
        return False
    
    # 원격 저장소 설정
    print(f"🌐 Setting up remote: {GITHUB_REPO}")
    try:
        origin = repo.remote('origin')
        origin.set_url(GITHUB_REPO)
        print("✅ Remote URL updated")
    except Exception:
        origin = repo.create_remote('origin', GITHUB_REPO)
        print("✅ Remote created")
    
    # main 브랜치로 설정
    try:
        repo.heads.main.checkout()
        print("✅ Switched to main branch")
    except IndexError:
        try:
            repo.create_head('main')
            repo.heads.main.checkout()
            print("✅ Created and switched to main branch")
        except Exception as e:
            print(f"⚠️  Branch setup error: {e}")
    
    # 푸시
    print("🚀 Pushing to GitHub...")
    try:
        origin.push(force=True)
        print("✅ Push successful!")
        print(f"\n📍 Repository URL: {GITHUB_REPO}")
        return True
    except Exception as e:
        print(f"❌ Push failed: {e}")
        print("\n⚠️  Note: You may need to authenticate with GitHub")
        print("   - If using SSH, ensure SSH key is configured")
        print("   - If using HTTPS, you may need to use a Personal Access Token")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)

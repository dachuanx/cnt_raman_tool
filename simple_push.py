#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的Git推送脚本
"""

import subprocess
import os
import sys

def run_command(cmd, cwd=None):
    """运行命令并返回输出"""
    print(f"执行命令: {cmd}")
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        print(f"输出:\n{result.stdout}")
        if result.stderr:
            print(f"错误:\n{result.stderr}")
        return result.returncode == 0
    except Exception as e:
        print(f"执行命令时出错: {e}")
        return False

def main():
    # 设置工作目录
    work_dir = r"G:\doctorcode\1DMaterialsAnalysisTool"
    git_path = r"D:\Program Files\Git\bin\git.exe"
    
    if not os.path.exists(work_dir):
        print(f"错误: 工作目录不存在: {work_dir}")
        return False
    
    # 检查Git状态
    print("1. 检查Git状态...")
    if not run_command(f'"{git_path}" status', cwd=work_dir):
        print("Git状态检查失败")
        return False
    
    # 添加所有文件
    print("\n2. 添加所有文件...")
    if not run_command(f'"{git_path}" add .', cwd=work_dir):
        print("添加文件失败")
        return False
    
    # 提交更改
    print("\n3. 提交更改...")
    commit_message = "Update project: Add English README and push script"
    if not run_command(f'"{git_path}" commit -m "{commit_message}"', cwd=work_dir):
        print("提交失败")
        return False
    
    # 推送到GitHub
    print("\n4. 推送到GitHub...")
    if not run_command(f'"{git_path}" push origin main', cwd=work_dir):
        print("推送失败")
        print("\n尝试使用HTTPS方式推送...")
        # 尝试使用HTTPS URL
        https_url = "https://github.com/dachuanx/cnt_raman_tool.git"
        if not run_command(f'"{git_path}" push {https_url} main', cwd=work_dir):
            print("HTTPS推送也失败")
            return False
    
    print("\n5. 完成!")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
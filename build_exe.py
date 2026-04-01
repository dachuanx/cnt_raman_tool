#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import sys
import os
from pathlib import Path

def install_packages():
    """安装必要的包"""
    print("正在安装PyInstaller...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller==6.0.0"])
    print("PyInstaller安装完成")

def build_exe():
    """构建exe文件"""
    print("开始构建exe文件...")
    
    # PyInstaller命令参数
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=Calculator",
        "--onefile",
        "--windowed",
        "--icon=NONE",  # 可以替换为图标文件路径
        "--add-data=.;.",  # 添加当前目录
        "--clean",
        "--noconfirm",
        "calculator.py"
    ]
    
    try:
        subprocess.check_call(cmd)
        print("exe文件构建成功！")
        
        # 检查生成的文件
        dist_dir = Path("dist")
        if dist_dir.exists():
            exe_file = dist_dir / "Calculator.exe"
            if exe_file.exists():
                print(f"生成的exe文件: {exe_file}")
                return exe_file
        return None
        
    except subprocess.CalledProcessError as e:
        print(f"构建失败: {e}")
        return None

def copy_to_desktop(exe_file):
    """复制到桌面"""
    if not exe_file or not exe_file.exists():
        print("没有找到exe文件，无法复制到桌面")
        return False
    
    # 获取桌面路径
    desktop_path = Path.home() / "Desktop"
    if not desktop_path.exists():
        print(f"桌面路径不存在: {desktop_path}")
        return False
    
    # 目标路径
    target_path = desktop_path / "Calculator.exe"
    
    try:
        # 如果已存在，先删除
        if target_path.exists():
            target_path.unlink()
        
        # 复制文件
        import shutil
        shutil.copy2(exe_file, target_path)
        print(f"已复制到桌面: {target_path}")
        return True
        
    except Exception as e:
        print(f"复制到桌面失败: {e}")
        return False

def main():
    print("=" * 50)
    print("计算器软件打包工具")
    print("=" * 50)
    
    # 检查Python版本
    print(f"Python版本: {sys.version}")
    
    # 安装必要的包
    try:
        install_packages()
    except Exception as e:
        print(f"安装包失败: {e}")
        print("请手动运行: pip install pyinstaller==6.0.0")
        return
    
    # 构建exe
    exe_file = build_exe()
    
    if exe_file:
        # 复制到桌面
        if copy_to_desktop(exe_file):
            print("\n" + "=" * 50)
            print("打包完成！")
            print(f"计算器软件已保存到桌面: Calculator.exe")
            print("=" * 50)
        else:
            print("\n构建完成，但复制到桌面失败。")
            print(f"你可以在以下位置找到exe文件: {exe_file}")
    else:
        print("\n打包失败，请检查错误信息。")

if __name__ == "__main__":
    main()
"""
生成碳纳米管衍射图
Carbon Nanotube Diffraction Pattern Generator
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import os

# 创建输出目录 (使用允许的工作空间路径)
output_dir = r"C:\Users\shida\.openclaw\workspace\cnt_diffraction"
os.makedirs(output_dir, exist_ok=True)

# 设置图像参数
image_size = 512
background_color = 'black'

# 创建黑色背景的图像
fig, ax = plt.subplots(figsize=(8, 8), dpi=64)
ax.set_facecolor(background_color)
ax.set_xlim(0, image_size)
ax.set_ylim(0, image_size)
ax.set_aspect('equal')
ax.axis('off')

# 碳纳米管参数
n, m = 10, 5  # 手性参数 (n, m)
diameter_nm = 1.2  # 直径 (nm)
lattice_spacing_a = 0.246  # 石墨烯晶格常数 (nm)

# 生成衍射斑点位置
# 碳纳米管的衍射图案通常是一系列沿水平方向的斑点层线
np.random.seed(42)

# 中心斑点（透射束）
center_x, center_y = image_size // 2, image_size // 2

# 绘制中心斑点
center_spot = Circle((center_x, center_y), 12, color='white', alpha=0.9)
ax.add_patch(center_spot)

# 生成层线衍射斑点
num_layers = 7  # 7条层线（符合典型碳纳米管衍射图特征）
layer_spacing = 45  # 层线间距（像素）

for layer in range(-num_layers//2, num_layers//2 + 1):
    if layer == 0:
        continue  # 跳过中心层（已绘制）
    
    layer_y = center_y + layer * layer_spacing
    
    # 每层线的斑点数量和位置
    if abs(layer) == 1:
        num_spots = 6  # 第一层线较多斑点
    elif abs(layer) == 2:
        num_spots = 4
    elif abs(layer) == 3:
        num_spots = 3
    else:
        num_spots = 2
    
    # 在层线上生成斑点
    for i in range(num_spots):
        # 斑点位置（沿水平方向分布）
        offset_x = (i - num_spots//2) * 35 + np.random.randint(-5, 5)
        spot_x = center_x + offset_x
        spot_y = layer_y + np.random.randint(-3, 3)
        
        # 斑点大小随机变化（模拟强度差异）
        spot_size = np.random.randint(4, 10)
        alpha = np.random.uniform(0.5, 0.9)
        
        spot = Circle((spot_x, spot_y), spot_size, color='white', alpha=alpha)
        ax.add_patch(spot)

# 添加一些随机噪声斑点（模拟背景噪声）
num_noise = 15
for _ in range(num_noise):
    noise_x = np.random.randint(50, image_size - 50)
    noise_y = np.random.randint(50, image_size - 50)
    noise_size = np.random.randint(1, 3)
    noise_alpha = np.random.uniform(0.2, 0.5)
    
    noise_spot = Circle((noise_x, noise_y), noise_size, color='white', alpha=noise_alpha)
    ax.add_patch(noise_spot)

# 保存图像
output_path = os.path.join(output_dir, f"cnt_generated_n{n}_m{m}.png")
plt.savefig(output_path, dpi=64, facecolor='black', edgecolor='none', 
            bbox_inches='tight', pad_inches=0)
plt.close()

print(f"[SUCCESS] Carbon nanotube diffraction pattern generated: {output_path}")
print(f"   手性参数: ({n}, {m})")
print(f"   图像尺寸: {image_size}x{image_size}")
print(f"   层线数量: {num_layers}")

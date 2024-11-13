import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 假设这是你的混淆矩阵数据
confusion_matrix = np.array([
    [98.3665, 0.0004, 1.3008, 0.1467, 0.0101, 0.1754],
    [0.0119, 97.5735, 2.344, 0.0446, 0.0, 0.0261],
    [0.3688, 0.2549, 98.4807, 0.5958, 0.2121, 0.0877],
    [0.1807, 0.0058, 5.4148, 93.8987, 0.4958, 0.0041],
    [0.0712, 0.0, 14.2639, 0.0153, 85.6496, 0.0],
    [2.6154, 0.0016, 3.097, 0.0, 0.0, 94.286],

])

# 自定义的标签名称
labels = ['Ground', 'Ceiling', 'Wall', 'Door', 'Cabinet', "Hedge"]

plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.weight'] = 'bold'
plt.rcParams['font.size'] = 18

# 设置绘图
plt.figure(figsize=(10, 8))
ax = sns.heatmap(confusion_matrix, annot=True, fmt='.2f', cmap='Blues',
                 xticklabels=labels, yticklabels=labels)

# 添加标题和轴标签
for _, spine in ax.spines.items():
    spine.set_visible(True)  # 显示边框
    spine.set_linewidth(1.5)  # 设置边框宽度
    spine.set_color("black")

cbar = ax.collections[0].colorbar

for _, i in cbar.ax.spines.items():
    i.set_visible(True)
    i.set_linewidth(1.5)
    i.set_color("black")






plt.title('Confusion Matrix', fontweight="bold", fontsize=18)
plt.xlabel('Predicted Label', fontweight="bold",fontsize=12)
plt.ylabel('True Label', fontweight="bold", fontsize=18)

# 边框


# 优化标签显示
plt.xticks(rotation=45, ha='right')
plt.yticks(rotation=0)

# 显示图形
plt.show()
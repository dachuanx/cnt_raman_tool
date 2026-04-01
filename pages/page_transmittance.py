# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from qfluentwidgets import FluentIcon as FIF


class TransmittanceInterface(QWidget):
    """透射率分析界面（空白页）"""
    
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("TransmittanceInterface")  # 添加 objectName
        
        # 创建布局
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # 添加标题标签
        title_label = QLabel("Transmittance Analysis")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title_label)
        
        # 添加提示信息
        info_label = QLabel("This is a placeholder for transmittance analysis interface.")
        info_label.setStyleSheet("color: #666; margin-top: 10px;")
        layout.addWidget(info_label)
# -*- coding: utf-8 -*-
import sys
import os
from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QSize, QUrl, QPoint
from PyQt5.QtGui import QIcon, QDesktopServices, QColor
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QApplication, QFrame, QStackedWidget
from qfluentwidgets import (NavigationItemPosition, MessageBox, MSFluentTitleBar, MSFluentWindow,
                           TabBar, SubtitleLabel, setFont, IconWidget,
                           TransparentDropDownToolButton, TransparentToolButton, setTheme, Theme, isDarkTheme)
from qfluentwidgets import FluentIcon as FIF

# 设置当前工作目录为脚本所在目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 获取当前文件所在目录的路径（即1DMaterialsAnalysisTool）
current_dir = os.path.dirname(os.path.abspath(__file__))

# 打印调试信息
print(f"当前目录: {current_dir}")
print("正在导入模块...")

# 检查pages目录是否存在
pages_dir = os.path.join(current_dir, 'pages')
print(f"pages目录: {pages_dir}")
print(f"pages目录是否存在: {os.path.exists(pages_dir)}")

if os.path.exists(pages_dir):
    # 检查pages目录中的文件
    print("pages目录中的文件:")
    for file in os.listdir(pages_dir):
        print(f"  - {file}")
else:
    print("警告: pages目录不存在!")

# 检查__init__.py文件是否存在
init_file = os.path.join(pages_dir, '__init__.py')
if not os.path.exists(init_file):
    print(f"创建__init__.py文件: {init_file}")
    with open(init_file, 'w', encoding='utf-8') as f:
        f.write('# pages package\n')

# 添加pages目录到Python路径
if pages_dir not in sys.path:
    sys.path.append(pages_dir)

# 导入新的主页界面组件
try:
    from pages.page_raman import RamanInterface
    print("成功导入: RamanInterface")
except ImportError as e:
    print(f"导入RamanInterface失败: {e}")
    sys.exit(1)

try:
    from pages.page_transmittance import TransmittanceInterface
    print("成功导入: TransmittanceInterface")
except ImportError as e:
    print(f"导入TransmittanceInterface失败: {e}")
    sys.exit(1)

try:
    from pages.page_absorption import AbsorptionInterface
    print("成功导入: AbsorptionInterface")
except ImportError as e:
    print(f"导入AbsorptionInterface失败: {e}")
    sys.exit(1)

print("所有模块导入成功!")








# 导入新的主页界面组件
from page_raman import RamanInterface
from page_transmittance import TransmittanceInterface
from page_absorption import AbsorptionInterface


class TabInterface(QFrame):
    """标签页界面组件，用于显示带图标和文本的内容页"""
    
    def __init__(self, text: str, icon, objectName, parent=None):
        super().__init__(parent=parent)
        # 创建图标部件
        self.iconWidget = IconWidget(icon, self)
        # 创建标签显示文本
        self.label = SubtitleLabel(text, self)
        # 设置图标固定大小为120x120像素
        self.iconWidget.setFixedSize(120, 120)

        # 创建垂直布局
        self.vBoxLayout = QVBoxLayout(self)
        # 设置布局内容居中对齐
        self.vBoxLayout.setAlignment(Qt.AlignCenter)
        # 设置布局内部件间距为30
        self.vBoxLayout.setSpacing(30)
        # 添加图标部件，居中对齐
        self.vBoxLayout.addWidget(self.iconWidget, 0, Qt.AlignCenter)
        # 添加文本标签，居中对齐
        self.vBoxLayout.addWidget(self.label, 0, Qt.AlignCenter)
        # 设置标签字体大小为24
        setFont(self.label, 24)

        # 设置对象名称
        self.setObjectName(objectName)


class CustomTitleBar(MSFluentTitleBar):
    """自定义标题栏，添加了工具栏按钮和标签栏"""
    
    def __init__(self, parent):
        super().__init__(parent)

        # 创建工具栏按钮布局
        self.toolButtonLayout = QHBoxLayout()
        # 根据当前主题设置按钮颜色
        color = QColor(206, 206, 206) if isDarkTheme() else QColor(96, 96, 96)
        # 创建搜索按钮
        self.searchButton = TransparentToolButton(FIF.SEARCH_MIRROR.icon(color=color), self)
        # 创建前进按钮
        self.forwardButton = TransparentToolButton(FIF.RIGHT_ARROW.icon(color=color), self)
        # 创建后退按钮
        self.backButton = TransparentToolButton(FIF.LEFT_ARROW.icon(color=color), self)

        # 初始时禁用前进按钮
        self.forwardButton.setDisabled(True)
        # 设置布局边距
        self.toolButtonLayout.setContentsMargins(20, 0, 20, 0)
        # 设置按钮间距
        self.toolButtonLayout.setSpacing(15)
        # 将按钮添加到布局
        self.toolButtonLayout.addWidget(self.searchButton)
        self.toolButtonLayout.addWidget(self.backButton)
        self.toolButtonLayout.addWidget(self.forwardButton)
        # 将工具栏布局插入到标题栏主布局的第4个位置
        self.hBoxLayout.insertLayout(4, self.toolButtonLayout)

        # 创建标签栏
        self.tabBar = TabBar(self)

        # 设置标签栏属性
        self.tabBar.setMovable(True)
        self.tabBar.setTabMaximumWidth(220)
        self.tabBar.setTabShadowEnabled(False)
        self.tabBar.setTabSelectedBackgroundColor(QColor(255, 255, 255, 125), QColor(255, 255, 255, 50))

        # 连接标签关闭请求信号
        self.tabBar.tabCloseRequested.connect(self.tabBar.removeTab)
        # 标签切换时打印当前标签文本
        self.tabBar.currentChanged.connect(lambda i: print(self.tabBar.tabText(i)))

        # 将标签栏插入到标题栏主布局
        self.hBoxLayout.insertWidget(5, self.tabBar, 1)
        self.hBoxLayout.setStretch(6, 0)

        # 创建头像按钮
        self.avatar = TransparentDropDownToolButton('resource/shoko.png', self)
        self.avatar.setIconSize(QSize(26, 26))
        self.avatar.setFixedHeight(30)
        self.hBoxLayout.insertWidget(7, self.avatar, 0, Qt.AlignRight)
        self.hBoxLayout.insertSpacing(8, 20)

    def canDrag(self, pos: QPoint):
        """重写拖拽判断方法，确保标签栏区域不可拖拽窗口"""
        if not super().canDrag(pos):
            return False

        # 调整坐标到标签栏的相对位置
        pos.setX(pos.x() - self.tabBar.x())
        # 如果点击位置在标签栏区域内，则不可拖拽
        return not self.tabBar.tabRegion().contains(pos)


class Window(MSFluentWindow):
    """主窗口类"""
    
    def __init__(self):
        super().__init__()
        # 设置自定义标题栏
        self.setTitleBar(CustomTitleBar(self))
        # 获取标题栏中的标签栏引用
        self.tabBar = self.titleBar.tabBar

        # 创建主页堆叠部件
        self.homeInterface = QStackedWidget(self, objectName='homeInterface')
        
        # 创建新的主页界面
        self.raman_page = RamanInterface(self)
        self.transmittance_page = TransmittanceInterface(self)
        self.absorption_page = AbsorptionInterface(self)
        
        # 将各界面添加到堆叠部件
        self.homeInterface.addWidget(self.raman_page)
        self.homeInterface.addWidget(self.transmittance_page)
        self.homeInterface.addWidget(self.absorption_page)
        
        # 创建其他功能界面
        self.appInterface = TabInterface('Application', FIF.APPLICATION, 'appInterface')
        self.videoInterface = TabInterface('Video', FIF.VIDEO, 'videoInterface')
        self.libraryInterface = TabInterface('Library', FIF.BOOK_SHELF, 'libraryInterface')

        # 初始化导航栏
        self.initNavigation()
        # 初始化窗口属性
        self.initWindow()

    def initNavigation(self):
        """初始化左侧导航栏"""
        self.addSubInterface(self.raman_page, FIF.CERTIFICATE, 'Raman')
        # 添加透射率导航项
        self.addSubInterface(self.transmittance_page, FIF.BRIGHTNESS, 'Transmittance')
        # 添加吸收光谱导航项
        self.addSubInterface(self.absorption_page, FIF.LEAF, 'Absorption')
        # 添加库界面导航项
        self.addSubInterface(self.libraryInterface, FIF.BOOK_SHELF,
                            'Library', FIF.LIBRARY_FILL, NavigationItemPosition.BOTTOM)
        # 添加帮助导航项
        self.navigationInterface.addItem(
            routeKey='Contact',
            icon=FIF.MAIL,
            text='Contact',
            onClick=self.showMessageBox,
            selectable=False,
            position=NavigationItemPosition.BOTTOM,
        )

        # 设置默认选中拉曼光谱
        self.navigationInterface.setCurrentItem(self.homeInterface.objectName())
        # 连接标签切换信号
        self.tabBar.currentChanged.connect(self.onTabChanged)
        # 连接标签添加请求信号
        self.tabBar.tabAddRequested.connect(self.onTabAddRequested)

    def initWindow(self):
        """初始化窗口属性和位置"""
        # 设置窗口初始大小
        self.resize(1200, 800)
        # 设置窗口图标
        self.setWindowIcon(QIcon(':/qfluentwidgets/images/logo.png'))
        # 设置窗口标题
        self.setWindowTitle('1D Materials Analysis Tool')

        # 获取桌面可用区域并居中显示
        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)

    def showMessageBox(self):
            """Display information about the laboratory"""
            w = MessageBox(
                'About This Tool',
                'This application is developed using the qfluentwidgets module and designed by the Atomic-level Materials Manufacturing Laboratory at Zhejiang University.',
                self
            )
            w.yesButton.setText('Contact Us')
            w.cancelButton.setText('Close')

            if w.exec():
                QDesktopServices.openUrl(QUrl("http://cn.zjuatomic.com/"))

    def onTabChanged(self, index: int):
        """标签页切换时的槽函数"""
        # 获取当前标签页的路由键
        objectName = self.tabBar.currentTab().routeKey()
        # 根据路由键找到对应的标签页界面部件
        tabInterface = self.findChild(TabInterface, objectName)
        if tabInterface:
            # 设置主页堆叠部件显示对应的标签页
            self.homeInterface.setCurrentWidget(tabInterface)
            # 切换到主页界面
            self.stackedWidget.setCurrentWidget(self.homeInterface)

    def onTabAddRequested(self):
        """添加新标签页的槽函数"""
        # 生成标签文本
        text = f'New Tab {self.tabBar.count() + 1}'
        # 添加新标签页
        self.addTab(text, text, 'resource/Smiling_with_heart.png')

    def addTab(self, routeKey, text, icon):
        """添加标签页的通用方法"""
        # 在标签栏中添加标签
        self.tabBar.addTab(routeKey, text, icon)
        # 在主页堆叠部件中添加对应的界面
        self.homeInterface.addWidget(TabInterface(text, icon, routeKey, self))


if __name__ == '__main__':
    # 设置高DPI缩放策略
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    # 创建应用实例
    app = QApplication(sys.argv)
    
    # 创建主窗口实例
    w = Window()
    # 显示窗口
    w.show()
    # 进入应用主循环
    app.exec_()
# -*- coding: utf-8 -*-
"""
absorption_interface.py - 紫外-可见吸收光谱分析界面组件
"""
import os
import pandas as pd
import numpy as np
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import (QFrame, QVBoxLayout, QHBoxLayout, QWidget,
                             QFileDialog, QListWidgetItem, QLabel,
                             QGroupBox, QFormLayout)
from qfluentwidgets import (BodyLabel, CaptionLabel, PrimaryPushButton,
                            ListWidget, InfoBar, InfoBarPosition,
                            isDarkTheme, setFont, FluentIcon as FIF,
                            CheckBox, SpinBox, DoubleSpinBox)

# 设置Matplotlib全局字体参数
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['Times New Roman', 'SimHei', 'Microsoft YaHei', 'DejaVu Sans']
matplotlib.rcParams['font.family'] = 'Times New Roman'
matplotlib.rcParams['axes.unicode_minus'] = False
matplotlib.rcParams['font.size'] = 12

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class AbsorptionCanvas(QWidget):
    """吸收光谱图显示画布"""
    axis_font_size_changed = pyqtSignal(int)
    label_font_size_changed = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.figure = Figure(figsize=(8, 6), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)
        self.base_canvas_size = (800, 600)
        self.base_axis_font_size = 12.0
        self.base_label_font_size = 10.0
        self.current_axis_font_size = 12
        self.current_label_font_size = 10
        self._plot_state = None
        self._showing_placeholder = True

        # 初始占位文本
        self.ax.text(0.5, 0.5, 'No Absorption spectrum data\nPlease import Excel files',
                     ha='center', va='center', fontsize=16,
                     transform=self.ax.transAxes, color='gray',
                     fontname='Times New Roman')
        self.ax.set_xlabel('Wavelength (nm)', fontsize=12, fontname='Times New Roman')
        self.ax.set_ylabel('Absorbance (a.u.)', fontsize=12, fontname='Times New Roman')
        self.ax.set_title('Absorption Spectra Comparison', fontsize=14, fontweight='bold',
                           fontname='Times New Roman')
        self.ax.grid(True, alpha=0.1)

        # 布局设置
        layout = QVBoxLayout(self)
        layout.addWidget(self.canvas)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

    def get_current_axis_font_size(self):
        """返回当前坐标轴字体大小"""
        return int(self.current_axis_font_size)

    def get_current_label_font_size(self):
        """返回当前标签字体大小"""
        return int(self.current_label_font_size)

    def set_axis_font_size(self, font_size):
        """设置当前窗口尺寸下的坐标轴目标字体大小"""
        scale_factor = self._get_font_scale_factor()
        self.base_axis_font_size = max(6.0, float(font_size) / scale_factor)
        self._update_font_size(redraw=True)

    def set_label_font_size(self, font_size):
        """设置当前窗口尺寸下的标签目标字体大小"""
        scale_factor = self._get_font_scale_factor()
        self.base_label_font_size = max(6.0, float(font_size) / scale_factor)
        self._update_font_size(redraw=True)

    def _get_font_scale_factor(self):
        """根据画布尺寸计算字体缩放比例"""
        width = max(self.canvas.width(), 1)
        height = max(self.canvas.height(), 1)
        width_scale = width / self.base_canvas_size[0]
        height_scale = height / self.base_canvas_size[1]
        return max(0.7, min(2.5, min(width_scale, height_scale)))

    def _get_font_config(self):
        """生成当前绘图所需的字体配置"""
        scale_factor = self._get_font_scale_factor()
        effective_axis_font_size = max(8, int(round(self.base_axis_font_size * scale_factor)))
        effective_label_font_size = max(8, int(round(self.base_label_font_size * scale_factor)))
        self.current_axis_font_size = effective_axis_font_size
        self.current_label_font_size = effective_label_font_size
        return {
            "title": max(10, int(round(effective_axis_font_size * 1.2))),
            "axis": max(9, int(round(effective_axis_font_size * 1.0))),
            "tick": max(8, int(round(effective_axis_font_size * 0.85))),
            "annotation": max(8, int(round(effective_label_font_size * 0.9))),
            "curve_label": max(8, int(round(effective_label_font_size * 1.0))),
            "placeholder": max(12, int(round(effective_axis_font_size * 1.25)))
        }

    def _update_font_size(self, redraw=False):
        """更新当前字体大小，并在需要时重绘"""
        previous_axis_font_size = self.current_axis_font_size
        previous_label_font_size = self.current_label_font_size
        font_config = self._get_font_config()
        if font_config["axis"] != previous_axis_font_size:
            self.axis_font_size_changed.emit(font_config["axis"])
        if font_config["curve_label"] != previous_label_font_size:
            self.label_font_size_changed.emit(font_config["curve_label"])
        if redraw:
            self._redraw_current_view()

    def _redraw_current_view(self):
        """根据当前状态重新绘制画布"""
        if self._plot_state:
            self.plot_multiple_spectra_comparison(**self._plot_state)
        elif self._showing_placeholder:
            self.clear_plot()

    def resizeEvent(self, event):
        """窗口尺寸变化时联动更新图表字体"""
        super().resizeEvent(event)
        self._update_font_size(redraw=True)

    def plot_multiple_spectra_comparison(self, spectra_data, x_lim=None, normalize=True,
                                          y_tick_segments=5, curve_gap=0.3, show_labels=True):
        """
        绘制多吸收光谱对比图（单条光谱选择即为单光谱显示）
        :param spectra_data: 光谱数据列表 [(x_data, y_data, curve_name), ...]
        :param x_lim: 横坐标显示范围 (x_min, x_max)，None则使用全范围
        :param normalize: 是否归一化
        :param y_tick_segments: Y轴刻度分段数
        :param curve_gap: 曲线间距
        :param show_labels: 是否显示样品名称标签
        """
        self._plot_state = {
            "spectra_data": spectra_data,
            "x_lim": x_lim,
            "normalize": normalize,
            "y_tick_segments": y_tick_segments,
            "curve_gap": curve_gap,
            "show_labels": show_labels
        }
        self._showing_placeholder = False
        self.figure.clear()
        self.ax = self.figure.add_subplot(111)
        font_config = self._get_font_config()

        if not spectra_data:
            self.ax.text(0.5, 0.5, 'No spectra data available\nPlease import Excel files',
                         ha='center', va='center', fontsize=font_config["placeholder"],
                         transform=self.ax.transAxes, color='gray',
                         fontname='Times New Roman')
            self.canvas.draw()
            return

        # 1. 确定X轴范围
        all_x = []
        for data in spectra_data:
            x_data, _, _ = data
            if len(x_data) > 0:
                all_x.extend(x_data)
        all_x = np.array(all_x)

        # 应用自定义显示范围
        if x_lim is not None:
            x_min, x_max = x_lim
            # 范围校验，避免超出数据边界
            x_min = max(float(np.min(all_x)), x_min)
            x_max = min(float(np.max(all_x)), x_max)
        else:
            x_min, x_max = np.min(all_x), np.max(all_x)
        xlim = (float(x_min), float(x_max))
        label_x_pos = xlim[0] + (xlim[1] - xlim[0]) * 0.42

        n_curves = len(spectra_data)
        single_curve_height = 1  # 单条曲线占用高度
        base_offset = 0.15  # 底部留白高度
        total_y_height = n_curves * single_curve_height + (n_curves - 1) * curve_gap + base_offset * 1.2

        # 计算每条曲线的Y轴区间（从下到上排列，新增底部偏移）
        curve_intervals = []
        for i in range(n_curves):
            bottom = i * (single_curve_height + curve_gap) + base_offset
            top = bottom + single_curve_height
            curve_intervals.append((bottom, top))

        # 颜色映射
        colors = matplotlib.cm.tab10(np.linspace(0, 1, min(10, n_curves)))
        if n_curves > 10:
            colors = matplotlib.cm.tab20(np.linspace(0, 1, min(20, n_curves)))

        all_yticks = []
        all_yticklabels = []

        # 遍历绘制每条曲线
        for idx, (x_data, y_data, curve_name) in enumerate(spectra_data):
            if len(x_data) == 0:
                continue

            bottom, top = curve_intervals[idx]
            color = colors[idx % len(colors)]

            # 按当前显示区间计算归一化范围
            range_mask = (x_data >= xlim[0]) & (x_data <= xlim[1])
            if np.any(range_mask):
                y_min_raw = np.min(y_data[range_mask])
                y_max_raw = np.max(y_data[range_mask])
            else:
                y_min_raw = np.min(y_data)
                y_max_raw = np.max(y_data)

            # 归一化处理
            if normalize and y_max_raw > y_min_raw:
                y_normalized = (y_data - y_min_raw) / (y_max_raw - y_min_raw) * single_curve_height * 0.8 + bottom
            else:
                scale_base = y_max_raw * 1.2 if y_max_raw != 0 else 1
                y_normalized = y_data / scale_base * single_curve_height * 0.8 + bottom

            # 绘制光谱曲线
            self.ax.plot(x_data, y_normalized, color=color, linewidth=1.5, label=curve_name)

            # 样品名称标签显示
            if show_labels:
                closest_x_idx = np.argmin(np.abs(x_data - label_x_pos))
                label_y_base = y_normalized[closest_x_idx]
                label_y_pos = label_y_base + 0.05
                self.ax.text(label_x_pos, label_y_pos,
                             curve_name, fontsize=font_config["curve_label"], color=color,
                             verticalalignment='bottom', horizontalalignment='left',
                             fontname='Times New Roman')

            # 生成Y轴刻度
            y_ticks = self._generate_y_ticks(y_max_raw, n_segments=y_tick_segments)
            for tick_value in y_ticks:
                if y_max_raw > y_min_raw:
                    if normalize:
                        tick_pos = (tick_value - y_min_raw) / (y_max_raw - y_min_raw) * single_curve_height * 0.8 + bottom
                    else:
                        scale_base = y_max_raw * 1.2 if y_max_raw != 0 else 1
                        tick_pos = tick_value / scale_base * single_curve_height * 0.8 + bottom
                    all_yticks.append(tick_pos)
                    # 刻度标签格式化
                    if tick_value >= 1000:
                        tick_label = f"{tick_value / 1000:.1f}k"
                    elif tick_value >= 100:
                        tick_label = f"{int(tick_value)}"
                    else:
                        tick_label = f"{tick_value:.2f}"
                    all_yticklabels.append(tick_label)

        # 图形属性设置
        self.ax.set_xlabel('Wavelength (nm)', fontsize=font_config["axis"], fontname='Times New Roman')
        self.ax.set_ylabel('Absorbance (a.u.)', fontsize=font_config["axis"], fontname='Times New Roman')
        self.ax.set_title('Absorption Spectra Comparison', fontsize=font_config["title"], fontweight='bold',
                           fontname='Times New Roman')

        # 坐标轴范围设置
        self.ax.set_xlim(xlim)
        self.ax.set_ylim(-0.05, total_y_height)

        # Y轴刻度设置
        self.ax.set_yticks(all_yticks)
        self.ax.set_yticklabels(all_yticklabels, fontsize=font_config["tick"], color='black', fontname='Times New Roman')

        # 横坐标刻度优化
        x_span = xlim[1] - xlim[0]
        if x_span <= 200:
            tick_interval = 20
        elif x_span <= 500:
            tick_interval = 50
        elif x_span <= 1000:
            tick_interval = 100
        else:
            tick_interval = 200
        start_tick = np.ceil(xlim[0] / tick_interval) * tick_interval
        end_tick = np.floor(xlim[1] / tick_interval) * tick_interval
        xticks = np.arange(start_tick, end_tick + tick_interval * 0.5, tick_interval)
        xticks = np.concatenate(([xlim[0]], xticks, [xlim[1]]))
        xticks = np.array(sorted(set(np.round(xticks, 4))))
        self.ax.set_xticks(xticks)
        self.ax.set_xticklabels(
            [f"{int(tick)}" if np.isclose(tick, round(tick)) else f"{tick:.1f}" for tick in xticks],
            fontsize=font_config["tick"],
            fontname='Times New Roman'
        )
        self.ax.set_xlim(xlim)

        # 网格与边框设置
        self.ax.grid(False)
        for spine in self.ax.spines.values():
            spine.set_color('black')
            spine.set_linewidth(1.5)

        # 刷新画布
        self.canvas.draw()
        self.canvas.flush_events()

    def _generate_y_ticks(self, y_max, n_segments=5):
        """生成规整的Y轴刻度"""
        if y_max <= 0:
            return [0]
        ideal_step = y_max / n_segments
        step_magnitude = 10 ** np.floor(np.log10(ideal_step))
        step_candidates = [
            0.1 * step_magnitude, 0.2 * step_magnitude, 0.5 * step_magnitude,
            1 * step_magnitude, 2 * step_magnitude, 5 * step_magnitude,
            10 * step_magnitude
        ]
        best_step = min(step_candidates, key=lambda x: abs(x - ideal_step))
        ticks = [i * best_step for i in range(n_segments + 1)]
        ticks = [t for t in ticks if t <= y_max * 1.05]

        if best_step < 1:
            decimal_places = abs(int(np.floor(np.log10(best_step))))
            ticks = [round(t, decimal_places) for t in ticks]
        else:
            ticks = [int(t) for t in ticks]
        return ticks

    def clear_plot(self):
        """清空图表"""
        self._plot_state = None
        self._showing_placeholder = True
        self.figure.clear()
        self.ax = self.figure.add_subplot(111)
        font_config = self._get_font_config()
        self.ax.text(0.5, 0.5, 'No Absorption spectrum data\nPlease import Excel files',
                     ha='center', va='center', fontsize=font_config["placeholder"],
                     transform=self.ax.transAxes, color='gray',
                     fontname='Times New Roman')
        self.ax.set_xlabel('Wavelength (nm)', fontsize=font_config["axis"], fontname='Times New Roman')
        self.ax.set_ylabel('Absorbance (a.u.)', fontsize=font_config["axis"], fontname='Times New Roman')
        self.ax.set_title('Absorption Spectra Comparison', fontsize=font_config["title"], fontweight='bold',
                           fontname='Times New Roman')
        self.ax.grid(True, alpha=0.3)
        self.canvas.draw()


class AbsorptionInterface(QFrame):
    """吸收光谱分析界面"""
    curve_selected = pyqtSignal(str)  # 光谱选择信号

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("AbsorptionInterface")
        self.absorption_spectra = {}  # 存储吸收光谱数据 {样品名: (x_data, y_data)}
        self.current_file = ""  # 当前选择的Excel文件
        self.data_x_min = 0.0  # 数据原始最小波长
        self.data_x_max = 0.0  # 数据原始最大波长
        self._syncing_axis_font_size_spin = False
        self._syncing_label_font_size_spin = False
        self.setup_ui()

    def setup_ui(self):
        """设置界面布局"""
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # 左侧：光谱显示区域
        left_widget = QFrame(self)
        left_widget.setObjectName("leftWidget")
        left_layout = QVBoxLayout(left_widget)
        self.absorption_canvas = AbsorptionCanvas(self)
        left_layout.addWidget(self.absorption_canvas)
        main_layout.addWidget(left_widget, 3)

        # 右侧：控制面板
        right_widget = QFrame(self)
        right_widget.setObjectName("rightWidget")
        right_layout = QVBoxLayout(right_widget)

        # 顶部操作按钮
        action_row = QHBoxLayout()
        action_row.setSpacing(8)

        self.import_button = PrimaryPushButton(FIF.FOLDER_ADD, 'Import Excel', self)
        self.import_button.clicked.connect(self.import_spectra)
        self.import_button.setFixedHeight(38)

        self.save_button = PrimaryPushButton(FIF.SAVE, 'Save Image', self)
        self.save_button.clicked.connect(self.save_results)
        self.save_button.setFixedHeight(38)

        action_row.addWidget(self.import_button)
        action_row.addWidget(self.save_button)
        right_layout.addLayout(action_row)

        # 当前文件标签
        self.file_label = CaptionLabel("No file selected", self)
        self.file_label.setStyleSheet("color: gray; padding: 5px;")
        right_layout.addWidget(self.file_label)

        right_layout.addSpacing(10)

        # 光谱选择列表
        spectrum_list_label = BodyLabel("Select Spectra for Comparison:", self)
        setFont(spectrum_list_label, 13)
        spectrum_list_label.setStyleSheet("font-weight: bold;")
        right_layout.addWidget(spectrum_list_label)

        self.spectrum_list = ListWidget(self)
        self.spectrum_list.setFixedWidth(250)
        self.spectrum_list.setSelectionMode(ListWidget.MultiSelection)
        self.spectrum_list.itemSelectionChanged.connect(self.redraw_comparison)
        right_layout.addWidget(self.spectrum_list)

        # 显示控制参数
        self.params_group = QGroupBox("Display Settings", self)
        params_layout = QFormLayout(self.params_group)

        # 波长范围设置（新增）
        self.x_min_spin = DoubleSpinBox(self)
        self.x_min_spin.setRange(100, 2000)
        self.x_min_spin.setSingleStep(0.1)
        self.x_min_spin.setValue(185)
        self.x_min_spin.valueChanged.connect(self.redraw_comparison)

        self.x_max_spin = DoubleSpinBox(self)
        self.x_max_spin.setRange(100, 2000)
        self.x_max_spin.setSingleStep(0.1)
        self.x_max_spin.setValue(1100)
        self.x_max_spin.valueChanged.connect(self.redraw_comparison)

        # 原有显示参数
        self.normalize_check = CheckBox("Normalize Spectra", self)
        self.normalize_check.setChecked(True)
        self.normalize_check.stateChanged.connect(self.redraw_comparison)

        self.show_labels_check = CheckBox("Show Labels", self)
        self.show_labels_check.setChecked(True)
        self.show_labels_check.stateChanged.connect(self.redraw_comparison)

        self.y_segments_spin = SpinBox(self)
        self.y_segments_spin.setRange(3, 10)
        self.y_segments_spin.setValue(5)
        self.y_segments_spin.valueChanged.connect(self.redraw_comparison)

        self.axis_font_size_spin = SpinBox(self)
        self.axis_font_size_spin.setRange(8, 48)
        self.axis_font_size_spin.setValue(self.absorption_canvas.get_current_axis_font_size())
        self.axis_font_size_spin.valueChanged.connect(self.on_axis_font_size_spin_changed)

        self.label_font_size_spin = SpinBox(self)
        self.label_font_size_spin.setRange(8, 48)
        self.label_font_size_spin.setValue(self.absorption_canvas.get_current_label_font_size())
        self.label_font_size_spin.valueChanged.connect(self.on_label_font_size_spin_changed)

        self.curve_gap_spin = DoubleSpinBox(self)
        self.curve_gap_spin.setRange(0.1, 1.0)
        self.curve_gap_spin.setSingleStep(0.1)
        self.curve_gap_spin.setValue(0.1)
        self.curve_gap_spin.valueChanged.connect(self.redraw_comparison)

        # 添加到表单布局
        params_layout.addRow("Min Wavelength (nm):", self.x_min_spin)
        params_layout.addRow("Max Wavelength (nm):", self.x_max_spin)
        params_layout.addRow("Normalize:", self.normalize_check)
        params_layout.addRow("Y-axis Segments:", self.y_segments_spin)
        params_layout.addRow("Axis Font Size:", self.axis_font_size_spin)
        params_layout.addRow("Label Font Size:", self.label_font_size_spin)
        params_layout.addRow("Curve Gap:", self.curve_gap_spin)
        params_layout.addRow("Show Labels:", self.show_labels_check)
        right_layout.addWidget(self.params_group)

        # 字体大小联动
        self.absorption_canvas.axis_font_size_changed.connect(self.update_axis_font_size_spin)
        self.absorption_canvas.label_font_size_changed.connect(self.update_label_font_size_spin)
        self.update_axis_font_size_spin(self.absorption_canvas.get_current_axis_font_size())
        self.update_label_font_size_spin(self.absorption_canvas.get_current_label_font_size())

        # 加载信息标签
        self.info_label = CaptionLabel("Loaded 0 spectra", self)
        self.info_label.setStyleSheet("color: #888; padding: 5px;")
        right_layout.addWidget(self.info_label)

        right_layout.addStretch(1)
        main_layout.addWidget(right_widget, 1)

        # 样式设置
        if isDarkTheme():
            bg_color = "rgba(40, 40, 40, 150)"
            border_color = "#444"
        else:
            bg_color = "rgba(255, 255, 255, 150)"
            border_color = "#e0e0e0"

        self.setStyleSheet(f"""
            QFrame#leftWidget, QFrame#rightWidget {{
                background-color: {bg_color};
                border-radius: 8px;
                border: 1px solid {border_color};
            }}
            ListWidget {{
                background-color: rgba(255, 255, 255, 100);
                border: 1px solid {border_color};
                border-radius: 5px;
            }}
            QGroupBox {{
                font-weight: bold;
                border: 1px solid {border_color};
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }}
        """)

    def on_axis_font_size_spin_changed(self, font_size):
        """同步用户设置的坐标轴字体大小"""
        if self._syncing_axis_font_size_spin:
            return
        self.absorption_canvas.set_axis_font_size(font_size)

    def on_label_font_size_spin_changed(self, font_size):
        """同步用户设置的标签字体大小"""
        if self._syncing_label_font_size_spin:
            return
        self.absorption_canvas.set_label_font_size(font_size)

    def update_axis_font_size_spin(self, font_size):
        """将当前实际坐标轴字体同步到界面控件"""
        self._syncing_axis_font_size_spin = True
        self.axis_font_size_spin.setValue(int(font_size))
        self._syncing_axis_font_size_spin = False

    def update_label_font_size_spin(self, font_size):
        """将当前实际标签字体同步到界面控件"""
        self._syncing_label_font_size_spin = True
        self.label_font_size_spin.setValue(int(font_size))
        self._syncing_label_font_size_spin = False

    def redraw_comparison(self):
        """重新绘制光谱对比图"""
        selected_items = self.spectrum_list.selectedItems()
        if not selected_items:
            self.absorption_canvas.clear_plot()
            return

        # 准备绘图数据
        spectra_data = []
        for item in selected_items:
            spectrum_name = item.text()
            if spectrum_name in self.absorption_spectra:
                x_data, y_data = self.absorption_spectra[spectrum_name]
                spectra_data.append((x_data, y_data, spectrum_name))

        # 获取用户设置的波长范围
        x_lim = (self.x_min_spin.value(), self.x_max_spin.value())

        if spectra_data:
            self.absorption_canvas.plot_multiple_spectra_comparison(
                spectra_data=spectra_data,
                x_lim=x_lim,
                normalize=self.normalize_check.isChecked(),
                y_tick_segments=self.y_segments_spin.value(),
                curve_gap=self.curve_gap_spin.value(),
                show_labels=self.show_labels_check.isChecked()
            )

    def import_spectra(self):
        """导入吸收光谱Excel文件"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Absorption Spectrum Excel File",
            "",
            "Excel Files (*.xlsx *.xls);;All Files (*)"
        )

        if not file_path:
            return

        self.current_file = file_path
        file_name = os.path.basename(file_path)
        if len(file_name) > 25:
            file_name = file_name[:22] + "..."
        self.file_label.setText(f"File: {file_name}")

        # 清空原有数据
        self.absorption_spectra.clear()
        self.spectrum_list.clear()

        try:
            # 读取Excel文件
            df = pd.read_excel(file_path)
            if df.shape[1] < 2:
                self.show_error_info("Excel file must have at least 2 columns (wavelength + absorbance)")
                return

            # 提取波长数据（第一列）
            x_data = pd.to_numeric(df.iloc[:, 0], errors='coerce')
            mask = ~np.isnan(x_data)
            x_data = x_data[mask]
            sorted_indices = np.argsort(x_data)
            x_data = x_data[sorted_indices].values

            # 数据范围校验
            if len(x_data) == 0:
                self.show_error_info("No valid wavelength data found in the first column")
                return

            # 更新数据原始范围和界面控件
            self.data_x_min = float(np.min(x_data))
            self.data_x_max = float(np.max(x_data))
            self.x_min_spin.setValue(self.data_x_min)
            self.x_max_spin.setValue(self.data_x_max)

            # 提取每个样品的吸收数据（第二列及以后）
            loaded_count = 0
            for col_idx in range(1, df.shape[1]):
                sample_name = str(df.columns[col_idx]).strip()
                if not sample_name:
                    sample_name = f"Sample_{col_idx}"

                y_data = pd.to_numeric(df.iloc[:, col_idx], errors='coerce')
                y_data = y_data[mask]
                y_data = y_data[sorted_indices].values

                if len(y_data) > 0 and not np.all(np.isnan(y_data)):
                    self.absorption_spectra[sample_name] = (x_data, y_data)
                    item = QListWidgetItem(FIF.DOCUMENT.icon(), sample_name)
                    self.spectrum_list.addItem(item)
                    loaded_count += 1

            # 更新信息
            self.info_label.setText(f"Loaded {loaded_count} spectra")
            if loaded_count > 0:
                # 默认全选
                for i in range(self.spectrum_list.count()):
                    self.spectrum_list.item(i).setSelected(True)
                self.show_success_info(f"Successfully loaded {loaded_count} spectra")
            else:
                self.show_error_info("No valid absorbance data found in the file")

        except Exception as e:
            self.show_error_info(f"Failed to load file: {str(e)}")

    def save_results(self):
        """保存当前显示的光谱图（支持自定义文件名与格式）"""
        default_filename = "absorption_spectra"
        file_filter = (
            "PNG Image (*.png);;"
            "JPEG Image (*.jpg *.jpeg);;"
            "TIFF Image (*.tif *.tiff);;"
            "PDF Vector File (*.pdf);;"
            "SVG Vector Image (*.svg)"
        )

        save_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Spectrum Image",
            default_filename,
            file_filter,
            initialFilter="PNG Image (*.png)"
        )

        if not save_path:
            return

        try:
            # 保存当前画布显示的图像
            self.absorption_canvas.figure.savefig(
                save_path,
                dpi=300,
                bbox_inches='tight'
            )
            self.show_success_info(f"Saved successfully: {os.path.basename(save_path)}")

        except Exception as e:
            self.show_error_info(f"Save failed: {str(e)}")

    def show_success_info(self, content: str):
        """显示成功信息"""
        InfoBar.success(
            title='Success',
            content=content,
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=2000,
            parent=self
        )

    def show_error_info(self, content: str):
        """显示错误信息"""
        InfoBar.error(
            title='Error',
            content=content,
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=2000,
            parent=self
        )

    def show_info(self, title: str, content: str, icon=FIF.INFO):
        """显示普通信息"""
        InfoBar(
            icon=icon,
            title=title,
            content=content,
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=2000,
            parent=self
        )

    def clear_all(self):
        """清空所有光谱数据"""
        self.absorption_spectra.clear()
        self.spectrum_list.clear()
        self.absorption_canvas.clear_plot()
        self.file_label.setText("No file selected")
        self.info_label.setText("Loaded 0 spectra")
        self.current_file = ""
        self.data_x_min = 0.0
        self.data_x_max = 0.0
        self.x_min_spin.setValue(185)
        self.x_max_spin.setValue(1100)
# -*- coding: utf-8 -*-
"""
raman_interface.py - 拉曼光谱分析界面组件
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
                            CheckBox, SpinBox, DoubleSpinBox, ToggleButton)

# 设置Matplotlib全局字体参数
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['Times New Roman', 'SimHei', 'Microsoft YaHei', 'DejaVu Sans']
matplotlib.rcParams['font.family'] = 'Times New Roman'
matplotlib.rcParams['axes.unicode_minus'] = False
matplotlib.rcParams['font.size'] = 12

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from scipy.signal import find_peaks


class CurveCanvas(QWidget):
    """拉曼光谱图显示画布"""
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
        self.ax.text(0.5, 0.5, 'No Raman spectrum data\nPlease import TXT files',
                     ha='center', va='center', fontsize=16,
                     transform=self.ax.transAxes, color='gray',
                     fontname='Times New Roman')
        self.ax.set_xlabel('Raman Shift (cm⁻¹)', fontsize=12, fontname='Times New Roman')
        self.ax.set_ylabel('Intensity (a.u.)', fontsize=12, fontname='Times New Roman')
        self.ax.set_title('Raman Spectra Comparison', fontsize=14, fontweight='bold',
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

    def plot_multiple_spectra_comparison(self, spectra_data, display_mode="full_range", normalize=True,
                                          y_tick_segments=5, curve_gap=0.3, show_labels=True,
                                          peaks_info_map=None):
        """
        绘制多光谱对比图（单条光谱选择即为单光谱显示）
        :param spectra_data: 光谱数据列表 [(x_data, y_data, curve_name), ...]
        :param display_mode: 显示模式 full_range(全频段) / rbm_mode(低频0-400 cm⁻¹)
        :param normalize: 是否归一化
        :param y_tick_segments: Y轴刻度分段数
        :param curve_gap: 曲线间距
        :param show_labels: 是否显示样品名称标签
        :param peaks_info_map: 峰值信息字典 {curve_name: (d_peak_x, d_peak_y, g_peak_x, g_peak_y, gd_ratio)}
        """
        self._plot_state = {
            "spectra_data": spectra_data,
            "display_mode": display_mode,
            "normalize": normalize,
            "y_tick_segments": y_tick_segments,
            "curve_gap": curve_gap,
            "show_labels": show_labels,
            "peaks_info_map": peaks_info_map
        }
        self._showing_placeholder = False
        self.figure.clear()
        self.ax = self.figure.add_subplot(111)
        font_config = self._get_font_config()

        if not spectra_data:
            self.ax.text(0.5, 0.5, 'No spectra data available\nPlease import spectra files',
                         ha='center', va='center', fontsize=font_config["placeholder"],
                         transform=self.ax.transAxes, color='gray',
                         fontname='Times New Roman')
            self.canvas.draw()
            return

        # 1. 根据显示模式设置X轴范围与标签位置
        all_x = []
        for data in spectra_data:
            x_data, _, _ = data
            if len(x_data) > 0:
                all_x.extend(x_data)
        all_x = np.array(all_x)

        if display_mode == "rbm_mode":
            rbm_x = all_x[(all_x >= 0) & (all_x <= 400)]
            if rbm_x.size > 0:
                x_min, x_max = np.min(rbm_x), np.max(rbm_x)
            else:
                x_min, x_max = np.min(all_x), np.max(all_x)
            xlim = (float(x_min), float(x_max))
            label_x_pos = xlim[0] + (xlim[1] - xlim[0]) * 0.78
        else:  # full_range全频段模式
            x_min, x_max = np.min(all_x), np.max(all_x)
            xlim = (float(x_min), float(x_max))
            label_x_pos = xlim[0] + (xlim[1] - xlim[0]) * 0.42

        n_curves = len(spectra_data)
        single_curve_height = 1  # 单条曲线占用高度
        # ========== 修复曲线贴底问题：新增底部基础偏移量 ==========
        base_offset = 0.15  # 底部留白高度，可根据需要调大/调小
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
        peaks_info_map = peaks_info_map or {}

        # 遍历绘制每条曲线
        for idx, (x_data, y_data, curve_name) in enumerate(spectra_data):
            if len(x_data) == 0:
                continue

            bottom, top = curve_intervals[idx]
            color = colors[idx % len(colors)]

            # ========== 修复RBM模式曲线过小问题：按当前显示区间计算归一化范围 ==========
            if display_mode == "rbm_mode":
                # RBM模式下，仅使用当前显示范围内的强度计算归一化
                rbm_mask = (x_data >= xlim[0]) & (x_data <= xlim[1])
                if np.any(rbm_mask):
                    y_min_raw = np.min(y_data[rbm_mask])
                    y_max_raw = np.max(y_data[rbm_mask])
                else:
                    y_min_raw = np.min(y_data)
                    y_max_raw = np.max(y_data)
            else:
                # 全频模式使用全范围强度
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

            # 2. 仅全频段模式下绘制峰值标注与G/D比，RBM模式跳过
            if display_mode == "full_range" and curve_name in peaks_info_map:
                d_peak_x, d_peak_y, g_peak_x, g_peak_y, gd_ratio = peaks_info_map[curve_name]
                raw_min = np.min(y_data)
                raw_max = np.max(y_data)

                # 计算峰值在显示坐标系的Y值
                if normalize and raw_max > raw_min:
                    d_peak_display_y = (d_peak_y - raw_min) / (raw_max - raw_min) * single_curve_height * 0.8 + bottom
                    g_peak_display_y = (g_peak_y - raw_min) / (raw_max - raw_min) * single_curve_height * 0.8 + bottom
                else:
                    scale_base = raw_max * 1.2 if raw_max != 0 else 1
                    d_peak_display_y = d_peak_y / scale_base * single_curve_height * 0.8 + bottom
                    g_peak_display_y = g_peak_y / scale_base * single_curve_height * 0.8 + bottom

                # 仅标注纵坐标强度，不绘制峰值点避免遮挡真实信号
                self.ax.annotate(f"D: {d_peak_y:.0f}", xy=(d_peak_x, d_peak_display_y),
                                 xytext=(d_peak_x + 10, d_peak_display_y + 0.05),
                                 fontsize=font_config["annotation"], color=color, fontname='Times New Roman')
                self.ax.annotate(f"G: {g_peak_y:.0f}", xy=(g_peak_x, g_peak_display_y),
                                 xytext=(g_peak_x + 10, g_peak_display_y + 0.05),
                                 fontsize=font_config["annotation"], color=color, fontname='Times New Roman')

                # G/D比值标注放在G峰右侧
                self.ax.text(g_peak_x + 30, top - 0.2,
                             f"G/D: {gd_ratio:.2f}", fontsize=font_config["annotation"], color=color,
                             ha='left', va='top', fontname='Times New Roman')

            # ========== 修复标签位置：显示在对应横坐标的曲线上方 ==========
            if show_labels:
                # 找到最接近label_x_pos的x坐标对应的曲线y值
                closest_x_idx = np.argmin(np.abs(x_data - label_x_pos))
                label_y_base = y_normalized[closest_x_idx]
                # 向上偏移0.05个单位，避免遮挡曲线
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
                        tick_label = f"{tick_value:.1f}"
                    all_yticklabels.append(tick_label)

        # 图形属性设置
        self.ax.set_xlabel('Raman Shift (cm⁻¹)', fontsize=font_config["axis"], fontname='Times New Roman')
        self.ax.set_ylabel('Intensity (a.u.)', fontsize=font_config["axis"], fontname='Times New Roman')
        self.ax.set_title('Raman Spectra Comparison', fontsize=font_config["title"], fontweight='bold',
                           fontname='Times New Roman')

        # ========== 坐标轴范围设置：底部新增留白，避免曲线贴底 ==========
        self.ax.set_xlim(xlim)
        self.ax.set_ylim(-0.05, total_y_height)  # 下限轻微负偏移，底部更美观

        # Y轴刻度设置
        self.ax.set_yticks(all_yticks)
        self.ax.set_yticklabels(all_yticklabels, fontsize=font_config["tick"], color='black', fontname='Times New Roman')

        # ========== 修复横坐标刻度显示不全问题 ==========
        x_span = xlim[1] - xlim[0]
        if x_span <= 500:
            tick_interval = 50
        elif x_span <= 1000:
            tick_interval = 200
        else:
            tick_interval = 500
        # 仅生成当前显示范围内的刻度，避免0刻度把显示范围重新撑回去
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
        self.ax.text(0.5, 0.5, 'No Raman spectrum data\nPlease import TXT files',
                     ha='center', va='center', fontsize=font_config["placeholder"],
                     transform=self.ax.transAxes, color='gray',
                     fontname='Times New Roman')
        self.ax.set_xlabel('Raman Shift (cm⁻¹)', fontsize=font_config["axis"], fontname='Times New Roman')
        self.ax.set_ylabel('Intensity (a.u.)', fontsize=font_config["axis"], fontname='Times New Roman')
        self.ax.set_title('Raman Spectra Comparison', fontsize=font_config["title"], fontweight='bold',
                           fontname='Times New Roman')
        self.ax.grid(True, alpha=0.3)
        self.canvas.draw()


class RamanInterface(QFrame):
    """拉曼光谱分析界面"""
    curve_selected = pyqtSignal(str)  # 光谱选择信号

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("RamanInterface")
        self.raman_spectra = {}  # 存储拉曼光谱数据 {文件名: (x_data, y_data)}
        self.current_folder = ""  # 当前选择的文件夹
        self.multiple_peaks_info = {}  # 多光谱模式下的峰信息
        self.display_mode = "full_range"  # 显示模式：full_range / rbm_mode
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
        self.raman_canvas = CurveCanvas(self)
        left_layout.addWidget(self.raman_canvas)
        main_layout.addWidget(left_widget, 3)

        # 右侧：控制面板
        right_widget = QFrame(self)
        right_widget.setObjectName("rightWidget")
        right_layout = QVBoxLayout(right_widget)

        # 顶部操作按钮
        action_row_1 = QHBoxLayout()
        action_row_1.setSpacing(8)
        action_row_2 = QHBoxLayout()
        action_row_2.setSpacing(8)

        self.import_button = PrimaryPushButton(FIF.FOLDER_ADD, 'import', self)
        self.import_button.clicked.connect(self.import_spectra)
        self.import_button.setFixedHeight(38)

        self.save_button = PrimaryPushButton(FIF.SAVE, 'save', self)
        self.save_button.clicked.connect(self.save_results)
        self.save_button.setFixedHeight(38)

        self.mode_toggle_button = ToggleButton('full range', self)
        self.mode_toggle_button.setCheckable(True)
        self.mode_toggle_button.clicked.connect(self.toggle_display_mode)
        self.mode_toggle_button.setFixedHeight(38)

        self.calc_peaks_button = PrimaryPushButton(FIF.CALORIES, 'peaks', self)
        self.calc_peaks_button.clicked.connect(self.calculate_peaks)
        self.calc_peaks_button.setFixedHeight(38)

        action_row_1.addWidget(self.import_button)
        action_row_1.addWidget(self.save_button)
        action_row_2.addWidget(self.mode_toggle_button)
        action_row_2.addWidget(self.calc_peaks_button)
        right_layout.addLayout(action_row_1)
        right_layout.addLayout(action_row_2)
        self.update_mode_toggle_button()

        # 当前文件夹标签
        self.folder_label = CaptionLabel("No folder selected", self)
        self.folder_label.setStyleSheet("color: gray; padding: 5px;")
        right_layout.addWidget(self.folder_label)

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
        self.axis_font_size_spin.setValue(self.raman_canvas.get_current_axis_font_size())
        self.axis_font_size_spin.valueChanged.connect(self.on_axis_font_size_spin_changed)

        self.label_font_size_spin = SpinBox(self)
        self.label_font_size_spin.setRange(8, 48)
        self.label_font_size_spin.setValue(self.raman_canvas.get_current_label_font_size())
        self.label_font_size_spin.valueChanged.connect(self.on_label_font_size_spin_changed)

        self.curve_gap_spin = DoubleSpinBox(self)
        self.curve_gap_spin.setRange(0.1, 1.0)
        self.curve_gap_spin.setSingleStep(0.1)
        self.curve_gap_spin.setValue(0.1)
        self.curve_gap_spin.valueChanged.connect(self.redraw_comparison)

        params_layout.addRow("Normalize:", self.normalize_check)
        params_layout.addRow("Y-axis Segments:", self.y_segments_spin)
        params_layout.addRow("Axis Size:", self.axis_font_size_spin)
        params_layout.addRow("Label Size:", self.label_font_size_spin)
        params_layout.addRow("Curve Gap:", self.curve_gap_spin)
        params_layout.addRow("Labels:", self.show_labels_check)
        right_layout.addWidget(self.params_group)
        self.raman_canvas.axis_font_size_changed.connect(self.update_axis_font_size_spin)
        self.raman_canvas.label_font_size_changed.connect(self.update_label_font_size_spin)
        self.update_axis_font_size_spin(self.raman_canvas.get_current_axis_font_size())
        self.update_label_font_size_spin(self.raman_canvas.get_current_label_font_size())

        # 加载信息标签
        self.info_label = CaptionLabel("Loaded 0 spectra", self)
        self.info_label.setStyleSheet("color: #888; padding: 5px;")
        right_layout.addWidget(self.info_label)

        # ========== 修复右侧面板被撑开问题：固定宽度+自动换行 ==========
        self.peaks_info_label = CaptionLabel("Peak info: Not calculated", self)
        self.peaks_info_label.setFixedWidth(250)  # 和列表宽度一致，避免横向撑开
        self.peaks_info_label.setWordWrap(True)  # 开启自动换行，长文本纵向显示
        self.peaks_info_label.setStyleSheet("color: #888; padding: 5px;")
        right_layout.addWidget(self.peaks_info_label)

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

    def update_mode_toggle_button(self):
        """同步模式切换按钮显示"""
        is_full_range = self.display_mode == "full_range"
        self.mode_toggle_button.setChecked(is_full_range)
        self.mode_toggle_button.setText("full range" if is_full_range else "RBM mode")

    def toggle_display_mode(self):
        """单按钮切换显示模式"""
        next_mode = "rbm_mode" if self.display_mode == "full_range" else "full_range"
        self.switch_display_mode(next_mode)

    def switch_display_mode(self, mode):
        """切换显示模式"""
        if mode == self.display_mode:
            return

        self.display_mode = mode
        self.update_mode_toggle_button()
        if mode == "full_range":
            self.calc_peaks_button.setEnabled(True)
            self.peaks_info_label.setText("Peak info: Not calculated" if not self.multiple_peaks_info else self.peaks_info_label.text())
        else:  # rbm_mode
            self.calc_peaks_button.setEnabled(False)  # RBM模式禁用峰值计算
            self.peaks_info_label.setText("Peak info: Disabled in RBM Mode")

        # 重新绘制
        self.redraw_comparison()

    def on_axis_font_size_spin_changed(self, font_size):
        """同步用户设置的坐标轴字体大小"""
        if self._syncing_axis_font_size_spin:
            return
        self.raman_canvas.set_axis_font_size(font_size)

    def on_label_font_size_spin_changed(self, font_size):
        """同步用户设置的标签字体大小"""
        if self._syncing_label_font_size_spin:
            return
        self.raman_canvas.set_label_font_size(font_size)

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
            self.raman_canvas.clear_plot()
            return

        # 准备绘图数据
        spectra_data = []
        peaks_info_map = {}
        for item in selected_items:
            spectrum_name = item.text()
            if spectrum_name in self.raman_spectra:
                x_data, y_data = self.raman_spectra[spectrum_name]
                spectra_data.append((x_data, y_data, spectrum_name))
                # 仅全频段模式传递峰值信息
                if self.display_mode == "full_range" and spectrum_name in self.multiple_peaks_info:
                    peaks_info_map[spectrum_name] = self.multiple_peaks_info[spectrum_name]

        if spectra_data:
            self.raman_canvas.plot_multiple_spectra_comparison(
                spectra_data=spectra_data,
                display_mode=self.display_mode,
                normalize=self.normalize_check.isChecked(),
                y_tick_segments=self.y_segments_spin.value(),
                curve_gap=self.curve_gap_spin.value(),
                show_labels=self.show_labels_check.isChecked(),
                peaks_info_map=peaks_info_map
            )

    def import_spectra(self):
        """导入拉曼光谱文件夹"""
        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Spectrum Folder",
            "",
            QFileDialog.ShowDirsOnly
        )

        if not folder:
            return

        self.current_folder = folder
        folder_name = os.path.basename(folder)
        if len(folder_name) > 20:
            folder_name = folder_name[:17] + "..."
        self.folder_label.setText(f"Folder: {folder_name}")

        # 清空原有数据
        self.raman_spectra.clear()
        self.spectrum_list.clear()
        self.multiple_peaks_info = {}
        self.peaks_info_label.setText("Peak info: Not calculated")

        # 查找支持的光谱文件
        supported_extensions = ['.txt', '.dat', '.csv']
        spectrum_files = []
        for file in os.listdir(folder):
            file_path = os.path.join(folder, file)
            if os.path.isfile(file_path) and any(file.lower().endswith(ext) for ext in supported_extensions):
                spectrum_files.append(file)

        if not spectrum_files:
            self.show_error_info("No supported spectrum files found")
            return

        self.show_info("Loading", f"Loading {len(spectrum_files)} spectra...", FIF.DOWNLOAD)

        # 加载光谱文件
        loaded_count = 0
        failed_count = 0
        for file in spectrum_files:
            file_path = os.path.join(folder, file)
            spectrum_name = os.path.splitext(file)[0]
            try:
                x_data, y_data = self._read_spectrum_file(file_path)
                if len(x_data) > 0 and len(y_data) > 0:
                    self.raman_spectra[spectrum_name] = (x_data, y_data)
                    item = QListWidgetItem(FIF.DOCUMENT.icon(), spectrum_name)
                    self.spectrum_list.addItem(item)
                    loaded_count += 1
            except Exception as e:
                print(f"Error loading file {file}: {str(e)}")
                failed_count += 1

        # 更新信息
        self.info_label.setText(f"Loaded {loaded_count} spectra")
        if loaded_count > 0:
            # 默认全选
            for i in range(self.spectrum_list.count()):
                self.spectrum_list.item(i).setSelected(True)
            self.show_success_info(f"Successfully loaded {loaded_count} spectra")
            if failed_count > 0:
                self.show_error_info(f"Failed to load {failed_count} files")
        else:
            self.show_error_info("Failed to load any spectrum files")

    def _read_spectrum_file(self, file_path):
        """读取光谱文件，兼容多编码和多格式"""
        x_data = []
        y_data = []
        if file_path.lower().endswith('.txt') or file_path.lower().endswith('.dat'):
            encodings_to_try = ['gbk', 'gb2312', 'utf-8', 'latin-1', 'cp1252', 'utf-8-sig']
            lines = []
            for encoding in encodings_to_try:
                try:
                    with open(file_path, 'r', encoding=encoding) as f:
                        lines = f.readlines()
                    break
                except UnicodeDecodeError:
                    continue
            if not lines:
                raise ValueError("Cannot decode file with any supported encoding")

            import re
            for line in lines:
                line = line.strip()
                if line and not line.startswith('#'):
                    parts = re.split(r'\s+', line)
                    if len(parts) >= 2:
                        try:
                            x_val = float(parts[0])
                            y_val = float(parts[1])
                            x_data.append(x_val)
                            y_data.append(y_val)
                        except ValueError:
                            continue

        elif file_path.lower().endswith('.csv'):
            try:
                df = pd.read_csv(file_path)
            except:
                try:
                    df = pd.read_csv(file_path, encoding='gbk')
                except:
                    df = pd.read_csv(file_path, encoding='utf-8')
            if df.shape[1] < 2:
                raise ValueError("CSV file must have at least 2 columns")
            x_data = df.iloc[:, 0].values
            y_data = df.iloc[:, 1].values

        # 数据清洗与排序
        x_data = pd.to_numeric(x_data, errors='coerce')
        y_data = pd.to_numeric(y_data, errors='coerce')
        mask = ~(np.isnan(x_data) | np.isnan(y_data))
        x_data = x_data[mask]
        y_data = y_data[mask]
        sorted_indices = np.argsort(x_data)
        return x_data[sorted_indices], y_data[sorted_indices]

    def calculate_peaks(self):
        """自动计算G峰、D峰和G/D比值（仅全频段模式可用）"""
        if self.display_mode != "full_range":
            self.show_error_info("Peak calculation is only available in Full Range Mode")
            return

        selected_items = self.spectrum_list.selectedItems()
        if not selected_items:
            self.show_error_info("Please select at least one spectrum first")
            return

        calculated_peaks = {}
        failed_spectra = []
        for item in selected_items:
            spectrum_name = item.text()
            if spectrum_name not in self.raman_spectra:
                failed_spectra.append(spectrum_name)
                continue
            x_data, y_data = self.raman_spectra[spectrum_name]
            try:
                calculated_peaks[spectrum_name] = self._detect_d_g_peaks(x_data, y_data)
            except Exception:
                failed_spectra.append(spectrum_name)

        if not calculated_peaks:
            self.show_error_info("No valid peaks found for the selected spectra")
            return

        self.multiple_peaks_info = calculated_peaks
        self.redraw_comparison()

        # 更新峰信息标签（已开启自动换行，无需截断）
        if len(calculated_peaks) == 1:
            name, info = next(iter(calculated_peaks.items()))
            self.peaks_info_label.setText(f"D: {info[1]:.0f}, G: {info[3]:.0f}, G/D: {info[4]:.2f}")
        else:
            peak_summary = " | ".join(f"{name}: G/D {info[4]:.2f}" for name, info in calculated_peaks.items())
            self.peaks_info_label.setText(f"Peak info: {peak_summary}")

        if failed_spectra:
            self.show_info("Partial Success", f"Calculated peaks for {len(calculated_peaks)} spectra, failed for {len(failed_spectra)}")
        else:
            self.show_success_info(f"Calculated D/G peaks for {len(calculated_peaks)} spectra")

    def _detect_d_g_peaks(self, x_data, y_data):
        """计算单条光谱的 D/G 峰和 G/D 比"""
        d_range = (1250, 1450)
        g_range = (1550, 1650)

        d_mask = (x_data >= d_range[0]) & (x_data <= d_range[1])
        g_mask = (x_data >= g_range[0]) & (x_data <= g_range[1])

        if not np.any(d_mask) or not np.any(g_mask):
            raise ValueError("No data found in expected peak ranges")

        d_x, d_y = x_data[d_mask], y_data[d_mask]
        g_x, g_y = x_data[g_mask], y_data[g_mask]

        # 寻找D峰
        d_peak_indices, _ = find_peaks(d_y, height=np.max(d_y) * 0.3, distance=10)
        if len(d_peak_indices) > 0:
            strongest_d_idx = d_peak_indices[np.argmax(d_y[d_peak_indices])]
            d_peak_x = d_x[strongest_d_idx]
            d_peak_y = d_y[strongest_d_idx]
        else:
            max_d_idx = np.argmax(d_y)
            d_peak_x = d_x[max_d_idx]
            d_peak_y = d_y[max_d_idx]

        # 寻找G峰
        g_peak_indices, _ = find_peaks(g_y, height=np.max(g_y) * 0.3, distance=10)
        if len(g_peak_indices) > 0:
            strongest_g_idx = g_peak_indices[np.argmax(g_y[g_peak_indices])]
            g_peak_x = g_x[strongest_g_idx]
            g_peak_y = g_y[strongest_g_idx]
        else:
            max_g_idx = np.argmax(g_y)
            g_peak_x = g_x[max_g_idx]
            g_peak_y = g_y[max_g_idx]

        gd_ratio = g_peak_y / d_peak_y if d_peak_y != 0 else float('inf')
        return (d_peak_x, d_peak_y, g_peak_x, g_peak_y, gd_ratio)

    def save_results(self):
        """保存当前显示的光谱图（支持自定义文件名与格式，全频段模式自动同步保存峰值分析报告）"""
        # 1. 根据当前显示模式设置默认文件名
        if self.display_mode == "full_range":
            default_filename = "raman_spectra_full_range"
        else:  # rbm_mode
            default_filename = "raman_spectra_rbm_mode"

        # 2. 定义支持的图片格式（适配科研常用格式）
        file_filter = (
            "PNG Image (*.png);;"
            "JPEG Image (*.jpg *.jpeg);;"
            "TIFF Image (*.tif *.tiff);;"
            "PDF Vector File (*.pdf);;"
            "SVG Vector Image (*.svg)"
        )

        # 3. 弹出文件保存对话框（可自定义文件名、选择格式）
        save_path, selected_filter = QFileDialog.getSaveFileName(
            self,
            "Save Spectrum Image",
            default_filename,  # 默认文件名
            file_filter,       # 格式过滤器
            initialFilter="PNG Image (*.png)"  # 默认选中PNG格式
        )

        # 用户点击取消，直接返回
        if not save_path:
            return

        try:
            # 4. 保存当前画布显示的图像（自动适配用户选择的格式）
            self.raman_canvas.figure.savefig(
                save_path,
                dpi=300,
                bbox_inches='tight'
            )

            # 5. 仅全频段模式且有峰值数据时，自动保存峰值分析报告
            saved_files = [save_path]
            if self.display_mode == "full_range" and self.multiple_peaks_info:
                # 生成和图片同名的分析报告路径
                base_path = os.path.splitext(save_path)[0]
                report_path = f"{base_path}_peak_analysis.txt"

                # 写入分析报告
                result_text = "Raman Spectrum Batch Analysis Results\n"
                result_text += "=========================================\n"
                for spectrum_name, peaks_info in self.multiple_peaks_info.items():
                    d_peak_x, d_peak_y, g_peak_x, g_peak_y, gd_ratio = peaks_info
                    result_text += f"\nSpectrum Name: {spectrum_name}\n"
                    result_text += f"D Peak Position: {d_peak_x:.2f} cm⁻¹\n"
                    result_text += f"D Peak Intensity: {d_peak_y:.2f}\n"
                    result_text += f"G Peak Position: {g_peak_x:.2f} cm⁻¹\n"
                    result_text += f"G Peak Intensity: {g_peak_y:.2f}\n"
                    result_text += f"G/D Ratio: {gd_ratio:.2f}\n"
                    result_text += "-----------------------------------------\n"

                with open(report_path, 'w', encoding='utf-8') as f:
                    f.write(result_text)
                saved_files.append(report_path)

            # 成功提示
            self.show_success_info(f"Saved successfully! Files: {'; '.join(os.path.basename(f) for f in saved_files)}")

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
        self.raman_spectra.clear()
        self.spectrum_list.clear()
        self.raman_canvas.clear_plot()
        self.folder_label.setText("No folder selected")
        self.info_label.setText("Loaded 0 spectra")
        self.peaks_info_label.setText("Peak info: Not calculated")
        self.multiple_peaks_info = {}

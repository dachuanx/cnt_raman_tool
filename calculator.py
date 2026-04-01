#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk, messagebox
import math

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("高级计算器")
        self.root.geometry("400x500")
        self.root.resizable(False, False)
        
        # 设置样式
        self.setup_styles()
        
        # 创建显示区域
        self.create_display()
        
        # 创建按钮区域
        self.create_buttons()
        
        # 初始化变量
        self.current_input = ""
        self.previous_input = ""
        self.operation = None
        self.result_displayed = False
        
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # 配置按钮样式
        style.configure('Number.TButton', font=('Arial', 12), padding=10)
        style.configure('Operator.TButton', font=('Arial', 12), padding=10, background='#f0f0f0')
        style.configure('Special.TButton', font=('Arial', 12), padding=10, background='#ff6b6b', foreground='white')
        
    def create_display(self):
        # 主显示框
        display_frame = ttk.Frame(self.root, padding=10)
        display_frame.pack(fill=tk.BOTH, expand=True)
        
        self.display_var = tk.StringVar(value="0")
        self.display = ttk.Entry(
            display_frame,
            textvariable=self.display_var,
            font=('Arial', 24),
            justify='right',
            state='readonly'
        )
        self.display.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 历史显示
        self.history_var = tk.StringVar(value="")
        history_label = ttk.Label(
            display_frame,
            textvariable=self.history_var,
            font=('Arial', 10),
            foreground='gray'
        )
        history_label.pack(anchor='e', padx=5)
        
    def create_buttons(self):
        # 按钮框架
        button_frame = ttk.Frame(self.root, padding=10)
        button_frame.pack(fill=tk.BOTH, expand=True)
        
        # 按钮布局
        buttons = [
            ['C', 'CE', '⌫', '÷'],
            ['7', '8', '9', '×'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '.', '±', '='],
            ['sin', 'cos', 'tan', '√'],
            ['π', 'e', 'x²', 'x³'],
            ['log', 'ln', '(', ')']
        ]
        
        for i, row in enumerate(buttons):
            for j, text in enumerate(row):
                # 确定按钮样式
                if text in ['C', 'CE', '⌫']:
                    style = 'Special.TButton'
                elif text in ['÷', '×', '-', '+', '=']:
                    style = 'Operator.TButton'
                elif text.isdigit() or text == '.':
                    style = 'Number.TButton'
                else:
                    style = 'Number.TButton'
                
                btn = ttk.Button(
                    button_frame,
                    text=text,
                    style=style,
                    command=lambda t=text: self.button_click(t)
                )
                btn.grid(row=i, column=j, sticky='nsew', padx=2, pady=2)
                
                # 设置网格权重
                button_frame.grid_columnconfigure(j, weight=1)
                button_frame.grid_rowconfigure(i, weight=1)
        
        # 调整特殊按钮大小
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)
        button_frame.grid_columnconfigure(2, weight=1)
        button_frame.grid_columnconfigure(3, weight=1)
        
    def button_click(self, text):
        if text == 'C':
            self.clear_all()
        elif text == 'CE':
            self.clear_entry()
        elif text == '⌫':
            self.backspace()
        elif text == '=':
            self.calculate()
        elif text in ['÷', '×', '-', '+']:
            self.set_operation(text)
        elif text == '±':
            self.toggle_sign()
        elif text in ['sin', 'cos', 'tan', '√', 'x²', 'x³', 'log', 'ln']:
            self.scientific_function(text)
        elif text in ['π', 'e']:
            self.insert_constant(text)
        elif text in ['(', ')']:
            self.insert_parenthesis(text)
        else:
            self.append_number(text)
    
    def clear_all(self):
        self.current_input = ""
        self.previous_input = ""
        self.operation = None
        self.display_var.set("0")
        self.history_var.set("")
        self.result_displayed = False
    
    def clear_entry(self):
        self.current_input = ""
        self.display_var.set("0")
    
    def backspace(self):
        if self.current_input:
            self.current_input = self.current_input[:-1]
            self.display_var.set(self.current_input if self.current_input else "0")
    
    def append_number(self, num):
        if self.result_displayed:
            self.current_input = ""
            self.result_displayed = False
        
        # 防止多个小数点
        if num == '.' and '.' in self.current_input:
            return
        
        self.current_input += num
        self.display_var.set(self.current_input)
    
    def set_operation(self, op):
        if self.current_input:
            if self.operation and self.previous_input:
                self.calculate()
            
            self.previous_input = self.current_input
            self.current_input = ""
            self.operation = op
            self.history_var.set(f"{self.previous_input} {self.get_operation_symbol(op)}")
            self.result_displayed = False
    
    def get_operation_symbol(self, op):
        symbols = {
            '÷': '÷',
            '×': '×',
            '-': '-',
            '+': '+'
        }
        return symbols.get(op, op)
    
    def toggle_sign(self):
        if self.current_input:
            if self.current_input[0] == '-':
                self.current_input = self.current_input[1:]
            else:
                self.current_input = '-' + self.current_input
            self.display_var.set(self.current_input)
    
    def scientific_function(self, func):
        try:
            if not self.current_input:
                return
            
            value = float(self.current_input)
            result = 0
            
            if func == 'sin':
                result = math.sin(math.radians(value))
            elif func == 'cos':
                result = math.cos(math.radians(value))
            elif func == 'tan':
                result = math.tan(math.radians(value))
            elif func == '√':
                if value < 0:
                    raise ValueError("不能对负数开平方根")
                result = math.sqrt(value)
            elif func == 'x²':
                result = value ** 2
            elif func == 'x³':
                result = value ** 3
            elif func == 'log':
                if value <= 0:
                    raise ValueError("对数函数的参数必须大于0")
                result = math.log10(value)
            elif func == 'ln':
                if value <= 0:
                    raise ValueError("自然对数的参数必须大于0")
                result = math.log(value)
            
            self.current_input = str(result)
            self.display_var.set(self.current_input)
            self.history_var.set(f"{func}({value}) = {result}")
            self.result_displayed = True
            
        except Exception as e:
            messagebox.showerror("错误", str(e))
            self.clear_entry()
    
    def insert_constant(self, const):
        if const == 'π':
            value = str(math.pi)
        elif const == 'e':
            value = str(math.e)
        
        if self.result_displayed:
            self.current_input = ""
            self.result_displayed = False
        
        self.current_input = value
        self.display_var.set(self.current_input)
    
    def insert_parenthesis(self, paren):
        if self.result_displayed:
            self.current_input = ""
            self.result_displayed = False
        
        self.current_input += paren
        self.display_var.set(self.current_input)
    
    def calculate(self):
        if not self.operation or not self.previous_input or not self.current_input:
            return
        
        try:
            num1 = float(self.previous_input)
            num2 = float(self.current_input)
            result = 0
            
            if self.operation == '÷':
                if num2 == 0:
                    raise ZeroDivisionError("不能除以零")
                result = num1 / num2
            elif self.operation == '×':
                result = num1 * num2
            elif self.operation == '-':
                result = num1 - num2
            elif self.operation == '+':
                result = num1 + num2
            
            # 显示结果
            self.history_var.set(f"{self.previous_input} {self.get_operation_symbol(self.operation)} {self.current_input} = {result}")
            self.current_input = str(result)
            self.display_var.set(self.current_input)
            
            # 重置状态
            self.previous_input = ""
            self.operation = None
            self.result_displayed = True
            
        except Exception as e:
            messagebox.showerror("错误", str(e))
            self.clear_all()

def main():
    root = tk.Tk()
    app = Calculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
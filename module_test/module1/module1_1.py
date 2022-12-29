from . import module1_2 # 同じディレクトリ内のmodule1_2を読み込む
import module2.module2 as mod2 # 別のモジュールを読み込む場合

def print_module_name():
  print('Module 1_1')

def print_related_module_name():
  module1_2.print_module_name()
  mod2.print_module_name()
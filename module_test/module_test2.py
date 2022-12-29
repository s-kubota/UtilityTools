import module1.module1_1 as module1_1
module1_1.print_related_module_name()

# 以下のようなコードでも可
'''
import module1.module1_1
module1.print_related_module_name()
'''

'''
from module1 import module1_1
module1_1.print_related_module_name()
'''

'''
from module1.module1_1 import print_related_module_name
print_related_module_name()
'''
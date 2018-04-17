import os
import sys

# import parents folder's module
packagePath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print(packagePath)
if packagePath in sys.path:
    # print("exist")
    sys.path.insert(0, packagePath)
else:
    sys.path.insert(0, packagePath)

# print(sys.path)

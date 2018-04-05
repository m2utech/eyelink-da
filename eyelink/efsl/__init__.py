import os, sys

#sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

print(sys.path)

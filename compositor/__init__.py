import os
import sys

this_file = os.path.abspath(__file__)
this_dir = os.path.split(this_file)[0]
root_dir = os.path.split(this_dir)[0]
pywayland_dir = os.path.join(root_dir, 'pywayland')
if os.path.exists(pywayland_dir):
    sys.path.insert(0, root_dir)

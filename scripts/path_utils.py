import os, sys

classes_dir = '../classes/'
scripts_dir = '../scripts/'
parameters_dir = '../parameters/'

'''

__file__ should get the directory that this file is in, so it should add
those dirs such that they make sense no matter where path_utils.py is called
from.

'''

sys.path.append(os.path.join(os.path.dirname(__file__), classes_dir))
sys.path.append(os.path.join(os.path.dirname(__file__), scripts_dir))
sys.path.append(os.path.join(os.path.dirname(__file__), parameters_dir))




#

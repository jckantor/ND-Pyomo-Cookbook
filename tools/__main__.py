import os
from generate_contents import *
from add_navigation import *
from add_course_info import *

add_course_info()
write_navbars()

directory = 'http://nbviewer.jupyter.org/github/jckantor/CBE30338/blob/master/notebooks/'
write_contents(INDEX_FILE, INDEX_HEADER, directory)
os.system(' '.join(['notedown', INDEX_FILE, '>', INDEX_NB]))
write_contents(README_FILE, README_HEADER, directory)

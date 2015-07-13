import sys

from compositor.compositor import Compositor
from compositor.tty import TTY

c = Compositor()
c.init_display()
c.init_socket()
c.run()
#t = TTY()
#t.setup()

#try:
#    pass
#finally:
#    t.finalize()

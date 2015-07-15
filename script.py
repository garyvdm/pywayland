from compositor.launcher import Launcher
t = Launcher()

try:
    t.setup()
    import time
    time.sleep(3)
finally:
    t.finalize()

#from compositor.compositor import Compositor
#c = Compositor()
#c.init_display()
#c.init_socket()
#c.run()

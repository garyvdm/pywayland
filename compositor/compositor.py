from pywayland.server import Display
from pywayland.protocol import Compositor as CompositorProtocol, Subcompositor, Surface
import os
import signal
import sys

keep = []


def _terminate(sig_num, display):
    print("caught signal {:d}, quitting".format(sig_num), file=sys.stderr)
    display.terminate()
    return 0


def create_surface(compositor):
    print('create: ', compositor)


def create_region(*args):
    print(args)


def _bind_compositor(resource):
    keep.append(resource)
    resource.listener['create_surface'] = create_surface
    resource.listener['create_region'] = create_region

class Compositor(object):
    def __init__(self):
        self.display = None
        self.globals_ = {}
        self.loop = None
        self._s1 = None
        self._s2 = None

    def init_display(self):
        # TODO: logging
        display = Display()
        loop = display.get_event_loop()

        s1 = loop.add_signal(signal.SIGTERM, _terminate, display)
        s2 = loop.add_signal(signal.SIGINT, _terminate, display)
        s3 = loop.add_signal(signal.SIGQUIT, _terminate, display)

        compositor = CompositorProtocol.global_class(display, 3)
        compositor.bind_handler = _bind_compositor

        subcompositor = Subcompositor.global_class(display, 1)
        # subcompositor.bind_handler = _bind_subcompositor

        self.loop = loop
        self.display = display
        self.globals_['compositor'] = compositor
        self.globals_['subcompositor'] = subcompositor

    def init_socket(self):
        sock = os.getenv("WAYLAND_DISPLAY")
        if sock is None:
            sock = "wayland-0"

        self.display.add_socket(sock)

    def run(self):
        self.display.run()
    #     s1, s2 = socket.socketpair(socket.AF_UNIX, socket.SOCK_SEQPACKET)
    #     os.set_inheritable(s1.fileno(), False)
    #     os.set_inheritable(s2.fileno(), True)
    #     self._s1 = s1
    #     self._s2 = s2

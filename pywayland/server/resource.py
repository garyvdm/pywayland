# Copyright 2015 Sean Vig
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from pywayland import ffi, lib
from .client import Client

from weakref import WeakKeyDictionary

weakkeydict = WeakKeyDictionary()


class Resource(object):
    """A server-side Interface object for the client

    Not created directly, created from the
    :class:`~pywayland.interface.Interface` object.

    :param client: The client that the Resource is for
    :type client: :class:`~pywayland.server.Client`
    :param version: The version to use for the
                    :class:`~pywayland.interface.Interface`, uses current
                    version if not specified
    :type version: `int`
    :param id: The id for the item
    :type id: `int`
    """
    def __init__(self, client, version=None, id=0):
        if version is None:
            version = self._interface.version

        self._handle = ffi.new_handle(self)
        self.version = version
        self.destructor = None

        if isinstance(client, Client):
            ptr = client._ptr
        else:
            ptr = client

        self._ptr = lib.wl_resource_create(ptr, self._interface._ptr, version, id)
        self.id = lib.wl_resource_get_id(self._ptr)

        lib.wl_resource_set_dispatcher(self._ptr, self.dispatcher._ptr, ffi.NULL,
                                       self._handle, self.dispatcher._destroyed_ptr)

    def destroy(self):
        """Destroy the Resource"""
        if self._ptr:
            lib.wl_resource_destroy(self._ptr)
            self._ptr = None

    def add_destroy_listener(self, listener):
        """Add a listener for the destroy signal

        :param listener: The listener object
        :type listener: :class:`~pywayland.server.DestroyListener`
        """
        lib.wl_resource_add_destroy_listener(self._ptr, listener._ptr)

    def _post_event(self, opcode, args):
        # Create wl_argument array
        args_ptr = self._interface.events[opcode].arguments_to_c(*args)
        # Make the cast to a wl_resource
        resource = ffi.cast('struct wl_resource *', self._ptr)

        lib.wl_resource_post_event_array(resource, opcode, args_ptr)

    def _post_error(self, code, msg=""):
        msg_ptr = ffi.new('char []', msg)
        lib.wl_resouce_post_error(self._ptr, code, msg_ptr)

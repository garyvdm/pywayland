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

from pywayland.interface import Interface
from .object import Object

import enum


class Core(Interface):
    """Interface object

    The interface object with the most basic content.
    """
    name = "wl_core"
    version = 1

    the_enum = enum.Enum("the_enum", {
        "zero": 0,
        "one": 1,
        "hex_two": 0x2,
    })


@Core.request("niuf", [Core, None, None, None])
def make_request(self, the_int, the_uint, the_fixed):
    """A request

    The request asks the server for an event.

    :param the_int: the arg summary
    :type the_int: `int`
    :param the_uint:
    :type the_uint: `uint`
    :param the_fixed:
    :type the_fixed: `fixed`
    :returns: :class:`Core`
    """
    id = self._marshal_constructor(0, Core, the_int, the_uint, the_fixed)
    return id


@Core.request("iufn", [None, None, None, Core])
def make_request2(self, the_int, the_uint, the_fixed):
    """A request

    The request asks the server for an event but move the args around.

    :param the_int: the arg summary
    :type the_int: `int`
    :param the_uint:
    :type the_uint: `uint`
    :param the_fixed:
    :type the_fixed: `fixed`
    :returns: :class:`Core` -- a :class:`Core` object
    """
    id = self._marshal_constructor(1, Core, the_int, the_uint, the_fixed)
    return id


@Core.event("no", [Core, Object])
def send_event(self, id, object):
    """A :class:`Core` event

    Send an event, but also put in some docs for our interface :class:`Core`,
    some other interface :class:`~pywayland.protocol.other.Other`, a local
    function call :func:`Core.func`, and another function call
    :func:`Other.func() <pywayland.protocol.other.Other.func>`.

    :param id: a :class:`Core` object
    :type id: :class:`Core`
    :param object: a :class:`~pywayland.protocol.object.Object` object
    :type object: :class:`~pywayland.protocol.object.Object`
    """
    self._post_event(0, id, object)


Core._gen_c()

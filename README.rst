pywayland
=========

|travis| |coveralls| |docs|

PyWayland provides a wrapper to the ``libwayland`` library using the CFFI
library to provide access to the Wayland library calls and written in pure
Python.

Below is outlined some of the basics of PyWayland and how to get up and
running.  For more help, see the `full documentation`_.

.. _full documentation: http://pywayland.readthedocs.org/

Current Release
---------------

PyWayland is still in a developmental state.  An initial version ``0.0.1a.dev5``
is available on the `cheese shop`_.  Current development versions can be
obtained from the `git repository`_, feedback, as well as any bug reports or
fixes are highly appreciated.

.. _cheese shop: https://pypi.python.org/pypi/pywayland/
.. _git repository: https://github.com/flacjacket/pywayland/

Dependencies
------------

PyWayland requires six_ and cffi_ to run on Python >=3.4.  On lower Python
versions, enum34_ is required.  PyWayland is tested against Python 2.7, 3.2+,
PyPy, and PyPy3 (see `Running Tests`_).

.. _cffi: https://cffi.readthedocs.org/
.. _enum34: https://pypi.python.org/pypi/enum34/
.. _six: https://pythonhosted.org/six/

Installing
----------

Installation can be done through pip to pull the most recently tagged release.
To see instructions on running from sounce, see the relevant documentation on
`installing from source`_.

.. _installing from source: http://pywayland.readthedocs.org/en/latest/install.html#installing-from-source

Building Wayland protocols
--------------------------

In order to run from source, you will need to generate the interfaces to the
Wayland protocol objects as defined in the wayland.xml file.  By default, this
file will be located in ``/usr/share/wayland/wayland.xml``.  In this case, the
protocol files can be generated from the setup.py file::

    $ python setup.py generate_protocol

See the help for this command to use non-default locations for the input and
output of the scanner.

The scanner is installed as a script ``pywayland-scanner`` when PyWayland is
installed.  See ``pywayland-scanner -h`` for more information.

Running Tests
-------------

PyWayland implements a (currently limited) test-suite in ``./tests``.  The
tests can be run through ``py.test``.  Be sure you build the protocol files
(see `Building Wayland protocols`_) before running the tests.

.. |coveralls| image:: https://coveralls.io/repos/flacjacket/pywayland/badge.svg?branch=master
    :alt: Build Coverage
    :target: https://coveralls.io/r/flacjacket/pywayland
.. |docs| image:: https://readthedocs.org/projects/pywayland/badge/?version=latest
    :target: https://readthedocs.org/projects/pywayland/?badge=latest
    :alt: Documentation Status
.. |travis| image:: https://travis-ci.org/flacjacket/pywayland.svg?branch=master
    :alt: Build Status
    :target: https://travis-ci.org/flacjacket/pywayland

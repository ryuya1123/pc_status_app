import platform

from pip import _internal

v = platform.platform()

_internal.main(['list'])

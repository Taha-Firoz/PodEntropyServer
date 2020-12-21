# Copyright (c) 2020 Andika Wasisto
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import platform
from ctypes import cdll, c_void_p, c_int, c_double, POINTER, c_char, c_char_p, cast


class QngWrapperLinux:

    def __init__(self):
        self._qwqng_wrapper = cdll.LoadLibrary('./libqwqng-wrapper-x86-64.so' if platform.machine().endswith('64') else './libqwqng-wrapper.so')
        self._qwqng_wrapper.GetQwqngInstance.restype = c_void_p
        self._qwqng_wrapper.RandInt32.argtypes = [c_void_p]
        self._qwqng_wrapper.RandInt32.restype = c_int
        self._qwqng_wrapper.RandUniform.argtypes = [c_void_p]
        self._qwqng_wrapper.RandUniform.restype = c_double
        self._qwqng_wrapper.RandNormal.argtypes = [c_void_p]
        self._qwqng_wrapper.RandNormal.restype = c_double
        self._qwqng_wrapper.RandBytes.argtypes = [c_void_p, c_int]
        self._qwqng_wrapper.RandBytes.restype = POINTER(c_char)
        self._qwqng_wrapper.DeviceID.argtypes = [c_void_p]
        self._qwqng_wrapper.DeviceID.restype = POINTER(c_char)
        self._qwqng_wrapper.Clear.argtypes = [c_void_p]
        self._qwqng_wrapper.Reset.argtypes = [c_void_p]
        self._qng_pointer = self._qwqng_wrapper.GetQwqngInstance()

    def deviceId(self):
        try:
            return cast(self._qwqng_wrapper.DeviceID(self._qng_pointer), c_char_p).value.decode("utf-8")
        except:
            self._qwqng_wrapper.Reset(self._qng_pointer)
            return cast(self._qwqng_wrapper.DeviceID(self._qng_pointer), c_char_p).value.decode("utf-8")
        
    def randint32(self):
        try:
            return self._qwqng_wrapper.RandInt32(self._qng_pointer)
        except:
            self._qwqng_wrapper.Reset(self._qng_pointer)
            return self._qwqng_wrapper.RandInt32(self._qng_pointer)

    def randuniform(self):
        try:
            return self._qwqng_wrapper.RandUniform(self._qng_pointer)
        except:
            self._qwqng_wrapper.Reset(self._qng_pointer)
            return self._qwqng_wrapper.RandUniform(self._qng_pointer)

    def randnormal(self):
        try:
            return self._qwqng_wrapper.RandNormal(self._qng_pointer)
        except:
            self._qwqng_wrapper.Reset(self._qng_pointer)
            return self._qwqng_wrapper.RandNormal(self._qng_pointer)

    def randbytes(self, length):
        try:
            return self._randbytes_arbitrary_length(length)
        except:
            self._qwqng_wrapper.Reset(self._qng_pointer)
            return self._randbytes_arbitrary_length(length)

    def _randbytes_arbitrary_length(self, length):
        if length <= 8192:
            return self._qwqng_wrapper.RandBytes(self._qng_pointer, length)[:length]
        else:
            data = bytearray()
            for x in range(length // 8192):
                data.extend(self._qwqng_wrapper.RandBytes(self._qng_pointer, 8192)[:8192])
            bytes_needed = length % 8192
            if bytes_needed != 0:
                data.extend(self._qwqng_wrapper.RandBytes(self._qng_pointer, bytes_needed)[:bytes_needed])
            return bytes(data)

    def clear(self):
        self._qwqng_wrapper.Clear(self._qng_pointer)

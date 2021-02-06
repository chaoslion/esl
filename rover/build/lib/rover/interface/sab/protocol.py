# PAYLOAD := ACC GYR MAG  (3*3*2*4 = 72 byte )
# 72 byte @ 115200 b/s (11520 byte/s) = 160 frames / 2
# FRAME := PAYLOAD

# 10 hz (100ms)

import asyncio
import io
from datetime import datetime
import struct
from typing import NamedTuple

from rover.interface.sab import frame


class SensorValue(NamedTuple):

    val1: int
    val2: int

    @classmethod
    def fmt(cls) -> str:
        return "ii"

    @property
    def tof(self) -> float:
        return self.val1 + self.val2 * 10 ** -6


class Frame(NamedTuple):

    # meta (pull out later)
    lost: int
    recv: int
    sync: int
    # frame
    ax: SensorValue
    ay: SensorValue
    az: SensorValue

    gx: SensorValue
    gy: SensorValue
    gz: SensorValue

    mx: SensorValue
    my: SensorValue
    mz: SensorValue

    @classmethod
    def fmt(cls) -> str:
        return "!{0}".format(
            SensorValue.fmt() * 9,
        )


class ProtocolParser(frame.FrameReader):

    def __init__(self, qout: asyncio.Queue):
        super().__init__()
        self._qout = qout
        self._frame = struct.Struct(Frame.fmt())

    def _parse_buffer(self):
        try:
            pyl = self._frame.unpack(self._buffer)
            frame = Frame(
                self._lost,
                self._recv,
                self._sync,
                # a
                SensorValue(*pyl[0:2]),
                SensorValue(*pyl[2:4]),
                SensorValue(*pyl[4:6]),
                # g
                SensorValue(*pyl[6:8]),
                SensorValue(*pyl[8:10]),
                SensorValue(*pyl[10:12]),
                # m
                SensorValue(*pyl[12:14]),
                SensorValue(*pyl[14:16]),
                SensorValue(*pyl[16:18]),
            )
            self._qout.put_nowait(frame)
        except struct.error:
            print(self._buffer.hex())
            print(self._orig_buffer.hex())
        super()._parse_buffer()

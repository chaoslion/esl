# -*- coding: utf-8 -*-

import asyncio
import sys
import datetime

from ahrs.filters import Madgwick
from ahrs.common import DEG2RAD, RAD2DEG
from ahrs.common.quaternion import Quaternion
import numpy as np
import serial_asyncio

from rovercore.interface.sab import protocol


class FrameProtocolReader(asyncio.Protocol):

    def __init__(self, consumer: asyncio.Queue):
        super().__init__()
        self._transport = None
        self._parser = protocol.ProtocolParser(consumer)

    def connection_made(self, transport):
        transport.serial.rts = False
        self._transport = transport

    def data_received(self, data):
        self._parser.receive(data)

    def connection_lost(self, exc):
        self._parser.close()


async def _printer(frames: asyncio.Queue):
    mad = Madgwick(frequency=10)
    q = np.tile([1., 0., 0., 0.], (1, 1))
    last = 0
    while True:
        now = datetime.datetime.now().timestamp()
        data: protocol.Frame = await frames.get()
        # diff = now - last
        # last = now
        # if not data:
        #     break
        # floats = list(
        #     map(
        #         lambda x: round(x.tof, 4),
        #         [
        #             data.ax, data.ay, data.az,

        #             data.mx, data.my, data.mz,
        #         ]
        #     )
        # )

        # d2g = ahrs.common.DEG2RAD
        q[0] = mad.updateMARG(
            q[0],
            list(map(lambda x: x.tof, [data.gx, data.gy, data.gz])),
            list(map(lambda x: x.tof, [data.ax, data.ay, data.az])),
            list(map(lambda x: x.tof, [data.mx, data.my, data.mz])),
        )
        quad = Quaternion(q[0])
        print(np.round(RAD2DEG * quad.to_angles(), 2))
        # yaw, pitch, roll = madgwick.Q.to_angles()
        # print(yaw, pitch, roll)

async def _main_loop():
    loop = asyncio.get_event_loop()
    q = asyncio.Queue()
    await serial_asyncio.create_serial_connection(
        loop,
        lambda: FrameProtocolReader(q),
        '/dev/ttyACM0',
        baudrate=115200,
    )
    await _printer(q)


def main():
    asyncio.run(_main_loop())
    return 0


if __name__ == "__main__":
    sys.exit(
        main(),
    )

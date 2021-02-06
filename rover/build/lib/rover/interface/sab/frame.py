# -*- coding: utf-8 -*-

import enum


@enum.unique
class FrameState(enum.IntEnum):

    STATE_SYNC = 0
    STATE_DATA = 1
    STATE_ESCP = 2


@enum.unique
class FrameFlags(enum.IntEnum):

    FLAG_SOF = 0x12
    FLAG_EOF = 0x13
    FLAG_DLE = 0x7D


class FrameWriter(object):

    def __init__(self, buffer: bytearray):
        self._buffer = buffer
        self._buffer.extend([FrameFlags.FLAG_SOF])

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self._buffer.extend([FrameFlags.FLAG_EOF])

    def _scan_byte(self, byte: int) -> bytearray:
        if byte in list(FrameFlags):
            return bytearray([FrameFlags.FLAG_DLE, byte])
        return bytearray([byte])

    def write(self, buffer: bytearray):
        for byte in buffer:
            scanned_buffer = self._scan_byte(byte)
            self._buffer.extend(scanned_buffer)


class FrameReader(object):

    def __init__(self):
        self._buffer = bytearray()
        self._orig_buffer = bytearray()
        self._lost = 0
        self._recv = 0
        self._sync = 0
        self._state: FrameState = FrameState.STATE_SYNC

    @property
    def lost(self) -> int:
        return self._lost

    def _push_byte(self, byte: int):
        self._buffer.extend(bytearray([byte]))

    def _state_sync(self, byte: int):
        if byte == FrameFlags.FLAG_SOF:
            self._buffer.clear()
            self._orig_buffer.clear()
            self._orig_buffer.extend([byte])
            self._state = FrameState.STATE_DATA
        else:
            self._lost += 1
            self._state = FrameState.STATE_SYNC

    def _state_data(self, byte: int):
        self._orig_buffer.extend([byte])

        if byte == FrameFlags.FLAG_SOF:
            # resync
            print("resync")
            self._sync += 1
            self._lost += len(self._buffer)
            self._buffer.clear()
            self._orig_buffer.clear()
            self._orig_buffer.extend([byte])
            self._state = FrameState.STATE_SYNC
        elif byte == FrameFlags.FLAG_DLE:
            self._state = FrameState.STATE_ESCP
        elif byte == FrameFlags.FLAG_EOF:
            self._recv += 1
            self._parse_buffer()
            self._state = FrameState.STATE_SYNC
        else:
            self._state = FrameState.STATE_DATA
            self._push_byte(byte)

    def _state_escp(self, byte: int):
        self._orig_buffer.extend([byte])
        self._push_byte(byte)
        self._state = FrameState.STATE_DATA

    def _single_step(self, byte: int):

        if self._state == FrameState.STATE_SYNC:
            self._state_sync(byte)
        elif self._state == FrameState.STATE_DATA:
            self._state_data(byte)
        elif self._state == FrameState.STATE_ESCP:
            self._state_escp(byte)

    def _parse_buffer(self):
        pass

    def receive(self, buffer: bytearray):
        for byte in buffer:
            self._single_step(byte)

    def close(self):
        self._qout.put_nowait(None)

    def reset(self):
        self._buffer.clear()
        self._orig_buffer.clear()
        self._lost = 0
        self._state = FrameState.STATE_SYNC

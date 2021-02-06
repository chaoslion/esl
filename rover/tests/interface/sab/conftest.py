# -*- coding: utf-8 -*-

import pytest

from rover.interface.sab import frame


@pytest.fixture
def fix_reference_buffer_data():
    return bytearray([0xFF])


@pytest.fixture
def fix_reference_buffer_sof():
    return bytearray([frame.FrameFlags.FLAG_SOF])

@pytest.fixture
def fix_reference_frame_data(fix_reference_buffer_data):
    return bytearray(
        [
            frame.FrameFlags.FLAG_SOF,
            *fix_reference_buffer_data,
            frame.FrameFlags.FLAG_EOF,
        ],
    )


@pytest.fixture
def fix_reference_frame_sof(fix_reference_buffer_sof):
    return bytearray(
        [
            frame.FrameFlags.FLAG_SOF,
            frame.FrameFlags.FLAG_DLE,
            *fix_reference_buffer_sof,
            frame.FrameFlags.FLAG_EOF,
        ],
    )


class DemoFrameReader(frame.FrameReader):

    def __init__(self):
        super().__init__()
        self._result = bytearray()

    @property
    def result(self) -> bytearray:
        return self._result

    def _parse_buffer(self):
        self._result = bytearray(self._buffer)
        super()._parse_buffer()

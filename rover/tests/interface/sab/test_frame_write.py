# -*- coding: utf-8 -*-

from rover.interface.sab import frame


def test_data(fix_reference_buffer_data, fix_reference_frame_data):
    frame_out = bytearray()
    with frame.FrameWriter(frame_out) as writer:
        writer.write(fix_reference_buffer_data)
    assert frame_out == fix_reference_frame_data


def test_sof(fix_reference_buffer_sof, fix_reference_frame_sof):
    frame_out = bytearray()
    with frame.FrameWriter(frame_out) as writer:
        writer.write(fix_reference_buffer_sof)
    assert frame_out == fix_reference_frame_sof

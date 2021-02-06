# -*- coding: utf-8 -*-

from . import conftest


def test_data(fix_reference_buffer_data, fix_reference_frame_data):
    reader = conftest.DemoFrameReader()
    reader.receive(fix_reference_frame_data)
    assert reader.result == fix_reference_buffer_data


def test_sof(fix_reference_buffer_sof, fix_reference_frame_sof):
    reader = conftest.DemoFrameReader()
    reader.receive(fix_reference_frame_sof)
    assert reader.result == fix_reference_buffer_sof

#ifndef __FRAME_H__
#define __FRAME_H__

#include <stdint.h>

struct FrameOut
{
    float a[3];
    float g[3];
    float m[3];
    uint8_t rgb[3];
    uint32_t cnt;
    // display
    // zephyr stats?
};

struct FrameIn
{
    uint8_t rgb[3];
};


void frame_tx(struct Frame*);

#endif

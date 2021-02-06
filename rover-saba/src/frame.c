#include "frame.h"

#define FLAG_SOF (uint8_t)0x12
#define FLAG_EOF (uint8_t)0x13
#define FLAG_DLE (uint8_t)0x7D

void send_out(const struct device *dev_uart, uint8_t data)
{
    uart_poll_out(dev_uart, data);
    // printk("%X\r\n", data);
}

void send_uint8(const struct device *dev_uart, uint8_t data)
{
    if ((data == FLAG_SOF) || (data == FLAG_EOF) || (data == FLAG_DLE))
    {
        send_out(dev_uart, FLAG_DLE);
        send_out(dev_uart, data);
    }
    else
    {
        send_out(dev_uart, data);
    }
}

void send_uint32(const struct device *dev_uart, uint32_t data)
{
    uint8_t a = (uint8_t)((data >> 24) & 0xFF);
    uint8_t b = (uint8_t)((data >> 16) & 0xFF);
    uint8_t c = (uint8_t)((data >> 8) & 0xFF);
    uint8_t d = (uint8_t)((data >> 0) & 0xFF);

    send_uint8(dev_uart, a);
    send_uint8(dev_uart, b);
    send_uint8(dev_uart, c);
    send_uint8(dev_uart, d);
}

void send_frame(struct Frame* frame)
{
    const struct device *dev_uart = device_get_binding(CONFIG_UART_CONSOLE_ON_DEV_NAME);
    send_out(dev_uart, FLAG_SOF);

    send_uint32(dev_uart, frame->ax.val1);
    send_uint32(dev_uart, frame->ax.val2);
    send_uint32(dev_uart, frame->ay.val1);
    send_uint32(dev_uart, frame->ay.val2);
    send_uint32(dev_uart, frame->az.val1);
    send_uint32(dev_uart, frame->az.val2);

    send_uint32(dev_uart, frame->gx.val1);
    send_uint32(dev_uart, frame->gx.val2);
    send_uint32(dev_uart, frame->gy.val1);
    send_uint32(dev_uart, frame->gy.val2);
    send_uint32(dev_uart, frame->gz.val1);
    send_uint32(dev_uart, frame->gz.val2);

    send_uint32(dev_uart, frame->mx.val1);
    send_uint32(dev_uart, frame->mx.val2);
    send_uint32(dev_uart, frame->my.val1);
    send_uint32(dev_uart, frame->my.val2);
    send_uint32(dev_uart, frame->mz.val1);
    send_uint32(dev_uart, frame->mz.val2);

    send_out(dev_uart, FLAG_EOF);
}

void transfer(struct Frame*)
{

}

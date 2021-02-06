#include <device.h>
#include <devicetree.h>
#include <display/mb_display.h>
#include <drivers/gpio.h>
#include <drivers/led_strip.h>
#include <drivers/sensor.h>
#include <drivers/uart.h>
#include <stdio.h>
#include <string.h>
#include <sys/printk.h>
#include <sys/util.h>
#include <timing/timing.h>
#include <version.h>
#include <zephyr.h>

#define DT_DEV_ACC DT_NODELABEL(bma280)
#define DT_DEV_GYR DT_NODELABEL(bmg160)
#define DT_DEV_MAG DT_NODELABEL(bmm150)

#define LED0_NODE DT_ALIAS(led0)

#define STRIP_LABEL		DT_LABEL(DT_ALIAS(led_strip))
#define STRIP_NUM_PIXELS	DT_PROP(DT_ALIAS(led_strip), chain_length)


void my_work_handler(struct k_work *work)
{
    struct Frame frame;
    const struct device *dev_acc = device_get_binding(DT_LABEL(DT_DEV_ACC));
    const struct device *dev_gyr = device_get_binding(DT_LABEL(DT_DEV_GYR));
    const struct device *dev_mag = device_get_binding(DT_LABEL(DT_DEV_MAG));

    sensor_sample_fetch(dev_acc);
    sensor_sample_fetch(dev_gyr);
    sensor_sample_fetch(dev_mag);

    sensor_channel_get(dev_acc, SENSOR_CHAN_ACCEL_X, &frame.ax);
    sensor_channel_get(dev_acc, SENSOR_CHAN_ACCEL_Y, &frame.ay);
    sensor_channel_get(dev_acc, SENSOR_CHAN_ACCEL_Z, &frame.az);

    sensor_channel_get(dev_gyr, SENSOR_CHAN_GYRO_X, &frame.gx);
    sensor_channel_get(dev_gyr, SENSOR_CHAN_GYRO_Y, &frame.gy);
    sensor_channel_get(dev_gyr, SENSOR_CHAN_GYRO_Z, &frame.gz);

    sensor_channel_get(dev_mag, SENSOR_CHAN_MAGN_X, &frame.mx);
    sensor_channel_get(dev_mag, SENSOR_CHAN_MAGN_Y, &frame.my);
    sensor_channel_get(dev_mag, SENSOR_CHAN_MAGN_Z, &frame.mz);

    send_frame(&frame);
}

K_WORK_DEFINE(my_work, my_work_handler);

void my_timer_handler(struct k_timer *dummy)
{
    k_work_submit(&my_work);
}

K_TIMER_DEFINE(my_timer, my_timer_handler, NULL);

#define RGB(_r, _g, _b) { .r = (_r), .g = (_g), .b = (_b) }

static const struct led_rgb colors[] = {
	RGB(0x0f, 0x00, 0x00), /* red */
	RGB(0x00, 0x0f, 0x00), /* green */
	RGB(0x00, 0x00, 0x0f), /* blue */
};

struct led_rgb pixels[1];

void main(void)
{
    const struct device *strip;

	strip = device_get_binding(STRIP_LABEL);

    memset(&pixels, 0x00, sizeof(pixels));
    memcpy(&pixels[0], &colors[2], sizeof(struct led_rgb));
    led_strip_update_rgb(strip, pixels, 1);

#if DT_NODE_HAS_STATUS(DT_DEV_ACC, okay)

    // printk("ACC: %p %s\n", dev_acc, dev_acc->name);
#else
    dev_acc = NULL;
#endif

#if DT_NODE_HAS_STATUS(DT_DEV_GYR, okay)

    // printk("GYR: %p %s\n", dev_gyr, dev_gyr->name);
#else
    dev_gyr = NULL;
#endif

#if DT_NODE_HAS_STATUS(DT_DEV_MAG, okay)

    // printk("MAG: %p %s\n", dev_mag, dev_mag->name);
#else
    dev_mag = NULL;
#endif

    k_timer_start(&my_timer, K_SECONDS(1), K_MSEC(100));
}

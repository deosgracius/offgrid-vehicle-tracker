#include "rlcd.h"
#include <Arduino.h>
#include <driver/spi_master.h>
#include <driver/gpio.h>
#include <esp_lcd_panel_io.h>
#include <esp_heap_caps.h>
#include <string.h>
#include "font8x8_basic.h"

// Board wiring per Waveshare demo: DisplayPort RlcdPort(12, 11, 5, 40, 41, 400, 300)
#define PIN_MOSI 12
#define PIN_SCLK 11
#define PIN_DC   5
#define PIN_CS   40
#define PIN_RST  41

static esp_lcd_panel_io_handle_t s_io;
static uint8_t *s_fb;                       // 400*300/8 = 15000 bytes, PSRAM
static const int FB_LEN = RLCD_W * RLCD_H / 8;

static void cmd(uint8_t c) { esp_lcd_panel_io_tx_param(s_io, c, NULL, 0); }
static void dat(uint8_t d) { esp_lcd_panel_io_tx_param(s_io, -1, &d, 1); }

bool rlcd_init(void) {
    spi_bus_config_t bus = {};
    bus.mosi_io_num = PIN_MOSI;
    bus.miso_io_num = -1;
    bus.sclk_io_num = PIN_SCLK;
    bus.quadwp_io_num = -1;
    bus.quadhd_io_num = -1;
    bus.max_transfer_sz = RLCD_W * RLCD_H;
    if (spi_bus_initialize(SPI3_HOST, &bus, SPI_DMA_CH_AUTO) != ESP_OK) return false;

    esp_lcd_panel_io_spi_config_t io = {};
    io.dc_gpio_num = PIN_DC;
    io.cs_gpio_num = PIN_CS;
    io.pclk_hz = 10 * 1000 * 1000;
    io.lcd_cmd_bits = 8;
    io.lcd_param_bits = 8;
    io.spi_mode = 0;
    io.trans_queue_depth = 10;
    if (esp_lcd_new_panel_io_spi((esp_lcd_spi_bus_handle_t)SPI3_HOST, &io, &s_io) != ESP_OK) return false;

    gpio_config_t rst = {};
    rst.mode = GPIO_MODE_OUTPUT;
    rst.pin_bit_mask = 1ULL << PIN_RST;
    rst.pull_up_en = GPIO_PULLUP_ENABLE;
    gpio_config(&rst);

    s_fb = (uint8_t *)heap_caps_malloc(FB_LEN, MALLOC_CAP_SPIRAM);
    if (!s_fb) return false;

    // Hardware reset
    gpio_set_level((gpio_num_t)PIN_RST, 1); vTaskDelay(pdMS_TO_TICKS(50));
    gpio_set_level((gpio_num_t)PIN_RST, 0); vTaskDelay(pdMS_TO_TICKS(20));
    gpio_set_level((gpio_num_t)PIN_RST, 1); vTaskDelay(pdMS_TO_TICKS(50));

    // ST7305 init — byte-for-byte from the Waveshare demo (do not "clean up").
    cmd(0xD6); dat(0x17); dat(0x02);
    cmd(0xD1); dat(0x01);
    cmd(0xC0); dat(0x11); dat(0x04);
    cmd(0xC1); dat(0x69); dat(0x69); dat(0x69); dat(0x69);
    cmd(0xC2); dat(0x19); dat(0x19); dat(0x19); dat(0x19);
    cmd(0xC4); dat(0x4B); dat(0x4B); dat(0x4B); dat(0x4B);
    cmd(0xC5); dat(0x19); dat(0x19); dat(0x19); dat(0x19);
    cmd(0xD8); dat(0x80); dat(0xE9);
    cmd(0xB2); dat(0x02);
    cmd(0xB3); dat(0xE5); dat(0xF6); dat(0x05); dat(0x46); dat(0x77);
               dat(0x77); dat(0x77); dat(0x77); dat(0x76); dat(0x45);
    cmd(0xB4); dat(0x05); dat(0x46); dat(0x77); dat(0x77); dat(0x77);
               dat(0x77); dat(0x76); dat(0x45);
    cmd(0x62); dat(0x32); dat(0x03); dat(0x1F);
    cmd(0xB7); dat(0x13);
    cmd(0xB0); dat(0x64);
    cmd(0x11); vTaskDelay(pdMS_TO_TICKS(200));
    cmd(0xC9); dat(0x00);
    cmd(0x36); dat(0x48);
    cmd(0x3A); dat(0x11);
    cmd(0xB9); dat(0x20);
    cmd(0xB8); dat(0x29);
    cmd(0x21);
    cmd(0x2A); dat(0x12); dat(0x2A);
    cmd(0x2B); dat(0x00); dat(0xC7);
    cmd(0x35); dat(0x00);
    cmd(0xD0); dat(0xFF);
    cmd(0x38);
    cmd(0x29);

    rlcd_clear(true);
    rlcd_flush();
    return true;
}

void rlcd_clear(bool white) { memset(s_fb, white ? 0xFF : 0x00, FB_LEN); }

// Landscape pixel layout per Waveshare demo (RLCD_SetLandscapePixel).
void rlcd_set_pixel(int x, int y, bool white) {
    if (x < 0 || x >= RLCD_W || y < 0 || y >= RLCD_H) return;
    int inv_y = RLCD_H - 1 - y;
    int index = (x / 2) * (RLCD_H / 4) + inv_y / 4;
    uint8_t bit = 7 - ((inv_y % 4) * 2 + (x % 2));
    if (white) s_fb[index] |= (1 << bit);
    else       s_fb[index] &= ~(1 << bit);
}

void rlcd_fill_rect(int x, int y, int w, int h, bool white) {
    for (int j = y; j < y + h; j++)
        for (int i = x; i < x + w; i++)
            rlcd_set_pixel(i, j, white);
}

int rlcd_draw_text(int x, int y, const char *s, int scale, bool white) {
    for (; *s; s++) {
        unsigned char c = (unsigned char)*s;
        if (c > 127) c = '?';
        const char *glyph = font8x8_basic[c];
        for (int row = 0; row < 8; row++) {
            uint8_t bits = (uint8_t)glyph[row];
            for (int col = 0; col < 8; col++) {
                if (bits & (1 << col)) {
                    rlcd_fill_rect(x + col * scale, y + row * scale, scale, scale, white);
                }
            }
        }
        x += 8 * scale;
    }
    return x;
}

void rlcd_draw_circle(int cx, int cy, int r, int thick, bool white) {
    for (int rr = r - thick + 1; rr <= r; rr++) {
        int x = rr, y = 0, err = 1 - rr;
        while (x >= y) {
            rlcd_set_pixel(cx + x, cy + y, white); rlcd_set_pixel(cx + y, cy + x, white);
            rlcd_set_pixel(cx - y, cy + x, white); rlcd_set_pixel(cx - x, cy + y, white);
            rlcd_set_pixel(cx - x, cy - y, white); rlcd_set_pixel(cx - y, cy - x, white);
            rlcd_set_pixel(cx + y, cy - x, white); rlcd_set_pixel(cx + x, cy - y, white);
            y++;
            if (err < 0) err += 2 * y + 1;
            else { x--; err += 2 * (y - x) + 1; }
        }
    }
}

void rlcd_flush(void) {
    cmd(0x2A); dat(0x12); dat(0x2A);
    cmd(0x2B); dat(0x00); dat(0xC7);
    cmd(0x2C);
    esp_lcd_panel_io_tx_color(s_io, -1, s_fb, FB_LEN);
}

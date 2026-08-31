// Minimal ST7305 reflective-LCD driver for the Waveshare ESP32-S3-RLCD-4.2.
// Landscape 400x300, 1bpp framebuffer in PSRAM. Init sequence and pixel
// layout adapted from Waveshare's demo (github.com/waveshareteam/ESP32-S3-RLCD-4.2).
// This is the DEBUG-display foundation; Josiah's real UI builds on/replaces it.
#pragma once
#include <stdint.h>
#include <stdbool.h>

#define RLCD_W 400
#define RLCD_H 300

bool rlcd_init(void);                          // SPI + panel init, clears to white
void rlcd_clear(bool white);
void rlcd_set_pixel(int x, int y, bool white); // bounds-checked
void rlcd_fill_rect(int x, int y, int w, int h, bool white);
// 8x8 font scaled by `scale` (char cell = 8*scale px). Returns x after text.
int  rlcd_draw_text(int x, int y, const char *s, int scale, bool white);
void rlcd_flush(void);                         // push framebuffer to panel

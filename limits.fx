# limits.fx


def init():
    pixels.sat = 1.0 # full colors
    pixels.hue = 0.0 # red
    pixels.val = 0.0 # off

    pixels.hs_fade = 1
    pixels.v_fade = 200

    db.gfx_frame_rate = 50

    # 59 on right
    pixels[0].val = 1.0
    pixels[59-1].val = 1.0

    # 32 on top
    pixels[59].val = 1.0
    pixels[59].hue = 0.25
    pixels[59+32-1].val = 1.0
    pixels[59+32-1].hue = 0.25

    # 60 on left
    pixels[59+32].val = 1.0
    pixels[59+32].hue = 0.5
    pixels[59+32+60-1].val = 1.0
    pixels[59+32+60-1].hue = 0.5

    # 32 on bottom
    pixels[59+32+60].val = 1.0
    pixels[59+32+60].hue = 0.75
    pixels[59+32+60+32-1].val = 1.0
    pixels[59+32+60+32-1].hue = 0.75
    

def loop():
    pixels[0].val = 1.0
hue = Number()
sat = Number()

def init():
    hue = 0.000
    sat = 1.000
    cursor = 0

    pixels.sat = sat
    pixels.hs_fade = 40
    pixels.val = 0.0

    db.gfx_frame_rate = 100


def loop():
    pixels.v_fade = 3000
    pixels.val = 0.0

    pixel = Number()
    pixel = rand(0, pixels.count)

    pixels[pixel].hue = hue
    pixels[pixel].v_fade = 100
    pixels[pixel].val = 1.0
    pixels[pixel].sat = sat

    tmp = Number()
    tmp = rand(3)
    if tmp == 0:
        hue = 0.000 + rand(0, 0.02)
        sat = 1.0
    elif tmp == 1:
        hue = 0.333 + rand(0, 0.02)
        sat = 1.0
    elif tmp == 2:
        hue = 0.000 + rand(0, 0.02)
        sat = 0.0



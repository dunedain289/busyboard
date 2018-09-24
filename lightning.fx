hue = Number()
cursor = Number()
tmp = Number()

def init():
    pixels.sat = 1.0
    pixels.val = 0.0
    pixels.hs_fade = 4000

    db.gfx_frame_rate = 100


def loop():
    # if rand() < 2000:
    #     return

    pixels.v_fade = 3000
    pixels.val = 0.0

    pixel = Number()
    pixel = rand(0, pixels.count)

    pixels[pixel].hue = hue
    pixels[pixel].v_fade = 100
    pixels[pixel].val = 1.0

    cursor += 1

    if cursor >= pixels.count:
        tmp = rand(3)
        if tmp == 0:
            hue = 0.333 # green
        elif tmp == 1:
            hue = 0.833 # purple
        elif tmp == 2:
            hue = 0.083 # orange
        hue += rand(100)
        cursor = 0


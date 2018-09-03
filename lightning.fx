hue = Number()
cursor = Number()

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
        hue = rand()
        cursor = 0


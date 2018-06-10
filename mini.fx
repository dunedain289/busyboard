# chaser.fx

# declare another variable for the cursor
cursor = Number()

# init - runs once when script is loaded
def init():
    # set pixels to full colors (maximum saturation)
    pixels.sat = 0.8

    # set pixels default hue to green
    pixels.hue = 0.333

    # set to on
    pixels.val = 0.6

    # set color fades to 500 milliseconds
    pixels.hs_fade = 500

    # override frame rate setting
    # db.gfx_frame_rate = 30


# runs periodically, frame rate is configurable
def loop():
    # set cursor - 1  pixel back to green
    pixels[cursor - 1].hs_fade = 400
    pixels[cursor - 1].sat = 0.8
    pixels[cursor - 1].v_fade = 400
    pixels[cursor - 1].val = 0.6

    # pixels at cursor to white with a 200 ms fade
    pixels[cursor].hs_fade = 100
    pixels[cursor].sat = 0.0
    pixels[cursor].v_fade = 100
    pixels[cursor].val = 1.0

    # increment cursor
    cursor += 1

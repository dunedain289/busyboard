# mini.fx

step = Number()

def init():
    pixels.sat = 1.0   # full colors
    pixels.hue = 0.333 # green
    pixels.val = 0.0   # off

    pixels.hs_fade = 500
    pixels.v_fade = 500

    step = 0

    db.gfx_frame_rate = 30

def loop():
    if pixels.is_fading == 0:
        if step == 0:
            pixels.val = 1.0
            
            for i in 59:
                pixels[i].sat = 1.0
            for i in 32:
                pixels[i+59].sat = 0
                pixels[i+59+32+60].sat = 0
            for i in 60:
                pixels[i+59+32].sat = 1.0
            
        elif step == 1:
            pixels.val = 0.0
        elif step == 2:
            pixels.val = 1.0
            
            for i in 59:
                pixels[i].sat = 0
            for i in 32:
                pixels[i+59].sat = 1.0
                pixels[i+59+32+60].sat = 1.0
            for i in 60:
                pixels[i+59+32].sat = 0

        else:
            pixels.val = 0.0

        step += 1
        if step > 3:
            step = 0

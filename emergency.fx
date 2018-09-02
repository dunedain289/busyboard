# emergency.fx

step = Number()

def init():
    pixels.sat = 1.0 # full colors
    pixels.hue = 0.0 # red
    pixels.val = 0.0 # off

    pixels.hs_fade = 1
    pixels.v_fade = 200

    step = 0

    db.gfx_frame_rate = 50

def loop():
    if pixels.is_fading == 0:
        if step == 0:
            pixels.val = 1.0
            
            for i in 59:
                pixels[i].hue = 0.0
            for i in 32:
                pixels[i+59].hue = 0.667
                pixels[i+59+32+60].hue = 0.667
            for i in 60:
                pixels[i+59+32].hue = 0.0
            
        elif step == 1:
            pixels.val = 0.0
        elif step == 2:
            pixels.val = 1.0
            
            for i in 59:
                pixels[i].hue = 0.667
            for i in 32:
                pixels[i+59].hue = 0.0
                pixels[i+59+32+60].hue = 0.0
            for i in 60:
                pixels[i+59+32].hue = 0.667

        else:
            pixels.val = 0.0

        step += 1
        if step > 3:
            step = 0

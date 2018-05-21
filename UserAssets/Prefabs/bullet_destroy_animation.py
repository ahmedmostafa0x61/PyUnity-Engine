from UserAssets.Scripts.basics import *

transform = Transform2D()
animation = Animation('Boom.png', 7, 3, smooth=False)

fade_out_speed = 6


def Start():
    global end_at_this_time
    end_at_this_time = None
    transform.scale = Vector3.ones(1.5)


def reset(scale=1):
    global end_at_this_time
    transform.scale = Vector3.ones(scale)
    end_at_this_time = Time.fixedTime + (1 / 3)


def Render():
    transform.applyTransformation()
    animation.render()


def Update():
    global end_at_this_time
    # check if the animation is still on
    if end_at_this_time is not None:
        # if animation is finished disable the script
        if Time.fixedTime > end_at_this_time:
            disable_script(__id__)
        else:
            # increase the scale for visual effects
            transform.scale += Vector3.ones() * fade_out_speed * Time.deltaTime

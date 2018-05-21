from UserAssets.Scripts.basics import *

frames = 2
transform = Transform2D()
animation = Animation('glow.png', 6, frames, smooth=False)

fade_out_speed = 2
max_scale = 5


def Start():
    reset()


def reset():
    global end_at_this_time
    end_at_this_time = None
    transform.scale = Vector3.ones(1)
    end_at_this_time = Time.fixedTime + (1 / frames)


def Render():
    transform.applyTransformation()
    animation.render()


def Update():
    global end_at_this_time
    if end_at_this_time is not None:
        if Time.fixedTime > end_at_this_time:
            disable_script(__id__)
        elif transform.scale.squareMagnitude() < max_scale * max_scale:
            transform.scale += Vector3.ones() * fade_out_speed * Time.deltaTime

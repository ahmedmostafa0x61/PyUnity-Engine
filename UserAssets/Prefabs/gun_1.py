from UserAssets.Scripts.basics import *

mag_size = 10
fire_rate = 5
transform = Transform2D()
gun_sound = SFX('sndShoot1')
gun = SpriteRenderer('gun_1.png', smooth=False)
bullet_shape = SpriteRenderer('bullet_1.png', smooth=False)


def Start():
    global last_shot_time, mag
    transform.scale = Vector3.ones(2)
    last_shot_time = Time.fixedTime

    mag = []
    # object pooling to save performance. what is object pooling? GOOGLE IT!
    for i in range(mag_size):
        # Create new bullet and add it to the queue
        bullet = instantiate_script('bullet')
        disable_script(bullet.__id__)
        set_bullet_settings(bullet)
        mag.append(bullet)


def set_bullet_settings(bullet):
    bullet.transform.scale = Vector3.ones(1.5)
    bullet.bullet_shape = bullet_shape
    bullet.speed = 15.0
    bullet.power = 26


def Render():
    transform.applyTransformation()
    gun.render()


def fire():
    global last_shot_time, mag

    # check if the gun can fire or need to reload
    if Time.fixedTime > last_shot_time + (1 / fire_rate) and Input.MouseKeyDown(0):
        last_shot_time = Time.fixedTime
        gun_sound.play()

        b = mag.pop(0)
        b.transform.position = transform.position
        b.transform.up = transform.right
        enable_script(b.__id__)
        mag.append(b)

from UserAssets.Scripts.basics import *

mag_size = 5
fire_rate = .7
transform = Transform2D()
gun_sound = SFX('sndShoot3')
gun = SpriteRenderer('gun_2.png', smooth=False)
bullet_shape = SpriteRenderer('bullet_2.png', smooth=False)


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
    bullet.speed = 18.0
    bullet.power = 40


def Render():
    transform.applyTransformation()
    gun.render()


def fire():
    global last_shot_time, mag

    # check if the gun can fire or need to reload
    if Time.fixedTime > last_shot_time + (1 / fire_rate):
        last_shot_time = Time.fixedTime
        gun_sound.play()

        b0 = mag.pop(0)
        b0.transform.position = transform.position
        b0.transform.up = transform.right
        enable_script(b0.__id__)
        mag.append(b0)

        b0 = mag.pop(0)
        b0.transform.position = transform.position
        b0.transform.up = transform.right + transform.up * 0.1
        enable_script(b0.__id__)
        mag.append(b0)

        b0 = mag.pop(0)
        b0.transform.position = transform.position
        b0.transform.up = transform.right - transform.up * 0.1
        enable_script(b0.__id__)
        mag.append(b0)

        b0 = mag.pop(0)
        b0.transform.position = transform.position
        b0.transform.up = transform.right + transform.up * 0.2
        enable_script(b0.__id__)
        mag.append(b0)

        b0 = mag.pop(0)
        b0.transform.position = transform.position
        b0.transform.up = transform.right - transform.up * 0.2
        enable_script(b0.__id__)
        mag.append(b0)

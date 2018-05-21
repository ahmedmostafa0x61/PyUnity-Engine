from UserAssets.Scripts.basics import *

mag_size = 10
fire_rate = 1.2
transform = Transform2D()
gun_sound = SFX('sndShoot2')
gun = SpriteRenderer('gun_3.png', smooth=False)
bullet_shape = SpriteRenderer('bullet_3.png', smooth=False)


def Start():
    global last_shot_time, mag
    transform.scale = Vector3.ones(3)
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
    bullet.transform.scale = Vector3.ones(1)
    bullet.bullet_shape = bullet_shape
    bullet.destructible = False
    bullet.speed = 25.0
    bullet.power = 100


def Render():
    glPushMatrix()
    transform.applyTransformation()
    gun.render()
    glPopMatrix()


def fire():
    global last_shot_time, mag

    # check if the gun can fire or need to reload
    if Time.fixedTime > last_shot_time + (1 / fire_rate):
        gun_sound.play()

        last_shot_time = Time.fixedTime
        b0 = mag.pop(0)
        b0.transform.position = transform.position + transform.right
        b0.transform.up = transform.right + transform.up * 0.1
        enable_script(b0.__id__)

        b1 = mag.pop(0)
        b1.transform.position = transform.position + transform.right
        b1.transform.up = transform.right - transform.up * 0.1
        enable_script(b1.__id__)

        mag.append(b0)
        mag.append(b1)

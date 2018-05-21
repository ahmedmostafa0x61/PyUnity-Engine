from UserAssets.Scripts.basics import *

left = 10
mag_size = 10
fire_rate = 10
transform = Transform2D()
gun_sound = SFX('sndShoot3')
gun = SpriteRenderer('gun_4.png', smooth=False)
bullet_shape = SpriteRenderer('bullet_4.png', smooth=False)


def Start():
    global last_shot_time, mag, ready
    transform.scale = Vector3.ones(2)
    last_shot_time = Time.fixedTime
    ready = False

    mag = []
    for i in range(mag_size):
        # Create new bullet and add it to the queue
        bullet = instantiate_script('bullet')
        disable_script(bullet.__id__)
        set_bullet_settings(bullet)
        mag.append(bullet)


def set_bullet_settings(bullet):
    bullet.transform.scale = Vector3.ones(1.5)
    bullet.bullet_shape = bullet_shape
    bullet.destructible = True
    bullet.speed = 20.0
    bullet.power = 36


def Render():
    transform.applyTransformation()
    gun.render()


def Update():
    global left, ready
    if left <= mag_size:
        left += Time.deltaTime * 3.5

    if left > 5:
        ready = True


def fire():
    global last_shot_time, mag, left, ready

    # check if the gun can fire or need to reload
    if Time.fixedTime > last_shot_time + (1 / fire_rate) and left > 0 and ready:
        gun_sound.play()

        last_shot_time = Time.fixedTime
        b = mag.pop(0)
        b.transform.position = transform.position + transform.right
        b.transform.up = transform.right
        enable_script(b.__id__)
        mag.append(b)
        left -= 1

    if left <= 0:
        ready = False

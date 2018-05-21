from UserAssets.Scripts.basics import *


speed = 4
power = 18
health = 100
max_speed = 10
active_game = True
transform = Transform2D()
die_sound = SFX('sndDie')
hit_sound = SFX('sndEnemy_hit_04')
animation = Animation('Enemy.png', 4, 1, smooth=False)


def Start():
    BoxCollider2D(.8, .8, transform, __id__, 'cell').on_collision_trigger(on_collision)

    global previous_hits, destroy_animation
    destroy_animation = instantiate_script('enemy_destroy_animation')
    disable_script(destroy_animation.__id__)
    transform.scale = Vector3.ones(3)
    previous_hits = {}


def Events(event_name, *args):
    global active_game

    if event_name == 'pause_the_game':
        active_game = False

    if event_name == 'resume_the_game':
        active_game = True


def Render():
    transform.applyTransformation()
    animation.render()


def Update():
    global speed

    if active_game is False:
        return

    target = get_script('player').transform.position
    direction = target - transform.position

    if direction.x > 0:
        transform.scale.x = +abs(transform.scale.x)
    else:
        transform.scale.x = -abs(transform.scale.x)

    transform.position += direction.normalized() * Time.deltaTime * speed

    if speed < max_speed:
        speed += Time.deltaTime


def LateUpdate():
    global health, destroy_animation

    if health <= 0:
        die_sound.play()
        get_script('settings').zombies_left -= 1

        destroy_animation.transform.position = transform.position
        enable_script(destroy_animation.__id__)
        destroy_animation.reset()
        disable_script(__id__)


def on_collision(hit_id, hit_tag):
    global health, previous_hits, speed
    if hit_tag == 'player':
        speed = max_speed / np.random.uniform(2, 3)

    # when colliding with another cell, go away from it.
    if hit_tag == 'cell':
        direction = transform.position - get_script(hit_id).transform.position
        transform.position += direction.normalized() * Time.deltaTime

    # if hit by bullet, take damage
    if hit_tag == 'bullet':
        if hit_id not in previous_hits:
            hit_sound.play()
            previous_hits[hit_id] = Time.fixedTime
            bullet_power = get_script(hit_id).power
            health -= bullet_power
            #get_script('player').transform.scale += Vector3(1, 1, 0)
        else:
            # if the bullet was there but long time is passed now, take damage again
            if Time.fixedTime > previous_hits[hit_id] + 2:
                previous_hits[hit_id] = Time.fixedTime
                bullet_power = get_script(hit_id).power
                health -= bullet_power


def reset(position=Vector3.zeros()):
    global health, previous_hits, speed
    transform.position = position
    speed = max_speed / 4
    previous_hits = {}
    health = 100

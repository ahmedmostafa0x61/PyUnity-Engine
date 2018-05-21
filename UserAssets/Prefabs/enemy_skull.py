from UserAssets.Scripts.basics import *

speed = 2
power = 25
health = 100
time_down = 2.5
active_game = True
transform = Transform2D()
die_sound = SFX('sndDie')
hit_sound = SFX('sndEnemy_hit_03')
animation = Animation('skull.png', 4, 1, smooth=False)


def Start():
    BoxCollider2D(.8, .8, transform, __id__, 'skull').on_collision_trigger(on_collision)

    global cooldown, swimming, target, previous_hits, destroy_animation
    destroy_animation = instantiate_script('enemy_destroy_animation')
    disable_script(destroy_animation.__id__)
    transform.scale = Vector3.ones(3)
    target = transform.position
    cooldown = Time.fixedTime
    previous_hits = {}
    swimming = False


def Events(event_name, *args):
    global active_game

    if event_name == 'pause_the_game':
        active_game = False

    if event_name == 'resume_the_game':
        active_game = True


def Render():
    global hit
    transform.applyTransformation()
    animation.render()


def Update():
    global cooldown, swimming, target

    if active_game is False:
        return

    if Time.fixedTime > cooldown + time_down:
        player_position = get_script('player').transform.position
        direction = (player_position - transform.position).normalized()

        if direction.x > 0:
            transform.scale.x = +abs(transform.scale.x)
        else:
            transform.scale.x = -abs(transform.scale.x)

        target = player_position + direction * speed * 2
        cooldown = Time.fixedTime
        swimming = True

    if swimming:
        transform.position = lerp(transform.position, target, Time.deltaTime * speed)


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
    global health, previous_hits
    # if hit by bullet, take damage
    if hit_tag == 'bullet':
        hit_sound.play()
        if hit_id not in previous_hits:
            previous_hits[hit_id] = Time.fixedTime
            bullet_power = get_script(hit_id).power
            health -= bullet_power
            #get_script('player').transform.scale += Vector3(1,1,0)

        else:
            # if the bullet was there but long time is passed now, take damage again
            if Time.fixedTime > previous_hits[hit_id] + 2:
                previous_hits[hit_id] = Time.fixedTime
                bullet_power = get_script(hit_id).power
                health -= bullet_power


def reset(position):
    global health, previous_hits
    transform.position = position
    previous_hits = {}
    health = 100

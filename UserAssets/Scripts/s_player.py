from UserAssets.Scripts.basics import *

# The Game Engine Components
__id__ = 'player'
current_hp = 1000
list_of_hits = {}
active_game = True
transform = Transform2D()
hit_sound = SFX('sndBhits_02')
animation = Animation('player_animation.png', 7, 2, smooth=False)

# User Data Variables.
player_speed = 5


def Events(event_name, *args):
    global active_game,collider
    # start moving the player and rendering it only when start button is pressed
    if event_name == 'start_the_game':
        StartPlayer()
        active_game = True
        enable_script(__id__)

    if event_name == 'pause_the_game':
        active_game = False

    if event_name == 'resume_the_game':
        active_game = True


def Start():
    disable_script(__id__)


def StartPlayer():
    global isMoving, player_gun, hit,collider

    # we simply editing the player settings here.
    isMoving, hit = False, False
    transform.scale = Vector3.ones(4)
    player_gun = instantiate_script(get_variable('player_gun', 'gun_1'))

    # create a box collider for the player and set collision method to our own
    collider = BoxCollider2D(1.5, 2, transform, __id__, 'player')
    collider.on_collision_trigger(on_collision)


def Render():
    global isMoving, hit
    transform.applyTransformation()
    animation.render(animate=isMoving, color=Vector3(1, .2, .2) if hit else Vector3.ones())
    hit = False


def Update():
    global isMoving, player_gun

    if active_game is False:
        return

    # Check wither or not the player is moving so that the moving animation can be triggered on or off.
    if Input.KeyHold('w') or Input.KeyHold('s') or Input.KeyHold('d') or Input.KeyHold('a'):
        isMoving = True
    else:
        isMoving = False

    # Check for keyboard strokes to move the player on the major axis. x, y
    if Input.KeyHold('w'):
        transform.position += Vector3(0, 1, 0) * Time.deltaTime * player_speed
    elif Input.KeyHold('s'):
        transform.position -= Vector3(0, 1, 0) * Time.deltaTime * player_speed

    if Input.KeyHold('d'):
        transform.position += Vector3(1, 0, 0) * Time.deltaTime * player_speed
    elif Input.KeyHold('a'):
        transform.position -= Vector3(1, 0, 0) * Time.deltaTime * player_speed

    # Rotate the gun and flip player direction based on mouse position
    mouse_pos = Camera.screenToWorld(Input.MousePosition())
    player_gun.transform.right = (mouse_pos - player_gun.transform.position).normalized()

    if player_gun.transform.right.x > 0:
        transform.scale.x = +abs(transform.scale.x)
        player_gun.transform.scale.y = +abs(player_gun.transform.scale.y)
    else:
        transform.scale.x = -abs(transform.scale.x)
        player_gun.transform.scale.y = -abs(player_gun.transform.scale.y)

    # Reposition the gun
    player_gun.transform.position = transform.position - transform.up * 0.3

    # Shoot
    if Input.MouseKeyHoldDown(0):
        player_gun.fire()

    if current_hp <= 0:
        instantiate_script('game_over_screen')
        castEvent('pause_the_game', None)

    # Camera follow the player
    Camera.position = lerp(Camera.position, transform.position, Time.deltaTime * player_speed * 0.4)
    Camera.position.z = -10


def on_collision(hit_id, hit_tag):
    global hit, current_hp, list_of_hits

    # check if the player is hit with enemy to set the color flag and check to damages
    if hit_tag == 'skull' or hit_tag == 'cell':
        hit = True

        # check if 2.5 sec were past since the last hit from the same enemy, if so. reset the take new hit
        if hit_id in list_of_hits:
            if Time.fixedTime > list_of_hits[hit_id] + 2.5:
                del list_of_hits[hit_id]
        else:
            # if hit. take the damage and add the enemy to the list
            list_of_hits[hit_id] = Time.fixedTime
            enm_power = get_script(hit_id).power

            if active_game:
                current_hp -= enm_power
                hit_sound.play()

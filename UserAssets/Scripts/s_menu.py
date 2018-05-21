from UserAssets.Scripts.basics import *

menu_state = 'start_game_menu'
__id__="1"
# Different transforms to move each button at desired location
exit_button_transform = Transform2D()
start_button_transform = Transform2D()
pause_button_transform = Transform2D()

gun_1_transform = Transform2D()
gun_2_transform = Transform2D()
gun_3_transform = Transform2D()
gun_4_transform = Transform2D()

# texture of the buttons that will be drawn
background = SpriteRenderer('Background.png')
exit_button_sprite = SpriteRenderer('exit.png')
start_button_sprite = SpriteRenderer('newgame.png')
pause_button_sprite = SpriteRenderer('pause.png', smooth=False)

gun_1_sprite = SpriteRenderer('gun_1.png')
gun_2_sprite = SpriteRenderer('gun_2.png')
gun_3_sprite = SpriteRenderer('gun_3.png')
gun_4_sprite = SpriteRenderer('gun_4.png')

#disable_script(__id__)
def Start():
    global start_darken, exit_darken, active_gun

    # move evey button to it's location
    start_darken, exit_darken = False, False
    active_gun = get_variable('player_gun', 'gun_1')

    pause_button_transform.scale = Vector3.ones(2)
    start_button_transform.position.y = 3
    exit_button_transform.position.y = -3

    gun_1_transform.position = Vector3(-5, 0, 0)
    gun_2_transform.position = Vector3(-2, 0, 0)
    gun_3_transform.position = Vector3(+2, 0, 0)
    gun_4_transform.position = Vector3(+5, 0, 0)

    gun_1_transform.scale = Vector3.ones(3)
    gun_2_transform.scale = Vector3.ones(3)
    gun_3_transform.scale = Vector3.ones(3)
    gun_4_transform.scale = Vector3.ones(3)


def Events(event_name, *arg):
    global menu_state
    if event_name == 'resume_the_game' or event_name == 'start_the_game':
        menu_state = 'mid_game_menu'


def Render():
    global start_darken, exit_darken, active_gun

    # render the background and buttons
    # push and pop to isolate every transform from the one before it
    # start_darken and exit_darken are used to identify wither the mouse is on the buttons or not
    if menu_state == 'start_game_menu':
        background.render()

        glPushMatrix()
        start_button_transform.applyTransformation()
        start_button_sprite.render(brightness=0.5 if start_darken else 1)
        glPopMatrix()

        glPushMatrix()
        exit_button_transform.applyTransformation()
        exit_button_sprite.render(brightness=0.5 if exit_darken else 1)
        glPopMatrix()

        glPushMatrix()
        gun_1_transform.applyTransformation()
        gun_1_sprite.render(brightness=1 if active_gun == 'gun_1' else .2)
        glPopMatrix()

        glPushMatrix()
        gun_2_transform.applyTransformation()
        gun_2_sprite.render(brightness=1 if active_gun == 'gun_2' else .2)
        glPopMatrix()

        glPushMatrix()
        gun_3_transform.applyTransformation()
        gun_3_sprite.render(brightness=1 if active_gun == 'gun_3' else .2)
        glPopMatrix()

        glPushMatrix()
        gun_4_transform.applyTransformation()
        gun_4_sprite.render(brightness=1 if active_gun == 'gun_4' else .2)
        glPopMatrix()

    if menu_state == 'mid_game_menu':
        glPushMatrix()
        pause_button_transform.applyTransformation()
        pause_button_sprite.render(color=Vector3(.5, .5, .5))
        glPopMatrix()


def Update():
    global start_darken, exit_darken, active_gun, menu_state

    # initialize mouse on buttons to False.
    start_darken, exit_darken = False, False

    if Input.KeyDown(' '):
        castEvent('resume_the_game', None)

    if menu_state == 'mid_game_menu':
        if mouse_inside_transform(pause_button_transform, 1, 1) and Input.MouseKeyDown(0):
            castEvent('pause_the_game', None)
            menu_state = 'paused_game_menu'

    if menu_state == 'start_game_menu':
        # check if the mouse is inside the button start and if so set start_darken
        if mouse_inside_transform(start_button_transform, 3, 1):
            start_darken = True

            # if the user pressed the button start disable this script and cast start_the_game event
            if Input.MouseKeyDown(0):
                menu_state = 'mid_game_menu'
                castEvent('start_the_game')

        # same idea as above
        if mouse_inside_transform(exit_button_transform, 2, 1):
            exit_darken = True
            if Input.MouseKeyDown(0):
                save_data_base()
                quit()

        # Select gun
        if mouse_inside_transform(gun_1_transform, 1.2, .8) and Input.MouseKeyDown(0):
            set_variable('player_gun', 'gun_1')

        if mouse_inside_transform(gun_2_transform, 1.2, .8) and Input.MouseKeyDown(0):
            set_variable('player_gun', 'gun_2')

        if mouse_inside_transform(gun_3_transform, 1.2, .8) and Input.MouseKeyDown(0):
            set_variable('player_gun', 'gun_3')

        if mouse_inside_transform(gun_4_transform, 1.2, .8) and Input.MouseKeyDown(0):
            set_variable('player_gun', 'gun_4')

        active_gun = get_variable('player_gun', 'gun_1')


def LateUpdate():
    pause_button_transform.position = Camera.screenToWorld(Vector3(1, 1, 0)) + Vector3(-1.3, -1, 0)


def mouse_inside_transform(t, w, h):
    """

    :param t: (Transform2D) the transform of the box
    :param w: (float)       the width of the box
    :param h: (float)       the height of the box
    :return: True of False wither the mouse is on the box
    """

    # get the mouse position
    mouse_pos = Camera.screenToWorld(Input.MousePosition())

    # if the mouse_pos outside the x axis return False
    if mouse_pos.x > t.position.x + w or mouse_pos.x < t.position.x - w:
        return False

    # if the mouse_pos outside the y axis return False
    if mouse_pos.y > t.position.y + h or mouse_pos.y < t.position.y - h:
        return False

    return True





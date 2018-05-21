from UserAssets.Scripts.basics import *


enemy_list = []
enemies_alive = 0
active_game = True
max_enemies_alive = 3
enemies_pooling_size = 20
zombie_spawn_interval = 3
enemies = {'enemy_cell': .65, 'enemy_skull': .35}


def Start():
    load_zombies()
    reset()

    # we disable this script so that it won't spawn anything until the start event is triggered
    disable_script(__id__)


def Events(event_name, *args):
    global active_game

    # we only enable the map spawning if the start button is pressed
    if event_name == 'start_the_game':
        enable_script(__id__)
        reset()

    if event_name == 'pause_the_game':
        active_game = False

    if event_name == 'resume_the_game':
        active_game = True


def load_zombies():
    global player_transform, last_spawn_time

    # get the player transform and store a pointer to it to use it later
    player_transform = get_script('player').transform

    # last_spawn_time determine when to spawn a new enemy
    last_spawn_time = Time.fixedTime

    # enemies pooling
    # this way we save tons of the performance.
    # make list of the enemies and disable them all.
    # instead of loading the enemies evey time, we load them once and queue them.

    names = list(enemies.keys())
    probabilities = list(enemies.values())

    for _ in range(enemies_pooling_size):
        selected_zombie = np.random.choice(names, p=probabilities)
        obj = instantiate_script(selected_zombie)
        enemy_list.append(obj)
        disable_script(obj.__id__)


def reset():
    global last_zombies_alive, zombie_spawn_interval, max_enemies_alive
    zombie_spawn_interval = 3
    last_zombies_alive = get_script('settings').zombies_left
    max_enemies_alive = 3


def Update():
    global last_spawn_time, player_transform, enemies_alive, last_zombies_alive, zombie_spawn_interval

    if active_game is False or get_script('settings').zombies_left + enemies_alive <= 0:
        return

    # check if a zombie died so that it can spawn new one
    if get_script('settings').zombies_left < last_zombies_alive:
        dead_count = last_zombies_alive - get_script('settings').zombies_left
        last_zombies_alive = get_script('settings').zombies_left
        enemies_alive = enemies_alive - dead_count

    # check isf 3 secs were passed after the last spawn.
    if Time.fixedTime > last_spawn_time + zombie_spawn_interval and enemies_alive < max_enemies_alive:
        last_spawn_time = Time.fixedTime
        enemies_alive += 1

        # we get a new enemy from the end of the list and spawn it. then we add it to the beginning of the list
        enemy = enemy_list.pop(0)
        enemy.reset(player_transform.position + random_point_on_unit_circle() * 20)
        enable_script(enemy.__id__)
        enemy_list.append(enemy)

    if zombie_spawn_interval > 0.5:
        zombie_spawn_interval -= 0.02 * Time.deltaTime

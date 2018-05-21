from UserAssets.Scripts.basics import *


transform = Transform2D()
destructible = True
bullet_shape = None
speed = 0
power = 0


def Start():
    global rotation_speed, destroy_animation
    BoxCollider2D(.2, .2, transform, __id__, 'bullet').on_collision_trigger(on_collision)
    rotation_speed = np.sign(random.randint(-100, 100)) * random.randint(400, 600)
    destroy_animation = instantiate_script('bullet_destroy_animation')
    disable_script(destroy_animation.__id__)


def Render():
    if bullet_shape is not None:
        transform.applyTransformation()
        bullet_shape.render()


def Update():
    transform.position += transform.up * Time.deltaTime * speed
    transform.rotation.z += rotation_speed * Time.deltaTime


def on_collision(hit_id, hit_tag):
    global destroy_animation
    if hit_tag == 'cell' or hit_tag == 'skull':
        destroy_animation.transform.position = transform.position
        enable_script(destroy_animation.__id__)
        destroy_animation.reset()

        if destructible:
            disable_script(__id__)

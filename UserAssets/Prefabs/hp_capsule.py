from UserAssets.Scripts.basics import *

transform = Transform2D()
capsule_taken_sound = SFX('sndCapsule')
capsule = SpriteRenderer('capsule_glow.png', smooth=False)


def Start():
    BoxCollider2D(.2, .2, transform, __id__, 'capsule').on_collision_trigger(on_collision)
    transform.scale = Vector3.ones(2)


def Render():
    transform.applyTransformation()
    capsule.render(color=Vector3(.5, 1, .75))


def on_collision(hit_id, hit_tag):
    if hit_tag == 'player':
        ds = instantiate_script('bullet_destroy_animation')
        ds.transform.position = transform.position
        ds.reset(2)

        get_script(hit_id).current_hp += 30
        capsule_taken_sound.play()
        disable_script(__id__)

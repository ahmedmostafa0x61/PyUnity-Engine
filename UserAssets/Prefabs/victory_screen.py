from UserAssets.Scripts.basics import *

transform = Transform2D()
victory = SpriteRenderer('victory.png', smooth=False)


def Start():
    transform.position = Camera.position
    transform.scale = Vector3.ones(1.8)
    transform.position.z = -5


def Render():
    transform.applyTransformation()
    victory.render()


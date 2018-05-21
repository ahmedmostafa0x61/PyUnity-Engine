from UserAssets.Scripts.basics import *

transform = Transform2D()
game_over = SpriteRenderer('game_over.png', smooth=False)


def Start():
    transform.position = Camera.position
    transform.position.z = -5


def Render():
    transform.applyTransformation()
    game_over.render()


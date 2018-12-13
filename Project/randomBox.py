from .framework import (Framework, main)
from Box2D import (b2EdgeShape, b2FixtureDef, b2PolygonShape, b2Random, b2_dynamicBody, b2CircleShape,)
import random

def box_sizes():
    return(random.uniform(1, 3),random.uniform(1, 6))

def position_vectors():
    return (random.uniform(5,8) ,random.uniform(0, 30))

class randomBox (Framework):
    name = "randomBox"

    def __init__(self):
        super(randomBox, self).__init__()

        ground = self.world.CreateStaticBody(
            position=(0, 0),
            shapes=[b2EdgeShape(vertices=[(-50, 0), (50, 0)])]
        )

        rect_density = 30.0
        struct_length = random.randint(1,4)
        struct_height = random.randint(4,8)

        for i in range(struct_length):
            for j in range(struct_height):
                self.world.CreateDynamicBody(
                        position=position_vectors(),
                        fixtures=b2FixtureDef(
                            shape=b2PolygonShape(box=box_sizes()),
                            density=rect_density)
                    )
if __name__ == "__main__":
    main(randomBox)

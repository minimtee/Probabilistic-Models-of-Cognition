from .framework import (Framework, main)
from Box2D import (b2EdgeShape, b2FixtureDef, b2PolygonShape, b2Random, b2_dynamicBody, b2CircleShape,)

class Tower (Framework):
    name = "Tower"

    def __init__(self):
        super(Tower, self).__init__()

        #Ground
        ground = self.world.CreateStaticBody(
            position=(0, 0),
            shapes=[b2EdgeShape(vertices=[(-30, 0), (30, 0)])]#,
##            b2PolygonShape(box=(0.2, 5, (0.5, 5),0))]
        )

##        self.world.CreateStaticBody(
##            shapes=[b2PolygonShape(box=[1, 1, (5, 15), 0]),
##                    b2PolygonShape(box=[1, 1, (-2, 12), 0]),
##                    ]
##        )

        self._x = 0


##        self.body = self.world.CreateDynamicBody(
##            position=(0.5, 10),
##            fixtures=b2FixtureDef(
##                shape=b2PolygonShape(box=(4, 0.1)), density=1.0),
##        )

        # Small circle
        #circle = b2FixtureDef(
            #shape=b2CircleShape(radius=0.25),
            #density=100.0,
        #)

        # Generate bullet (circle)
        #self.bullet = self.world.CreateBody(
            #position=(self._x, 30),
            #bullet=True,
            #type=b2_dynamicBody,
            #fixtures=circle,
            #linearVelocity=(0, -50)
        #)


        self.stack1 = self.world.CreateDynamicBody(
            position=(self._x, 0),
##            bullet=True,
            type=b2_dynamicBody,
            fixtures=b2FixtureDef(shape=b2PolygonShape(
                box=(5, 7)), density=100.0),
            linearVelocity=(0, -50)
        )

        self.stack2 = self.world.CreateDynamicBody(
            position=(self._x, 0),
##            bullet=True,
            type=b2_dynamicBody,
            fixtures=b2FixtureDef(shape=b2PolygonShape(
                box=(4, 4)), density=100.0),
            linearVelocity=(0, -50)
        )


    def Launch(self):
##        self.stack1
##        self.stack2
##        self.body.transform = [(0.5, 10), 0]
##        self.body.linearVelocity = (0, 0)
##        self.body.angularVelocity = 0

        self.x = 0
        self.stack1.transform = [(0, 18), 0]
        self.stack1.linearVelocity = (0, -50)
        self.stack1.angularVelocity = 0
##
        self.stack2.transform = [(0, 6), 0]
        self.stack2.linearVelocity = (0, -50)
        self.stack2.angularVelocity = 0
##
    def Step(self, settings):
        super(Tower, self).Step(settings)

        if (self.stepCount % 60) == 0:
            self.Launch()

if __name__ == "__main__":
    main(Tower)

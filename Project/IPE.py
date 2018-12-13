from .framework import (Framework, main)
from Box2D import (b2EdgeShape, b2FixtureDef, b2PolygonShape, b2Random, b2_dynamicBody, b2CircleShape,b2World)
import random

########################################### Global Variables ###########################################################################
struct_length = random.randint(1,2)
struct_height = random.randint(3,5)
position_list = random.choice([-20,20]) ##So we can randomly select whether to push from left of table or right

if (position_list == 20): ##push table to the left
    push_force = random.uniform(-15,-45)
else:                     ##push table to the right
    push_force = random.uniform(15,45)

row_height_list = []
box_length_list = []
total_height_displacement_list = []
total_row_displacement_list = []
rect_density_list = []

############################################# Ground Level Simulation #################################################################
class fallingObjects (Framework):
    name = "fallingObjects"

    def __init__(self):
        super(fallingObjects, self).__init__()

        ground = self.world.CreateStaticBody(
            position=(0, 0),
            fixtures = b2FixtureDef(
                shape=(b2EdgeShape(vertices=[(-50, 0), (50, 0)])),
                friction = 10)
        )
        total_height_displacement = 8 #total height of the structure thus far

        self.body = self.world.CreateDynamicBody( ##table leg
            position=(-5, 4),
            fixtures=b2FixtureDef(
                shape=b2PolygonShape(box=(2, 4)), density=200.0),
        )

        self.body = self.world.CreateDynamicBody( ##table leg
            position=(5, 4),
            fixtures=b2FixtureDef(
                shape=b2PolygonShape(box=(2, 4)), density=200.0),
        )

        self.body = self.world.CreateDynamicBody( ##table surface
            position=(0, 8),
            fixtures=b2FixtureDef(
                shape=b2PolygonShape(box=(20, 0.1)), density=200.0),
        )

        self.bullet = self.world.CreateDynamicBody(
            position=(position_list, 8),
            bullet=True,
            fixtures=b2FixtureDef(shape=b2PolygonShape(
                box=(1, 1)), density=50.0),
            linearVelocity=(push_force,0)
        )

        for i in range(struct_height):
            row_height = random.uniform(2, 5) #creates constant height for each row so that towers will have some stability
            row_height_list.append(row_height)

            total_height_displacement += row_height
            total_height_displacement_list.append(total_height_displacement)

            total_row_displacement = random.uniform(-5, -8) #Starting point to move rightward
            total_row_displacement_list.append(total_row_displacement)

            for j in range(struct_length):
                rect_density = random.uniform(1,20) ##Chooses arbitrary weights for all the blocks
                rect_density_list.append(rect_density)

                box_length = random.uniform(1,3)
                box_length_list.append(box_length)

                total_row_displacement += box_length #adjusts for new box length

                self.world.CreateDynamicBody(
                        position=(total_row_displacement,total_height_displacement),
                        fixtures=b2FixtureDef(
                            shape=b2PolygonShape(box=(box_length,row_height)),
                            density=rect_density, friction = 0.5) #friction is constant for all blocks
                )
                total_row_displacement += box_length #adjusts for the next box length
            total_height_displacement += row_height #adjusts for the next box height


####################################### IPE Simulation ############################################################################


class fallingObjectsIPE (Framework):
    name = "fallingObjectsIPE"

    def __init__(self):
        super(fallingObjectsIPE, self).__init__()
        ground = self.world.CreateStaticBody(
            position=(0, 0),
            fixtures = b2FixtureDef(
                shape=(b2EdgeShape(vertices=[(-50, 0), (50, 0)])),
                friction = 10)
        )

        self.body = self.world.CreateDynamicBody( ##table leg
            position=(-5, 4),
            fixtures=b2FixtureDef(
                shape=b2PolygonShape(box=(2, 4)), density=200.0),
        )

        self.body = self.world.CreateDynamicBody( ## table leg
            position=(5, 4),
            fixtures=b2FixtureDef(
                shape=b2PolygonShape(box=(2, 4)), density=200.0),
        )

        self.body = self.world.CreateDynamicBody( ##table surface
            position=(0, 8),
            fixtures=b2FixtureDef(
                shape=b2PolygonShape(box=(20, 0.1)), density=200.0),
        )

        delta = random.uniform(0.8,1.2) ##Push strength uncertainty (External forces)
        self.bullet = self.world.CreateDynamicBody(
            position=(position_list, 8),
            bullet=True,
            fixtures=b2FixtureDef(shape=b2PolygonShape(
                box=(1, 1)), density=50.0),
            linearVelocity=(delta*push_force,0) ## How hard the push is now affected by a probabilistic delta
        )

        total_height_displacement = 8
        j_counter = 0
        for i in range(struct_height):
            alpha1=random.uniform(0.8,1.2) #height alpha (object visibility)
            row_height = row_height_list[i] * alpha1
            total_height_displacement += row_height
            total_row_displacement = total_row_displacement_list[i]

            for j in range(struct_length):
                beta1 = random.uniform(0,1)  #object friction (intrinsic physical qualities of objects)
                beta2 = random.uniform(0.8,1.2) #object density (intrinsic physical qualities of objects)
                alpha2=random.uniform(0.8,1.2) #length alpha (object visibility)

                box_length = box_length_list[j_counter] *alpha2
                rect_density = rect_density_list[j_counter] *beta2

                total_row_displacement += box_length

                self.world.CreateDynamicBody(
                        position=(total_row_displacement,total_height_displacement),
                        fixtures=b2FixtureDef(
                            shape=b2PolygonShape(box=(box_length,row_height)),
                            density=rect_density,friction = beta1)          #friction/density now varies among the blocks
                )
                j_counter+=1
                total_row_displacement += box_length #adjusts for the next box length
            total_height_displacement += row_height #adjusts for the next box height

#################################################### Main functions #############################################################

if __name__ == "__main__":
    main(fallingObjects)

if __name__ == "__main__":
    main(fallingObjectsIPE)

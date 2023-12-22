from panda3d.bullet import BulletWorld, BulletDebugNode
from panda3d.bullet import BulletPlaneShape, BulletBoxShape, BulletSphereShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.core import Vec3, BitMask32, Quat

PHYSICS_TASK = "physics_task"
GROUND_POS = (0, 0, -2)

GRAVITY = -10.0
FORCE = 30.0
TORQUE = 50.0
MASS = .1


class PhysicsWorld(BulletWorld):

    def __init__(self):
        BulletWorld.__init__(self)
        base.ode_world = self
        self.generate_physics_world()

    def generate_physics_world(self):
        self.np = render.attach_new_node("physics_world")
        self.debug = self.np.attach_new_node(
            BulletDebugNode("physics_debug"))
        self.debug.show()
        self.debug.node().show_wireframe(True)
        self.debug.node().show_constraints(True)
        self.debug.node().show_bounding_boxes(False)
        self.debug.node().show_normals(True)

        self.set_gravity(Vec3(0, 0, GRAVITY))
        self.set_debug_node(self.debug.node())

        self.plane = BulletPlaneShape(Vec3(0, 0, 1), 1)
        self.ground = self.np.attach_new_node(
            BulletRigidBodyNode('ground'))
        self.ground.node().add_shape(self.plane)
        self.ground.set_pos(GROUND_POS)
        self.ground.set_collide_mask(BitMask32.all_on())

        self.attach_rigid_body(self.ground.node())

    def box_test(self):
        shape = BulletBoxShape(Vec3(0.5, 0.5, 0.5))
        self.box_np = self.np.attach_new_node(
                                            BulletRigidBodyNode("box"))
        self.box_np.node().set_mass(MASS)
        self.box_np.node().add_shape(shape)
        self.box_np.set_pos(0, 0, 2)
        self.box_np.set_collide_mask(BitMask32.all_on())

        self.attach_rigid_body(self.box_np.node())
        visual_np = loader.load_model('shapes/box.egg')
        visual_np.clear_model_nodes()
        visual_np.reparent_to(self.box_np)

        base.box_np = self.box_np


class BulletTest():

    def __init__(self, actor, joint_hierarchy):
        self.actor = actor
        self.joint_hierarchy = joint_hierarchy

        self.controlled_joints = {}
        self.shapes = []

        if not hasattr(base, "physics_world"):
            base.physics_world = PhysicsWorld()

        self.control_joints()
        taskMgr.add(self.update_physics, PHYSICS_TASK)

    def control_joints(self):
        for modelroot, joints in self.joint_hierarchy.items():
            controlled_joint_list = []
            for joint_name in joints:
                if isinstance(joint_name, int):
                    continue # will do something with this later.
                joint = self.actor.control_joint(None, modelroot, joint_name)
                shape_np = self.add_joint(joint)

                self.shapes.append(shape_np)
                controlled_joint_list.append(joint)

            self.controlled_joints[modelroot] = controlled_joint_list

    def update_physics(self, task):
        dt = globalClock.get_dt()
        self.process_physics(dt)
        base.physics_world.do_physics(dt, 5, 1.0/180.0)

        return task.cont

    def process_physics(self, dt):
        force = Vec3(0, 0, 0)
        torque = Vec3(0, 0, 0)

        force *= FORCE
        torque *= TORQUE

        i = 0
        for shape in self.shapes:
            force = render.get_relative_vector(shape, force)
            torque = render.get_relative_vector(shape, torque)

            shape.node().set_active(True)
            shape.node().apply_central_force(force)
            shape.node().apply_torque(torque)

        i = 0
        for part in self.controlled_joints:
            for joint in self.controlled_joints[part]:
                shape = self.shapes[i]
                #body.write()
                joint.set_pos(shape.get_pos())
                joint.set_quat(shape.get_quat())
                i += 1

    def add_joint(self, joint):
        shape = BulletSphereShape(.05)
        shape_np = joint.attach_new_node(
            BulletRigidBodyNode("box"))
        shape_np.node().set_mass(MASS)
        shape_np.node().add_shape(shape)
        shape_np.set_pos(0, 0, 2)
        shape_np.set_collide_mask(BitMask32.all_on())

        base.ode_world.attach_rigid_body(shape_np.node())
        #visual_np = loader.load_model('shapes/box.egg')
        #visual_np.clear_model_nodes()
        #visual_np.reparent_to(shape_np)

        return shape_np
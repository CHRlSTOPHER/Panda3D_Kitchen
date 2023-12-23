from direct.directtools.DirectSelection import DirectBoundingBox
from panda3d.ode import (OdeWorld, OdeSimpleSpace, OdeQuadTreeSpace,
                         OdePlaneGeom, OdeBoxGeom, OdeSphereGeom,
                         OdeCappedCylinderGeom, OdeBallJoint,
                         OdeJointGroup, OdeBody, OdeMass,
                         )
from panda3d.core import (Quat, BitMask32, Vec4,
                          CollisionNode, CollisionSphere)
from panda3d.core import CharacterJoint

GRAVITY = -9.81
BOX_MASS = (11340, 1, 1, 1)
ORIGIN = (0, 0, 0)
EXTENSION = (511, 511, 0)
DEPTH = 0
COLL_BITS = BitMask32(0x00000001)
CAT_BITS = BitMask32(0x00000002)
RADIUS = .5

BAD_JOINTS = ['joint_nameTag', 'joint_shadow']


class PhysicsWorld(OdeWorld):

    def __init__(self):
        OdeWorld.__init__(self)
        base.ode_world = self
        self.set_gravity(0, 0, GRAVITY)
        self.init_surface_table(1)
        self.set_surface_entry(pos1=0, pos2=0, mu=150.0,
                               bounce=0.0, bounce_vel=9.1,
                               soft_erp=0.9, soft_cfm=.00001,
                               slip=0.0, dampen=0.002)

        base.ode_space = OdeSimpleSpace() # ORIGIN, EXTENSION, DEPTH
        base.ode_space.set_auto_collide_world(self)
        base.ode_contact = OdeJointGroup()
        base.ode_space.set_auto_collide_joint_group(base.ode_contact)

        base.ode_ground = OdePlaneGeom(base.ode_space, Vec4(0, 0, 1, 0))
        base.ode_ground.set_collide_bits(COLL_BITS)
        base.ode_ground.set_category_bits(CAT_BITS)


class Ragdoll():

    def __init__(self, actor):
        self.actor = actor
        self.joints = []
        self.previous_body = None

        if not hasattr(base, "ode_world"):
            PhysicsWorld()

        model_parts = [part for part in actor.get_part_names()]
        for part in model_parts:
            bundle = actor.get_part_bundle(part)
            self.control_joints(actor, bundle, actor, part)

        # taskMgr.doMethodLater(1.0, self.simulation_task, "simulation_task")

    def control_joints(self, actor, part, parentNode, modelroot):
        if isinstance(part, CharacterJoint):
            joint_nodepath = parentNode.attachNewNode(part.getName())
            actor.controlJoint(joint_nodepath, modelroot, part.getName())

            # Preserve joint's original transform.
            joint_nodepath.setMat(part.getDefaultValue())

            visualizer = loader.load_model("shapes/ball.egg")
            visualizer.reparent_to(render)
            visualizer.set_scale(.25)
            # visualizer.hide()
            self.previous_body = self.create_joint_body(
                joint_nodepath, visualizer, parentNode)

            parentNode = joint_nodepath

        for i in range(part.getNumChildren()):
            joint_name = part.get_child(i).get_name()
            if not joint_name in BAD_JOINTS:
                self.previous_body = self.control_joints(
                    actor, part.get_child(i), parentNode, modelroot)

    def create_joint_body(self, joint_nodepath, visualizer, parentNode):
        density = 1
        radius = 1

        body = OdeBody(base.ode_world)
        M = OdeMass()
        M.setSphere(density, radius)
        body.setMass(M)
        body.setPosition(joint_nodepath.getPos(render))
        body.setQuaternion(joint_nodepath.getQuat(render))

        geom = OdeSphereGeom(base.ode_space, radius)
        geom.setCollideBits(BitMask32(0x00000002))
        geom.setCategoryBits(BitMask32(0x00000001))
        geom.setBody(body)

        if self.previous_body:
            ode_joint = OdeBallJoint(base.ode_world)
            ode_joint.attach(body, self.previous_body)
            ode_joint.set_anchor(parentNode.get_pos(render))

        self.joints.append((joint_nodepath, body, visualizer))

        return body

    def simulation_task(self, task):
        base.ode_space.auto_collide()
        base.ode_world.quick_step(base.clock.dt)
        base.ode_contact.empty()

        for nodepath, body, visualizer in self.joints:
            pos = body.get_position()
            quat = Quat(body.get_quaternion())
            nodepath.set_pos_quat(render, pos, quat)
            visualizer.set_pos_quat(render, pos, quat)

        return task.cont
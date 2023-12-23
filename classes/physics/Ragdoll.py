from direct.directtools.DirectSelection import DirectBoundingBox
from panda3d.ode import (OdeWorld, OdeSimpleSpace, OdeQuadTreeSpace,
                         OdePlaneGeom, OdeBoxGeom, OdeSphereGeom,
                         OdeCappedCylinderGeom, OdeBallJoint,
                         OdeJointGroup, OdeBody, OdeMass,
                         )
from panda3d.core import (Quat, BitMask32, Vec4,
                          CollisionNode, CollisionSphere)
import sys, os, random, time
from math import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

GRAVITY = -9.81
BOX_MASS = (11340, 1, 1, 1)
ORIGIN = (0, 0, 0)
EXTENSION = (511, 511, 0)
DEPTH = 0
COLL_BITS = BitMask32(0x00000001)
CAT_BITS = BitMask32(0x00000002)
RADIUS = .5

VISUALIZER_PATH = "shapes/ball.egg"


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

    def __init__(self, actor, joint_hierarchy):
        self.actor = actor
        self.joint_hierarchy = joint_hierarchy
        self.controlled_joints_list = []
        self.controlled_joints_dict = {}
        self.ode_bodyparts = []

        self.delta_time = 0.0
        self.step_size = 1.0 / 90.0

        if not hasattr(base, "ode_world"):
            PhysicsWorld()

        self.load_ragdoll_structure()
        # taskMgr.doMethodLater(1.0, self.simulation_task, "simulation_task")

    def load_ragdoll_structure(self):

        for actor_part, joints in self.joint_hierarchy.items():
            self.control_joints(actor_part, joints)

    def control_joints(self, modelroot, joints):
        joint_names = []
        self.controlled_joints_list = []
        root = joints[0][1:]
        joint_ct = self.actor.expose_joint(None, modelroot, root)
        joint_names.append(root)
        self.controlled_joints_list.append(joint_ct)
        for joint_name in joints:
            print(joint_ct)
            ode_bodypart, joint_ct = self.create_ode_bodypart(
                                                        modelroot,
                                                        joint_names,
                                                        joint_name, joint_ct)

            # Debug
            visualizer = loader.load_model(VISUALIZER_PATH)
            visualizer.reparent_to(joint_ct)
            # print(visualizer.get_pos(render), joint_ex.get_pos())
            # visualizer.set_scale(RADIUS)

            joint_names.append(joint_name)
            self.controlled_joints_list.append(joint_ct)
            self.ode_bodyparts.append(ode_bodypart)

        self.controlled_joints_dict[modelroot] = self.controlled_joints_list

    def create_ode_bodypart(self, modelroot,
                            joint_names, joint_name, joint_ct):
        body = OdeBody(base.ode_world)
        mass = OdeMass()

        density = 5000
        mass.set_sphere(density, RADIUS)
        body.set_mass(mass)
        body.set_position(joint_ct.get_pos(render))
        body.set_quaternion(joint_ct.get_quat(render))

        geom = OdeSphereGeom(base.ode_space, RADIUS)
        geom.set_collide_bits(CAT_BITS)  # reverse entries
        geom.set_category_bits(COLL_BITS)
        geom.set_body(body)

        if int(joint_name[0]) == 0:
            return body, joint_ct

        # We reverse the list since we are going up from the bottom of the
        # tree hierarchy.
        joint_names.reverse()
        self.controlled_joints_list.reverse()
        i = 0
        joint_found = False
        joint_child = int(joint_name[0])
        joint_hierarchy_increase = -1
        # Search for the parent of the child node based on the numerical flag
        # at the start of the joint name
        while not joint_found:
            joint_parent = int(joint_names[i][0])
            if joint_child + joint_hierarchy_increase == joint_parent:
                parent = self.ode_bodyparts[i]
                child = body
                child_node = joint_ct.attach_new_node(joint_name[1:])
                print(joint_ct.get_pos(self.actor))
                joint_ct = self.actor.control_joint(child_node,
                                                    modelroot, joint_name[1:])
                # Link the child joint to the parent joint.
                ball_joint = OdeBallJoint(base.ode_world)
                ball_joint.attach(child, parent)
                ball_joint.set_anchor(
                    self.controlled_joints_list[i].get_pos(render))
                joint_found = True
            i += 1

        # Put the lists back to normal so we correctly append more joints.
        joint_names.reverse()
        self.controlled_joints_list.reverse()
        return body, joint_ct

    def simulation_task(self, task):
        base.ode_space.auto_collide()
        base.ode_world.step(base.clock.dt)

        i = 0
        for part in self.controlled_joints:
            for joint in self.controlled_joints[part]:
                body = self.ode_bodyparts[i]
                joint.set_pos_quat(render, body.get_position(),
                                        Quat(body.get_quaternion()))
                i += 1

        base.ode_contact.empty()
        return task.cont
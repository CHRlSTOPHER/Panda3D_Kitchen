from direct.directbase import DirectStart
from direct.directtools.DirectGeometry import LineNodePath
from panda3d.core import *
from panda3d.ode import *

# Load the smiley and frowney models
smiley = loader.loadModel("smiley.egg")
smiley.reparentTo(render)
smiley.setPos(-5, 0, -5)
frowney = loader.loadModel("frowney.egg")
frowney.reparentTo(render)
frowney.setPos(-12.5, 0, -7.5)

# Setup our physics world
world = OdeWorld()
world.setGravity(0, 0, -9.81)

# Setup the body for the smiley
smileyBody = OdeBody(world)
M = OdeMass()
M.setSphere(5000, 1.0)
smileyBody.setMass(M)
smileyBody.setPosition(smiley.getPos(render))
smileyBody.setQuaternion(smiley.getQuat(render))

# Now, the body for the frowney
frowneyBody = OdeBody(world)
M = OdeMass()
M.setSphere(5000, 1.0)
frowneyBody.setMass(M)
frowneyBody.setPosition(frowney.getPos(render))
frowneyBody.setQuaternion(frowney.getQuat(render))

# Create the joints
smileyJoint = OdeBallJoint(world)
smileyJoint.attach(smileyBody, None) # Attach it to the environment
smileyJoint.setAnchor(0, 0, 0)
frowneyJoint = OdeBallJoint(world)
frowneyJoint.attach(smileyBody, frowneyBody)
frowneyJoint.setAnchor(-5, 0, -5)

# Set the camera position
base.disableMouse()
base.camera.setPos(0, 50, -7.5)
base.camera.lookAt(0, 0, -7.5)

# We are going to be drawing some lines between the anchor points and the joints
lines = LineNodePath(parent=render, thickness=3.0, colorVec=(1, 0, 0, 1))
def drawLines():
    # Draws lines between the smiley and frowney.
    lines.reset()
    lines.drawLines([((frowney.getX(), frowney.getY(), frowney.getZ()),
                      (smiley.getX(), smiley.getY(), smiley.getZ())),
                     ((smiley.getX(), smiley.getY(), smiley.getZ()),
                      (0, 0, 0))])
    lines.create()

# The task for our simulation
def simulationTask(task):
    # Step the simulation and set the new positions
    world.quickStep(globalClock.getDt())
    frowney.setPosQuat(render, frowneyBody.getPosition(), frowneyBody.getQuaternion())
    smiley.setPosQuat(render, smileyBody.getPosition(), smileyBody.getQuaternion())
    drawLines()
    return task.cont

drawLines()
taskMgr.doMethodLater(0.5, simulationTask, "Physics Simulation")

base.run()
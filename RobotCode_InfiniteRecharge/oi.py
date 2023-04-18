from state import state
<<<<<<< HEAD
import wpilib


if state["Controller"] == "PacificRim":
	import PacificRim as Controller_inputs

elif state["Controller"] == "Chasis":
	import Chasis_control as Controller_inputs

elif state["Controller"] == "Abilities":
	import Abilities_control as Controller_inputs




def read_control_inputs(control_type):

	if control_type == "PacificRim":

		read_chasis_inputs(0)
		read_abilities_inputs(1)

	elif control_type == "Chasis" or control_type == "Abilities":

		read_abilities_inputs(0)
		read_chasis_inputs(0)

	else:

		print ("Non-existent control type")
		wpilib.DriverStation.reportWarning(str("Non-existent control type"),True)



def read_chasis_inputs(control_port):

	chasis_controller = wpilib.Joystick(control_port)

	x = chasis_controller.getX()
	state["mov_x"] = x

	y = chasis_controller.getY()
	state["mov_y"] = y

	z = chasis_controller.getRawAxis(4)
	state["mov_z"] = z

def read_abilities_inputs(control_port):

	abilities_controller = wpilib.Joystick(control_port)

	#cannon
	
	eje_t = abilities_controller.getZ()

	left_shoulder_button = abilities_controller.getRawButton(4)

	right_shoulder_button = abilities_controller.getRawButton(5)
	state["cannon_piston_activated"] = right_shoulder_button

	if eje_t > 0:
		print("hola funciono")
		state["cannon_motor_activated"] = 0.7
	else:
		state["cannon_motor_activated"] = 0

	if left_shoulder_button:
		state["sucker_activited"] = 0.7
	else:
		state["sucker_activited"] = 0




	
=======
import wpilib 

def ReadControllerInputs():

	chasis_controller = wpilib.Joystick(0)
	abilities_controller = wpilib.Joystick(1)

	state["x_axis"] = chasis_controller.getX()
	state["y_axis"] = chasis_controller.getY()
	state["z_axis"] = chasis_controller.getRawAxis(4)

>>>>>>> 044c5d9b525d229370c1d4c1ce8e99e8b1b1193f


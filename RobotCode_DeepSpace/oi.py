# Se importa el control requerido automáticamente

from state import state
import wpilib 

if state["Controller"] == "PacificRim":
	import PacificRim as Controller_inputs

elif state["Controller"] == "ControlPiko":
	import ControlPiko as Controller_inputs

elif state["Controller"] == "ControlPelon":
	import ControlPelon as Controller_inputs



def read_control_inputs(control_type):

	if control_type == "PacificRim":

		read_chasis_inputs(0)
		read_abilities_inputs(1)

	elif control_type == "ControlPiko" or control_type == "ControlPelon":

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

	align_button = chasis_controller.getRawButton(Controller_inputs.accomodate)
	state["align_activated"] = align_button

	# button_2 = chasis_controller.getRawButton(Controller_inputs.turbo)
	# state["turbo_activated"] = button_2


def read_abilities_inputs(control_port):

	abilities_controller = wpilib.Joystick(control_port)

	# Codewide button breaker

	button_breaker = abilities_controller.getRawButton(Controller_inputs.button_breaker)
	state["codewide_breaker"] = button_breaker

	# botones del elevador y predeterminados

	POV = wpilib.interfaces.GenericHID(control_port)

	eje_t = abilities_controller.getZ()
	eje_z =abilities_controller.getThrottle()

	button_medio_piston = abilities_controller.getRawButton(Controller_inputs.up_platform_middle_piston)
	button_alto_piston = abilities_controller.getRawButton(Controller_inputs.up_platform_high_piston)


	button_2 = abilities_controller.getRawButton(Controller_inputs.turbo)
	state["turbo_activated"] = button_2

	# Uso de los botones


	# if POV.getPOV() == 180 and state["Controller"] == "PacificRim" or state["Controller"] == "ControlPiko" and eje_t > 0:
	# 	state["lift_motor"] = 0.5

	# elif POV.getPOV() == 0 and state["Controller"] == "PacificRim" or state["Controller"] == "ControlPiko" and eje_z > 0:
	# 	state["lift_motor"] = -1
	# else:
	# 	state["lift_motor"] = 0

	if state["Controller"] == "PacificRim" and eje_t > 0:
		state["lift_motor"] = 0.5

	elif state["Controller"] == "PacificRim" and eje_z > 0:
		state["lift_motor"] = -1
	else:
		state["lift_motor"] = 0

	
	if button_medio_piston:

		state["position"] = "media"
		state["mechanism"] = "piston"

	elif button_alto_piston:

		state["position"] = "high"
		state["mechanism"] = "piston"


	#Inputs de Solenoides, pistones, wheelers y subir o bajar garra (los cuales se quitaron del robot asi que ya solo queda lo del piston)

	# impulsor_on = abilities_controller.getRawButton(Controller_inputs.on_and_off_impulsor)
	# state["impulsor_on"] = impulsor_on

	turn_piston_on = abilities_controller.getRawButton(Controller_inputs.on_and_off_piston)
	turn_piston_off = abilities_controller.getRawButton(Controller_inputs.off_piston)
	# impulsor_on_button = abilities_controller.getRawButton(Controller_inputs.manual_impulsor_on)

	# impulsor_off_button = abilities_controller.getRawButton(Controller_inputs.manual_impulsor_off)


	#Configuracion para el uso de pistones e impulsores
	# if turn_piston_on == True:
	# 	state["timer_button"] += 1

	# 	if state["piston_state_button"] == False and state["timer_button"] > 14.8:
			
	# 		state["piston_activated"] = True
			
	# 		state["piston_state_button"] = True
	# 		state["timer_button"] = 0

	# 	elif state["piston_state_button"] and state["timer_button"] > 14.8:

	# 		state["piston_activated"] = False
						
	# 		state["piston_state_button"] = False
	# 		state["timer_button"] = 0
	if turn_piston_on:

		state["piston_activated"] = True
	if turn_piston_off:

		state["piston_activated"] = False



	# if turn_piston_on or state["timer_piston"] != 0:
	# 	state["timer_piston"] += 1
	# 	if state["timer_piston"] < 35: 
	# 		state["piston_activated"] = True
	# 	elif state["timer_piston"] < 60:
	# 		state["piston_activated"] = False
	# 	else:
	# 		state["timer_piston"] = 0


	# if impulsor_on_button:

	# 	state["impulsor_situation_front"] = 1
	# 	state["impulsor_situation_trasero"] = 1

	# if impulsor_off_button

	# 	state["impulsor_situation_front"] = 2
	# 	state["impulsor_situation_trasero"] = 2













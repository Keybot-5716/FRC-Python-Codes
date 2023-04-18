
import wpilib
from wpilib.drive import MecanumDrive
import time
from networktables import NetworkTables
import threading
import logging

state = {
"x_axis": 0,
"y_axis": 0, 	
"z_axis": 0,
"right_trigger": 0,
"left_trigger": 0,
"timer_auto":0,
"botonA":False,
"hasAValidTarget":False,
}


def ReadControllerInputs():
	chasis_controller = wpilib.Joystick(1)
	state["x_axis"] = chasis_controller.getRawAxis(4)
	state["y_axis"] = chasis_controller.getRawAxis(1)
	state["z_axis"] = chasis_controller.getRawAxis(0)
	state["botonA"] = chasis_controller.getRawButton(1)



class MyRobot(wpilib.TimedRobot):


	def robotInit(self):

		self.STEER_K = 0.03
		self.DRIVE_K = 0.26
		self.MAX_DRIVE = 0.7

		# NetworkTables.startClientTeam(5716)
		logging.basicConfig(level=logging.DEBUG)
		NetworkTables.initialize()
		#self.pc = NetworkTables.getTable("SmartDashboard")
		self.limelight = NetworkTables.getTable('limelight')
		self.timer = wpilib.Timer()
		self.front_left_motor = wpilib.Talon(3)
		self.rear_left_motor = wpilib.Talon(1)
		self.front_right_motor = wpilib.Talon(4)
		self.rear_right_motor = wpilib.Talon(2)

		self.front_left_motor.setInverted(True)

		self.drive = MecanumDrive(
			self.front_left_motor,
			self.rear_left_motor,
			self.front_right_motor,
			self.rear_right_motor)


		
	def autonomousInit(self):
		#self.timer.reset()
		#self.timer.start()
		pass

	def autonomousPeriodic(self):
		#position = self.pc.getString("Posicion", "Not jalando")
		#print(position)
		#wpilib.DriverStation.reportWarning(position,True)
		pass


#-----------------------------------------------------------------------------------------------------------

	def teleopPeriodic(self):
		
		ReadControllerInputs()

		x = state["x_axis"]
		y = state["y_axis"]
		z = state["z_axis"]
		botonA = state["botonA"]

		powerX = 0 if x < 0.20 and x > -0.20 else x
		powerY = 0 if y < 0.20 and y > -0.20 else y
		powerZ = 0 if z < 0.20 and z > -0.20 else z

		# Lee los valores generados por la limelight
		tv = self.limelight.getNumber("tv",0)
		tx = self.limelight.getNumber("tx",0)
		ty = self.limelight.getNumber("ty",0)
		ta = self.limelight.getNumber("ta",0)

		# Si se presiono el botón A y se detecto un objetivo, activa el modo seguimiento
		if (botonA):
			if (tv < 1.0):
				state["hasAValidTarget"] = False
			else:
				state["hasAValidTarget"] = True
				powerX = tx * self.STEER_K
				self.drive.driveCartesian(powerX * -0.9,powerY * 0.9, powerZ * -0.9, 0)
		else:
			self.drive.driveCartesian(powerX * -0.9,powerY * 0.9, powerZ * -0.9, 0)
#----------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
	wpilib.run(MyRobot)

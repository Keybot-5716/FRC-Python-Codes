import ctre
import wpilib
from wpilib.drive import DifferentialDrive
import time
from networktables import NetworkTables
import threading
import logging
from robotpy_ext.control.toggle import Toggle

state = {
"x_axis": 0,
"y_axis": 0, 	
"right_trigger": 0,
"left_trigger": 0,
"timer_auto":0,
"botonA":False,
"botonB":False,
"botonX":False,
"hasAValidTarget":False,
}


def ReadControllerInputs():
	chasis_controller = wpilib.Joystick(0)
	state["x_axis"] = chasis_controller.getRawAxis(2)
	state["y_axis"] = chasis_controller.getRawAxis(1)
	state["botonA"] = chasis_controller.getRawButton(1)
	state["botonB"] = chasis_controller.getRawButton(2)
	state["botonX"] = chasis_controller.getRawButton(3)
	state["botonY"] = chasis_controller.getRawButton(4)




class MyRobot(wpilib.TimedRobot):


	def robotInit(self):

		self.STEER_K = 0.03
		self.DRIVE_K = 0.26
		self.MAX_DRIVE = 0.7

		NetworkTables.startClientTeam(5716)
		logging.basicConfig(level=logging.DEBUG)
		NetworkTables.initialize()
		self.pc = NetworkTables.getTable("SmartDashboard")
		self.limelight = NetworkTables.getTable('limelight')
		self.timer = wpilib.Timer()

		self.right1 = wpilib.Talon(3)
		self.right1.setInverted(True)
		self.right2 = wpilib.Talon(4)
		self.right2.setInverted(True)
		self.right = wpilib.SpeedControllerGroup(self.right1,self.right2)

		self.left1 = wpilib.Talon(1)
		self.left2 = wpilib.Talon(2)
		self.left2.setInverted(True)
		self.left = wpilib.SpeedControllerGroup(self.left1,self.left2)

		#self.arduino = wpilib.SerialPort(57600)
	


		#Prueba recoge pelotas
		self.colector = wpilib.Talon(5)

		# Prueba FALCON
		self.falcon500= ctre.WPI_TalonSRX(5)
	
		self.drive = DifferentialDrive(self.left,self.right)
	


		


		
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
		botonA = state["botonA"]
		botonB = state["botonB"]
		botonX = state["botonX"]
		botonY = state["botonY"]

		powerX = 0 if x < 0.20 and x > -0.20 else x
		powerY = 0 if y < 0.20 and y > -0.20 else y

		# Lee los valores generados por la limelight
		#tv = self.limelight.getNumber("tv",0)
		#tx = self.limelight.getNumber("tx",0)
		#ty = self.limelight.getNumber("ty",0)
		#ta = self.limelight.getNumber("ta",0)

		# Prueba recoge pelotas A - Tragar B - Sacar	
		if (botonA):
			self.colector.set(-1) 
		elif (botonB):
			self.colector.set(1) 
			if (botonY):
				self.falcon500.set(1)
		elif (botonY):
			self.falcon500.set(1)
		else:		
			self.colector.set(0.0) 
			self.falcon500.set(0.0)
		#Codigo Limelight copiado de Dif&Allign
		tv = self.limelight.getNumber("tv",0)
		tx = self.limelight.getNumber("tx",0)
		ty = self.limelight.getNumber("ty",0)
		ta = self.limelight.getNumber("ta",0)
		tlong = self.limelight.getNumber("tlong",0)
	
		if (botonX):
			if (tv < 1.0):
				state["hasAValidTarget"] = False
			else:
				state["hasAValidTarget"] = True
				powerX = tx * 0.03
				self.drive.arcadeDrive(powerY * -0.9,powerX * -0.25)



		#bA = state["botonA"]
		#bB = state["botonB"]
		#if (bA): 
	#		byteBuff = [1]
	#	elif (bB):
	#		byteBuff = [2]
	#	self.arduino.write(byteBuff)	

		self.drive.arcadeDrive(powerY * 0.9,powerX * -0.9)
#----------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
	wpilib.run(MyRobot)

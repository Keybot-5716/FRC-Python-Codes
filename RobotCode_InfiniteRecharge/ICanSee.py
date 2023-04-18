import cv2
import numpy
import time

				

class VideoRecorder():
	def __init__(self):
		super(VideoRecorder, self).__init__()
		
		
		self.video = cv2.VideoCapture(0)

		self.color_data = "color_data"

		self.hexagon_status = ""

		self.width = self.video.get(3)
		self.height = self.video.get(4)

		# Divides videos width and height into 3, to create the quadrants

		self.q_width = self.width/3
		self.q_height = self.height/3

		#green_color_range
		self.green_lower = numpy.array([38,70,15], numpy.uint8)
		self.green_upper = numpy.array([73,255,255], numpy.uint8)

	def VariablesInit(self):

		self.check,self.frame = self.video.read()

		# self.Lrectangle = cv2.rectangle(self.frame, (0,720), (426,0), (0,255,0), 1)
		# self.Mrectangle = cv2.rectangle(self.frame, (426,720), (852,0), (0,255,0), 1)
		# self.Rrectangle = cv2.rectangle(self.frame, (852,720), (1280,0), (0,255,0), 1)

		# self.Urectangle = cv2.rectangle(self.frame, (0,240), (1280,0), (0,255,0), 1)
		# self.MMrectangle = cv2.rectangle(self.frame, (0,480), (1280,241), (0,255,0), 1)
		# self.Drectangle = cv2.rectangle(self.frame, (0,720), (1280,480), (0,255,0), 1)

		# print (check)
		# print (frame)
		# blur = cv2.GaussianBlur(self.frame ,(5,5), 0)
		# self.image = cv2.Canny(blur,50,150)

		self.HSV = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)

		self.green = cv2.inRange(self.HSV, self.green_lower, self.green_upper)


	def SmartColorRecognizer(self,color,rectangle_color,min_area,max_area):

		if color == "red":
			self.color_data = self.red
		elif color == "blue":
			self.color_data = self.blue
		elif color == "yellow":
			self.color_data = self.yellow
		elif color == "green":
			self.color_data = self.green
		elif color == "orange":
			self.color_data = self.orange
		elif color == "black":
			self.color_data = self.black
		elif color == "white":
			self.color_data = self.white

		(contours,hierarchy) = cv2.findContours(self.color_data, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		for pic, countour in enumerate(contours):
			area = cv2.contourArea(countour)
			if area > min_area:
				x,y,w,h = cv2.boundingRect(countour)
				box = cv2.rectangle(self.frame, (x,y), (x+w, y+h),rectangle_color ,2)
				cv2.putText(box, color, (x,y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, rectangle_color)
				if color == "green":
					approx = cv2.approxPolyDP(countour,0.01*cv2.arcLength(countour,True),True)
					if len(approx) == 6:
						cv2.putText(self.frame, "Distance: " + str(area), (30,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
						ObjectWidth = w + x 
						ObjectHeight = y + h
					
					# ObjectHeight = 
					# height/3 = 240 
					# width/3 = 426 
					
					# determines the position of the given shape
					
						if ObjectWidth < self.q_width and ObjectHeight > (self.q_height)*2:
							self.hexagon_status = "Bottom Left"
						elif ObjectWidth < self.q_width and ObjectHeight < (self.q_height)*2 and ObjectHeight > self.q_height:
							self.hexagon_status = "Middle Left"
						elif ObjectWidth < self.q_width and ObjectHeight < self.q_height:
							self.hexagon_status = "Top Left"
						elif ObjectWidth > (self.q_width)*2 and ObjectHeight > (self.q_height)*2:
							self.hexagon_status = "Bottom Right"
						elif ObjectWidth > (self.q_width)*2 and ObjectHeight < (self.q_height)*2 and ObjectHeight > self.q_height:
							self.hexagon_status = "Middle Right"
						elif ObjectWidth > (self.q_width)*2 and ObjectHeight < self.q_height:
							self.hexagon_status = "Top Right"
						elif ObjectWidth < (self.q_width)*2 and ObjectWidth > self.q_width and ObjectHeight < self.q_height:
							self.hexagon_status = "Top Middle"
						elif ObjectWidth < (self.q_width)*2 and ObjectWidth > self.q_width and ObjectHeight > (self.q_height)*2:
							self.hexagon_status = "Bottom Middle"
						else:
							self.hexagon_status = "Centered"
				else:
					pass


	def StartRecording(self):

		cv2.imshow("Color Tracking",self.frame)

	def StopRecording(self):

		self.video.release()
		cv2.destroyAllWindows()


Video = VideoRecorder()

while True:
	
	Video.VariablesInit()
	Video.SmartColorRecognizer("green",(0,255,0),600, 3000)
	Video.StartRecording()

	key = cv2.waitKey(1)
	if key == ord("q"):
		break

Video.StopRecording()


	
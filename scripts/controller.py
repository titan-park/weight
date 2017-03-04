#!/usr/bin/python

import rospy
import time
from std_msgs.msg import String
from weight.msg import Sensor
import math

pub = rospy.Publisher("power", Sensor, queue_size = 2)

th = 30
pre_out = 0
output = 0
pre_err = 0
error = 0

def callback(data):
	global pub
	global pre_out
	global output
	global pre_err
	global error

	target = 0

	tmp = data.data

	tmp_sen = tmp.strip().split(',')
	
	kp = 1.5
	kd = 0.1

	if len(tmp_sen) == 2:
		sen1 = int(tmp_sen[0])
		sen2 = int(tmp_sen[1])

		#print "Sensor Data:" , sen1 , ',' , sen2
		gain = 10
#		if sen2 > 512 :
#			target = 512 - (sen2 - 512)

#		else :
#			target = sen2
#		output = sen2 - sen1
#		target *= 2

		target = int(1000.0*math.sin(sen2*math.pi/1024.0))
		pre_err = error
		error = target - sen1

		if abs(error) < th :
			error = 0
				
		output = int(kp*error + kd*(error - pre_err))
		if output > 1000 :
			output = 1000
		elif output < -1000 :
			output = -1000

		if not output == pre_out :
			print "Load cell: ", sen1, ", ", "Target: ", target ,", ",  "Output: ", output
			pub.publish(output)
			pre_out = output

		print "Load cell: ", sen1, ", ", "Target: ", target, ", ","Ooutput: ", output 

def controller():
	rospy.init_node('controller', anonymous=True)
	rospy.loginfo("Controller Start!")
	rospy.Subscriber("Data", String, callback)
	
	rate = rospy.Rate(10)

	rospy.spin()


if __name__ == '__main__':
	try:
		controller()
	except rospy.ROSInterruptException:
		pass

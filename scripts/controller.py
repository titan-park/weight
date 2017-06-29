#!/usr/bin/python

import rospy
import time
from std_msgs.msg import String
from weight.msg import Sensor
import math
import numpy

pub = rospy.Publisher("power", Sensor, queue_size = 2)

th = 10
pre_out = 0
output = 0
pre_err = 0
error = 0
count = 0
count2 = 0
sen1 = [0,0,0,0,0]
sen2 = [0,0,0,0,0]
out_sen1 = 0
out_sen2 = 0
pre_out_sen2 = 0
diff = 1
pre_diff = 0
tmp_sen2 = [0,0,0,0,0,0,0,0,0,0]


def callback2(data):
	global diff
	tmp = data.data
	
	if tmp == 'r':
		diff = 0
	elif tmp == 'd':
		diff = 1

def callback(data):
	global pub
	global pre_out
	global output
	global pre_err
	global error
	global count
	global sen1
	global sen2
	global out_sen1
	global out_sen2
	global pre_out_sen2
	global count2
	global diff
	global pre_diff

	target = 0

	sample = 5

	tmp = data.data

	tmp_sen = tmp.strip().split(',')
	
	kp = 2.0
	kd = 1.5
	th_min = 30

	if len(tmp_sen) == 2:
		
		sen1[count] = int(tmp_sen[0])
		sen2[count] = int(tmp_sen[1])

		count += 1

		if count == sample:
			count = 0

			out_sen1 = numpy.mean(sen1)-20
			std_sen2 = numpy.std(sen2)
			if std_sen2 < 5 :
				out_sen2 = numpy.mean(sen2) - 50

				if out_sen2 < 0 :
					out_sen2 = 0
			else :
				out_sen2 = pre_out_sen2
			
#			if out_sen2 < 350 and diff == 0:
#				amp = [600, 100]
#			else :
			amp = [11500, 1000]

			d = 0.073
			l = 0.075/2
			l_slide = out_sen2/950*0.075

			if out_sen2 > 950:
				l_slide = 0.075

			tmp_cal = (l_slide+d-l)*(l_slide+d-l)

			theta = math.acos((tmp_cal - d*d - l*l)/(-2*d*l))

			target = int(amp[diff]*l*d*math.sin(theta)/numpy.sqrt(d*d + l*l - 2*d*l*math.cos(theta)))
#			target = int(amp[diff]*math.sin(theta))
			pre_err = error
			error = target - out_sen1

			if abs(error) < th :
				error = 0
				
			output = int(kp*error + kd*(error - pre_err))

			if out_sen1 < 1000 :
				if output > 1000 :
					output = 1000
				elif output < -1000 :
					output = -1000

			else :
				output = -200

			if not output == pre_out :
#				output = int(2*output)
				if abs(output) < th_min :
					if output < 0:
						output = -th_min
					else :
						output = th_min

				pub.publish(output)
				pre_out = output
				
			print "Load cell: ", out_sen1, ", ", "Position:  ", out_sen2, ", ","dir: ", diff, ", ",  "Target: ", target, ", ","Ooutput: ", output 

			pre_out_sen2 = out_sen2
def controller():
	rospy.init_node('controller', anonymous=True)
	rospy.loginfo("Controller Start!")
	rospy.Subscriber("Data", String, callback)
	rospy.Subscriber("chatter", String, callback2)

	rate = rospy.Rate(10)

	rospy.spin()


if __name__ == '__main__':
	try:
		controller()
	except rospy.ROSInterruptException:
		pass

#!/usr/bin/python

import rospy
import serial
import logging
import time
from weight.msg import Sensor
from std_msgs.msg import String

ser = serial.Serial(port = '/dev/ttyACM0', baudrate=115200)

def rosToSerial():
#	pub = rospy.Publisher("sensor1", Sensor, queue_size=10)
#	pub2 = rospy.Publisher("sensor2", Sensor, queue_size=10)
	pub3 = rospy.Publisher("Data", String, queue_size=10)

	rospy.init_node('rosToSerial', anonymous=True)

	rate = rospy.Rate(10)

	rospy.loginfo("Data Receiving Start")

	loadcell = open("test.txt", "w")

	while not rospy.is_shutdown():
		tmp = ser.readline()
		t = time.time()
		t_tmp = str(t)
		loadcell.write(t_tmp + "," + tmp)

		print tmp

#		pub3.publish(tmp)
#		print "Raw Data: ", tmp
#		tmp_sen = tmp.strip().split(',')
#		print tmp_sen[0]
#		if len(tmp_sen) == 2 :
#			sen1 = int(tmp_sen[0])
#			sen2 = int(tmp_sen[1])

		#	rospy.loginfo(sen1)
		#	rospy.loginfo(sen2)
		#	pub.publish(sen1)
		#	pub.publish(sen2)

if __name__ == '__main__':
	try:
		rosToSerial()
	except rospy.ROSInterruptException:
		pass

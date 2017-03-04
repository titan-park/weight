#!/usr/bin/python

import rospy
import serial
from weight.msg import Sensor

ser = serial.Serial(port = '/dev/ttyUSB0', baudrate=57200)

START = 0xff
ID = 0x01
WRITE = 0x03
CW_LIMIT = 0x06
CCW_LIMIT = 0x08
LIMIT_DATA = 0x00
LENGTH = 0x05
SPEED = 0x20
checkSum = 0x00


def callback(data):
	tmp = data.x
	direction = 0x04 #CW
	if tmp < 0 :
		direction = 0x00
	else :
		direction = 0x04

	tmp = abs(tmp)

	if tmp < 255 :
		val_L = tmp
	
		val_H = direction

	else :
		val_L = tmp%256
		val_H = direction | int(tmp/256)

	tmp_sum = ID + LENGTH+WRITE+SPEED+val_L+val_H

	tmp_sum %= 256

	checkSum = ~tmp_sum

	if checkSum < 0:
		checkSum += 256

	pack = [START, START, ID, LENGTH, WRITE, SPEED, val_L, val_H, checkSum]	

#	print "Package: ", pack

	ser.write(bytearray(pack))

def dynamixel():

	rospy.init_node('dynamixel', anonymous=True)

	rate = rospy.Rate(5)

	rospy.loginfo("Motor Control")
	rospy.Subscriber("power", Sensor, callback)

	rospy.spin()

if __name__ == '__main__':
	try:
		dynamixel()
	except rospy.ROSInterruptException:
		pass	

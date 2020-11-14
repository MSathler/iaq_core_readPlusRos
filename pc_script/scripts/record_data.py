#!/usr/bin/env python

import rospy
import std_msgs.msg
from std_msgs.msg import Float32MultiArray
import time


def callback(data):
	now = rospy.get_rostime()
	arquivo.write(str(now.secs) + "\n")
	arquivo.write(str(data.data) + "\n")
#	arquivo.close()

def init_():
	rospy.init_node('co2subscriber')
	pub = rospy.Subscriber("Modulo/CO2", std_msgs.msg.Float32MultiArray, callback)
	rate = rospy.spin() #Rate(1)

if __name__ == '__main__':
        arquivo = open('/home/espeleo/catkin_ws/src/espeleo/espeleo_embedded/espeleo_gas_sensor/leituras/leitura.txt', 'a')
	arquivo.write("----------------------------------------------------- \n")
	init_()


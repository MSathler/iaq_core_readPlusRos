#!/usr/bin/env python


import rospy
import std_msgs.msg
from std_msgs.msg import Float32MultiArray
from smbus2 import SMBus, i2c_msg
import time

bus = SMBus(1)
ADDRESS = 0x5a
M = []
co2 = 0
info = -1
array_dados = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

def co2_plus_status(array_dados):
        co2 = array_dados[0] << 8
        co2 = co2 | array_dados[1]
        return co2

def informacao(array_dados):
        if (array_dados[2] == 0x00):
                info = 0
#                rospy.loginfo('Leituras OK')
        elif (array_dados[2] == 0x10):
                info = 1
#                rospy.loginfo('Modulo em Aquecimento, o aquecimento demora por$
        elif (array_dados[2] == 0x01):
                info = 2
#                rospy.loginfo('Sensor Ocupado/BUSY')
        elif (array_dados[2] == 0x80):
                info = 3
#                rospy.loginfo('Se esta mensagem aparecer sequencialmente, troq$
        return info

def resistencia(array_dados):
        resist_1 = array_dados[4] << 16
        resist_2 = resist_1 | array_dados[5] << 8
        resist = resist_2 | array_dados[6]
        return resist

def Tvoc(array_dados):
        Tvoc_eq = array_dados[7] << 8
        Tvoc_eq = Tvoc_eq | array_dados[8]
        return Tvoc_eq

def init_():
        pub = rospy.Publisher('Modulo/CO2', std_msgs.msg.Float32MultiArray, queue_size= 10)
        rospy.init_node('CO2')
        rate = rospy.Rate(1)
#       rospy.loginfo('Modulo ligado mensagem no topico /Modulo/CO2 tem a estru$
#       rospy.loginfo('[Leitura CO2(ppm),Qualidade dos dados,Resistencia intern$
#       rospy.loginfo('Qualidade e definida em 0 = OK ; 1 = Aquecimento ; 2 = B$
        while not rospy.is_shutdown():
                L_co2 = std_msgs.msg.Float32MultiArray()
                read = i2c_msg.read(ADDRESS,9)
                h = bus.i2c_rdwr(read)
                array_dados = list(read)
                L_co2.data = [co2_plus_status(array_dados),informacao(array_dad$
                pub.publish(L_co2)
                rate.sleep()

if __name__ == '__main__':
        try:
                init_()
        except rospy.ROSInterruptException:
                pass





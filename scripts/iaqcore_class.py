import rospy
import std_msgs.msg
from std_msgs.msg import Float32MultiArray
from smbus2 import SMBus, i2c_msg
import time


class iaq_sensor():
    def __init__(self,bus = 1, address = 0x5a):
        self.bus = SMBus(bus)
        self.ADDRESS = address
        self.M = []
        self.co2 = 0
        self.info = -1
        self.data_array = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.rate = rospy.Rate(1)

        rospy.init_node('CO2')
        self.pub = rospy.Publisher('Module/CO2', std_msgs.msg.Float32MultiArray, queue_size= 10)
        self.read_co2 = std_msgs.msg.Float32MultiArray()

        self.read_data()

    def co2_plus_status(self, data_array):
        self.co2 = data_array[0] << 8
        self.co2 = self.co2 | data_array[1]
        return self.co2

    def information(self, data_array):
        if (self.data_array[2] == 0x00):
                self.info = 0
#                rospy.loginfo('Leituras OK')
        elif (self.data_array[2] == 0x10):
                self.info = 1
#                rospy.loginfo('Modulo em Aquecimento, o aquecimento demora por$
        elif (self.data_array[2] == 0x01):
                self.info = 2
#                rospy.loginfo('Sensor Ocupado/BUSY')
        elif (self.data_array[2] == 0x80):
                self.info = 3
#                rospy.loginfo('Se esta mensagem aparecer sequencialmente, troq$
        return self.info

    def resistance(self, data_array):
        self.resist_1 = self.data_array[4] << 16
        self.resist_2 = self.resist_1 | self.data_array[5] << 8
        self.resist = self.resist_2 | self.data_array[6]
        return self.resist

    def Tvoc(self, data_array):
        self.Tvoc_eq = self.data_array[7] << 8
        self.Tvoc_eq = self.Tvoc_eq | self.data_array[8]
        return self.Tvoc_eq


    def read_data(self):
        
        
#       rospy.loginfo('Modulo ligado mensagem no topico /Modulo/CO2 tem a estru$
#       rospy.loginfo('[Leitura CO2(ppm),Qualidade dos dados,Resistencia intern$
#       rospy.loginfo('Qualidade e definida em 0 = OK ; 1 = Aquecimento ; 2 = B$
        while not rospy.is_shutdown():
                #self.Read_co2 = std_msgs.msg.Float32MultiArray()
            self.read = i2c_msg.read(self.ADDRESS,9)
            self.h = self.bus.i2c_rdwr(self.read)
            self.data_array = list(self.read)
            self.read_co2.data = [self.co2_plus_status(self.data_array),
                                self.information(self.data_array),
                                self.resistance(self.data_array),
                                self.Tvoc(self.data_array)]
            self.pub.publish(self.read_co2)
            self.rate.sleep()

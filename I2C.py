import wiringpi
import smbus
import time


Illu_Scale = 0
Temp_Scale = 15
Rain_Scale = 5
# BH1750 ADDR

__DEV_ADDR=0x23


__CMD_PWR_OFF=0x00
__CMD_PWR_ON=0x01
__CMD_RESET=0x07
__CMD_CHRES=0x10
__CMD_CHRES2=0x11
__CMD_CLHRES=0x13
__CMD_THRES=0x20
__CMD_THRES2=0x21
__CMD_TLRES=0x23
__CMD_SEN100H=0x42
__CMD_SEN100L=0X65
__CMD_SEN50H=0x44
__CMD_SEN50L=0x6A
__CMD_SEN200H=0x41
__CMD_SEN200L=0x73




bus=smbus.SMBus(1)
bus.write_byte(__DEV_ADDR,__CMD_PWR_ON)
bus.write_byte(__DEV_ADDR,__CMD_RESET)
bus.write_byte(__DEV_ADDR,__CMD_SEN100H)
bus.write_byte(__DEV_ADDR,__CMD_SEN100L)
bus.write_byte(__DEV_ADDR,__CMD_PWR_OFF)

class Test:
    def __init__(self, PRain, PSnow, PSun):
        self.PRain = PRain
        self.PSnow = PSnow
        self.PSun  = PSun
    def P_generate(self, Mea_Temp, Mea_Humd, Mea_Illu, Mea_Rain):
        if Mea_Rain>Rain_Scale :
            if Mea_Temp>15 :
                tempo_PSun  = 10+(Mea_Illu-Illu_Scale)
                tempo_PRain = 90-(Mea_Illu-Illu_Scale)
                tempo_PSnow = 0
            elif Mea_Temp<=15 :
                    if Mea_Humd > 80:
                        tempo_PRain = 80-(Temp_Scale-Mea_Temp)
                        tempo_PSun  = 10
                        tempo_PSnow = 10+(Temp_Scale-Mea_Temp)
                    else:
                        tempo_PSnow = 40+(Temp_Scale-Mea_Temp)
                        tempo_PRain = 40-(Temp_Scale-Mea_Temp)
                        tempo_PSun = 20
        else:
            if Mea_Temp>15
                tempo_PSun  = 70 - (Illu_Scale-Mea_Illu)
                tempo_PRain = 25 + (Illu_Scale-Mea_Illu)
                tempo_PSnow = 5
            else:
                tempo_PSnow = 30 + (Illu_Scale-Mea_Illu)
                tempo_PSun  = 50 + (Mea_Illu-Illu_Scale)
                tempo_PRain = 20
        self.PRain = tempo_PRain
        self.PSnow = tempo_PSnow
        self.PSun = tempo_PSun
    def function_test(self, psun, prain, psnow):
        self.PSun = psun
        self.PSnow= psnow
        self.PRain= prain

def getIlluminance():
    bus.write_byte(__DEV_ADDR,__CMD_PWR_ON)
    bus.write_byte(__DEV_ADDR,__CMD_THRES2)
    time.sleep(0.2)
    res=bus.read_word_data(__DEV_ADDR,0)
    res=((res>>8)&0xff)|(res<<8)&0xff00
    res=round(res/(2*1.2),2)
    result="illu:"+str(res)+"lx"
    return result


def get_Temp():
    fd = wiringpi.wiringPiI2CSetup(0x40)
    temp_org = wiringpi.wiringPiI2CReadReg8(fd, 0x03)
    temp = (temp_org << 8) | temp_org
    T = -46.85 + 175.72 / 65536 * temp
    return T

def get_Humid():
    fd = wiringpi.wiringPiI2CSetup(0x40)
    humd_org = wiringpi.wiringPiI2CReadReg8(fd, 0x05)
    humd = (humd_org << 8) | humd_org
    RH = -6.0 + 125.0 / 65536 * humd
    return RH

Illu=getIlluminance()


print("Current Temperature=", T)
print("Relative Humidity=", RH)
print("illu=", Illu)
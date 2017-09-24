import smbus  
import time  

# 打开 /dev/i2c-1  
bus = smbus.SMBus(1)  

def SHT20_Measure():







for i in range(0,4):
  bus.write_byte( 0x20 , (1<<i) )
  time.sleep(0.1)  # delay 100ms
while True:
  pass
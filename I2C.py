import wiringpi

fd = wiringpi.wiringPiI2CSetup(0x40)
temp_org = wiringpi.wiringPiI2CReadReg8(fd, 0x03)
humd_org = wiringpi.wiringPiI2CReadReg8(fd, 0x05)

temp = (temp_org << 8) | temp_org
humd = (humd_org << 8) | humd_org
T = -46.85 + 175.72 / 65536 * temp
RH = -6.0 + 125.0 / 65536 * humd
print("Current Temperature=", T)
print("Relative Humidity=", RH)

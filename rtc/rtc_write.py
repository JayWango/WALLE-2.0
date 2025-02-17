import smbus2
import time
from datetime import datetime

# DS3231 I2C address
DS3231_I2C_ADDR = 0x68

# Register addresses
REG_SECONDS = 0x00
REG_MINUTES = 0x01
REG_HOURS = 0x02
REG_DAY = 0x03
REG_DATE = 0x04
REG_MONTH = 0x05
REG_YEAR = 0x06

def dec_to_bcd(dec):
    return (dec // 10) * 16 + (dec % 10)

def set_time(bus, dt):
    bus.write_byte_data(DS3231_I2C_ADDR, REG_SECONDS, dec_to_bcd(dt.second))
    bus.write_byte_data(DS3231_I2C_ADDR, REG_MINUTES, dec_to_bcd(dt.minute))
    bus.write_byte_data(DS3231_I2C_ADDR, REG_HOURS, dec_to_bcd(dt.hour))
    bus.write_byte_data(DS3231_I2C_ADDR, REG_DAY, dec_to_bcd(dt.isoweekday()))
    bus.write_byte_data(DS3231_I2C_ADDR, REG_DATE, dec_to_bcd(dt.day))
    bus.write_byte_data(DS3231_I2C_ADDR, REG_MONTH, dec_to_bcd(dt.month))
    bus.write_byte_data(DS3231_I2C_ADDR, REG_YEAR, dec_to_bcd(dt.year - 2000))

# Initialize I2C (SMBus)
bus = smbus2.SMBus(1)

# Set time on DS3231
current_time = datetime.now()
set_time(bus, current_time)
print("Time set successfully: ", current_time)

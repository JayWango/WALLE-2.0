import smbus2
import time

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

def bcd_to_dec(bcd):
    return (bcd // 16) * 10 + (bcd % 16)

def read_time(bus):
    seconds = bcd_to_dec(bus.read_byte_data(DS3231_I2C_ADDR, REG_SECONDS))
    minutes = bcd_to_dec(bus.read_byte_data(DS3231_I2C_ADDR, REG_MINUTES))
    hours = bcd_to_dec(bus.read_byte_data(DS3231_I2C_ADDR, REG_HOURS))
    day = bcd_to_dec(bus.read_byte_data(DS3231_I2C_ADDR, REG_DAY))
    date = bcd_to_dec(bus.read_byte_data(DS3231_I2C_ADDR, REG_DATE))
    month = bcd_to_dec(bus.read_byte_data(DS3231_I2C_ADDR, REG_MONTH))
    year = bcd_to_dec(bus.read_byte_data(DS3231_I2C_ADDR, REG_YEAR)) + 2000
    
    return f"{year}-{month:02}-{date:02} {hours:02}:{minutes:02}:{seconds:02}"

# Initialize I2C (SMBus)
bus = smbus2.SMBus(1)

# Read time from DS3231
current_time = read_time(bus)
print("Current time:", current_time)

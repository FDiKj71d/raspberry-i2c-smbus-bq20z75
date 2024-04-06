import smbus
import time
import datetime

new_capacity = 4400
unseal_key_1 = 0x0414
unseal_key_2 = 0x3672
full_access_key_1 = 0xFFFF
full_access_key_2 = 0xFFFF
pf_clear_key_1 = 0x2673
pf_clear_key_2 = 0x1712

# Define the I2C address of the device
DEVICE_ADDRESS = 0x0B
addr = DEVICE_ADDRESS

# Define the I2C bus number
BUS_NUMBER = 1

# Define the clock frequency for I2C communication
CLOCK_FREQUENCY = 50000

# Initialize the I2C bus
bus = smbus.SMBus(BUS_NUMBER)
#bus.write_byte_data(DEVICE_ADDRESS, 0x00, 0x41)  # Reset the device

# Wait for the device to reset
time.sleep(1)

# Function to write SMB word
def write_smb_word(comm, data):

    bus.write_word_data(addr, comm, data)

# Function to read SMB subclass
def read_smb_subclass(id, page):
    write_smb_word(0x77, id)
    time.sleep(0.1)
    data = read_block_smb(page)
    return data


def read_123():
    # Read the device type
    device_type = bus.read_word_data(DEVICE_ADDRESS, 0x0001)
    print(f"Device Type: {hex(device_type)}")

    # Read the firmware version
    firmware_version = bus.read_word_data(DEVICE_ADDRESS, 0x0002)
    print(f"Firmware Version: {hex(firmware_version)}")

    # Read the hardware version
    hardware_version = bus.read_word_data(DEVICE_ADDRESS, 0x0003)
    print(f"Hardware Version: {hex(hardware_version)}")

# Read pack info
def read_pack_info():
    # Read the design capacity
    design_capacity = bus.read_word_data(DEVICE_ADDRESS, 0x0018)
    print(f"Design Capacity: {design_capacity} mAh")

    # Read the full charge capacity
    full_charge_capacity = bus.read_word_data(DEVICE_ADDRESS, 0x0010)
    print(f"Full Charge Capacity: {full_charge_capacity} mAh")

    # Read the cycle count
    cycle_count = bus.read_word_data(DEVICE_ADDRESS, 0x0017)
    print(f"Cycle Count: {cycle_count}")

    # Read the date
    date = bus.read_word_data(DEVICE_ADDRESS, 0x001B)
    print("Date: {:d}-{:02d}-{:02d}".format(1980 + ((date>>9)&0x7f), (date>>5)&0x0f, (date)&0x1f))

    # Read the design voltage
    design_voltage = bus.read_word_data(DEVICE_ADDRESS, 0x0019)
    print(f"Design Voltage: {design_voltage} mV")

    # Read the manufacturer name
    manufacturer_name = bus.read_i2c_block_data(DEVICE_ADDRESS, 0x0020, 16)
    print(f"Manufacturer Name: {''.join(map(chr, manufacturer_name))}")

    # Read the device name
    device_name = bus.read_i2c_block_data(DEVICE_ADDRESS, 0x0021, 16)
    print(f"Device Name: {''.join(map(chr, device_name))}")

    # Read the serial number
    serial_number = bus.read_word_data(DEVICE_ADDRESS, 0x001C)
    print(f"Serial Number: {hex(serial_number)}")

    # Read the charging current
    charging_current = bus.read_word_data(DEVICE_ADDRESS, 0x0014)
    print(f"Charging Current: {charging_current} mA")

    # Read the charging voltage
    charging_voltage = bus.read_word_data(DEVICE_ADDRESS, 0x0015)
    print(f"Charging Voltage: {charging_voltage} mV")

    # Read the device chemistry
    device_chemistry = bus.read_i2c_block_data(DEVICE_ADDRESS, 0x0022, 16)
    print(f"Device Chemistry: {''.join(map(chr, device_chemistry))}")

    # Read other pack info...

    temperature = bus.read_word_data(DEVICE_ADDRESS, 0x08)
    print("Temperature:", temperature/ 10 - 273, "C")

    voltage = bus.read_word_data(DEVICE_ADDRESS, 0x09)
    print("Voltage:", voltage, "mV")

    current = bus.read_word_data(DEVICE_ADDRESS, 0x0A)
    print("Current:", current, "mA")
    
    relative_soc = bus.read_word_data(DEVICE_ADDRESS, 0x0D)
    print("RelativeSOC:", relative_soc, "%")
    
    absolute_soc = bus.read_word_data(DEVICE_ADDRESS, 0x0E)
    print("AbsoluteSOC:", absolute_soc, "%")
    
    remaining_capacity = bus.read_word_data(DEVICE_ADDRESS, 0x0F)
    print("Remaining Capacity:", remaining_capacity, "mAh")
    
    
    VCELL4 = bus.read_word_data(DEVICE_ADDRESS, 0x3C)
    print("VCELL4:", VCELL4, "mV")

    VCELL3 = bus.read_word_data(DEVICE_ADDRESS, 0x3D)
    print("VCELL3:", VCELL3, "mV")

    VCELL2 = bus.read_word_data(DEVICE_ADDRESS, 0x3E)
    print("VCELL2:", VCELL2, "mV")

    VCELL1 = bus.read_word_data(DEVICE_ADDRESS, 0x3F)
    print("VCELL1:", VCELL1, "mV")

    SpecificationInfo = bus.read_word_data(DEVICE_ADDRESS, 0x1A)
    print("SpecificationInfo:", hex(SpecificationInfo))

    BatteryStatus = bus.read_word_data(DEVICE_ADDRESS, 0x16)
    print("Battery Status:", hex(BatteryStatus))
    print_status(BatteryStatus, ["OCA", "TCA", "OTA", "TDA", "RCA", "RTA", "INIT", "DSG"])

    OperationStatus = bus.read_word_data(DEVICE_ADDRESS, 0x0054)
    print("Operation Status:", hex(OperationStatus))
    print_status(OperationStatus, ["PRES", "FAS", "SS", "CSV", "LDMD", "WAKE", "DSG", "XDSG", "XDSGI", "R_DIS", "VOK", "QEN"])

    if OperationStatus & 0b00100000:
        print("Sealed")
        read_123()
    else:
        print("Unsealsed")
        max_error = bus.read_byte_data(DEVICE_ADDRESS, 0x0C)
        print("MaxError:", max_error, "%")

        safety_status = bus.read_word_data(DEVICE_ADDRESS, 0x0051)
        if safety_status == 0:
            print("SafetyStatus: OK")
        else:
            print("SafetyStatus:", safety_status)
            print_status(safety_status, ["OTD","OTC","OCD","OCC","OCD2","OCC2","PUV","POV","CUV","COV","PF","HWDG","WDF","AOCD","SCC","SCD"])

        pf_status = bus.read_word_data(DEVICE_ADDRESS, 0x0053)
        if pf_status == 0:
            print("PFStatus: OK")
        else:
            print("PFStatus:", pf_status)
            print_status(pf_status, ["FBF","SOPT","SOCD","SOCC","AFE_P","AFE_C","DFF","DFETF","CFETF","CIM","SOTD","SOTC","SOV","PFIN"])

        charging_status = bus.read_word_data(DEVICE_ADDRESS, 0x0055)
        if charging_status == 0:
            print("Charging Status: OK")
        else:
            print("Charging Status:", charging_status)
            print_status(charging_status, ["XCHG","CHGSUSP","PCHG","MCHG","TCHG1","TCHG2","FCHG","PULSE","PLSOFF","CB","PCMTO","FCMTO","OCHGV","OCHGI","OC","XCHGLV"])

        read_123()

        manufacturer_status = bus.read_word_data(DEVICE_ADDRESS, 0x0006)
        print_status(manufacturer_status, ["FET1","FET0","PF1","PF0","STATE3","STATE2","STATE1","STATE0"])
        
        chemistry_id = bus.read_word_data(DEVICE_ADDRESS, 0x0008)
        print("Chemistry ID:", chemistry_id)
        time.sleep(0.1)

        battery_mode = bus.read_byte_data(DEVICE_ADDRESS, 0x03)
        print_status(battery_mode, ["CapM","ChgM","AM","PB","CC","CF","PBS","ICC"])
        

def print_status(value, status):
    if value & 0b10000000:
        print(status[0], end='|')
    if value & 0b01000000:
        print(status[1], end='|')
    if value & 0b00100000:
        print(status[2], end='|')
    if value & 0b00010000:
        print(status[3], end='|')
    if value & 0b00001000:
        print(status[4], end='|')
    if value & 0b00000100:
        print(status[5], end='|')
    if value & 0b00000010:
        print(status[6], end='|')
    if value & 0b00000001:
        print(status[7], end='|')
    print()

# Function to reset the pack
def pack_reset():
    write_smb_word(0x00, 0x0041)
    time.sleep(1)

# Function to unseal the pack
def unseal_pack():
    write_smb_word(0x00, unseal_key_1)
    write_smb_word(0x00, unseal_key_2)

# Function to move the pack to full access mode
def move_to_full_access_mode():
    write_smb_word(0x00, full_access_key_1)
    write_smb_word(0x00, full_access_key_2)

# Function to clear a permanent failure
def clear_permanent_failure():
    write_smb_word(0x00, pf_clear_key_1)
    write_smb_word(0x00, pf_clear_key_2)

# Function to clear the cycle count
def clear_cycle_count():
    write_smb_word(0x17, 0x0000)

# Function to set the current date
def set_current_date():
    today = datetime.date.today()
    year = today.year
    month = today.month
    day = today.day

    date = (year - 1980) << 9
    date |= month << 5
    date |= day
    date
    write_smb_word(0x1B, (year - 1980) * 512 + int(month) * 32 + day)

# Function to write the design capacity, QMAX, update status, and Ra_table
def write_data():
    write_smb_word(0x18, new_capacity)
    time.sleep(0.1)
    data = read_smb_subclass(82, 0x78)
    data[1] = new_capacity >> 8
    data[2] = new_capacity & 0xFF
    data[3] = new_capacity >> 8
    data[4] = new_capacity & 0xFF
    data[5] = new_capacity >> 8
    data[6] = new_capacity & 0xFF
    data[7] = new_capacity >> 8
    data[8] = new_capacity & 0xFF
    data[9] = new_capacity >> 8
    data[10] = new_capacity & 0xFF
    data[13] = 0x00
    write_smb_subclass(82, 0x78, data)
    for i in range(88, 96):
        data = [0x20, 0xFF, 0x55 if i < 92 else 0xFF, 0x00, 0xA0, 0x00, 0xA6, 0x00, 0x99, 0x00, 0x97, 0x00, 0x91, 0x00, 0x98, 0x00, 0xB0, 0x00, 0xCC, 0x00, 0xDE, 0x00, 0xFE, 0x01, 0x3B, 0x01, 0xB5, 0x02, 0x8B, 0x03, 0xE9, 0x05, 0xB2]
        write_smb_subclass(i, 0x78, data)

# Function to begin the impedance track algorithm
def begin_impedance_track_algorithm():
    write_smb_word(0x00, 0x0021)

# Main function
def main():
    print("Raspberry Smart Battery")
    print("Several utilities for working with TI bq20z... IC")
    print("Checking communication with the device at address 0x{:02X}...".format(addr))
    while True:
        try:
            bus.write_byte(addr, 0x00)
            break
        except IOError:
            print("The device is not responding.")
            time.sleep(1)
    print("The device was found !!!")
    while True:
        time.sleep(0.1)
        print("--------------------")
        print("Select operation:")
        print("1. Read pack info.")
        print("2. Pack Reset.")
        print("3. Unsealing a pack.")
        print("4. Move pack to Full Access mode.")
        print("5. Clearing a Permanent Failure.")
        print("6. Clearing CycleCount.")
        print("7. Setting current date.")
        print("8. Writing DesignCapacity, QMAX, Update status, Ra_table.")
        print("9. Begin the Impedance Track algorithm.")
        choice = input("Enter your choice: ")
        print("**************************************")
        if choice == "1":
            print("Pack Info...")
            read_pack_info()
        elif choice == "2":
            pack_reset()
            print("Reseting...")
            time.sleep(1)
        elif choice == "3":
            unseal_pack()
            print("Unsealing...")
        elif choice == "4":
            move_to_full_access_mode()
            print("Move to Full Access mode...")
        elif choice == "5":
            clear_permanent_failure()
            print("Clearing a Permanent Failure...")
        elif choice == "6":
            clear_cycle_count()
            print("Clearing CycleCount...")
        elif choice == "7":
            set_current_date()
            print("Setting current date...")
        elif choice == "8":
            write_data()
            print("Writing DesignCapacity, QMAX, Update status, Ra_table...")
        elif choice == "9":
            begin_impedance_track_algorithm()
            print("Begin the Impedance Track algorithm...")
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

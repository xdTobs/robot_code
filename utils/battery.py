def get_battery_status():
    max_voltage = 7.5
    min_voltage = 6
    try:
        with open('/sys/class/power_supply/lego-ev3-battery/voltage_now', 'r') as file:
            voltage_now = int(file.read().strip()) / 1000000
            percentage = ((voltage_now - min_voltage) / (max_voltage - min_voltage)) * 100
        return min(max(percentage, 0), 100)
    except Exception as e:
        print("Error getting battery status", e)
        return 0

class LogitechDevice:
    def __init__(self, name, min_dpi, max_dpi):
        self.name = name
        self.min_dpi = min_dpi
        self.max_dpi = max_dpi

# Creating instances of LogitechDevice for each device
devices = [
    LogitechDevice("MX Master 3", 200, 4000),
    LogitechDevice("MX Master 3 for Mac", 200, 4000),
    LogitechDevice("MX Master 2S", 200, 4000),
    LogitechDevice("MX Master", 400, 1600),
    LogitechDevice("MX Anywhere 2S", 200, 4000),
    LogitechDevice("MX Anywhere 3", 200, 4000),
    LogitechDevice("MX Vertical", 400, 4000),
    LogitechDevice("MX Ergo", 512, 2048),
    LogitechDevice("MX Ergo M575", 400, 2000),
    LogitechDevice("M720 Triathlon", 200, 3200),
    LogitechDevice("M590 Multi-Device Silent", 1000, 2000),
    LogitechDevice("M500s Advanced Corded Mouse", 200, 4000),
]

# Accessing the DPI range of a specific device
device_name = "MX Master 3"
for device in devices:
    if device.name == device_name:
        min_dpi = device.min_dpi
        max_dpi = device.max_dpi
        print(f"DPI range for {device_name}: {min_dpi}-{max_dpi}")
        break

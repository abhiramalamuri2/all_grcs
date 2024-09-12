'''
import uhd
import time


# Initialize the USRP device
usrp = uhd.usrp.MultiUSRP()

# Select GPIO bank (e.g., 'FP0' or 'FP1')
gpio_bank = "FP0"

# Configure GPIO direction
# 1 means output, 0 means input
direction_mask = 0x01  # Set GPIO pin 0 as output
usrp.set_gpio_attr(gpio_bank, "DDR", direction_mask, direction_mask)

# Configure GPIO output enable
output_enable_mask = 0x01  # Enable GPIO pin 0 for output
usrp.set_gpio_attr(gpio_bank, "OUT_EN", output_enable_mask, output_enable_mask)

# Set the GPIO pin to logic high (1)
usrp.set_gpio_attr(gpio_bank, "OUT", 0x01, 0x01)

# Wait for a while
time.sleep(1)

# Set the GPIO pin to logic low (0)
usrp.set_gpio_attr(gpio_bank, "OUT", 0x00, 0x01)

# Wait again
time.sleep(1)

print("Done sending dummy data.")
'''
import uhd
import time

# Initialize the USRP device
usrp = uhd.usrp.MultiUSRP()

# Choose an available GPIO bank, such as FP0A
gpio_bank = "FP0A"

# Configure GPIO direction
direction_mask = 0x01  # Set GPIO pin 0 as output
usrp.set_gpio_attr(gpio_bank, "DDR", direction_mask, direction_mask, 0)  # Use radio index 0

# Commenting out the "OUT_EN" line to see if it's necessary
# output_enable_mask = 0x01  # Enable GPIO pin 0 for output
# usrp.set_gpio_attr(gpio_bank, "OUT_EN", output_enable_mask, output_enable_mask, 0)  # Use radio index 0

# Infinite loop to toggle GPIO high and low
try:
    while True:
        # Set the GPIO pin to logic high (1)
        usrp.set_gpio_attr(gpio_bank, "OUT", 0x01, 0x01, 0)  # Use radio index 0
        print("GPIO HIGH")
        time.sleep(1.5)

        # Set the GPIO pin to logic low (0)
        usrp.set_gpio_attr(gpio_bank, "OUT", 0x00, 0x01, 0)  # Use radio index 0
        print("GPIO LOW")
        time.sleep(1.5)

except KeyboardInterrupt:
    print("\nExiting...")
    
    
    
    

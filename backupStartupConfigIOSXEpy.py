from netmiko import ConnectHandler
import datetime

# Device details
cisco_device = {
    'device_type': 'cisco_ios', # Choose your device os
    'host': '1.1.1.1',  # Replace with your switch's IP address
    'username': 'username',  # Replace with your username
    'password': 'password',  # Replace with your password
#    'secret': 'your_enable_password',  # Replace with your enable password if necessary
}

# TFTP server details
tftp_server = '1.1.1.1'

# Establish an SSH connection to the device
with ConnectHandler(**cisco_device) as net_connect:
    # Elevate privileges
    net_connect.enable()

    # Fetch the hostname for filename purposes
    hostname_output = net_connect.send_command("show run | include hostname")
    # Extract the hostname assuming the output is in the form of 'hostname <device_hostname>'
    hostname = hostname_output.split()[-1].strip()

    # Generate a timestamp for the filename
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

    # Create the filename using the hostname and timestamp
    filename = f"startup-config-{hostname}-{timestamp}"

    # Prepare the copy command
    copy_command = f"copy nvram:startup-config tftp://{tftp_server}/{filename}"

    # Send the copy command
    output = net_connect.send_command_timing(copy_command)

    # Handle possible prompts
    if 'Address or name of remote host' in output:
        output += net_connect.send_command_timing(tftp_server)
    if 'Destination filename' in output:
        output += net_connect.send_command_timing(filename)

    # Print output for debugging
    print(output)

# Note: This script does not handle the post-transfer file management on the TFTP server.
# You will need to manually organize the files or create a separate script to automate it.

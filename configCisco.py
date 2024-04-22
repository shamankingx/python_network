from netmiko import ConnectHandler

# Function to read IP addresses from a file
def read_ip_addresses(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if line.strip()]

# Define the device information
device_info = {
    'device_type': 'cisco_ios', # Choose your device OS
    'username': 'username', # Replace with your username
    'password': 'password', # Replace with your password
}

# Read IP addresses from the file
ip_addresses = read_ip_addresses('ipfile.txt') # Place IP Address list in "ipfile.txt"

# Iterate over each IP address
for ip_address in ip_addresses:
    device_info['ip'] = ip_address

    # Connect to the device
    net_connect = ConnectHandler(**device_info)

    # Send the configuration command
    config_commands = ['lldp run'] # Replace with your command with privilege
    output = net_connect.send_config_set(config_commands)

    # Print the output
    print(f"Configuration for {ip_address}:\n", output)

    # Disconnect from the device
    net_connect.disconnect()

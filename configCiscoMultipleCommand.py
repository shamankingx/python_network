from netmiko import ConnectHandler
from concurrent.futures import ThreadPoolExecutor

# Function to read IP addresses from a file
def read_ip_addresses(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if line.strip()]
 
# Function to configure a device
def configure_device(ip_address, username, password, commands):
    device_info = {
        'device_type': 'cisco_ios', # Choose your device OS
        'ip': ip_address,
        'username': username,
        'password': password,
    }

    with ConnectHandler(**device_info) as net_connect:
        output = net_connect.send_config_set(commands)
        print(f"Configuration for {ip_address}:\n", output)

# Read IP addresses from the file
ip_addresses = read_ip_addresses('ipfile.txt') # Place ip address list in "ipfile.txt"

# User input for configuration commands
config_commands = input("Enter configuration commands (comma-separated): ").split(',')

# Define your credentials
username = 'username' # Replace with your username
password = 'password' # Replace with your password

# Use ThreadPoolExecutor for parallel execution
with ThreadPoolExecutor(max_workers=len(ip_addresses)) as executor:
    # Submit tasks for each IP address
    futures = [executor.submit(configure_device, ip, username, password, config_commands) for ip in ip_addresses]

    # Wait for all tasks to complete
    for future in futures:
        future.result()

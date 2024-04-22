from netmiko import ConnectHandler
import re
import os
from datetime import datetime
import sys

# Fixed username, password, and commands
username = "username" #replace with your username
password = "password" #replace with your password
commands_to_execute = ["show run", "show version", "write memory"] #replace with your command without privilege

def generate_folder_name():
    current_month_year = datetime.now().strftime('%m-%B')
    return current_month_year

def ssh_commands(ip):
    device = {
        'device_type': 'brocade_fastiron', #choose your device os. In this example using brocade_fastiron (Ruckus)
        'ip': ip,
        'username': username,
        'password': password,
    }

    try:
        ssh_conn = ConnectHandler(**device)
        hostname = re.search(r'(\S+)\s?[>#]', ssh_conn.find_prompt()).group(1)
        output = ""
        for cmd in commands_to_execute:
            output += f"Command: {cmd}\n"
            output += ssh_conn.send_command(cmd)
            output += "\n"

        timestamp = datetime.now().strftime('%Y%b%d_%H%M')
        filename = f"{hostname}_{timestamp}.txt"
        folder_name = generate_folder_name()

        if getattr(sys, 'frozen', False):
            # Running as a PyInstaller executable
            output_location = os.path.dirname(sys.executable)
        else:
            # Running as a regular Python script
            output_location = os.path.dirname(os.path.abspath(__file__))

        full_folder_path = os.path.join(output_location, folder_name)
        full_output_path = os.path.join(full_folder_path, filename)
        output_with_header = f"Hostname: {hostname}\n\n{output}"
        os.makedirs(full_folder_path, exist_ok=True)
        with open(full_output_path, "w") as output_file:
            output_file.write(output_with_header)
            print(f"Output from {ip} saved in {full_output_path}")

        ssh_conn.disconnect()
    except Exception as ex:
        print(f"An error occurred while connecting to {ip}: {ex}")

if __name__ == "__main__":
    with open("ipfile.txt", "r") as file: #place ip address list in "ipfile.txt"
        ip_addresses = file.read().splitlines()

    for ip in ip_addresses:
        ssh_commands(ip)

from netmiko import ConnectHandler
import re
import os
from datetime import datetime

# Fixed username, password, and commands
username = "username" #replace with your username
password = "password" #replace with your password
commands_to_execute = ["config terminal", "lldp run", "do wr"] #replace with your command with privilege

def generate_folder_name():
    current_month_year = datetime.now().strftime('%m-%B')
    return current_month_year

def ssh_commands(ip):
    device = {
        'device_type': 'cisco_ios',  # Change the device type to Cisco IOS
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
        full_folder_path = os.path.join(output_location, folder_name)
        full_output_path = os.path.join(full_folder_path, filename)

        output_with_header = f"Hostname: {hostname}\n\n{output}"

        os.makedirs(full_folder_path, exist_ok=True)
        with open(full_output_path, "w") as output_file:
            output_file.write(output_with_header)
            print(f"Output from {ip} saved in {full_output_path}")

        ssh_conn.disconnect()
    #except SSHException as ex:
    #    print(f"SSH error occurred while connecting to {ip}: {ex}")
    except Exception as ex:
        print(f"An error occurred while connecting to {ip}: {ex}")

if __name__ == "__main__":
    output_location = os.path.dirname(os.path.abspath(__file__))  # Set the output location to the script's directory

    with open("ipfile.txt", "r") as file: #place ip address list in "ipfile.txt"
        ip_addresses = file.read().splitlines()

    for ip in ip_addresses:
        ssh_commands(ip)

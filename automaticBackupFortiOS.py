import paramiko
import time
import re

# Configuration
username = 'username'  # SSH username for connecting to FortiGate devices. Please replace with your username
password = 'password'  # SSH password for connecting to FortiGate devices. Please replace with your password
tftp_server_ip = '1.1.1.1'  # IP address of the TFTP server for backing up configurations. Please replace with your tftp server ip address
firewall_ip_file = 'firewallip.txt'  # File containing IP addresses of FortiGate devices to backup

def get_firewall_version(ssh_shell):
    """
    Function to retrieve the firewall version from the FortiGate device.

    Args:
        ssh_shell: Paramiko SSH shell object for sending commands to the FortiGate device.

    Returns:
        Tuple: A tuple containing major, minor, patch, and build version numbers if found, otherwise (None, None, None, None).
    """
    # Sends command to retrieve system status
    ssh_shell.send('get system status\n')
    time.sleep(2)  # Wait for the command to execute
    output = ssh_shell.recv(10000).decode('utf-8')

    # Parses the output to extract firewall version information
    match = re.search(r'Version: FortiGate-\d+[A-Z]? v(\d+)\.(\d+)\.(\d+),build(\d+)', output)
    if match:
        major, minor, patch, build = match.groups()
        return major, minor, patch, build
    else:
        return None, None, None, None

def backup_fortigate(fortigate_ip):
    """
    Function to perform backup of configuration from a FortiGate device.

    Args:
        fortigate_ip (str): IP address of the FortiGate device.
    """
    # Establishes SSH connection to the FortiGate device
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(fortigate_ip, username=username, password=password)

    # Starts SSH session
    ssh_shell = ssh.invoke_shell()
    time.sleep(1)  # Wait for the shell to start

    # Retrieves hostname of the FortiGate device
    ssh_shell.send('config system global\nshow full-configuration | grep hostname\nend\n')
    time.sleep(2)  # Wait for the command to execute
    output = ssh_shell.recv(10000).decode('utf-8')
    hostname_line = next((line for line in output.split('\n') if 'set hostname' in line), None)
    hostname = hostname_line.split('"')[1] if hostname_line else 'FortiGate'

    # Retrieves firewall version using the previously defined function
    major, minor, patch, build = get_firewall_version(ssh_shell)

    if major and minor and patch and build:
        # Formats filename with timestamp and version
        timestamp = time.strftime('%Y%m%d-%H%M%S')
        version_str = f"{major}_{minor}-{build}"
        backup_filename = f"{hostname}_{version_str}_{timestamp}.conf"

        # Waits for command prompt
        time.sleep(1)
        ssh_shell.recv(65535)

        # Sends backup command to FortiGate to backup configuration to TFTP server
        backup_command = f'execute backup config tftp {backup_filename} {tftp_server_ip}\n'
        ssh_shell.send(backup_command)
        time.sleep(5)  # Wait for the backup to complete

        print(f"Backup completed for {fortigate_ip}: {backup_filename}")  # Prints backup completion message
    else:
        print(f"Failed to retrieve version information for {fortigate_ip}")  # Prints failure message if version information cannot be retrieved

    # Closes SSH session
    ssh_shell.close()
    ssh.close()

# Reads IP addresses from file and backs up each one
with open(firewall_ip_file, 'r') as file:
    for line in file:
        firewall_ip = line.strip()
        if firewall_ip:  # Checks if the line is not empty
            print(f"Starting backup for {firewall_ip}")  # Prints message indicating backup initiation
            try:
                backup_fortigate(firewall_ip)  # Calls the function to backup the FortiGate device
            except Exception as e:
                print(f"Failed to backup {firewall_ip}: {e}")  # Prints failure message if backup fails

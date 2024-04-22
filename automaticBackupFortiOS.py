import paramiko
import time

# Configuration
username = 'username' #replace with your username
password = 'password' #replace with your password
tftp_server_ip = '1.1.1.1' #replace with your tftp server
firewall_ip_file = 'firewallip.txt' #place ip address list in this file

def backup_fortigate(fortigate_ip):
    # Establish SSH connection
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(fortigate_ip, username=username, password=password)

    # Start SSH session
    ssh_shell = ssh.invoke_shell()
    time.sleep(1)  # Wait for the shell to start

    # Retrieve hostname
    ssh_shell.send('config system global\nshow full-configuration | grep hostname\nend\n')
    time.sleep(2)  # Wait for the command to execute
    output = ssh_shell.recv(10000).decode('utf-8')

    # Parse hostname
    hostname_line = next((line for line in output.split('\n') if 'set hostname' in line), None)
    hostname = hostname_line.split('"')[1] if hostname_line else 'FortiGate'

    # Format filename with timestamp and add .conf extension
    timestamp = time.strftime('%Y%m%d-%H%M%S')
    backup_filename = f"{hostname}_{timestamp}.conf"

    # Send backup command to FortiGate
    backup_command = f'execute backup config tftp {backup_filename} {tftp_server_ip}\n'
    ssh_shell.send(backup_command)
    time.sleep(5)  # Wait for the backup to complete

    # Close SSH session
    ssh_shell.close()
    ssh.close()

    print(f"Backup completed for {fortigate_ip}: {backup_filename}")

# Read IP addresses from file and backup each one
with open(firewall_ip_file, 'r') as file:
    for line in file:
        firewall_ip = line.strip()
        if firewall_ip:  # Check if the line is not empty
            print(f"Starting backup for {firewall_ip}")
            try:
                backup_fortigate(firewall_ip)
            except Exception as e:
                print(f"Failed to backup {firewall_ip}: {e}")

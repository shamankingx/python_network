import paramiko
import time

def send_command_over_ssh(ssh_client, command):
    ssh_client.send(command + '\n')
    time.sleep(1)
    output = ssh_client.recv(65535).decode("utf-8")
    return output

def configure_switch(hostname, username, password):
    # Create an SSH client instance
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Connect to the switch
        ssh_client.connect(hostname, username=username, password=password, timeout=5)

        # Invoke the shell
        ssh_shell = ssh_client.invoke_shell()

        # Send configuration commands
        commands = [
            "conf t",                # Enter configuration mode
            "ntp server 2.2.2.2" # Set NTP IP address server as 2.2.2.2
            "exit" # Exit
            "wr" # Write memory
#            "line vty 0 4",          # Access virtual terminal lines 0 to 4
#            "transport input telnet",# Allow telnet connections
#            "exit",                   # Exit from line configuration mode
#            "exit"                    # Exit from configuration mode
        ]

        for command in commands:
            output = send_command_over_ssh(ssh_shell, command)
            print(output)

        # Close the SSH connection
        ssh_client.close()
        print("Configuration completed successfully.")
    except Exception as e:
        print("Error:", e)

# Replace these values with your switch credentials
hostname = "1.1.1.1" # Replace with your device IP address
username = "username" # Replace with you username
password = "password" # Replace with your password

configure_switch(hostname, username, password)

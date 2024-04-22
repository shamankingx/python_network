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
            #"ntp server 10.66.10.254",
            "snmp-server contact IT Department",
            "snmp-server location Office",
            "exit",
            "wr"
        ]

        for command in commands:
            output = send_command_over_ssh(ssh_shell, command)
            print(output)

        # Close the SSH connection
        ssh_client.close()
        print("Configuration completed successfully.")
    except Exception as e:
        print("Error:", e)

def main():
    # Read IP addresses from the file
    with open("ipfile.txt", "r") as file: # Place IP address list in "ipfile.txt"
        ip_addresses = file.read().splitlines()

    # Replace these values with your switch credentials
    username = "username" # Replace with your username
    password = "password" # Replace with your password

    # Iterate over each IP address and configure the switch
    for ip in ip_addresses:
        print("Configuring switch at", ip)
        configure_switch(ip, username, password)

if __name__ == "__main__":
    main()

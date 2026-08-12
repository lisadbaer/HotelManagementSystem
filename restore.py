import subprocess


def restore_backup(filename):

    command = ["mariadb", "-u", "root", "-pYOUR_PASSWORD", "hostel_management"]

    with open(filename, "r") as file:
        subprocess.run(command, stdin=file, check=True)

import subprocess
from datetime import datetime
import os


def create_backup():

    os.makedirs("backups", exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    filename = f"backups/hostel_{timestamp}.sql"

    command = ["mariadb-dump", "-u", "root", "-pYOUR_PASSWORD", "hostel_management"]

    with open(filename, "w") as file:
        subprocess.run(command, stdout=file, check=True)

    return filename

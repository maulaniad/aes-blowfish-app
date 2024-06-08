import subprocess
import os


def start_tailwind():
    if os.name == "nt":
        executable = "tailwindcss.exe"
    else:
        executable = "tailwindcss.sh"

    try:
        cmd = [f"./{executable}", "-i", "static/src/input.css", "-o", "static/src/output.css", "--watch"]
        subprocess.run(cmd)
    except FileNotFoundError:
        print("Tailwind CSS (Standalone) execeutable not found")
        print("You can download it from : https://github.com/tailwindlabs/tailwindcss/releases")
        print("After Download, put the executable file in the same folder as this script")
        print(f"Rename it to {executable}")
    except PermissionError:
        cmd = ["chmod", "+x", executable]
        subprocess.run(cmd)

        cmd = [f"./{executable}", "-i", "static/src/input.css", "-o", "static/src/output.css", "--watch"]
        subprocess.run(cmd)


if __name__ == "__main__":
    start_tailwind()

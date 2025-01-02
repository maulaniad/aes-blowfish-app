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
        print()
        print("FATAL ERROR !")
        print("Tailwind CSS (Standalone binary) executable not found")
        print("You can download it from : https://github.com/tailwindlabs/tailwindcss/releases")
        print("After Download, put the executable file in the same folder as this script")
        print(f"Rename it to {executable}")
    except PermissionError:
        cmd = ["chmod", "+x", executable]
        subprocess.run(cmd)

        cmd = [f"./{executable}", "-i", "static/src/input.css", "-o", "static/src/output.css", "--watch"]
        subprocess.run(cmd)


if __name__ == "__main__":
    try:
        print("Starting Tailwind CSS...")
        print("Only for Development Usage! Do not use it in production!")
        print("Finalized css will be in: static/src/output.css")
        print()
        print("Press [CTRL+C] to Stop")
        start_tailwind()
    except KeyboardInterrupt:
        print()
        print("Exiting...")
        print("Bye...")

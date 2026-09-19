import subprocess
import webbrowser
from datetime import datetime
from pathlib import Path

import ctypes


class ToolManager:

    # ==================================================
    # Open Application
    # ==================================================

    def open_app(self, app):

        apps = {
            "notepad": "notepad.exe",
            "calculator": "calc.exe",
            "paint": "mspaint.exe",
            "explorer": "explorer.exe",
        }

        app = app.lower().strip()

        if app not in apps:

            return (
                f"I don't have permission to open "
                f"{app}, sir."
            )

        try:

            subprocess.Popen(
                apps[app],
                shell=False
            )

            return (
                f"{app.capitalize()} opened, sir."
            )

        except Exception as error:

            print(
                f"Open app error: {error}"
            )

            return (
                f"I couldn't open {app}, sir."
            )

    # ==================================================
    # Open Website
    # ==================================================

    def open_website(self, url):

        try:

            if not url.startswith(
                ("http://", "https://")
            ):

                url = "https://" + url

            webbrowser.open(url)

            return "Website opened, sir."

        except Exception as error:

            print(
                f"Website error: {error}"
            )

            return (
                "I couldn't open that website, sir."
            )

    # ==================================================
    # Get Time
    # ==================================================

    def get_time(self):

        current_time = datetime.now().strftime(
            "%I:%M %p"
        )

        return (
            f"The current time is "
            f"{current_time}, sir."
        )

    # ==================================================
    # Get Date
    # ==================================================

    def get_date(self):

        current_date = datetime.now().strftime(
            "%A, %d %B %Y"
        )

        return (
            f"Today is "
            f"{current_date}, sir."
        )

    # ==================================================
    # Set Volume
    # ==================================================

    def set_volume(self, level):

        try:

            level = int(level)

            if level < 0:
                level = 0

            if level > 100:
                level = 100

            # 0-100 becomes 0-50 volume steps
            steps = round(level / 2)

            # Bring volume down to zero
            for _ in range(50):

                ctypes.windll.user32.keybd_event(
                    0xAE,
                    0,
                    0,
                    0
                )

                ctypes.windll.user32.keybd_event(
                    0xAE,
                    0,
                    2,
                    0
                )

            # Increase to requested level
            for _ in range(steps):

                ctypes.windll.user32.keybd_event(
                    0xAF,
                    0,
                    0,
                    0
                )

                ctypes.windll.user32.keybd_event(
                    0xAF,
                    0,
                    2,
                    0
                )

            return (
                f"Volume set to {level} percent, sir."
            )

        except Exception as error:

            print(
                f"Volume error: {error}"
            )

            return (
                "I couldn't change the volume, sir."
            )

    # ==================================================
    # Create Folder
    # ==================================================

    def create_folder(self, path):

        try:

            folder = Path(path)

            if folder.exists():

                return (
                    f"{folder.name} already exists, sir."
                )

            # Create the folder AND every
            # missing parent folder.
            folder.mkdir(
                parents=True,
                exist_ok=False
            )

            return (
                f"{folder.name} created successfully, sir."
            )

        except Exception as error:

            print(
                f"Create folder error: {error}"
            )

            return (
                "I couldn't create that folder, sir."
            )

    # ==================================================
    # Create File
    # ==================================================

    def create_file(
        self,
        path,
        content=""
    ):

        try:

            file_path = Path(path)

            if file_path.exists():

                return (
                    f"{file_path.name} already exists, sir."
                )

            # Create EVERY missing parent folder.
            file_path.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            # Create the file.
            file_path.write_text(
                content,
                encoding="utf-8"
            )

            return (
                f"{file_path.name} created successfully, sir."
            )

        except Exception as error:

            print(
                f"Create file error: {error}"
            )

            return (
                "I couldn't create that file, sir."
            )
from Frontend.Ui import UltronUI
from Backend.wakeword import WakeWordListener


class Ultron:
    def __init__(self):
        # -------------------------
        # UI
        # -------------------------

        self.ui = UltronUI()

        # Start hidden
        self.ui.hide()

        # -------------------------
        # Wake Word
        # -------------------------

        self.wakeword = WakeWordListener(
            self.on_wake
        )

    # ==================================================
    # Wake word detected
    # ==================================================

    def on_wake(self):
        print("ULTRON ACTIVATED")

        # Tkinter must be updated from its own main thread
        self.ui.app.after(
            0,
            self.ui.show
        )

    # ==================================================
    # Start Ultron
    # ==================================================

    def start(self):
        print("ULTRON v1.26")
        print("System started.")
        print("Waiting for wake word...")

        self.wakeword.start()

        self.ui.run()


# ======================================================
# Main
# ======================================================

if __name__ == "__main__":
    ultron = Ultron()
    ultron.start()


import customtkinter as ctk
from pathlib import Path
from PIL import Image


class UltronUI:
    def __init__(self):
        # -------------------------
        # Appearance
        # -------------------------

        self.app = ctk.CTk()
        self.app.title("ULTRON")

        # Fullscreen + no Windows title bar
        self.app.attributes("-fullscreen", True)
        self.app.overrideredirect(True)

        self.app.configure(fg_color="#050608")

        # -------------------------
        # Screen size
        # -------------------------

        self.screen_width = self.app.winfo_screenwidth()
        self.screen_height = self.app.winfo_screenheight()

        # Design reference: 1920x1080
        base_width = 1920
        base_height = 1080

        scale_x = self.screen_width / base_width
        scale_y = self.screen_height / base_height

        # Preserve proportions
        self.scale = min(scale_x, scale_y)

        # Prevent UI becoming ridiculously small/large
        self.scale = max(0.65, min(self.scale, 1.5))

        def scale(value):
            return max(1, int(value * self.scale))

        self.s = scale

        # -------------------------
        # State
        # -------------------------

        self.pulse_state = 0
        self.scan_position = 15

        # -------------------------
        # Image path
        # -------------------------

        self.face_path = (
            Path(__file__).resolve().parent
            / "Static"
            / "Images"
            / "Face.png"
        )

        # -------------------------
        # Header
        # -------------------------

        self.title_label = ctk.CTkLabel(
            self.app,
            text="ULTRON",
            font=("Arial", self.s(38), "bold"),
            text_color="#E6E6E6"
        )

        self.title_label.pack(
            pady=(self.s(35), 0)
        )

        self.subtitle = ctk.CTkLabel(
            self.app,
            text="PERSONAL AI SYSTEM",
            font=("Arial", self.s(14)),
            text_color="#777777"
        )

        self.subtitle.pack(
            pady=(self.s(3), self.s(15))
        )

        # -------------------------
        # Responsive face frame
        # -------------------------

        frame_width = min(
            int(self.screen_width * 0.75),
            self.s(760)
        )

        frame_height = min(
            int(self.screen_height * 0.60),
            self.s(650)
        )

        self.face_frame = ctk.CTkFrame(
            self.app,
            width=frame_width,
            height=frame_height,
            corner_radius=self.s(24),
            fg_color="#090B0F",
            border_width=self.s(1),
            border_color="#20242A"
        )

        self.face_frame.pack(
            pady=self.s(20)
        )

        self.face_frame.pack_propagate(False)

        # -------------------------
        # Face image
        # -------------------------

        if self.face_path.exists():

            image = Image.open(self.face_path)

            face_size = min(
                int(frame_width * 0.65),
                int(frame_height * 0.75)
            )

            self.face_image = ctk.CTkImage(
                light_image=image,
                dark_image=image,
                size=(face_size, face_size)
            )

            self.face = ctk.CTkLabel(
                self.face_frame,
                text="",
                image=self.face_image
            )

            self.face.place(
                relx=0.5,
                rely=0.52,
                anchor="center"
            )

        else:

            self.face = ctk.CTkLabel(
                self.face_frame,
                text="Face.png not found",
                font=("Arial", self.s(22), "bold"),
                text_color="#555555"
            )

            self.face.place(
                relx=0.5,
                rely=0.52,
                anchor="center"
            )

        # -------------------------
        # Scanner
        # -------------------------

        scanner_width = int(
            frame_width * 0.50
        )

        self.scanner = ctk.CTkFrame(
            self.face_frame,
            width=scanner_width,
            height=self.s(2),
            fg_color="#666666"
        )

        self.scanner.place(
            relx=0.5,
            rely=0.15,
            anchor="center"
        )

        # -------------------------
        # Status
        # -------------------------

        self.status_frame = ctk.CTkFrame(
            self.app,
            fg_color="transparent"
        )

        self.status_frame.pack(
            pady=(self.s(8), self.s(5))
        )

        self.status_dot = ctk.CTkLabel(
            self.status_frame,
            text="●",
            font=("Arial", self.s(18)),
            text_color="#555555"
        )

        self.status_dot.pack(
            side="left",
            padx=(0, self.s(8))
        )

        self.status = ctk.CTkLabel(
            self.status_frame,
            text="STANDBY",
            font=("Arial", self.s(16), "bold"),
            text_color="#888888"
        )

        self.status.pack(
            side="left"
        )

        # -------------------------
        # Activity text
        # -------------------------

        self.command = ctk.CTkLabel(
            self.app,
            text="Waiting for activation...",
            font=("Arial", self.s(14)),
            text_color="#555555"
        )

        self.command.pack(
            pady=self.s(5)
        )

        # -------------------------
        # Animations
        # -------------------------

        self.animate_scanner()
        self.animate_pulse()

    # ==================================================
    # Show / Hide
    # ==================================================

    def show(self):
        self.app.deiconify()
        self.app.attributes("-fullscreen", True)
        self.app.lift()
        self.app.focus_force()

    def hide(self):
        self.app.withdraw()

    # ==================================================
    # Scanner animation
    # ==================================================

    def animate_scanner(self):

        self.scan_position += 1

        if self.scan_position >= 86:
            self.scan_position = 15

        self.scanner.place(
            relx=0.5,
            rely=self.scan_position / 100,
            anchor="center"
        )

        self.app.after(
            35,
            self.animate_scanner
        )

    # ==================================================
    # Status pulse
    # ==================================================

    def animate_pulse(self):

        self.pulse_state += 1

        if self.pulse_state % 80 < 40:

            self.status_dot.configure(
                text_color="#666666"
            )

        else:

            self.status_dot.configure(
                text_color="#333333"
            )

        self.app.after(
            80,
            self.animate_pulse
        )

    # ==================================================
    # Backend → UI
    # ==================================================

    def set_status(self, status):

        status = status.upper()

        self.status.configure(
            text=status
        )

        if status == "LISTENING":

            self.status_dot.configure(
                text_color="#AAAAAA"
            )

            self.command.configure(
                text="Listening for command..."
            )

        elif status == "THINKING":

            self.status_dot.configure(
                text_color="#777777"
            )

            self.command.configure(
                text="Processing..."
            )

        elif status == "SPEAKING":

            self.status_dot.configure(
                text_color="#999999"
            )

            self.command.configure(
                text="Speaking..."
            )

        else:

            self.status_dot.configure(
                text_color="#555555"
            )

            self.command.configure(
                text="Waiting for activation..."
            )

    # ==================================================
    # Activity text
    # ==================================================

    def set_command(self, text):
        self.command.configure(
            text=text
        )

    # ==================================================
    # Start UI
    # ==================================================

    def run(self):
        self.app.mainloop()


# ======================================================
# Test
# ======================================================

if __name__ == "__main__":

    ui = UltronUI()
    ui.run()


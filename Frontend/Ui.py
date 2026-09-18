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

        # Normal Windows window with title bar
        self.app.overrideredirect(False)
        self.app.resizable(True, True)

        self.app.configure(fg_color="#050608")

        # -------------------------
        # Window size
        # -------------------------

        # Start maximized
        self.app.state("zoomed")

        # Minimum usable size
        self.app.minsize(700, 600)

        # -------------------------
        # Design reference
        # -------------------------

        self.base_width = 1920
        self.base_height = 1080

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
            font=("Arial", 38, "bold"),
            text_color="#E6E6E6"
        )

        self.title_label.pack()

        self.subtitle = ctk.CTkLabel(
            self.app,
            text="PERSONAL AI SYSTEM",
            font=("Arial", 14),
            text_color="#777777"
        )

        self.subtitle.pack()

        # -------------------------
        # Responsive face frame
        # -------------------------

        self.face_frame = ctk.CTkFrame(
            self.app,
            corner_radius=24,
            fg_color="#090B0F",
            border_width=1,
            border_color="#20242A"
        )

        self.face_frame.pack()

        self.face_frame.pack_propagate(False)

        # -------------------------
        # Face image
        # -------------------------

        if self.face_path.exists():

            image = Image.open(self.face_path)

            self.original_face_image = image

            self.face_image = ctk.CTkImage(
                light_image=image,
                dark_image=image,
                size=(400, 400)
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
                font=("Arial", 22, "bold"),
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

        self.scanner = ctk.CTkFrame(
            self.face_frame,
            height=2,
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

        self.status_frame.pack()

        self.status_dot = ctk.CTkLabel(
            self.status_frame,
            text="●",
            font=("Arial", 18),
            text_color="#555555"
        )

        self.status_dot.pack(
            side="left"
        )

        self.status = ctk.CTkLabel(
            self.status_frame,
            text="STANDBY",
            font=("Arial", 16, "bold"),
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
            font=("Arial", 14),
            text_color="#555555"
        )

        self.command.pack()

        # -------------------------
        # Resize handling
        # -------------------------

        self.app.bind(
            "<Configure>",
            self.on_resize
        )

        self.resize_job = None

        self.app.after(
            100,
            self.update_layout
        )

        # -------------------------
        # Animations
        # -------------------------

        self.animate_scanner()
        self.animate_pulse()

    # ==================================================
    # Responsive Layout
    # ==================================================

    def on_resize(self, event):

        # Only respond to the main window
        if event.widget != self.app:
            return

        # Avoid running layout hundreds of times
        if self.resize_job is not None:
            self.app.after_cancel(self.resize_job)

        self.resize_job = self.app.after(
            30,
            self.update_layout
        )

    # ==================================================

    def update_layout(self):

        self.resize_job = None

        width = self.app.winfo_width()
        height = self.app.winfo_height()

        if width <= 1 or height <= 1:
            return

        # -------------------------
        # Calculate responsive scale
        # -------------------------

        scale_x = width / self.base_width
        scale_y = height / self.base_height

        scale = min(
            scale_x,
            scale_y
        )

        # Keep things usable at small sizes
        scale = max(
            0.55,
            min(scale, 1.5)
        )

        self.scale = scale

        def s(value):
            return max(
                1,
                int(value * self.scale)
            )

        self.s = s

        # -------------------------
        # Header
        # -------------------------

        self.title_label.configure(
            font=("Arial", s(38), "bold")
        )

        self.title_label.pack_configure(
            pady=(s(35), 0)
        )

        self.subtitle.configure(
            font=("Arial", s(14))
        )

        self.subtitle.pack_configure(
            pady=(s(3), s(15))
        )

        # -------------------------
        # Face frame
        # -------------------------

        available_width = int(width * 0.75)
        available_height = int(height * 0.60)

        frame_width = min(
            available_width,
            s(760)
        )

        frame_height = min(
            available_height,
            s(650)
        )

        # Prevent the frame from becoming unusable
        frame_width = max(
            s(400),
            frame_width
        )

        frame_height = max(
            s(300),
            frame_height
        )

        self.face_frame.configure(
            width=frame_width,
            height=frame_height,
            corner_radius=s(24),
            border_width=s(1)
        )

        self.face_frame.pack_configure(
            pady=s(20)
        )

        # -------------------------
        # Face image
        # -------------------------

        if self.face_path.exists():

            face_size = min(
                int(frame_width * 0.65),
                int(frame_height * 0.75)
            )

            face_size = max(
                s(150),
                face_size
            )

            self.face_image.configure(
                size=(face_size, face_size)
            )

        else:

            self.face.configure(
                font=("Arial", s(22), "bold")
            )

        # -------------------------
        # Scanner
        # -------------------------

        scanner_width = int(
            frame_width * 0.50
        )

        self.scanner.configure(
            width=scanner_width,
            height=s(2)
        )

        # -------------------------
        # Status
        # -------------------------

        self.status_frame.pack_configure(
            pady=(s(8), s(5))
        )

        self.status_dot.configure(
            font=("Arial", s(18))
        )

        self.status_dot.pack_configure(
            padx=(0, s(8))
        )

        self.status.configure(
            font=("Arial", s(16), "bold")
        )

        # -------------------------
        # Activity
        # -------------------------

        self.command.configure(
            font=("Arial", s(14))
        )

        self.command.pack_configure(
            pady=s(5)
        )

        # -------------------------
        # Keep scanner in place
        # -------------------------

        self.scanner.place(
            relx=0.5,
            rely=self.scan_position / 100,
            anchor="center"
        )

    # ==================================================
    # Show / Hide
    # ==================================================

    def show(self):

        # Restore Ultron if minimized/hidden
        self.app.deiconify()

        # Maximize the normal Windows window
        self.app.state("zoomed")

        # Temporarily put Ultron above other windows
        self.app.attributes(
            "-topmost",
            True
        )

        # Bring Ultron to the front
        self.app.lift()

        # Give Ultron keyboard focus
        self.app.focus_force()

        # Refresh immediately
        self.app.update_idletasks()
        self.app.update()

        # Remove topmost after Ultron is brought forward
        self.app.after(
            300,
            lambda: self.app.attributes(
                "-topmost",
                False
            )
        )

    def hide(self):

        # Minimize Ultron instead of destroying the window
        self.app.iconify()

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


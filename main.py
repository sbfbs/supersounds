import tkinter as tk
from tkinter import messagebox
import os
import sys
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL

def is_windows():
    return sys.platform.startswith('win')

def set_max_volume():
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = interface.QueryInterface(IAudioEndpointVolume)
        volume.SetMasterVolumeLevelScalar(1.0, None)
        return True
    except Exception as e:
        messagebox.showerror("Error", f"Failed to set volume: {e}")
        return False

def show_instructions():
    instructions = (
        "To further boost the sound, you can enable Loudness Equalization:\n\n"
        "1. Click the 'Open Sound Settings' button below.\n"
        "2. In the Sound settings, right-click on your default playback device and select 'Properties'.\n"
        "3. Go to the 'Enhancements' tab.\n"
        "4. Check 'Loudness Equalization' and click 'OK'."
    )
    messagebox.showinfo("Instructions", instructions)

def maximize_sound():
    if set_max_volume():
        show_instructions()

def open_sound_settings():
    try:
        os.system("control mmsys.cpl,,0")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open sound settings: {e}")

def main():
    if not is_windows():
        messagebox.showerror("Unsupported OS", "This tool is only supported on Windows.")
        return

    root = tk.Tk()
    root.title("Sound Maximizer")
    root.geometry("400x300")

    warning_label = tk.Label(root, text="Warning: Extremely loud sounds can damage your hearing and speakers. Use this tool responsibly.", fg="red", wraplength=380)
    warning_label.pack(pady=10)

    ack_var = tk.BooleanVar()
    ack_check = tk.Checkbutton(root, text="I understand the risks and wish to proceed", variable=ack_var)
    ack_check.pack(pady=5)

    max_sound_button = tk.Button(root, text="Maximize Sound", state="disabled", command=maximize_sound)
    max_sound_button.pack(pady=10)

    open_settings_button = tk.Button(root, text="Open Sound Settings", command=open_sound_settings)
    open_settings_button.pack(pady=10)

    def update_button_state():
        if ack_var.get():
            max_sound_button.config(state="normal")
        else:
            max_sound_button.config(state="disabled")

    ack_var.trace("w", lambda *args: update_button_state())

    root.mainloop()

if __name__ == "__main__":
    main()

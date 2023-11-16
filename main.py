import os
import tkinter as tk
import tkinterdnd2
from tkinterdnd2 import TkinterDnD, DND_FILES
from tkinter import filedialog


def join_and_convert(input_folder, output_format="mp3"):
    status_label.config(text="Processing...")
    root.update()

    try:
        # Get all OPUS files in the folder
        opus_files = [
            file for file in os.listdir(input_folder) if file.endswith(".opus")
        ]

        # Sort the files to join them in order
        opus_files.sort()

        # Output file path
        output_format = output_format.lower()
        output_extension = "mp3" if output_format == "mp3" else "m4b"
        output_file = os.path.join(
            input_folder, f"{os.path.basename(input_folder)}.{output_extension}"
        )

        # Create a command to concatenate and convert OPUS files
        ffmpeg_command = (
            f"ffmpeg -hide_banner -i \"concat:{'|'.join([os.path.join(input_folder, opus) for opus in opus_files])}\" "
            f'-c:a libmp3lame -q:a 0 "{output_file}"'
        )

        # Execute the ffmpeg command
        os.system(ffmpeg_command)

        status_label.config(text="Conversion complete. Output file: " + output_file)
    except Exception as e:
        status_label.config(text="Error during conversion. " + str(e))


def on_drop(event):
    input_folder = event.data
    join_and_convert(input_folder)


def open_dialog():
    input_folder = filedialog.askdirectory()
    join_and_convert(input_folder)


root = TkinterDnD.Tk()
root.title("Audio Converter")

status_label = tk.Label(root, text="Drag and drop a folder or click below to select.")
status_label.pack(pady=20)

# Create a drop target
root.drop_target_register(DND_FILES)


def update_status_label():
    status_label.update()
    root.after(100, update_status_label)


# Keep updating the status label
update_status_label()

root.dnd_bind("<<Drop>>", on_drop)


# Create a button to open a file dialog
def open_dialog():
    input_folder = filedialog.askdirectory()
    join_and_convert(input_folder)


button = tk.Button(root, text="Select Folder", command=open_dialog)
button.pack(pady=10)

root.mainloop()

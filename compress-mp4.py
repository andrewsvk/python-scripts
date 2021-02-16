import os
import shutil
from ffmpy import FFmpeg


def get_filelist(path):
    """
    Return list of all .mp4 files in given directory and its subdirectories
    """
    filelist = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".mp4"):
                filelist.append(os.path.join(root, file))
    return filelist


def compress_file(file, ffmpeg_exe, crf):
    """
    Run compression at given file, removes the original one.
    """
    file_short = file.split("\\")[-2] + "\\" + file.split("\\")[-1]
    print(f"Processing: {file_short}...", end="")

    out_name = file.replace(".mp4", "-Compressed.mp4")

    # Setting FFmpeg args, see http: // ffmpeg.org/ffmpeg.html for more.
    in_args = {file: None}
    out_args = {
        out_name: f'-vcodec libx264 -crf {crf} -loglevel quiet -preset veryfast'}

    ff = FFmpeg(ffmpeg_exe, inputs=in_args, outputs=out_args)
    ff.run()

    os.remove(file)  # Remove original file
    os.rename(out_name, file)  # Set original name to compressed file

    print(" done")


def compress_all_files(filelist, ffmpeg_exe, crf=28):
    """
    Runs compress_file function at all files in a given filelist.
    """
    for file in filelist:
        compress_file(file, ffmpeg_exe, crf)


# crf = 28  # Constant Rate Factor 0-50
# path = "SET_PATH"  # Path to directory which will be processed
ffmpeg_path = shutil.which("ffmpeg")

if __name__ == "__main__":
    if not ffmpeg_path:
        ffmpeg_path = input(
            "ffmpeg.exe not found.\nPlease enter path to ffmpeg.exe: ")

    crf = int(input("Enter constant rate factor [0-50]: "))
    path = input(
        "Enter path to directory which will be processed\nincluding subdirectories: ")

    filelist = get_filelist(path)
    compress_all_files(filelist, ffmpeg_path, crf)
    print("Everything done.")

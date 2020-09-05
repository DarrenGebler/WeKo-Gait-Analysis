import os
import subprocess

path = "Videos/Flipped/"


def get_video_length(filename):
    """
    Gets video duration.

    :param filename: filename and location
    :return: video duration
    """
    video = subprocess.check_output(f"ffprobe -v error -select_streams v:0 -show_entries stream=duration -of "
                                    f"default=noprint_wrappers=1:nokey=1 {filename}", shell=True)
    video_duration = float(video.rstrip().decode())
    video_duration = int(video_duration)

    return video_duration


def split_by_seconds(filename):
    """
    Splits video into 2 second segments, spaced 0.2 seconds apart.

    :param filename: filename and location
    """
    video_length = get_video_length(filename)
    split_count = video_length - 2
    split_command = ["ffmpeg", "-i", filename]
    filebase = ".".join(filename.split(".")[:-1])
    fileext = filename.split(".")[-1]
    for n in range(0, split_count + 1):
        if n != split_count:
            i = 0.000
            while i < 1:
                split_args = []
                split_start = n + i
                split_end = 2
                if 0.6 <= i >= 0.8:
                    split_end = 3
                split_args += ["-ss", "{:.3f}".format(split_start), "-t", "{}".format(split_end), filebase + "-" + "{:.1f}".format(split_start) + "-of-" + \
                               str(split_count) + "." + fileext]
                subprocess.check_output(split_command+split_args)
                i += 0.2
        else:
            split_args = ["-ss", str(video_length - 2), "-t", "2", filebase + "-" + str(video_length - 2) + "-of-" + \
                           str(split_count) + "." + fileext]
            subprocess.check_output(split_command + split_args)


if __name__ == '__main__':
    for filenames in os.listdir(path):
        filenames = filenames.replace(" ", "")
        new_file_name = 'Videos/Normalised_flipped/normalise_{}'.format(filenames)
        path_filename = path+filenames
        os.system(f"ffmpeg -i {path_filename} -filter:v fps=fps=24 -an {new_file_name}")
        split_by_seconds(new_file_name)

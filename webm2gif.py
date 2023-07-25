import os
import shutil
import subprocess
import tempfile
from datetime import datetime

from PIL import Image

current_date = datetime.now().strftime('%Y-%m-%d')

tmp_dir = tempfile.mkdtemp(prefix=f'web2pngs-{current_date}-')


def _webm2pngs(webm_path: str) -> str:
    """
        Convert a WebM video into a series of PNG images.

        This function uses 'ffmpeg' to convert a WebM video file into a series of PNG images.
        'ffmpeg' must be installed on the system for this conversion to work.

        Parameters:
            webm_path (str): The path to the WebM video file.

        Returns:
            str: The path to the directory containing the generated PNG images.

        Raises:
            FileNotFoundError: If 'ffmpeg' command is not found in the system.

        Note:
            'ffmpeg' is required to be installed and accessible from the command line for this function to work.
            The generated PNG images will be saved in a subdirectory named after the input WebM video file.

        Example:
            webm_path = "/path/to/input.webm"
            pngs_dir_path = _webm2pngs(webm_path)
            print("PNG images saved at:", pngs_dir_path)
        """
    try:
        subprocess.run(['ffmpeg', '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    except FileNotFoundError:
        print("ffmpeg command not found")
        exit(1)

    frame_output_path = os.path.join(tmp_dir, os.path.basename(webm_path))

    if not os.path.exists(frame_output_path):
        os.makedirs(frame_output_path)
    else:
        return frame_output_path

    command = ['ffmpeg', '-c', 'libvpx-vp9', '-i', webm_path, os.path.join(frame_output_path, 'frame_%d.png')]

    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        if result.returncode == 0:
            return frame_output_path
        else:
            print("ffmpeg call process execute error")
    except subprocess.CalledProcessError as e:
        print('ffmpeg call process error:', e)


def _pngs2gif(pngs_dir_path: str, duration=50, loop=0, transparency=0) -> str:
    """
        Convert a sequence of PNG images into a GIF animation.

        This function takes a directory path containing a sequence of PNG images and converts them
        into a GIF animation. The images are sorted in alphabetical order based on their filenames.

        Parameters:
            pngs_dir_path (str): The path to the directory containing PNG images.
            duration (int, optional): The display duration of each frame in milliseconds. Default is 50ms.
            loop (int, optional): The number of times the GIF animation should loop (0 for infinite loop). Default is 0.
            transparency (int, optional): The transparency index for the GIF animation. Default is 0 (transparency).

        Returns:
            str: The path to the resulting GIF animation file.

        Note:
            The PNG images in the specified directory should be named in a way that represents their correct order.
            The resulting GIF animation will be saved as 'output.gif' in the same directory as the PNG images.

        Example:
            pngs_dir_path = "/path/to/png_images"
            result_gif_path = _pngs2gif(pngs_dir_path, duration=100, loop=0, transparency=0)
            print("GIF animation created at:", result_gif_path)
        """
    image_files = sorted([f for f in os.listdir(pngs_dir_path) if f.endswith('.png')])

    frames = [Image.open(os.path.join(pngs_dir_path, filename)).convert('P') for filename in image_files]

    result_gif_path = os.path.join(pngs_dir_path, 'output.gif')
    frames[0].save(result_gif_path, format='GIF',
                   append_images=frames[1:],
                   save_all=True,
                   duration=duration, loop=loop, transparency=transparency)
    return result_gif_path


def _clear_files_by_extension(directory_path, file_extension):
    if not os.path.exists(directory_path):
        return
    files = os.listdir(directory_path)

    files_to_delete = [file for file in files if file.lower().endswith(file_extension.lower())]

    if not files_to_delete:
        return

    for file_name in files_to_delete:
        file_path = os.path.join(directory_path, file_name)
        os.remove(file_path)


def webm2gif(webm_path: str, *args, **kwargs) -> str:
    """
        Converts a WebM video to a GIF animation.

        This function takes the path to a WebM video and converts it to a GIF animation
        using a series of PNG images. It internally calls the '_webm2pngs' function to
        extract frames from the WebM video and '_pngs2gif' function to create the GIF.

        Parameters:
            webm_path (str): The path to the WebM video file.
            *args: Variable length argument list. These arguments will be passed to the '_pngs2gif' function.
            **kwargs: Arbitrary keyword arguments. These arguments will be passed to the '_pngs2gif' function.

        Returns:
            str: The path to the resulting GIF animation file.

        Note:
            This function relies on the '_webm2pngs' and '_pngs2gif' functions to process the WebM video.
            The resulting GIF animation will be saved as 'output.gif' in the same directory as the input WebM video.

        Example:
            webm_path = "example.webm"
            result_gif_path = webm2gif(webm_path, duration=100, loop=0, transparency=0)
            print("GIF animation saved at:", result_gif_path)
        """
    pngs_dir_path = _webm2pngs(webm_path)
    gif_path = _pngs2gif(pngs_dir_path, *args, **kwargs)
    _clear_files_by_extension(pngs_dir_path, 'png')
    return gif_path


def tmp_dir_remove():
    if os.path.exists(tmp_dir):
        shutil.rmtree(tmp_dir)


def tmp_dir_clear():
    if os.path.exists(tmp_dir):
        for root, dirs, files in os.walk(tmp_dir, topdown=False):
            for file in files:
                file_path = os.path.join(root, file)
                os.remove(file_path)
            for dir in dirs:
                dir_path = os.path.join(root, dir)
                os.rmdir(dir_path)


if __name__ == '__main__':
    webm2gif('test.webm')

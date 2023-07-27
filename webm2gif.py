import subprocess


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
    try:
        subprocess.run(['ffmpeg', '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    except FileNotFoundError:
        print("ffmpeg command not found")
        exit(1)

    command = ['ffmpeg', '-y', '-c', 'libvpx-vp9', '-i', webm_path, '-lavfi', 'split[v],palettegen,[v]paletteuse',
               f'{webm_path}.gif']

    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        if result.returncode == 0:
            return f'{webm_path}.gif'
        else:
            print("ffmpeg call process execute error")
    except subprocess.CalledProcessError as e:
        print('ffmpeg call process error:', e)


if __name__ == '__main__':
    print(webm2gif('test.webm'))

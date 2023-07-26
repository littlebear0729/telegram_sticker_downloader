import os.path
import tempfile
from datetime import datetime
from pathlib import Path

import docker

client = docker.from_env()

current_date = datetime.now().strftime('%Y-%m-%d')

tmp_dir = tempfile.mkdtemp(prefix=f'tgs2gif-{current_date}-')


# Reference: https://github.com/vadolasi/tgs-to-git-api/blob/main/main.py
def tgs2gif(tgs_file_path: str, compress: bool = False) -> str:
    with open(tgs_file_path, 'rb') as buffer:
        content = buffer.read()

    with tempfile.TemporaryDirectory() as file_dir:
        file_name = f'{file_dir}/sticker.tgs'

        with open(file_name, 'wb') as buffer:
            buffer.write(content)

            client.containers.run(
                'edasriyan/tgs-to-gif',
                volumes={file_dir: {'bind': '/source', 'mode': 'rw'}},
                environment={
                    'WIDTH': '64' if compress else '512',
                    'HEIGHT': '64' if compress else '512',
                    'FPS': '20' if compress else '50',
                    'QUALITY': '45' if compress else '90'
                }
            )

        with open(f'{file_dir}/sticker.tgs.gif', 'rb') as buffer:
            gif_content = buffer.read()

        output_path = os.path.join(tmp_dir, (Path(tgs_file_path).stem + '.gif'))
        with open(output_path, 'wb') as output_file:
            output_file.write(gif_content)

        return output_path


if __name__ == '__main__':
    print(tgs2gif('test.tgs'))

# Telegram Sticker Downloader

Telegram Sticker Downloader is a Telegram bot designed to download both static and animated stickers from Telegram. This bot runs in a Docker container and can be easily deployed and run on a Linux system. 

## How to Run

Follow these steps to run Telegram Sticker Downloader on a Linux system:

1. **Install Docker and Docker Compose** (if not already installed):

   - Install Docker: Follow the instructions in the [official Docker documentation](https://docs.docker.com/get-docker/) to install Docker.
   - Install Docker Compose: Follow the instructions in the [official Docker Compose documentation](https://docs.docker.com/compose/install/) to install Docker Compose.

2. **Clone the Project Repository**:

   Use the following command to clone the project code to your local machine:

   ```bash
   git clone https://github.com/littlebear0729/telegram_sticker_downloader.git
   cd telegram_sticker_downloader
   ```

3. **Configure Bot Token**:

   Copy the `config.sample.json` file and rename it to `config.json`:

   ```bash
   cp config.sample.json config.json
   ```

   Edit the `config.json` file in a text editor and update it with your Telegram Bot Token and user IDs for the admin and whitelist fields

4. **Build the Docker Container**:

   In the project root directory, run the following command to build the Docker container:

   ```bash
   docker-compose build
   ```

5. **Start the Telegram Bot**:

   Run the following command to start the Telegram Bot:

   ```bash
   docker-compose up -d
   ```

   The bot will run in the background, and you can interact with it via Telegram.

## Notes

- Ensure that your Telegram Bot Token is correctly configured and has the necessary permissions to download stickers.
- If you require further customization or configuration, refer to the project code and make modifications as needed.


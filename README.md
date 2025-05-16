# E-Ink Display Server

This project provides a **FastAPI** server to interact with an e-ink display, enabling the display of images, text, weather forecasts, quotes, and QR codes for Wi-Fi and SSH access. It is designed for Raspberry Pi or similar hardware with an e-ink display, requiring an `OPEN_WEATHER_API` key for weather functionality.

## Features

- **Image Display**: Render images from local storage or uploaded files on the e-ink display.
- **Text Rendering**: Display customizable text with specified position, size, color, and centering.
- **Weather Forecasts**: Fetch and display weather data using OpenWeatherMap API, with visual forecast images.
- **Daily Quotes**: Retrieve and display inspirational quotes from ZenQuotes API.
- **QR Code Generation**: Generate QR codes for Wi-Fi credentials or SSH public keys.
- **IP Address Display**: Show the device’s IP address as text on the display.
- **RESTful API**: Control the display via HTTP GET and POST requests.
- **Clear and Reset**: Initialize, clear, or reset the display with optional sleep mode.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/dazemc/ink_manager.git
   cd ink_manager
   ```

2. **Set Up a Virtual Environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**:
   - Set the `OPEN_WEATHER_API` key for weather functionality:
     ```bash
     export OPEN_WEATHER_API='your_openweathermap_api_key'  # On Windows: set OPEN_WEATHER_API=your_key
     ```
   - Obtain a free API key from [OpenWeatherMap](https://openweathermap.org/).

5. **Set Up the E-Ink Display**:
   - Install drivers and libraries for your e-ink hardware (e.g., Waveshare e-Paper).
   - Ensure the `ink_display` library is compatible with your display model.

6. **Run the Server**:
   ```bash
   uvicorn app:app --host 0.0.0.0 --port 8000
   ```
   - Access the API at `http://<device-ip>:8000`.

## Dependencies

- `fastapi`: Web framework for the API server.
- `python-multipart`: Handles file uploads.
- `pillow`: Image manipulation for rendering and QR codes.
- `requests`: Fetches data from external APIs (e.g., ZenQuotes).
- `qrcode`: Generates QR codes for Wi-Fi and SSH.
- `ink_display`: Custom library for e-ink display control (ensure compatibility with your hardware).
- `WeatherData`: Custom library for weather data fetching and rendering.
- `logging`: Configurable logging with `logging.json`.
- `subprocess`: Executes shell commands (e.g., IP address, Wi-Fi PSK).

Install dependencies via:
```bash
pip install fastapi python-multipart pillow requests qrcode
```

## API Endpoints

### `/` [GET]
- **Description**: Home endpoint.
- **Response**: `"Nothing here yet"`.

### `/test` [GET]
- **Description**: Runs a test sequence: displays an image, draws text ("hello", "world", "goodbye world") with lines, and clears the display.
- **Response**: `"Success"`.

### `/text` [POST]
- **Description**: Renders text on the display with customizable parameters.
- **Request Body** (JSON, using `Text` model):
  - `text` (str): Text to display.
  - `color` (str): Hex color code (e.g., `"FF0000"` for red).
  - `pos` (str): Position as `x,y` (e.g., `"10,20"`).
  - `size` (int): Font size in points.
  - `center` (bool): Center the text if `true`.
- **Example**:
  ```bash
  curl -X POST "http://<device-ip>:8000/text" -H "Content-Type: application/json" -d '{"text":"Hello","color":"FF0000","pos":"5,0","size":24,"center":false}'
  ```
- **Response**: `"Success"`.

### `/display` [GET]
- **Description**: Displays the current drawing on the e-ink screen.
- **Response**: `"Success"`.

### `/reset` [GET]
- **Description**: Resets the display to a blank image.
- **Response**: `"Success"`.

### `/ip` [GET]
- **Description**: Displays the device’s IP address on the screen, fetched via `get_ip.sh`.
- **Response**: IP address as a string (e.g., `"192.168.1.100"`).

### `/upload_image` [POST]
- **Description**: Uploads an image file, converts it to BMP, and displays it.
- **Request**: Multipart form-data with a file.
- **Example**:
  ```bash
  curl -X POST "http://<device-ip>:8000/upload_image" -F "file=@/path/to/image.jpg"
  ```
- **Response**: JSON with `{"filename": "<filename>", "message": "File uploaded and displaying"}`.

### `/update_weather` [GET]
- **Description**: Fetches weather data via OpenWeatherMap and displays a forecast image.
- **Weather Icons**: See [OpenWeatherMap Icon List](https://openweathermap.org/weather-conditions#Icon-list).
- **Response**: `"Success"`.

### `/clear` [GET]
- **Description**: Clears the display and optionally puts it to sleep.
- **Query Parameters**:
  - `sleep` (bool, default: `true`): If `true`, puts the display to sleep.
- **Example**:
  ```bash
  curl "http://<device-ip>:8000/clear?sleep=false"
  ```
- **Response**: `"Success"`.

### `/quote` [GET]
- **Description**: Fetches a daily quote from [ZenQuotes API](https://zenquotes.io) and displays it with the author.
- **Response**: `"Success"`.

### `/qr-code/wifi` [GET]
- **Description**: Generates and displays a QR code for Wi-Fi credentials (SSID and PSK) using `iwgetid` and `get_psk.sh`.
- **Notes**: Requires plaintext PSK in Wi-Fi configuration (Raspberry Pi Imager’s hashed PSK won’t work).
- **Response**: `"Success"`.

### `/qr-code/ssh` [GET]
- **Description**: Generates and displays a QR code for the SSH public key from `/home/daze/.ssh/id_rsa.pub`.
- **Response**: `"Success"`.

## Configuration

- **Environment Variables**:
  - `OPEN_WEATHER_API`: Required for `/update_weather`. Sign up at [OpenWeatherMap](https://openweathermap.org/).
- **Logging**: Configured via `logging.json`. Set `DEBUG = True` in `app.py` for verbose logs.
- **Fonts**: Uses `Inktype.ttf` in `./assets/fonts/`.
- **Uploads**: Stores uploaded images in `./assets/images/uploads/`.

## File Structure

- `app.py`: Main FastAPI application.
- `assets/`:
  - `images/`: Test images, weather forecasts, and uploads.
  - `fonts/`: Font files (e.g., `Inktype.ttf`).
  - `scripts/`: Shell scripts (e.g., `get_ip.sh`, `get_psk.sh`).
- `logging.json`: Logging configuration.
- `requirements.txt`: Python dependencies.
- `InkDisplay.py`: Custom e-ink display library (not included; ensure compatibility).
- `WeatherData.py`: Custom weather data library.
- `utils.py`: Helper functions (e.g., `center_text`).

## Logging

- Logs are output to the console and configured via `logging.json`.
- Enable `DEBUG = True` in `app.py` for detailed logging of API requests, errors, and operations.

## Notes

- **E-Ink Hardware**: Ensure your e-ink display is compatible with the `ink_display` library. Follow hardware-specific setup instructions (e.g., Waveshare e-Paper).
- **Wi-Fi QR Code**: The `/qr-code/wifi` endpoint requires a plaintext PSK in `/etc/wpa_supplicant/wpa_supplicant.conf`. If using Raspberry Pi Imager, manually set the PSK to avoid hashing.
- **SSH QR Code**: Ensure `/home/daze/.ssh/id_rsa.pub` exists for `/qr-code/ssh`.
- **Performance**: E-ink displays are slow to refresh. Endpoints include sleep calls to manage power and refresh cycles.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/YourFeature`).
3. Commit changes (`git commit -m 'Add YourFeature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a pull request.

Please open an issue to discuss proposed changes or report bugs.

## Contact

For questions or support, open an issue on the [GitHub repository](https://github.com/dazemc/ink_manager).

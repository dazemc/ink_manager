# E-Ink Display Server

This project provides a Flask-based server to interact with an e-ink display. It allows for displaying images, text, weather updates, and more on an e-ink screen.

## Features

- **Display Images:** Load and display images on the e-ink display.
- **Text Rendering:** Render text with customizable position, size, and color.
- **Weather Updates:** Fetch and display weather forecasts.
- **RESTful API:** Easily interact with the display using HTTP requests.
- **Clear Display:** Reset and clear the display content.

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/dazemc/ink_manager.git
    cd e-ink-display-server
    ```

2. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3. **Set up the e-ink display:**
    - Ensure the e-ink display drivers and libraries are properly installed. The exact setup depends on your specific e-ink hardware.

4. **Run the server:**

    ```bash
    python app.py
    ```

## Dependencies

- **Flask:** For building the web server.
- **Flask-CORS:** To handle Cross-Origin Resource Sharing.
- **Pillow:** For image manipulation.
- **Ink Display Library:** Custom library for interacting with the e-ink display.
- **WeatherData:** Custom library for fetching and rendering weather data.

## API Endpoints

### `/test` [GET]

- **Description:** Test endpoint to display a series of images and text on the e-ink display.
- **Returns:** `"Success"` if the operation completes.

### `/text` [GET]

- **Description:** Display text on the e-ink display.
- **Query Parameters:**
  - `text` (str): Text to display.
  - `color` (str): Text color in hexadecimal format (e.g., `FF0000` for red).
  - `pos` (str): Position as `x,y` coordinates (e.g., `10,20`).
  - `size` (int): Font size.
  - `center` (str): Center the text if `"true"`.
- **Returns:** `"Success"` if the operation completes.

### `/display` [GET]

- **Description:** Display the current drawing on the e-ink display.
- **Returns:** `"Success"` if the operation completes.

### `/reset` [GET]

- **Description:** Reset the display and create a new blank image.
- **Returns:** `"Success"` if the operation completes.

### `/upload_image` [GET, POST]

- **GET:** Display a test image.
- **POST:** Upload and display an image from the request.
- **Returns:** `"Success"` if the operation completes.

### `/update_weather` [GET]

- **Description:** Fetch the latest weather data and display it on the e-ink screen.
- **Returns:** `"Success"` if the operation completes.

### `/clear` [GET]

- **Description:** Clear the e-ink display.
- **Query Parameters:** 
  - `sleep` (bool): Put the display to sleep if `true`.
- **Returns:** `"Success"` if the operation completes.

## Configuration

- **`DEBUG`**: Set to `True` for verbose logging, `False` for minimal output.

## File Structure

- `app.py`: Main application file.
- `assets/`: Directory for images and fonts.
  - `images/`: Contains test and uploaded images.
  - `tools/forecast_builder/`: Contains weather data tools.

## Logging

Logs are generated to help trace the execution flow and debug issues. These logs can be found in the console output where the server is running.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contribution

Contributions are welcome! Please open an issue or submit a pull request.

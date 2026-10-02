# E-Ink Display Server

A **FastAPI-based server for controlling an e-ink display** from a Raspberry Pi or similar Linux device.

The server provides a REST API for displaying images, text, weather forecasts, quotes, random images, facts, QR codes, and device information. It is designed around an SPI-connected e-paper display and uses the `e-paper-lib` Git submodule for display hardware support.

## Features

* **Image Display** — Display local images or uploaded images.
* **Text Rendering** — Draw text with configurable position, size, color, and centering.
* **Weather Forecasts** — Retrieve weather data from OpenWeatherMap and generate a forecast image.
* **Daily Quotes** — Retrieve daily quotes from ZenQuotes.
* **Random Facts** — Retrieve random facts and display them with a QR code linking to the source.
* **Random Images** — Retrieve random images from Lorem Picsum.
* **Wi-Fi QR Codes** — Generate a QR code containing the current Wi-Fi credentials.
* **SSH QR Codes** — Display an SSH public key as a QR code.
* **IP Address Display** — Display the device's current IP address.
* **REST API** — Control the display through HTTP endpoints.
* **Systemd Integration** — Run the server as a system service and automatically update the display using user-level timers.
* **Avahi Integration** — Advertise the display server on the local network.

## Hardware

The project is designed for an e-ink/e-paper display connected to a Raspberry Pi through SPI.

The display implementation is provided by the [`e-paper-lib`](https://github.com/dazemc/e-paper-lib) Git submodule.

The current display configuration uses an **800 × 480** Spectra 6 display.

## Installation

### 1. Clone the Repository

Clone the repository and initialize its Git submodule:

```bash
git clone --recurse-submodules https://github.com/dazemc/ink_manager.git
cd ink_manager
```

If the repository was already cloned without its submodules:

```bash
git submodule update --init --recursive
```

The e-paper display library will be available under:

```text
lib/
```

### 2. Enable Long-Running User Services

Enable systemd user services to continue running when the user is not logged in:

```bash
loginctl enable-linger
```

### 3. Install `uv`

The project uses [`uv`](https://docs.astral.sh/uv/) for Python environment and dependency management.

Install `uv` with:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

After installation, make sure `uv` is available in your shell.

### 4. Install Python Dependencies

From the repository directory:

```bash
uv sync
```

This creates the project's virtual environment and installs the dependencies defined in `pyproject.toml`.

### 5. Install System Dependencies

The project requires several system packages for GPIO, SPI, and Python extension support:

```bash
sudo apt install swig python3.13-dev liblgpio-dev
```

The Python dependencies are managed by `uv` and are listed in `pyproject.toml` and `uv.lock`.

### 6. Configure the Environment

Create a `.env` file in the project directory:

```env
OPEN_WEATHER_API='your_openweathermap_api_key'
```

`OPEN_WEATHER_API` is required by the weather functionality.

A free API key is available from [OpenWeatherMap](https://openweathermap.org/).

### 7. Enable SPI

Enable SPI using Raspberry Pi's configuration utility:

```bash
sudo raspi-config
```

Navigate to:

```text
Interface Options
    → SPI
        → Enable
```

**A reboot is not required after enabling SPI.**

Once SPI has been enabled, the display can be accessed immediately.

### 8. Run the Server

Start the FastAPI server:

```bash
./start.sh
```

The server listens on all interfaces on port `8000`:

```text
http://<device-ip>:8000
```

`start.sh` launches:

```text
uvicorn main:app --host 0.0.0.0
```

## Systemd Installation

The repository includes systemd units for running the server and automatically updating the display.

The installation script also configures Avahi for local network service discovery.

Run:

```bash
./scripts/install.sh
```

The installation script:

* Installs and configures Avahi.
* Installs the server under `/opt/ink_manager`.
* Installs the system-level `ink.service`.
* Installs the user-level display timers.
* Runs `uv sync` for the installed copy.
* Reloads the systemd configuration.

### Enable the Server

```bash
sudo systemctl enable --now ink.service
```

### Enable Automatic Display Updates

Enable the user-level timers:

```bash
systemctl --user enable --now \
    ink_quote.timer \
    ink_random_image.timer \
    ink_weather.timer \
    ink_fact.timer
```

The timers run their corresponding services automatically.

### Manually Run a Display Service

For example:

```bash
systemctl --user start ink_quote.service
```

Other available services include:

```text
ink_weather.service
ink_random_image.service
ink_fact.service
```

## Automatic Display Schedule

The systemd timers are configured as follows:

| Timer                    | Schedule                           | Content          |
| ------------------------ | ---------------------------------- | ---------------- |
| `ink_weather.timer`      | Every hour at `:00`                | Weather forecast |
| `ink_quote.timer`        | Every hour at `:30`                | Daily quote      |
| `ink_random_image.timer` | Every hour at `:45`                | Random image     |
| `ink_fact.timer`         | Defined by its timer configuration | Random fact      |

The timers call the local FastAPI server through HTTP.

## API

The API is served on port `8000`.

Replace `<device-ip>` with the IP address of the Raspberry Pi.

### `/` — GET

Home endpoint.

**Response:**

```text
Nothing here yet
```

---

### `/test` — GET

Runs a display test sequence.

The test:

1. Clears the display.
2. Creates a drawing.
3. Displays `hello`.
4. Displays `world`.
5. Draws a line.
6. Displays the drawing.
7. Displays `goodbye world`.
8. Clears and resets the display.

**Example:**

```bash
curl "http://<device-ip>:8000/test"
```

**Response:**

```text
Success
```

---

### `/text` — POST

Draws text onto the current display image.

#### Request Body

```json
{
  "text": "Hello",
  "color": "FF0000",
  "pos": "5,0",
  "size": 24,
  "center": false
}
```

| Parameter | Type    | Description              |
| --------- | ------- | ------------------------ |
| `text`    | string  | Text to display          |
| `color`   | string  | Hex color without `#`    |
| `pos`     | string  | Position in `x,y` format |
| `size`    | integer | Font size                |
| `center`  | boolean | Center the text          |

#### Example

```bash
curl -X POST "http://<device-ip>:8000/text" \
  -H "Content-Type: application/json" \
  -d '{"text":"Hello","color":"FF0000","pos":"5,0","size":24,"center":false}'
```

**Response:**

```text
Success
```

The endpoint modifies the current drawing. Use `/display` to send the current drawing to the physical display.

---

### `/display` — GET

Initializes the display and displays the current drawing.

```bash
curl "http://<device-ip>:8000/display"
```

**Response:**

```text
Success
```

---

### `/reset` — GET

Resets the in-memory drawing to a blank image.

This does not itself update the physical display.

```bash
curl "http://<device-ip>:8000/reset"
```

**Response:**

```text
Success
```

---

### `/clear` — GET

Initializes and clears the physical display.

By default, the display is put into sleep mode after clearing.

#### Query Parameters

| Parameter | Type    | Default | Description                                    |
| --------- | ------- | ------- | ---------------------------------------------- |
| `sleep`   | boolean | `true`  | Put the display into sleep mode after clearing |

#### Example

```bash
curl "http://<device-ip>:8000/clear"
```

Keep the display awake:

```bash
curl "http://<device-ip>:8000/clear?sleep=false"
```

**Response:**

```text
Success
```

---

### `/ip` — GET

Retrieves the device's IP address and displays it on the e-ink screen.

The IP address is obtained using:

```text
scripts/get_ip.sh
```

#### Example

```bash
curl "http://<device-ip>:8000/ip"
```

**Response:**

```text
192.168.1.100
```

---

### `/upload_image` — POST

Uploads an image, converts it to BMP, and displays it.

#### Example

```bash
curl -X POST "http://<device-ip>:8000/upload_image" \
  -F "file=@/path/to/image.jpg"
```

Uploaded files are stored under:

```text
assets/images/uploads/
```

The uploaded image is converted to BMP before being displayed.

**Response:**

```json
{
  "filename": "<filename>",
  "message": "File uploaded and displaying"
}
```

---

### `/random_image` — GET

Downloads a randomly selected image from [Lorem Picsum](https://picsum.photos/) and displays it.

```bash
curl "http://<device-ip>:8000/random_image"
```

The image is downloaded using a randomly generated seed and saved under:

```text
assets/images/random_image.*
```

**Response:**

```text
Success
```

---

### `/update_weather` — GET

Retrieves weather data from OpenWeatherMap, generates a forecast image, and displays it.

```bash
curl "http://<device-ip>:8000/update_weather"
```

The generated forecast is saved as:

```text
assets/images/weather_forecast/forecast.png
```

Weather functionality requires:

```env
OPEN_WEATHER_API='your_openweathermap_api_key'
```

The weather implementation currently retrieves location information for:

```text
Enumclaw, WA, US
```

and displays a five-day forecast.

**Response:**

```text
Success
```

---

### `/quote` — GET

Retrieves the daily quote from [ZenQuotes](https://zenquotes.io/) and displays it centered on the e-ink screen.

```bash
curl "http://<device-ip>:8000/quote"
```

The quote and author are automatically sized and positioned to fit the display.

**Response:**

```text
Success
```

---

### `/random_fact` — GET

Retrieves a random fact from the [Useless Facts API](https://uselessfacts.jsph.pl/) and displays it.

A QR code containing the fact's source URL is also displayed.

```bash
curl "http://<device-ip>:8000/random_fact"
```

**Response:**

```text
Success
```

---

### `/qr-code/wifi` — GET

Generates a QR code containing the current Wi-Fi network credentials and displays it on the e-ink screen.

The SSID is retrieved using:

```bash
iwgetid -r
```

The PSK is retrieved using:

```text
scripts/get_psk.sh
```

#### Important

The PSK must be available in plaintext.

If Raspberry Pi Imager creates a hashed PSK in the Wi-Fi configuration, this endpoint cannot retrieve the original password.

When configuring Wi-Fi with Raspberry Pi Imager, manually providing the PSK rather than allowing it to be hashed is required for this endpoint.

---

### `/qr-code/ssh` — GET

Reads the SSH public key from:

```text
/home/daze/.ssh/id_rsa.pub
```

and displays it as a QR code.

```bash
curl "http://<device-ip>:8000/qr-code/ssh"
```

The SSH public key must exist at the expected path.

## Configuration

### Environment Variables

| Variable           | Required    | Description            |
| ------------------ | ----------- | ---------------------- |
| `OPEN_WEATHER_API` | For weather | OpenWeatherMap API key |

The application loads environment variables using `python-dotenv`.

### Display Configuration

Display handling is provided by the `lib` Git submodule:

```text
lib/
```

The main application initializes the display with:

```python
ink = ink_display.InkDisplay()
```

The current application expects an 800 × 480 display.

### Fonts

Fonts are stored under:

```text
assets/fonts/
```

Current fonts include:

```text
Font.ttc
Helvetica.ttc
Inktype.ttf
Steelworks.ttf
```

The primary application display font is:

```text
Inktype.ttf
```

## Project Structure

```text
ink_manager/
├── assets/
│   ├── fonts/
│   │   ├── Font.ttc
│   │   ├── Helvetica.ttc
│   │   ├── Inktype.ttf
│   │   └── Steelworks.ttf
│   ├── images/
│   │   ├── test/
│   │   ├── weather_forecast/
│   │   └── weather_icons/
│   └── tools/
│       ├── colorsheet/
│       └── scripts/
│
├── avahi/
│   └── dazeink.service
│
├── lib/
│   └── e-paper-lib/          # Git submodule
│
├── scripts/
│   ├── get_ip.sh
│   ├── get_psk.sh
│   ├── image_test.py
│   ├── install.sh
│   └── test.py
│
├── systemd/
│   ├── system/
│   │   └── ink.service
│   └── user/
│       ├── ink_fact.service
│       ├── ink_fact.timer
│       ├── ink_quote.service
│       ├── ink_quote.timer
│       ├── ink_random_image.service
│       ├── ink_random_image.timer
│       ├── ink_weather.service
│       └── ink_weather.timer
│
├── main.py
├── models.py
├── pyproject.toml
├── start.sh
├── update_weather.py
├── utils.py
├── uv.lock
└── WeatherData.py
```

## Python Dependencies

The project uses the following primary Python packages:

* FastAPI
* GPIO Zero
* `lgpio`
* Pillow
* `python-dotenv`
* `qrcode`
* Requests
* `rpi-gpio`
* `spidev`

The exact versions and transitive dependencies are managed by:

```text
uv.lock
```

## System Dependencies

The project currently requires:

```text
swig
python3.13-dev
liblgpio-dev
```

Avahi is installed automatically by `scripts/install.sh`:

```text
avahi-daemon
avahi-utils
```

## Avahi / Network Discovery

The installation script configures Avahi using:

```text
avahi/dazeink.service
```

The service advertises the FastAPI server on port `8000` using the custom service type:

```text
_dazeInk._tcp
```

This allows compatible clients to discover the e-ink server on the local network.

## Logging

The application configures logging through the logging configuration provided by the e-paper library:

```text
lib/logging.json
```

`main.py` currently starts with:

```python
DEBUG = True
```

and initializes the logger when debugging is enabled.

## Running Without systemd

For development or manual operation, the server can be started directly:

```bash
./start.sh
```

The script runs:

```text
uvicorn main:app --host 0.0.0.0
```

For development, the API can then be accessed at:

```text
http://localhost:8000
```

or:

```text
http://<device-ip>:8000
```

## Notes

### SPI Does Not Require a Reboot

After enabling SPI through:

```bash
sudo raspi-config
```

there is **no need to reboot the Raspberry Pi**.

Select:

```text
Interface Options
    → SPI
        → Enable
```

and continue with the installation or start the server.

### E-Ink Refresh Performance

E-ink displays are significantly slower to refresh than conventional displays. Display operations may therefore take several seconds.

The application explicitly sleeps the display after many operations to reduce power consumption and leave the display in its low-power state.

### Wi-Fi QR Code Security

The Wi-Fi QR-code endpoint exposes the configured Wi-Fi password through the generated QR code. This endpoint does not work with Raspberry Pi Imager configurations where the Wi-Fi password has been stored as a hash.

Only use `/qr-code/wifi` in an environment where displaying the Wi-Fi credentials is appropriate.

### SSH QR Code

The SSH QR-code endpoint currently uses:

```text
/home/daze/.ssh/id_rsa.pub
```

If the public key is stored elsewhere, the endpoint will need to be modified accordingly.

## License

This project is licensed under the MIT License.

See [LICENSE](LICENSE) for the full license text.

## Contributing

Contributions are welcome.

1. Fork the repository.

2. Create a feature branch:

   ```bash
   git checkout -b feature/YourFeature
   ```

3. Make your changes.

4. Commit the changes:

   ```bash
   git commit -m "Add YourFeature"
   ```

5. Push the branch:

   ```bash
   git push origin feature/YourFeature
   ```

6. Open a pull request.

For larger changes, please open an issue first to discuss the proposed change.

## Contact

For questions, bug reports, or feature requests, open an issue on the [GitHub repository](https://github.com/dazemc/ink_manager).

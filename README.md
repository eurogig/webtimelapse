# WebTimelapse

A Python script that captures screenshots of a webpage at regular intervals and automatically assembles them into a timelapse video. Perfect for monitoring website changes, tracking visual evolution, or creating content for presentations and documentation.

## Features

- **Automated Screenshots**: Capture webpage screenshots at configurable intervals
- **Flexible Timing**: Set either total number of shots or total duration
- **Full Page Support**: Option to capture entire page height (not just viewport)
- **Automatic Video Generation**: Uses ffmpeg to create MP4 timelapse videos
- **Chronological Ordering**: Videos are assembled in chronological order, even across multiple script runs
- **Headless Browser**: Runs Chrome in headless mode for server compatibility
- **Customizable Output**: Adjust resolution, FPS, and output formats

## Prerequisites

- **Python 3.6+**
- **Chrome/Chromium browser** installed on your system
- **ffmpeg** (optional, for video generation)

## Installation

### Option 1: Direct Download (Recommended)

1. Clone or download this repository:
   ```bash
   git clone https://github.com/eurogig/webtimelapse.git
   cd webtimelapse
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Make the script executable (optional):
   ```bash
   chmod +x main.py
   ```

4. Ensure Chrome/Chromium is installed on your system

### Option 2: Install as Package

1. Install from GitHub:
   ```bash
   pip install git+https://github.com/eurogig/webtimelapse.git
   ```

2. Ensure Chrome/Chromium is installed on your system

### Option 3: Development Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/eurogig/webtimelapse.git
   cd webtimelapse
   ```

2. Install in development mode:
   ```bash
   pip install -e .
   ```

### Optional: Install ffmpeg

For automatic video generation, install ffmpeg:

**macOS:**
```bash
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**Windows:**
Download from [ffmpeg.org](https://ffmpeg.org/download.html) or use Chocolatey:
```bash
choco install ffmpeg
```

## Usage

### Basic Examples

**Capture 10 screenshots every 5 minutes:**
```bash
# Direct execution
python main.py --url "https://example.com" --shots 10 --interval 300

# Or if executable
./main.py --url "https://example.com" --shots 10 --interval 300

# Or if installed as package
webtimelapse --url "https://example.com" --shots 10 --interval 300
```

**Capture for 1 hour every 2 minutes:**
```bash
python main.py --url "https://example.com" --duration 3600 --interval 120
```

**Capture for 1 month every day:**
```bash
python main.py --url "https://example.com" ---shots 30 --interval 86400
```

**Full page capture with custom resolution:**
```bash
python main.py --url "https://example.com" --shots 20 --interval 180 --fullpage --width 1920 --height 1080
```

### Command Line Options

| Option | Description | Default | Required |
|--------|-------------|---------|----------|
| `--url` | Webpage URL to capture | - | **Yes** |
| `--out` | Output folder for images/video | `./captures` | No |
| `--interval` | Seconds between shots | `300` (5 min) | No |
| `--shots` | Total number of screenshots | - | **Yes** (or `--duration`) |
| `--duration` | Total duration in seconds | - | **Yes** (or `--shots`) |
| `--width` | Browser width in pixels | `1280` | No |
| `--height` | Browser height in pixels | `800` | No |
| `--fullpage` | Attempt full page screenshots | `False` | No |
| `--load-wait` | Seconds to wait after page load | `3.0` | No |
| `--fps` | Output video frames per second | `12` | No |
| `--video` | Output video filename | `timelapse.mp4` | No |

**Note:** You must specify either `--shots` or `--duration`, but not both.

## How It Works

1. **Setup**: Creates output directory and initializes headless Chrome browser
2. **Capture Loop**: 
   - Navigates to the specified URL
   - Waits for JavaScript to settle
   - Takes screenshot (viewport or full page)
   - Sleeps until next scheduled interval
3. **Video Generation**: Automatically assembles screenshots into MP4 using ffmpeg in chronological order
4. **Cleanup**: Closes browser and saves all files

## Output

The script generates:
- **Screenshots**: PNG files named `screenshot_XXXXXX_YYYYMMDD-HHMMSS.png`
- **Video**: MP4 timelapse (if ffmpeg is available)
- **Logs**: Console output showing progress and any errors

## Examples

### Monitor a News Website
```bash
# Capture homepage every 10 minutes for 24 hours
python main.py --url "https://news.ycombinator.com" --duration 86400 --interval 600 --fullpage
```

### Track E-commerce Changes
```bash
# Monitor product page every hour for a week
python main.py --url "https://store.example.com/product/123" --duration 604800 --interval 3600 --width 1920 --height 1080
```

### Document Website Evolution
```bash
# Capture development site every 30 minutes during workday
python main.py --url "https://dev.example.com" --shots 16 --interval 1800 --fullpage --fps 24
```

## Troubleshooting

### Common Issues

**Chrome/ChromeDriver not found:**
- Ensure Chrome is installed and accessible
- The script uses Selenium 4.6+ which auto-downloads ChromeDriver

**ffmpeg not found:**
- Install ffmpeg (see Installation section)
- The script will still capture screenshots without video generation

**Page not loading completely:**
- Increase `--load-wait` value for slower pages
- Some dynamic content may require longer wait times

**Memory issues with very long pages:**
- The script caps full-page height at 20,000px to prevent crashes
- Use viewport-only mode for extremely long pages

### Performance Tips

- **Lower resolution** for faster processing and smaller files
- **Increase interval** for longer monitoring periods
- **Use viewport mode** instead of full-page for better performance
- **Monitor disk space** for long-running captures

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

## Dependencies

- **selenium**: Web browser automation
- **ffmpeg**: Video processing (external dependency)
- **Chrome/Chromium**: Web browser (external dependency)

## Version History

- **v1.0**: Initial release with basic screenshot and video generation functionality

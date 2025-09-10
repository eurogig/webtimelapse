#!/usr/bin/env python3
"""
WebTimelapse - Capture screenshots of a webpage at intervals and create timelapse videos.

Usage:
    python main.py --url "https://example.com" --shots 10 --interval 300
    ./main.py --url "https://example.com" --shots 10 --interval 300
    webtimelapse --url "https://example.com" --shots 10 --interval 300
"""

import argparse
import os
import sys
import time
import shutil
import subprocess
from datetime import datetime, timedelta

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def parse_args():
    p = argparse.ArgumentParser(
        description="Capture a webpage at intervals and build a timelapse video."
    )
    p.add_argument("--url", required=True, help="Webpage URL to capture")
    p.add_argument("--out", default="./captures", help="Output folder for images/video")
    p.add_argument("--interval", type=int, default=300, help="Seconds between shots (default: 300)")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--shots", type=int, help="Total number of screenshots to capture")
    g.add_argument("--duration", type=int, help="Total duration in seconds (script computes shots)")
    p.add_argument("--width", type=int, default=1280, help="Browser width (px)")
    p.add_argument("--height", type=int, default=800, help="Browser height (px)")
    p.add_argument("--fullpage", action="store_true", help="Attempt full page screenshots")
    p.add_argument("--load-wait", type=float, default=3.0,
                   help="Seconds to wait after load for JS to settle (default: 3.0)")
    p.add_argument("--fps", type=int, default=12, help="Output video frames per second (default: 12)")
    p.add_argument("--video", default="timelapse.mp4", help="Output video filename")
    return p.parse_args()

def ensure_out_dir(path):
    os.makedirs(path, exist_ok=True)

def new_driver(width, height):
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument(f"--window-size={width},{height}")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--hide-scrollbars")
    # Selenium 4.6+ will download/manage ChromeDriver automatically.
    driver = webdriver.Chrome(options=opts)
    driver.set_page_load_timeout(120)
    return driver

def get_timestamped_name(idx):
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    return f"screenshot_{idx:06d}_{ts}.png"

def scroll_to_top(driver):
    driver.execute_script("window.scrollTo(0, 0);")

def fullpage_screenshot(driver, path):
    """
    Attempts a full-page screenshot by resizing the window to the page height.
    Works well for many pages (not guaranteed for extremely tall/lazy pages).
    """
    # Get full height using JS
    total_height = driver.execute_script("""
        const body = document.body, html = document.documentElement;
        return Math.max(
          body.scrollHeight, body.offsetHeight,
          html.clientHeight, html.scrollHeight, html.offsetHeight
        );
    """)
    # Cap to something reasonable to avoid crash on extremely long pages
    max_height = min(int(total_height), 20000)
    # Change window size to capture
    w = driver.get_window_size()["width"]
    driver.set_window_size(w, max_height)
    # A small settle
    time.sleep(0.5)
    driver.save_screenshot(path)

def viewport_screenshot(driver, path):
    driver.save_screenshot(path)

def capture_once(driver, url, wait_after_load, fullpage, path):
    driver.get(url)
    time.sleep(wait_after_load)
    scroll_to_top(driver)
    if fullpage:
        try:
            fullpage_screenshot(driver, path)
        except Exception:
            # Fallback to viewport on failure
            viewport_screenshot(driver, path)
    else:
        viewport_screenshot(driver, path)

def maybe_build_video(folder, fps, video_name, width=1920):
    """
    Uses ffmpeg if available to assemble screenshots into a timelapse MP4.
    Assumes files share prefix 'screenshot_' and end with '.png'.
    """
    if shutil.which("ffmpeg") is None:
        print("\n[!] ffmpeg not found on PATH. Skipping video assembly.")
        print("    You can install ffmpeg and run something like:\n")
        print(f'    ffmpeg -framerate {fps} -pattern_type glob -i "{folder}/screenshot_*.png" '
              f'-vf "scale={width}:-1,pad={width}:ceil(ih/2)*2:0:0:black" -c:v libx264 -pix_fmt yuv420p "{os.path.join(folder, video_name)}"\n')
        return False

    # Get all screenshot files and sort by modification time (chronological order)
    import glob
    screenshot_files = glob.glob(os.path.join(folder, "screenshot_*.png"))
    screenshot_files.sort(key=os.path.getmtime)  # Sort by modification time
    
    if not screenshot_files:
        print("[!] No screenshot files found to build video")
        return False
    
    # Rename files temporarily to ensure chronological order in glob pattern
    temp_files = []
    for i, file_path in enumerate(screenshot_files):
        temp_name = os.path.join(folder, f"temp_{i:06d}.png")
        os.rename(file_path, temp_name)
        temp_files.append((file_path, temp_name))
    
    # Use the original working approach with glob pattern
    cmd = [
        "ffmpeg",
        "-y",
        "-framerate", str(fps),
        "-pattern_type", "glob",
        "-i", os.path.join(folder, "temp_*.png"),
        "-vf", f"scale={width}:-1,pad={width}:{width}:0:0:black",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        os.path.join(folder, video_name),
    ]
    print("[*] Building video with ffmpeg...")
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    # Restore original filenames
    for original_path, temp_path in temp_files:
        try:
            os.rename(temp_path, original_path)
        except:
            pass
    
    if res.returncode == 0:
        print(f"[✓] Video saved to: {os.path.join(folder, video_name)}")
        return True
    else:
        print("[!] ffmpeg failed. Output:\n", res.stderr)
        return False

def main():
    args = parse_args()
    ensure_out_dir(args.out)

    # Determine number of shots
    if args.shots is not None:
        nshots = args.shots
    else:
        # Compute from duration
        nshots = max(1, int(round(args.duration / args.interval)))

    print(f"URL: {args.url}")
    print(f"Output folder: {args.out}")
    print(f"Interval: {args.interval}s | Shots: {nshots} | Full page: {args.fullpage}")
    print(f"Viewport: {args.width}x{args.height} | Load wait: {args.load_wait}s")
    print(f"Will attempt to build video at {args.fps} fps -> {args.video}\n")

    driver = None
    try:
        driver = new_driver(args.width, args.height)
        start = datetime.now()
        for i in range(nshots):
            img_name = get_timestamped_name(i)
            img_path = os.path.join(args.out, img_name)
            t0 = datetime.now()
            print(f"[*] [{i+1}/{nshots}] Capturing {img_name} ... ", end="", flush=True)

            try:
                capture_once(driver, args.url, args.load_wait, args.fullpage, img_path)
                print("done.")
            except Exception as e:
                print(f"error: {e}")

            # Sleep until next scheduled tick
            if i < nshots - 1:
                elapsed = (datetime.now() - t0).total_seconds()
                sleep_for = max(0, args.interval - elapsed)
                time.sleep(sleep_for)

        total = datetime.now() - start
        print(f"\n[✓] Finished capturing {nshots} screenshots in ~{str(total).split('.')[0]}")

    finally:
        if driver:
            driver.quit()

    # Build video if possible
    maybe_build_video(args.out, args.fps, args.video, args.width)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Interrupted by user. Exiting.")
        sys.exit(1)

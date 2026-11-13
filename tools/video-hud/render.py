#!/usr/bin/env python3
"""Render the self-made cosmos HUD loop.

Source scene: tools/video-hud/scene.html (canvas, no third-party art, no text).
Frames: Playwright calls renderFrame(t) at 24 fps for 8 seconds, 640x360.
Encode: ffmpeg H.264 mp4 + VP9 webm, no audio. Poster: first frame as webp.

Run from the repo root:
  python3 tools/video-hud/render.py
Outputs:
  assets/video/cosmos-hud.mp4
  assets/video/cosmos-hud.webm
  assets/video/hud-poster.webp
"""
import base64, pathlib, shutil, subprocess, sys
ROOT = pathlib.Path(__file__).resolve().parents[2]
SCENE = pathlib.Path(__file__).resolve().parent / 'scene.html'
OUT = ROOT / 'assets' / 'video'
FRAMES = pathlib.Path('/tmp/hud-frames')
FPS, SECONDS, N = 24, 8, 24 * 8

def main():
    from playwright.sync_api import sync_playwright
    if FRAMES.exists():
        shutil.rmtree(FRAMES)
    FRAMES.mkdir(parents=True)
    OUT.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = None
        err = None
        for kwargs in (
            dict(channel='chrome', headless=True, args=['--no-sandbox', '--disable-dev-shm-usage']),
            dict(headless=True, args=['--no-sandbox', '--disable-dev-shm-usage']),
        ):
            try:
                browser = p.chromium.launch(**kwargs)
                break
            except Exception as e:
                err = e
        if browser is None:
            raise err
        page = browser.new_page(viewport={'width': 640, 'height': 360})
        page.goto(SCENE.as_uri())
        page.wait_for_function('window.renderFrame')
        for i in range(N):
            b64 = page.evaluate('(t) => window.renderFrame(t)', i / N)
            (FRAMES / f'f{i:04d}.jpg').write_bytes(base64.b64decode(b64))
            if i % 24 == 0:
                print('frame', i, flush=True)
        browser.close()
    mp4 = OUT / 'cosmos-hud.mp4'
    webm = OUT / 'cosmos-hud.webm'
    poster = OUT / 'hud-poster.webp'
    subprocess.check_call([
        'ffmpeg', '-y', '-framerate', str(FPS), '-i', str(FRAMES / 'f%04d.jpg'),
        '-an', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '32', '-preset', 'slow',
        '-movflags', '+faststart', '-tune', 'animation', str(mp4)])
    subprocess.check_call([
        'ffmpeg', '-y', '-framerate', str(FPS), '-i', str(FRAMES / 'f%04d.jpg'),
        '-an', '-c:v', 'libvpx-vp9', '-b:v', '0', '-crf', '40', '-row-mt', '1', '-deadline', 'good',
        str(webm)])
    subprocess.check_call([
        'ffmpeg', '-y', '-i', str(FRAMES / 'f0000.jpg'), '-c:v', 'libwebp', '-quality', '55', str(poster)])
    for f in (mp4, webm, poster):
        print(f'{f.name}\t{f.stat().st_size} bytes')

if __name__ == '__main__':
    sys.exit(main())

#!/usr/bin/env python3
"""Build an Instagram slideshow Reel (1080x1920, H.264, 30fps) from a post's images.

Usage: python3 tools/reel.py out.mp4 img1.jpeg [img2.jpeg ...] [--music track.mp3]

- Each image is fit to 9:16 over a blurred, zoomed copy of itself (no cropping of the photo).
- Every slide gets a gentle slow push-in; a single image runs ~6 s.
- 2+ images: ~2.3-3 s each with 0.4 s crossfades, total kept between ~5.5 and 10 s.
- No text. Audio: a silent AAC track, or --music (trimmed to length, 1.5 s fade-out).
"""
import os, subprocess, sys, tempfile

W, H, FPS, XF = 1080, 1920, 30, 0.4


def run(cmd):
    subprocess.run(cmd, check=True)


def durations(n):
    if n == 1:
        return 6.0
    per = max(2.5, (5.5 + (n - 1) * XF) / n)
    per = min(per, 3.0, (10.0 + (n - 1) * XF) / n)
    return round(per, 2)


def still(img, out):
    # 2x canvas so the zoom stays smooth; blurred cover background + contained foreground
    w2, h2 = W * 2, H * 2
    vf = (f"[0:v]split[a][b];"
          f"[a]scale={w2}:{h2}:force_original_aspect_ratio=increase,crop={w2}:{h2},gblur=sigma=60,eq=brightness=-0.06[bg];"
          f"[b]scale={w2}:{h2}:force_original_aspect_ratio=decrease[fg];"
          f"[bg][fg]overlay=(W-w)/2:(H-h)/2,format=yuv420p")
    run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-i", img, "-filter_complex", vf,
         "-frames:v", "1", "-q:v", "1", out])


def clip(png, dur, out):
    frames = int(round(dur * FPS))
    z = f"1+0.06*on/{frames}"
    vf = (f"zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s={W}x{H}:fps={FPS},"
          f"format=yuv420p,setsar=1")
    run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-i", png, "-vf", vf, "-frames:v", str(frames),
         "-c:v", "libx264", "-preset", "slow", "-crf", "14", "-pix_fmt", "yuv420p", out])


def main():
    args = sys.argv[1:]
    music = None
    if "--music" in args:
        i = args.index("--music"); music = args[i + 1]; del args[i:i + 2]
    out, imgs = args[0], args[1:]
    n = len(imgs)
    d = durations(n)
    total = d if n == 1 else n * d - (n - 1) * XF
    with tempfile.TemporaryDirectory() as t:
        clips = []
        for k, img in enumerate(imgs):
            png = os.path.join(t, f"s{k}.png"); still(img, png)
            c = os.path.join(t, f"c{k}.mp4"); clip(png, d, c); clips.append(c)
        cmd = ["ffmpeg", "-nostdin", "-loglevel", "error", "-y"]
        for c in clips:
            cmd += ["-i", c]
        if music:
            cmd += ["-i", music]
        else:
            cmd += ["-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100"]
        fc, last = [], "[0:v]"
        for k in range(1, n):
            off = round(k * (d - XF), 3)
            lab = f"[v{k}]"
            fc.append(f"{last}[{k}:v]xfade=transition=fade:duration={XF}:offset={off}{lab}")
            last = lab
        fc.append(f"{last}format=yuv420p[vout]")
        a = n
        if music:
            fc.append(f"[{a}:a]atrim=0:{total},afade=t=out:st={max(0, total - 1.5)}:d=1.5,"
                      f"aformat=sample_rates=44100:channel_layouts=stereo[aout]")
        else:
            fc.append(f"[{a}:a]atrim=0:{total}[aout]")
        cmd += ["-filter_complex", ";".join(fc), "-map", "[vout]", "-map", "[aout]",
                "-t", f"{total}", "-r", str(FPS), "-c:v", "libx264", "-preset", "slow", "-crf", "16",
                "-profile:v", "high", "-level", "4.1", "-pix_fmt", "yuv420p", "-maxrate", "12M",
                "-bufsize", "24M", "-g", "60", "-c:a", "aac", "-b:a", "128k", "-ar", "44100",
                "-movflags", "+faststart", out]
        run(cmd)
    print(f"{out}: {n} image(s), {total:.2f}s")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
QR Code Generator for AR/Video Phone Experience
------------------------------------------------
Generates a styled QR code that points to your GitHub Pages URL.
When scanned, the phone opens the AR/video experience directly in the browser
— no app install required.

Usage:
    python generate_qr.py                        # uses default URL from config
    python generate_qr.py --url https://your.url # custom URL
    python generate_qr.py --help                 # show all options
"""

import argparse
import sys
import os

# ─── CONFIG ──────────────────────────────────────────────────────────────────
# Edit these to match your GitHub Pages URL after you push the repo
GITHUB_USERNAME  = "mukesh725"
REPO_NAME        = "qr-ar-experience"
DEFAULT_URL      = f"https://{GITHUB_USERNAME}.github.io/{REPO_NAME}/"

OUTPUT_FILE      = "qr_code.png"
QR_SIZE          = 10          # box size in pixels (bigger = larger PNG)
QR_BORDER        = 4           # quiet zone modules
QR_ERROR_CORRECT = "H"         # H = 30% damage tolerance (best for printed QR)

# Colors — dark purple gradient feel (edit freely)
QR_FILL_COLOR    = "#1a0533"   # dark module color
QR_BACK_COLOR    = "#ffffff"   # background

# Optional: path to a logo PNG to embed in the center (leave "" to skip)
LOGO_PATH        = ""          # e.g. "media/logo.png"
LOGO_RATIO       = 0.25        # logo takes up 25% of QR width
# ─────────────────────────────────────────────────────────────────────────────


def validate_deps():
    """Check required libraries are installed."""
    missing = []
    try:
        import qrcode  # noqa: F401
    except ImportError:
        missing.append("qrcode[pil]")
    try:
        from PIL import Image  # noqa: F401
    except ImportError:
        missing.append("Pillow")

    if missing:
        print(f"[ERROR] Missing libraries: {', '.join(missing)}")
        print(f"        Run:  pip install {' '.join(missing)}")
        sys.exit(1)


def make_qr(url: str, output: str, logo: str | None = None):
    """Generate a high-quality QR code PNG."""
    import qrcode
    from PIL import Image, ImageDraw, ImageFont

    ec_map = {"L": qrcode.constants.ERROR_CORRECT_L,
              "M": qrcode.constants.ERROR_CORRECT_M,
              "Q": qrcode.constants.ERROR_CORRECT_Q,
              "H": qrcode.constants.ERROR_CORRECT_H}

    qr = qrcode.QRCode(
        version=None,                    # auto-size
        error_correction=ec_map[QR_ERROR_CORRECT],
        box_size=QR_SIZE,
        border=QR_BORDER,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color=QR_FILL_COLOR, back_color=QR_BACK_COLOR)
    img = img.convert("RGBA")

    # ── Embed logo in center (optional) ──────────────────────────────────────
    if logo and os.path.isfile(logo):
        logo_img = Image.open(logo).convert("RGBA")
        qr_w, qr_h = img.size
        logo_size  = int(qr_w * LOGO_RATIO)
        logo_img   = logo_img.resize((logo_size, logo_size), Image.LANCZOS)

        # White padding around logo
        pad     = 8
        padded  = Image.new("RGBA", (logo_size + pad * 2, logo_size + pad * 2), "white")
        padded.paste(logo_img, (pad, pad), logo_img)

        pos = ((qr_w  - padded.width)  // 2,
               (qr_h  - padded.height) // 2)
        img.paste(padded, pos, padded)
        print(f"[✓] Logo embedded from: {logo}")
    elif logo:
        print(f"[!] Logo not found at '{logo}' — skipping.")

    # ── Add caption below QR ─────────────────────────────────────────────────
    caption_height = 50
    canvas = Image.new("RGBA", (img.width, img.height + caption_height), "white")
    canvas.paste(img, (0, 0))

    draw = ImageDraw.Draw(canvas)
    caption = "Scan me · AR experience opens instantly"
    # Use default font (no external font required)
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 18)
    except Exception:
        font = ImageFont.load_default()

    bbox  = draw.textbbox((0, 0), caption, font=font)
    tw    = bbox[2] - bbox[0]
    tx    = (canvas.width - tw) // 2
    ty    = img.height + (caption_height - (bbox[3] - bbox[1])) // 2
    draw.text((tx, ty), caption, fill=QR_FILL_COLOR, font=font)

    canvas.save(output, "PNG", optimize=True)
    print(f"[✓] QR code saved → {output}")
    print(f"    Size: {canvas.width}×{canvas.height}px")
    print(f"    URL:  {url}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate a QR code for the AR phone experience.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--url",    default=DEFAULT_URL,  help="URL to encode in QR (default: GitHub Pages URL)")
    parser.add_argument("--output", default=OUTPUT_FILE,  help=f"Output PNG filename (default: {OUTPUT_FILE})")
    parser.add_argument("--logo",   default=LOGO_PATH,    help="Path to a logo PNG to embed in center")
    args = parser.parse_args()

    if "YOUR_GITHUB_USERNAME" in args.url:
        print("[!] Warning: URL still contains placeholder 'YOUR_GITHUB_USERNAME'.")
        print("    Edit GITHUB_USERNAME at the top of generate_qr.py, or pass --url.")
        print()

    validate_deps()
    make_qr(url=args.url, output=args.output, logo=args.logo or None)
    print()
    print("Next steps:")
    print("  1. Push this repo to GitHub")
    print("  2. Enable GitHub Pages (Settings → Pages → Deploy from branch: gh-pages)")
    print("  3. Re-run with your real URL to regenerate the final QR")


if __name__ == "__main__":
    main()

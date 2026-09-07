import argparse
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("Pillow is required. Install it with: pip install Pillow",
        file=sys.stderr)
    raise SystemExit(1)


def convert(input_file, output_file, width, height, keep_aspect=False):
    if width <= 0 or height <= 0:
        raise ValueError("width and height must be positive")

    src = Path(input_file)
    if not src.is_file():
        raise FileNotFoundError(f"Input image not found: {src}")

    image = Image.open(src).convert("RGB")

    if keep_aspect:
        target_ratio = width / height
        source_ratio = image.width / image.height

        if source_ratio > target_ratio:
            new_width = round(image.height * target_ratio)
            left = (image.width - new_width) // 2
            image = image.crop((left, 0, left + new_width, image.height))
        elif source_ratio < target_ratio:
            new_height = round(image.width / target_ratio)
            top = (image.height - new_height) // 2
            image = image.crop((0, top, image.width, top + new_height))

    image = image.resize((width, height), Image.Resampling.LANCZOS)

    out = Path(output_file)
    with out.open("w", encoding="ascii", newline="\n") as f:
        f.write("v2.0 raw\n")

        for y in range(height):
            words = []
            for x in range(width):
                r, g, b = image.getpixel((x, y))
                rgb = (r << 16) | (g << 8) | b
                words.append(f"{rgb:08x}")
            f.write(" ".join(words) + "\n")

    return src, out, image.size


def main():
    parser = argparse.ArgumentParser(
        description="Convert an image to a Logisim Evolution v2.0 raw RAM file."
    )
    parser.add_argument("input", help="Input image (PNG, JPG, BMP, GIF, etc.)")
    parser.add_argument("output", help="Output RAM file, e.g. image.hex")
    parser.add_argument("--width", type=int, default=1920,
                        help="Output width (default: 1920)")
    parser.add_argument("--height", type=int, default=1080,
                        help="Output height (default: 1080)")
    parser.add_argument(
        "--keep-aspect", action="store_true",
        help="Center-crop instead of stretching the image to the target ratio."
    )
    args = parser.parse_args()

    try:
        src, out, size = convert(
            args.input, args.output, args.width, args.height, args.keep_aspect
        )
        pixels = size[0] * size[1]
        print("Conversion successful.")
        print(f"Input:        {src}")
        print(f"Output:       {out}")
        print(f"Resolution:   {size[0]} x {size[1]}")
        print(f"Pixels:       {pixels:,}")
        print("RAM word:     32-bit")
        print("Pixel format: 0x00RRGGBB")
    except (OSError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()

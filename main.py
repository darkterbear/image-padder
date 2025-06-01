import argparse
import os
from datetime import datetime
from PIL import Image, ImageOps, ImageDraw, ImageFont

COLOR_MAP = {
  "white": (255, 255, 255),
  "black": (0, 0, 0),
}

def parse_ratio_str(ratio_str: str):
  [aspect_ratio_width, aspect_ratio_height] = ratio_str.split(":")
  return float(aspect_ratio_width), float(aspect_ratio_height)

def compute_padded_size(old_size, aspect_ratio_width, aspect_ratio_height, padding):
  width = int(max(old_size[1] / aspect_ratio_height * aspect_ratio_width, old_size[0]))
  height = int(max(old_size[0] / aspect_ratio_width * aspect_ratio_height, old_size[1]))

  width /= (1-padding)
  height /= (1-padding)
  return int(width), int(height)

def scale_image(im, short_side=2048):
  if im.width < im.height:
    # Width is the shortest side
    new_width = short_side
    new_height = int(im.height * (new_width / im.width))
  else:
    # Height is the shortest side
    new_height = short_side
    new_width = int(im.width * (new_height / im.height))

  return im.resize((new_width, new_height))

def get_output_filepath(input_filepath: str, aspect_ratio_width, aspect_ratio_height):
  filename, ext = os.path.splitext(input_filepath)
  return f"{filename}-{aspect_ratio_width}x{aspect_ratio_height}-{datetime.now().strftime('%Y%m%d%H%M%S')}{ext}"

def main(args):
  aspect_ratio_width, aspect_ratio_height = parse_ratio_str(args.ratio)
  
  im = Image.open(args.path)
  
  # Image .size's are in (width, height) format
  old_size = im.size
  new_size = compute_padded_size(old_size, aspect_ratio_width, aspect_ratio_height, args.padding)
  
  # Create a new image and paste the resized on it
  new_im = Image.new("RGB", new_size, COLOR_MAP[args.color])
  new_im.paste(im, ((new_size[0] - old_size[0]) // 2,
                    (new_size[1] - old_size[1]) // 2))

  # Scale to standard size.
  new_im = scale_image(new_im, short_side=2048)

  # Add caption, if applicable
  if args.caption:
    draw = ImageDraw.Draw(new_im)
    font = ImageFont.truetype("/mnt/c/Windows/Fonts/Bahnschrift.ttf", 48)
    draw.text((new_im.width // 2, new_im.height - 100), args.caption, fill="#888888", font=font, anchor="mm")

  new_im.save(get_output_filepath(args.path, aspect_ratio_width, aspect_ratio_height))


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('path', help='Path to the image file. Only JPGs are supported.')
  parser.add_argument('--ratio', required=False, default="1:1", help='Aspect ratio, in "width:height" format, e.g. "16:9".')
  parser.add_argument('--color', required=False, default="white", help='Color to pad with. "white" (default) or "black".')
  parser.add_argument('--padding', required=False, default=0.0, type=float, help='Proportion of padding to image for the output image, e.g. 0.15')
  parser.add_argument('--caption', required=False, default="", type=str, help='Text caption')
  args = parser.parse_args()
  main(args)

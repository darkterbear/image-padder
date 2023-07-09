import argparse
import os
from datetime import datetime
from PIL import Image, ImageOps

COLOR_MAP = {
  "white": (255, 255, 255),
  "black": (0, 0, 0),
}

def parse_ratio_str(ratio_str: str):
  [aspect_ratio_width, aspect_ratio_height] = ratio_str.split(":")
  return float(aspect_ratio_width), float(aspect_ratio_height)

def compute_padded_size(old_size, aspect_ratio_width, aspect_ratio_height):
  width = int(max(old_size[1] / aspect_ratio_height * aspect_ratio_width, old_size[0]))
  height = int(max(old_size[0] / aspect_ratio_width * aspect_ratio_height, old_size[1]))
  return width, height

def get_output_filepath(input_filepath: str, aspect_ratio_width, aspect_ratio_height):
  filename, ext = os.path.splitext(input_filepath)
  return f"{filename}-{aspect_ratio_width}x{aspect_ratio_height}-{datetime.now().strftime('%Y%m%d%H%M%S')}{ext}"

def main(args):
  aspect_ratio_width, aspect_ratio_height = parse_ratio_str(args.ratio)
  
  im = Image.open(args.path)
  
  # Image .size's are in (width, height) format
  old_size = im.size
  new_size = compute_padded_size(old_size, aspect_ratio_width, aspect_ratio_height)
  
  # create a new image and paste the resized on it
  new_im = Image.new("RGB", new_size, COLOR_MAP[args.color])
  new_im.paste(im, ((new_size[0] - old_size[0]) // 2,
                    (new_size[1] - old_size[1]) // 2))

  new_im.save(get_output_filepath(args.path, aspect_ratio_width, aspect_ratio_height))


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('path', help='Path to the image file. Only JPGs are supported.')
  parser.add_argument('ratio', help='Aspect ratio, in "width:height" format, e.g. "16:9".')
  parser.add_argument('--color', required=False, default="white", help='Color to pad with. "white" (default) or "black".')
  args = parser.parse_args()
  main(args)
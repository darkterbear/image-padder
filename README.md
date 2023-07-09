# image-padder

Lightweight Python utilities to pad images to aspect ratios

## Prerequisites

- Python 3.8.10+
- PIL (`pip3 install Pillow`)

## Usage

```
python3 main.py image_path aspect_ratio [--color white|black]
```

- `image_path`: path to the image file
- `aspect_ratio`: the desired aspect ratio in "width:height" format; e.g. "4:3"
- `color`: the desired padding color; only "white" (default) and "black" are currently supported

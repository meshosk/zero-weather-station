# zero-weather-station

Warn: Code generted wtih use of copilot (yeah, i'm lazy to do basic stuff...)


# How to docker
Project consist of multiple parts that plyat together.

```
docker run --rm -it -v ${PWD}:/mnt/app  -w "/mnt/app/" python:latest bash
```

# Setup
To install&setup all parts run `install.sh` script first. This will create virtaual python eviroment. Make sure that submodules were downloaded in `external` folder. Ther should be these ones:
- [IT8951](https://github.com/GregDMeyer/IT8951)
- [weather-icon](https://github.com/meshosk/weather-icons)
- [nameday-api](https://github.com/xnekv03/nameday-api)

```
bash install.sh
```

# Waveshare 7.8" HD e-ink make-it-run steps for zero 2W
This should work on other devices too.

1. enable SPI in `sudo raspi-config` no other addition to `/boot/config.txt`
2. Download as local module `https://github.com/GregDMeyer/IT8951` and run setup
3. check if all libraries in python has needed version and install other needed libraries
4. set vcom value. for 7.8" HD is value -1.56 (-1.80 works better)
5. try running following test script until it runs (tested and it runs on bulleye lite)
6. script with SPI may need authorization to ise SPI, so run it with _sudo_ or add SPI group

```python
from IT8951.interface import EPD
from IT8951.display import AutoEPDDisplay
from IT8951 import constants

import numpy as np
from PIL import Image, ImageDraw

# Nastavenie rozlíšenia pre 7.8": 1872 × 1404
# WIDTH = 1872
# HEIGHT = 1404 

display = AutoEPDDisplay(vcom=-1.56, spi_hz=24000000) 

img_path = '<PUT HERE ANY IMAGE to show on display>'
print('Displaying "{}"...'.format(img_path))

# clearing image to white
display.frame_buf.paste(0xFF, box=(0, 0, display.width, display.height))

img = Image.open(img_path)

# TODO: this should be built-in
dims = (display.width, display.height)

img.thumbnail(dims)
paste_coords = [dims[i] - img.size[i] for i in (0,1)]  # align image with bottom of display
display.frame_buf.paste(img, paste_coords)

display.draw_full(constants.DisplayModes.GC16)
```
# How to run it?

Just run `fetch-weather.py` (get weather data before first creen render) and `render-screen.py` with env in cron every minute or so like this:

```
*/30 * * * * cd /home/THE-USER/zero-weather-station &&  .venv/bin/python fetch-weather.py
* * * * * cd /home/THE-USER/zero-weather-station &&  .venv/bin/python render-screen.py
0 0 * * * cd /home/THE-USER/zero-weather-station &&  .venv/bin/python reset_epaper.py
```




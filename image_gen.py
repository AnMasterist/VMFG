from PIL import Image
import configparser
cfg = configparser.ConfigParser()
cfg.read("config_vmfg.cfg")
img = Image.new("RGB", (int(32768/float(cfg["CONFIG_VAR"]['chunk_max'])), int(32768/float(cfg["CONFIG_VAR"]['chunk_max']))), (255, 255, 255))
img.save("image/map_example.png", "PNG")
img.close()
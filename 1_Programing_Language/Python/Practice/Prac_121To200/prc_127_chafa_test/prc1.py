import chafa
from chafa.loader import Loader

# Load the image
image = Loader("./image.jpg")

print(image.width, image.height)
print(image.rowstride)
print(image.pixel_type)

# Create config
config = chafa.CanvasConfig()

# config.height = image.height
# config.width  = image.width
config.height = 100
config.width  = 100

# Create canvas
canvas = chafa.Canvas(config)


# Draw to the canvas
canvas.draw_all_pixels(
    image.pixel_type,
    image.get_pixels(),
    image.width, image.height,
    image.rowstride
)

# print output
output = canvas.print().decode()

print(output)
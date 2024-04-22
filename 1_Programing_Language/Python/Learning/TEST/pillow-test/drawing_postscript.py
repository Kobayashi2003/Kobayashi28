# Drawing PostScript
from PIL import Image
from PIL import PSDraw

im = Image.open("./image.jpg")
title = "image"
box = (1*72, 2*72, 7*72, 10*72) # in points

ps = PSDraw.PSDraw() # default is sys.stdout
ps.begin_document(title)

# draw the image (75 dpi)
ps.image(box, im, 75)
ps.rectangle(box)

# draw centered title
ps.setfont("HelveticaNarrow-Bold", 36)
ps.text((4*72, 4*72), title)

ps.end_document()

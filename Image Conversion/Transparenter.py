#Source
#https://www.geeksforgeeks.org/create-transparent-png-image-with-python-pillow/

from PIL import Image
  
img = Image.open('images/fun/g_a.png')
rgba = img.convert("RGBA")
datas = rgba.getdata()
  
newData = []
for item in datas:
    if item[0] == 255 and item[1] == 255 and item[2] == 255:  # finding yellow colour
        # replacing it with a transparent value
        newData.append((255, 255, 255, 0))
    else:
        newData.append(item)
  
rgba.putdata(newData)
rgba.save("transparent_image.png", "PNG")
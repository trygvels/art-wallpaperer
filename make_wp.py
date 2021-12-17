import os
from PIL import Image, ImageDraw, ImageFont
import math
def resize_canvas(im_old_path, w_new=2880, h_new=1800,):
    """
    Resize the canvas of old_image_path.

    Store the new image in new_image_path. Center the image on the new canvas.

    Parameters
    ----------
    old_image_path : str
    new_image_path : str
    canvas_width : int
    canvas_height : int
    """
    fname, ftype = im_old_path.rsplit(".",1)
    print(fname.encode("utf-8"))
    
    im = Image.open(im_old_path)
    w_old, h_old = im.size

    scaling = math.sqrt((w_new*h_new)/(5.0*w_old*h_old)) # Scaling so image takes 1/2 of area
    w_old = int(w_old*scaling)
    h_old = int(h_old*scaling)
    im_ = im.resize((w_old, h_old))
    # Center the image
    x1 = int(math.floor((w_new - w_old) / 2))
    y1 = int(math.floor((h_new - h_old) / 2))
    
    mode = im.mode
    if len(mode) == 1:  # L, 1
        bg_new = (255)
    if len(mode) == 3:  # RGB
        bg_new = (255, 255, 255)
    if len(mode) == 4:  # RGBA, CMYK
        bg_new = (255, 255, 255, 255)

    im_new = Image.new(mode, (w_new, h_new), bg_new)
    im_new.paste(im_, (x1, y1, x1 + w_old, y1 + h_old))
    draw = ImageDraw.Draw(im_new)
    font = ImageFont.truetype("~/Library/Fonts/Supplemental/Arial.ttf", 20)
    artist, title = fname.split(" - ", 1)
    w_text, h_text = draw.textsize(title, font)
    w_text2, h_text2 = draw.textsize(artist, font)
    if h_text2>h_text:
        h_text = h_text2
    draw.text( ((w_new-w_text)//2, h_old//2 + h_new//2 + h_text), title, fill=(0,0,0), font=font)
    draw.text( ((w_new-w_text2)//2, h_old//2 + h_new//2 + 2*h_text) , artist, fill=(0,0,0), font=font)
    im_new.save(fname+"_formatted."+ftype)

#if not os.path.exists('formatted'):
#    os.makedirs('formatted')
    
for fname in os.listdir('.'):
    if fname.endswith('.jpg') or fname.endswith('.jpeg'):
        if fname.endswith('_formatted.jpg'):
            continue
        #print(fname)
        try:
            resize_canvas(fname)
        except ValueError as err:
            print(err)
        

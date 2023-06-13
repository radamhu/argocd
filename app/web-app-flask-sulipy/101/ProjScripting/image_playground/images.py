from PIL import Image, ImageFilter

img = Image.open('Pokedex/pikachu.jpg')
filter_img = img.filter(ImageFilter.BLUR)
filter_img.save("blur.png", 'png')
filter_img.show(img)

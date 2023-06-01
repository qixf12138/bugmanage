#from captcha.image import ImageCaptcha
import random, string


def create_random_str(str_len=8):
    chr_all = string.ascii_letters + string.digits
    random_str = ''.join(random.sample(chr_all, 8))
    return random_str
# def create_vcode_img():
#     chr_all = string.ascii_letters + string.digits
#     chr_4 = ''.join(random.sample(chr_all, 4))
#     image = ImageCaptcha().generate_image(chr_4)
#     return image,chr_4
# image.save('./%s.jpg' % chr_4)

print(create_random_str())




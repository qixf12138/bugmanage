import random, string

from captcha.image import ImageCaptcha


# 创建随机字符串
def create_random_str(str_len=8):
    chr_all = string.ascii_letters + string.digits
    random_str = ''.join(random.sample(chr_all, str_len))
    return random_str


# 创建随机图片验证码和验证码字符串
def create_vcode_img():
    chr_4 = create_random_str(4)
    image = ImageCaptcha().generate_image(chr_4)
    return image, chr_4
    #image.save('./%s.jpg' % chr_4)




from PIL import Image

def img2ico(filename):
    if not filename.endswith('.png'):
        raise ValueError('filename must be a PNG image')
    try:
        with Image.open(filename) as im:
            im.save(filename.replace('.png', '.ico'))
    except:
        raise ValueError('Wrong image path')

if __name__ == '__main__':
    img_path = 'D:\\MISC\\WallPaper\\test.png'
    img2ico(img_path)
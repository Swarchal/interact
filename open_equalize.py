from skimage import io
from skimage import exposure
from skimage import img_as_ubyte

def open_equalize(url, **kwargs):
    """ open an image, equalize and transform to 8 bit """
    return exposure.equalize_adapthist(img_as_ubyte(io.imread(url)), **kwargs)

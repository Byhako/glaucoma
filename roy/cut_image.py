import matplotlib.pyplot as plt
from skimage.transform import resize
from skimage.measure import label, regionprops
from mnet_utils import BW_img, disc_crop
import model_discSeg as DiscModel
from PIL import Image
import numpy as np
import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

def procesar_imagen(
    ruta_imagen,
    discROI_size=200,
):
    """
    Leo una imagen, la recoto en un tamaño
    factor*128, la redimensiono a 512x512, encuento el disco en la imagen
    y la retorno en un tamaño de 200x200.
    """

    # 1. Cargar la imagen original como array NumPy
    img = Image.open(ruta_imagen)
    ancho, alto = img.size
    size_image = 512


    if ancho != 512 and alto != 512:
        # # Redimensiona la imagen a 512x512 píxeles
        min_size = min(ancho, alto)
        factor = min_size // 128

        size_image = factor * 128

        img, _, _ = disc_crop(np.asarray(img), size_image, ancho//2, alto//2)

        size_image = 512
        tamaño_nuevo = (size_image, size_image)
        img = Image.fromarray(img.astype(np.uint8))
        img = img.resize(tamaño_nuevo, Image.LANCZOS)

    org_img = np.asarray(img)  # (H, W, 3)

    # 2. Cargar el modelo de segmentación del disco
    model_disSeg_path = 'Model_DiscSeg_pretrain.h5'

    discSeg_model = DiscModel.DeepModel(size_set=size_image)
    discSeg_model.load_weights(model_disSeg_path)

    # 3. Redimensionar la imagen a size_image
    temp_org_img = resize(org_img, (size_image, size_image, 3))
    temp_org_img = np.reshape(temp_org_img, (1, size_image, size_image, 3)) * 255.0

    prob_10 = discSeg_model.predict(temp_org_img)  # (1,640,640) o (1,640,640,1)
    disc_map = np.reshape(prob_10, (size_image, size_image))
    # Binarizar la salida (disco vs no-disco)
    org_img_disc_map = BW_img(disc_map, 0.5)

    # Encontrar la región del disco y su centroide
    regions = regionprops(label(org_img_disc_map))
    if len(regions) == 0:
        print("No se detectó el disco en la imagen.")
        return None

    # Centroid en la imagen de 640 px
    cx, cy = regions[0].centroid  # (fila, columna)

    # 4. Recortar la imagen original en (cx, cy)
    org_img_disc_region, _, _ = disc_crop(org_img, discROI_size, cx, cy, size_image)

    if org_img_disc_region is None:
        return None

    org_img_disc_region_pil = Image.fromarray(org_img_disc_region.astype(np.uint8))

    return org_img_disc_region_pil

if __name__ == '__main__':
    ruta_imagen = '..\\..\\archive\\ORIGA\\Images\\001.jpg'
    image = procesar_imagen(ruta_imagen)

    plt.imshow(image)
    plt.axis('off')
    plt.show()

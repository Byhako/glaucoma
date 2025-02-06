import os
import cv2
import numpy as np
from skimage.morphology import binary_erosion
from keras.preprocessing import image
from skimage.transform import rotate, resize
from skimage.measure import label, regionprops
from mnet_utils import  BW_img, disc_crop
import model_discSeg as DiscModel
from PIL import Image


def procesar_imagen_sin_mascara(
    ruta_imagen,
    DiscSeg_model_path='Model_DiscSeg_pretrain.h5',
    DiscROI_size=400,
    DiscSeg_size=640,

):
    """
    Procesa UNA sola imagen para:
      - Segmentar automáticamente el disco óptico con el modelo U-Net (sin usar ruta_mascara).
      - Encontrar el centro del disco en la imagen.
      - Recortar un ROI (p.ej. 400x400) centrado en el disco en la imagen original.
      - Retornar el ROI como PIL.Image (para que luego el usuario dibuje a mano copa/disco en la interfaz).

    Retorna:
      org_img_disc_region_pil: Imagen recortada (PIL) alrededor del disco
      C_x, C_y: Coordenadas del centro del disco (por si se necesitan)
    """
    # 1) Cargar el modelo
    DiscSeg_model = DiscModel.DeepModel(size_set=DiscSeg_size)
    DiscSeg_model.load_weights(DiscSeg_model_path)

    # Cargar la imagen
    org_img = np.asarray(image.load_img(ruta_imagen))
    H, W = org_img.shape[0], org_img.shape[1]

    # Segmentar para localizar disco y recortar
    temp_org_img = resize(org_img, (DiscSeg_size, DiscSeg_size, 3)) * 255
    temp_org_img = np.reshape(temp_org_img, (1, DiscSeg_size, DiscSeg_size, 3))

    prob_10 = DiscSeg_model.predict(temp_org_img)
    disc_map = np.reshape(prob_10, (DiscSeg_size, DiscSeg_size))
    disc_map_bw = BW_img(disc_map, 0.5)

    # Hallar la región disco y su centroide
    regions = regionprops(label(disc_map_bw))
    if len(regions) == 0:
        print("No se detectó el disco en la imagen.")
        return None, None, None, 0.0, 0.0

    cx_640, cy_640 = regions[0].centroid # (fila, columna) en 640x640
    # Escalar a (H,W) original
    C_x = int(cx_640 * H / DiscSeg_size)
    C_y = int(cy_640 * W / DiscSeg_size)

    # Recortar el ROI en org_img
    org_img_disc_region, _, _ = disc_crop(org_img, DiscROI_size, C_x, C_y)

    # 5) Convertir a PIL la ROI
    org_img_disc_region_pil = Image.fromarray(org_img_disc_region.astype(np.uint8))
    org_copy = Image.fromarray((org_img_disc_region * 255) .astype(np.uint8))

    # Por ahora no hay copa ni disco binario. Retornamos None o lo que necesitemos.
    # Ratios a 0, pues no tenemos nada.
    return org_img_disc_region_pil, C_x, C_y, org_copy

def procesar_imagen(
    ruta_imagen,
    ruta_mascara=None,
    DiscSeg_model_path='Model_DiscSeg_pretrain.h5',
    DiscROI_size=400,
    DiscSeg_size=640,
    is_polar_coordinate=False
):
    """
    Procesa UNA sola imagen (y su máscara, si existe) para:
      - Segmentar el disco óptico con un modelo U-Net (cargado desde DiscSeg_model_path).
      - Encontrar el centro del disco óptico.
      - Recortar un ROI (por defecto 400x400) centrado en el disco de la imagen original.
      - Si existe máscara, recorta también la parte del disco y de la copa.

    Parámetros
    ----------
    ruta_imagen : str
        Ruta de la imagen original (por ejemplo, 'C:/.../imagen.jpg').
    ruta_mascara : str, opcional
        Ruta de la máscara correspondiente (por ejemplo, 'C:/.../mascara.png').
        Se asume que la máscara codifica:
          - Disco donde `pixel < 255`
          - Copa donde `pixel == 0`
          - Fondo donde `pixel == 255`
        Si no se proporciona o no existe, se devuelven `None` en las máscaras recortadas.
    DiscSeg_model_path : str
        Ruta del archivo .h5 con los pesos del modelo de segmentación de disco.
    DiscROI_size : int
        Tamaño del recorte a realizar alrededor del centro del disco (por defecto 400).
    DiscSeg_size : int
        Tamaño al que se redimensiona la imagen antes de pasarla al modelo (640 por defecto).
    is_polar_coordinate : bool
        Si True, aplica la transformación a coordenadas polares sobre el recorte (opcional).

    Retorna
    -------
    (PIL.Image, PIL.Image, PIL.Image)
        org_img_disc_region, org_mask_disc_region, org_cup_region

        - org_img_disc_region : Recorte de la imagen original (RGB) alrededor del disco.
        - org_mask_disc_region : Recorte de la máscara del disco óptico (binaria), si hay máscara.
        - org_cup_region : Recorte de la máscara de la copa (binaria), si hay máscara.

        Si no hay ruta_mascara, se retorna (img, None, None).
    """

    # -------------------------------------------------
    # 1. Cargar el modelo de segmentación del disco
    # ------------------------------------------------
    DiscSeg_model = DiscModel.DeepModel(size_set=DiscSeg_size)
    DiscSeg_model.load_weights(DiscSeg_model_path)

    # ------------------------------------------------
    # 2. Cargar la imagen original como array NumPy
    # ------------------------------------------------
    org_img = np.asarray(image.load_img(ruta_imagen))  # (H, W, 3)
    H, W = org_img.shape[0], org_img.shape[1]

    # ------------------------------------------------
    # 3. Redimensionar la imagen a DiscSeg_size y predecir
    # ------------------------------------------------
    temp_org_img = resize(org_img, (DiscSeg_size, DiscSeg_size, 3))
    temp_org_img = np.reshape(temp_org_img, (1, DiscSeg_size, DiscSeg_size, 3)) * 255.0
    prob_10 = DiscSeg_model.predict(temp_org_img)  # (1,640,640) o (1,640,640,1)
    disc_map = np.reshape(prob_10, (DiscSeg_size, DiscSeg_size))

    # binarizar la salida (disco vs no-disco)
    org_img_disc_map = BW_img(disc_map, 0.5)

    # Encontrar la región del disco y su centroide
    regions = regionprops(label(org_img_disc_map))
    if len(regions) == 0:
        print("No se detectó el disco en la imagen.")
        return None, None, None

    # Centroid en la imagen de 640 px
    cx_640, cy_640 = regions[0].centroid  # (fila, columna)
    # Escalar a (H,W) original
    C_x = int(cx_640 * H / DiscSeg_size)
    C_y = int(cy_640 * W / DiscSeg_size)

    # ------------------------------------------------
    # 4. Recortar la imagen original en (C_x, C_y)
    # ------------------------------------------------
    org_img_disc_region, _, _ = disc_crop(org_img, DiscROI_size, C_x, C_y)

    # Convertir a PIL
    org_img_disc_region_pil = Image.fromarray(org_img_disc_region.astype(np.uint8))

    # ------------------------------------------------
    # 5. Manejo de la máscara (si ruta_mascara existe)
    # ------------------------------------------------
    org_mask_disc_region_pil = None
    org_cup_region_pil = None

    if ruta_mascara and os.path.exists(ruta_mascara):
        # 5.a Cargar la máscara como array
        org_mask = np.asarray(image.load_img(ruta_mascara))
        # Si es RGB, tomar un canal
        if len(org_mask.shape) == 3:
            org_mask = org_mask[:, :, 0]

        # 5.b Definir disco y copa  criterio
        org_disc = (org_mask < 255)  # True/False
        org_cup  = (org_mask == 0)

        # 6.c Recortar dichas máscaras booleanas
        org_disc_region, _, _ = disc_crop(org_disc, DiscROI_size, C_x, C_y)
        org_cup_region, _, _ = disc_crop(org_cup, DiscROI_size, C_x, C_y)

        # Si is_polar_coordinate -> aplica la misma lógica polar
        if is_polar_coordinate:
            org_mask_disc_region = rotate(
                cv2.linearPolar(
                    org_disc_region.astype(np.uint8)*255,
                    (DiscROI_size / 2, DiscROI_size / 2),
                    DiscROI_size / 2,
                    cv2.INTER_NEAREST + cv2.WARP_FILL_OUTLIERS
                ), -90
            )
            org_cup_region = rotate(
                cv2.linearPolar(
                    org_cup_region.astype(np.uint8)*255,
                    (DiscROI_size / 2, DiscROI_size / 2),
                    DiscROI_size / 2,
                    cv2.INTER_NEAREST + cv2.WARP_FILL_OUTLIERS
                ), -90
            )
            # Convertir a booleano de nuevo (opcional)
            org_disc_region = org_disc_region < 128
            org_cup_region = org_cup_region < 128

        # Convertir a PIL (0 o 1 mapeado a 0..255)
        org_disc_region_pil = Image.fromarray((org_disc_region*255).astype(np.uint8))
        org_cup_region_pil = Image.fromarray((org_cup_region*255).astype(np.uint8))

    # ----------------------------------------------------------------------------
    # 7. Mascara total y Contorno
    # ------------------------------------------------------------------------------------

    disc_bw = org_disc_region.astype(np.uint8)  # 0..1
    cup_bw = org_cup_region.astype(np.uint8)
    combo = disc_bw + 2 * cup_bw


    combined_mask = np.full(disc_bw.shape, 255, dtype=np.uint8)  # fondo blanco
    combined_mask[disc_bw == 1] = 128  # disco gris
    combined_mask[cup_bw == 1] = 0  # copa negra

    combined_mask_pil = Image.fromarray(combined_mask)

    # Disco binario: 1 donde ==128, 0 en resto
    disc_bw = (combined_mask == 128)
    # Copa binario: 1 donde ==0, 0 en resto
    cup_bw = (combined_mask == 0)

    # Borde = original AND NOT(erosion)
    disc_edge = disc_bw & ~binary_erosion(disc_bw)
    cup_edge = cup_bw & ~binary_erosion(cup_bw)

    # Pintar contornos en copia del ROI
    roi_contour = org_img_disc_region.copy()
    roi_contour[disc_edge] = [0, 255, 0]  # verde
    roi_contour[cup_edge] = [255, 0, 0]  # rojo

    # ---------------------------------------------------------------------
    # relación CDR Valor.
    # ---------------------------------------------------------------------

    # area (en píxeles) es la suma de True en cada máscara
    disc_area = np.sum(disc_bw)  # número de píxeles True
    cup_area = np.sum(cup_bw)

    cup_to_disc_ratio = cup_area / disc_area
    print("C/D ratio (área) =", cup_to_disc_ratio)

    # la relación de diámetros (vertical/horizontal)

    # Disco
    lbl_disc = label(disc_bw)
    props_disc = regionprops(lbl_disc)
    props_disc[0].bbox  # => (min_row, min_col, max_row, max_col)
    props_disc[0].major_axis_length # > si la región se asume elipsoidal

    # Copa
    lbl_cup = label(cup_bw)
    props_cup = regionprops(lbl_cup)

    disc_diam_vert = props_disc[0].bbox[2] - props_disc[0].bbox[0]  # max_row - min_row
    cup_diam_vert = props_cup[0].bbox[2] - props_cup[0].bbox[0]

    cd_ratio_vert = cup_diam_vert / disc_diam_vert
    print("C/D vertical =", cd_ratio_vert)

    # formato PIL para enviar
    org_contorn_region_pil = Image.fromarray(roi_contour)  # * 255) # .astype(np.uint8))

    # ------------------------------------------------
    # 9. Retornar las tres imágenes en tipo PIL
    # ------------------------------------------------
    # org_mask_disc_region_pil
    return org_img_disc_region_pil, combined_mask_pil, org_contorn_region_pil, cup_to_disc_ratio, cd_ratio_vert
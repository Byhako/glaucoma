from cut_image import procesar_imagen
import matplotlib.pyplot as plt
import os

folder_name = 'E:\\Documentos\\bodega\\archive\\G1\\square'
folder_target = 'E:\\Documentos\\bodega\\archive\\G1\\cropped'

test_positive = os.listdir(f'{folder_name}\\Test\\positive')
test_negative = os.listdir(f'{folder_name}\\Test\\negative')
train_positive = os.listdir(f'{folder_name}\\Train\\positive')
train_negative = os.listdir(f'{folder_name}\\Train\\negative')

# print('\n===> Test positive')
# for name in test_positive:
#     print(name)
#     ruta_imagen = f'{folder_name}\\Test\\positive\\{name}'
#     imagen = procesar_imagen(ruta_imagen)

#     if imagen != None:
#         plt.imshow(imagen)
#         plt.axis('off')  # Ocultar los ejes
#         plt.savefig(f'{folder_target}\\Test\\positive\\{name}', bbox_inches='tight', pad_inches=0)

print('\n===> Test negative')
for name in test_negative:
    print(name)
    ruta_imagen = f'{folder_name}\\Test\\negative\\{name}'
    imagen = procesar_imagen(ruta_imagen)

    if imagen != None:
        plt.imshow(imagen)
        plt.axis('off')  # Ocultar los ejes
        plt.savefig(f'{folder_target}\\Test\\negative\\{name}', bbox_inches='tight', pad_inches=0)



print('\n===> Train positive')
for name in train_positive:
    print(name)
    ruta_imagen = f'{folder_name}\\Train\\positive\\{name}'
    imagen = procesar_imagen(ruta_imagen)

    if imagen != None:
        plt.imshow(imagen)
        plt.axis('off')  # Ocultar los ejes
        plt.savefig(f'{folder_target}\\Train\\positive\\{name}', bbox_inches='tight', pad_inches=0)


print('\n===> Train negative')
for name in train_negative:
    print(name)
    ruta_imagen = f'{folder_name}\\Train\\negative\\{name}'
    imagen = procesar_imagen(ruta_imagen)

    if imagen != None:
        plt.imshow(imagen)
        plt.axis('off')  # Ocultar los ejes
        plt.savefig(f'{folder_target}\\Train\\negative\\{name}', bbox_inches='tight', pad_inches=0)


print('end')
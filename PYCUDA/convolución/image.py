import numpy as np
import matplotlib.image as img
import matplotlib.pyplot as plt
import os

from PIL import Image
'''definición de la funcion para la apertura de la imagen 
en el folder de origen  '''
def load_image(filename):
    base_dir = os.getcwd()
    folder_images = 'images'
    path = os.path.join(base_dir, folder_images)
    if not (os.path.exists(path)):
        os.mkdir(path)
    image_path = os.path.join(path, filename)
    return Image.open(image_path)

'''definición de la funcion para la converción de la imagen 
de array a tipo vector para realizar el procesamineto '''
def array2vector(image):
    height, width= image.shape
    image_array_list = []

    for row in range(height):
        for column in range(width):
            image_array_list.append(image[row][column])

    return np.array(image_array_list)

'''definición de la funcion para la converción de la imagen 
de array a tipo vector para realizar el resṕectivo procesamineto '''
def array2image(image_array):
    image = Image.fromarray(image_array)
    return image.convert('RGB')



'''definición de la funcion para almacenar a imagen procesada en el folder destino '''

def save_image(image, filename):
    base_dir = os.getcwd()
    folder_images = 'images'
    path = os.path.join(base_dir, folder_images)
    if not (os.path.exists(path)):
        os.mkdir(path)
    image_path = os.path.join(path, filename)
    image.save(image_path)
import numpy as np

from image import array2image,load_image, array2vector,save_image
from gray2bin import gray2bin
import matplotlib.image as img
import matplotlib.pyplot as plt


def main():
    input_name = 'shingeki_gray.jpeg'
    output_name = 'shingeki_bin.jpeg'

    input_image = load_image(input_name)
    image = np.array(
        input_image.getdata()).reshape(input_image.size[1], input_image.size[0], 3
    )

    print(image.shape)

    image_gray=image[:,:,0]
    
    print(image_gray.shape)
    
    image_vector = array2vector(image_gray)

    height, width = image_gray.shape

  
    threshold=150

    output_image_array = gray2bin(image_vector, height, width,threshold)
    
    output_image = array2image(output_image_array)

    print(output_image, input_image)
    save_image(output_image, output_name)

    plt.imshow(output_image_array,cmap='gray')
    plt.show()
    


if __name__=='__main__':
    main()
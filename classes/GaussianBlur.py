# Размытие картинки по Гауссу

import pygame
from scipy.ndimage.filters import *


class GaussianBlur:
    def __init__(self, kernelsize=7):
        self.kernel_size = kernelsize

# # Метод применения фильтра Гаусса к изображению
    def filter(self, srfc, xpos, ypos, width, height):
        nSrfc = pygame.Surface((width, height)) # Создание новой поверхности с заданными размерами
        pxa = pygame.surfarray.array3d(srfc) # Преобразование поверхности в трехмерный массив пикселей
        blurred = gaussian_filter(pxa, sigma=(self.kernel_size, self.kernel_size, 0)) # Применение фильтра Гаусса к массиву пикселей
        pygame.surfarray.blit_array(nSrfc, blurred) # Копирование отфильтрованного массива пикселей на новую поверхность
        del pxa # Очистка массива пикселей
        return nSrfc # Возврат отфильтрованной поверхности

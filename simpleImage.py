import numpy as np
from PIL import Image
from PyInquirer import prompt
from utils import MAT_ESP, MAT_REF, MAT_TESTE, IMPORTER

#TODO: Transformar isso aqui em várias classes 

class SimpleImage:

    def __init__(self, imgPath: str, save_f: bool = False) -> None:
        self.imgPath = imgPath
        self.image = Image.open(self.imgPath)
        self.pixel_data = self.image.load()
        self.data = np.asarray(self.image)
        self.width = self.image.width
        self.heigth = self.image.height
        self.save_f = save_f
        self.mode = self.image.mode

    def save_file(self, name: str, image) -> None:
        if self.save_f:
            image.save(f'out/{name}_{self.imgPath[7:]}')

    def in_grayscale(self) -> None:

        def set_grayscale(values: tuple) -> list:
            if self.mode == "RGB":
                mean = sum(values) // 3
                return [mean, mean, mean]
            else:
                mean = (sum(values) - values[3]) // 3
                return [mean, mean, mean, values[3]]

        temp = []
        for rows in self.data:
            pixel_list = []
            for pixel in rows:
                pixel_list.append(set_grayscale(pixel))
            temp.append(pixel_list)

        data = np.array(temp, dtype=np.uint8)
        newImage = Image.fromarray(data)
        newImage.show()
        self.save_file(f"Gray", newImage)

    def interpolação(self, type: str) -> None:
        if 'Vizinho' in type:
            if 'Ampliação' in type:
                self.interpolacao_vizinhos_ampliacao()
            else:
                self.interpolacao_vizinhos_reducao()
        elif 'Bilinear' in type:
            if 'Ampliação' in type:
                self.interpolacao_bilinear_ampliacao()
            else:
                self.interpolacao_bilinear_reducao()

    def interpolacao_vizinhos_reducao(self) -> None:
        imgList = []
        for y in range(0, self.heigth-1, 2):
            row = []
            for x in range(0, self.width-1, 2):
                row.append(self.pixel_data[x, y])
            imgList.append(row)
        data = np.array(imgList, dtype=np.uint8)
        newImage = Image.fromarray(data)
        newImage.show()
        self.save_file('VizinhosRedução', newImage)

    def interpolacao_vizinhos_ampliacao(self) -> None:
        imgList = []
        for y in range(self.heigth):
            row = []
            for x in range(self.width):
                row.append(self.pixel_data[x, y])
                row.append(self.pixel_data[x, y])
            imgList.append(row)
            imgList.append(row)

        data = np.array(imgList, dtype=np.uint8)
        newImage = Image.fromarray(data)
        newImage.show()
        self.save_file('VizinhosAmpliação', newImage)

    def calcular_rgb_media(self, *val: tuple) -> list:

        r, g, b, a = 0, 0, 0, 0
        for pixel in val:
            r += pixel[0]
            g += pixel[1]
            b += pixel[2]

        if self.mode == "RGBA":
            a = sum([x[3] for x in val])
            return [i//len(val) for i in [r, g, b, a]]

        return [i//len(val) for i in [r, g, b]]

    def interpolacao_bilinear_reducao(self) -> None:

        imgList = []
        for y in range(0, self.heigth - 1, 2):
            row = []
            for x in range(0, self.width - 1, 2):
                row.append(self.calcular_rgb_media(
                    self.pixel_data[x, y],
                    self.pixel_data[x, y+1],
                    self.pixel_data[x+1, y],
                    self.pixel_data[x+1, y+1]
                ))

            imgList.append(row)
        data = np.array(imgList, dtype=np.uint8)
        newImage = Image.fromarray(data)
        newImage.show()
        self.save_file('BilinearRedução', newImage)

    def interpolacao_bilinear_ampliacao(self) -> None:

        imgList = []
        for y in range(self.heigth):
            row = []
            middleRow = []
            for x in range(self.width):
                if x == self.width-1 or y == self.heigth-1:
                    row.append(self.pixel_data[x, y])
                    row.append(self.pixel_data[x, y])

                    middleRow.append(self.pixel_data[x, y])
                    middleRow.append(self.pixel_data[x, y])

                else:
                    row.append(self.pixel_data[x, y])
                    row.append(self.calcular_rgb_media(
                        self.pixel_data[x, y],
                        self.pixel_data[x, y+1]
                    ))

                    middleRow.append(self.calcular_rgb_media(
                        self.pixel_data[x, y],
                        self.pixel_data[x+1, y]
                    ))

                    middleRow.append(self.calcular_rgb_media(
                        self.pixel_data[x, y],
                        self.pixel_data[x, y+1],
                        self.pixel_data[x+1, y+1],
                        self.pixel_data[x+1, y]
                    ))

            imgList.append(row)
            imgList.append(middleRow)

        data = np.array(imgList, dtype=np.uint8)
        newImage = Image.fromarray(data)

        newImage.show()
        self.save_file('BilinearAmpliação', newImage)

    def reflexão_espelhamento(self, type: str) -> None:

        newImage = Image.new(self.mode, self.image.size)
        newImage_pixels = newImage.load()

        if type == "Espelhamento":
            for y in range(self.heigth):
                for x in range(self.width):
                    matrixCalc = np.dot(MAT_ESP, [x, y, 1])
                    newImage_pixels[x, y] = self.pixel_data[self.width -
                                                            1 + matrixCalc[0], matrixCalc[1]]
        elif type == "Reflexão":
            for y in range(self.heigth):
                for x in range(self.width):
                    matrixCalc = np.dot(MAT_REF, [x, y, 1])
                    newImage_pixels[x, y] = self.pixel_data[x,
                                                            self.heigth - 1 + matrixCalc[1]]
        else:
            for y in range(self.heigth):
                for x in range(self.width):
                    matrixCalc = np.dot(MAT_TESTE, [x, y, 1])
                    newImage_pixels[x, y] = self.pixel_data[self.width - 1 + matrixCalc[0],
                                                            self.heigth - 1 + matrixCalc[1]]

        newImage.show()
        self.save_file(type, newImage)

    def negativo(self) -> None:

        def inverterPixel(pixel: tuple):
            val = [255 - val for val in pixel]
            if self.mode == "RGB":
                return tuple(val)
            else:
                val[3] = pixel[3]
                return tuple(val)

        newImage = Image.new(self.mode, self.image.size)
        newImage_pixels = newImage.load()

        for y in range(self.heigth):
            for x in range(self.width):
                pixel = self.pixel_data[x, y]
                newImage_pixels[x, y] = inverterPixel(pixel)

        newImage.show()
        self.save_file("Negativo", newImage)

    def aritmetica(self, type: str) -> None:
        results = prompt(IMPORTER)
        img_2 = SimpleImage(results['imgPath'], False)
        self.adicao(img_2) if 'Adição' in type else self.subtracao(img_2)

    def adicao(self, second: 'SimpleImage') -> None:
        imgList = []
        for y in range(self.heigth):
            row = []
            for x in range(self.width):
                row.append(self.calcular_rgb_media(
                    self.pixel_data[x, y], second.pixel_data[x, y]))
            imgList.append(row)

        data = np.array(imgList, dtype=np.uint8)
        newImage = Image.fromarray(data)
        newImage.show()
        self.save_file('Adição', newImage)

    def subtracao(self, second: 'SimpleImage') -> None:

        def calcular_rgb(pixel1: tuple, pixel2: tuple) -> tuple:
            r = abs(pixel1[0] - pixel2[0])
            g = abs(pixel1[1] - pixel2[1])
            b = abs(pixel1[2] - pixel2[2])
            return (r, g, b)

        imgList = []
        for y in range(self.heigth):
            row = []
            for x in range(self.width):
                row.append(calcular_rgb(
                    self.pixel_data[x, y], second.pixel_data[x, y]))
            imgList.append(row)

        data = np.array(imgList, dtype=np.uint8)
        newImage = Image.fromarray(data)
        newImage.show()
        self.save_file('Subtração', newImage)

    def intensidade(self, type: str) -> None:
        if type == 'Transformar em cinza':
            self.in_grayscale()
        elif type == 'Transformar em negativo':
            self.negativo()
        else:
            self.histograma()

    def histograma(self) -> None:
        self.in_grayscale()
        pass
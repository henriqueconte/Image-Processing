from tkinter import * 
from PIL import Image, ImageTk, ImageDraw, ImageOps, ImageEnhance
import matplotlib.pyplot as plt 

class ImageProcessor(Tk):

    brightnessCount = 0
    contrastCount = 0
    zoomCout = 0
    isCurrentlyGray = False
    scaleValue = 1

    def __init__(self):
        Tk.__init__(self)
        self.setupInterface()

    def setupInterface(self):
        buttonFrame = Frame(self, bd=3)        

        ### FIRST ROW
        # Creates interface buttons
        self.saveButton = Button(buttonFrame, text = "Salvar", command = self.save)
        self.horizontalMirrorButton = Button(buttonFrame, text="Espelhamento horizontal", command = self.horizontalMirror)
        self.verticalMirrorButton = Button(buttonFrame, text="Espelhamento vertical", command = self.verticalMirror)
        self.greyImageButton = Button(buttonFrame, text="Tons de cinza", command = self.greyImage)
        self.quantizationButton = Button(buttonFrame, text = "Quantização", command = self.quantization)
        self.histogramButton = Button(buttonFrame, text = "Ver histograma", command = self.showHistogram)
        self.decreaseBrightnessButton = Button(buttonFrame, text="Diminuir brilho", command = self.decreaseBrightness)
        self.increaseBrightnessButton = Button(buttonFrame, text="Aumentar brilho", command = self.increaseBrightness)  

        # Setups buttons on canvas
        self.saveButton.pack(side = 'left')
        self.horizontalMirrorButton.pack(side='left')
        self.verticalMirrorButton.pack(side='left')
        self.greyImageButton.pack(side='left')
        self.quantizationButton.pack(side='left')
        self.histogramButton.pack(side = 'left')
        self.decreaseBrightnessButton.pack(side = 'left')
        self.increaseBrightnessButton.pack(side = 'left')

        buttonFrame.pack(fill = 'x')    

        ### SECOND ROW
        secondRowButtonFrame = Frame(self, bd=3) 
        # Creates interface buttons     

        self.decreaseConstrastButton = Button(secondRowButtonFrame, text="Diminuir contraste", command = self.decreaseContrast)
        self.increaseConstrastButton = Button(secondRowButtonFrame, text="Aumentar contrsate", command = self.increaseContrast)
        self.negativeImageButton = Button(secondRowButtonFrame, text="Negativo", command = self.negativeImage)
        self.histogramEqualizationButton = Button(secondRowButtonFrame, text="Equalização de histograma", command = self.greyHistogramEqualization)
        self.histogramMatchingButton = Button(secondRowButtonFrame, text="Histogram matching", command = self.histogramMatching)
        self.zoomInButton = Button(secondRowButtonFrame, text="Zoom in", command = self.zoomIn)
        self.zoomOutButton = Button(secondRowButtonFrame, text="Zoom out", command = self.zoomOut)
        self.clockwiseRotationButton = Button(secondRowButtonFrame, text="Sentido horário", command = self.clockwiseRotation)
        self.counterClockwiseRotationButton = Button(secondRowButtonFrame, text="Sentido anti-horário", command = self.counterClockwiseRotation)

        # Setups buttons on canvas
        self.decreaseConstrastButton.pack(side='left')
        self.increaseConstrastButton.pack(side='left')
        self.negativeImageButton.pack(side='left')
        self.histogramEqualizationButton.pack(side='left')
        self.histogramMatchingButton.pack(side = 'left')
        self.zoomInButton.pack(side='left')
        self.zoomOutButton.pack(side='left')
        self.clockwiseRotationButton.pack(side='left')
        self.counterClockwiseRotationButton.pack(side='left')

        secondRowButtonFrame.pack(fill = 'x', pady = 1)

        ### THIRD ROW
        thirdRowButtonFrame = Frame(self, bd=3)

        convolutionOptions = [
            '-',
            'Gaussiano',
            'Laplaciano',
            'Passa alta genérico',
            'Prewitt Hx',
            'Prewitt Hy',
            'Sobel Hx',
            'Sobel Hy'
        ]
        # Creates interface buttons
        self.convolutionLabel = Label(thirdRowButtonFrame, text='Filtro para convolução: ')
        self.menuValue = StringVar(self)
        self.menuValue.set(convolutionOptions[0])
        self.convolutionMenu = OptionMenu(thirdRowButtonFrame, self.menuValue, *convolutionOptions)
        self.filterIntensityLabel = Label(thirdRowButtonFrame, text='       Peso do filtro: ')
        self.convolutionScale = Scale(thirdRowButtonFrame,  from_=1, to=10, length = 200, orient=HORIZONTAL, command=self.updateScaleValue)

        # Setups buttons on canvas
        self.convolutionLabel.pack(side='left')
        self.convolutionMenu.pack(side='left')
        self.filterIntensityLabel.pack(side='left')
        self.convolutionScale.pack(side='left')

        thirdRowButtonFrame.pack(fill = 'x', pady = 2)

        # Creates canvas
        self.canvas = Canvas(self, bd = 0, highlightthickness = 0, width = 200, height = 200)
        self.canvas.pack(fill = "both", expand = 1)

        # Setups original image
        imagePath = "./test_images/Space_187k.jpg"
        self.originalImage = Image.open(imagePath)
        self.originalImage.thumbnail((512, 512))

        # Setups working image
        self.workingImage = self.originalImage.copy()

        # Adds images to canvas
        self.originalTkImage = ImageTk.PhotoImage(self.originalImage)
        self.workingTkImage = ImageTk.PhotoImage(self.workingImage)

        self.canvasItem = self.canvas.create_image(10, 30, anchor = 'nw', image = self.originalTkImage)
        self.workingCanvasItem = self.canvas.create_image(self.originalImage.size[0] + 20, 30, anchor = 'nw', image = self.workingTkImage)

        self.canvas.config(width = self.originalImage.size[0] * 2 + 35, height = self.originalImage.size[1] * 1.3)

    def save(self):
        self.workingImage.save("editedImage.jpg")

    def horizontalMirror(self):
        copiedImage = self.workingImage.copy()
        originalPixelMap = copiedImage.load()
        workingPixelMap = self.workingImage.load()
        
        for i in range(0, self.workingImage.size[0]):
            for j in range(0, self.workingImage.size[1]):
                workingPixelMap[i,j] = originalPixelMap[self.workingImage.size[0] - i - 1, j]

        self.updateImage(self.workingImage)

    def verticalMirror(self):
        copiedImage = self.workingImage.copy()
        originalPixelMap = copiedImage.load()
        workingPixelMap = self.workingImage.load()
        
        for i in range(0, self.workingImage.size[0]):
            for j in range(0, self.workingImage.size[1]):
                workingPixelMap[i,j] = originalPixelMap[i, self.workingImage.size[1] - j - 1]

        self.updateImage(self.workingImage)

    def getGreyImageMap(self, image):
        copiedImage = image.copy()
        pixelMap = copiedImage.load()

        for i in range(0, copiedImage.size[0]):
            for j in range(0, copiedImage.size[1]):
                pixel = pixelMap[i,j]
                luminance = int(pixel[0] * 0.299 + pixel[1] * 0.587 + pixel[2] * 0.114)
                pixelMap[i,j] = (luminance, luminance, luminance, 0)

        return pixelMap

    def getGreyImage(self, image):
        copiedImage = image.copy()
        pixelMap = copiedImage.load()

        grayPixelMap = self.getGreyImageMap(image)

        for i in range(0, copiedImage.size[0]):
            for j in range(0, copiedImage.size[1]):
                pixelMap[i,j] = grayPixelMap[i,j]

        return image

    def greyImage(self):
        self.isCurrentlyGray = True
        pixelMap = self.workingImage.load()

        grayPixelMap = self.getGreyImageMap(self.workingImage)

        for i in range(0, self.workingImage.size[0]):
            for j in range(0, self.workingImage.size[1]):
                pixelMap[i,j] = grayPixelMap[i,j]

        self.updateImage(self.workingImage)

    def quantization(self):
        shadeLimit = 4
        self.greyImage()

        copiedImage = self.workingImage.copy()
        originalPixelMap = copiedImage.load()
        workingPixelMap = self.workingImage.load()

        maxColor = -1
        minColor = 99999999

        for i in range(0, self.workingImage.size[0]):
            for j in range(0, self.workingImage.size[1]):
                pixel = originalPixelMap[i,j]

                if pixel[0] > maxColor:
                    maxColor = pixel[0]

                if pixel[0] < minColor:
                    minColor = pixel[0]

        tam_int = maxColor - minColor + 1

        if shadeLimit < tam_int:
            binSize = tam_int / shadeLimit
            binBoundaries = []
            binColorList = []

            for i in range(0, shadeLimit):
                binBoundaries.append(binSize * i)
                newColor = int((binSize * i + binSize * (i + 1)) / 2)
                binColorList.append(newColor)


        for i in range(0, self.workingImage.size[0]):
            for j in range(0, self.workingImage.size[1]):
                pixel = workingPixelMap[i,j]

                for colorIndex in range(0, len(binBoundaries)):
                    if (colorIndex == len(binBoundaries) - 1) or (pixel[0] >= binBoundaries[colorIndex] and pixel[0] < binBoundaries[colorIndex + 1]):
                        currentColor = binColorList[colorIndex]
                        workingPixelMap[i, j] = (currentColor, currentColor, currentColor, 0)
                        break

        self.updateImage(self.workingImage)

    def updateImage(self, newImage):
        self.workingTkImage = ImageTk.PhotoImage(newImage)
        self.canvas.itemconfigure(self.workingCanvasItem, image = self.workingTkImage)

    def showHistogram(self):
        copiedImage = self.getGreyImage(self.workingImage)
        r,g,b = copiedImage.split()
        histValues = r.histogram()
        histSum = 0

        for element in histValues:
            histSum += element
        for i in range(0, 256):
            plt.bar(i, histValues[i] / histSum , color = 'green')

        plt.show()

    def changeBrightness(self):
        if self.isCurrentlyGray:
            originalPixelMap = self.getGreyImageMap(self.originalImage)
        else:
            originalPixelMap = self.originalImage.load()

        pixelMap = self.workingImage.load()

        for i in range(0, self.originalImage.size[0]):
            for j in range(0, self.originalImage.size[1]):
                pixel = originalPixelMap[i,j]
                pixel0 = pixel[0] + 10 * self.brightnessCount
                pixel1 = pixel[1] + 10 * self.brightnessCount
                pixel2 = pixel[2] + 10 * self.brightnessCount
                if pixel0 < 0:
                    pixel0 = 0
                if pixel1 < 0:
                    pixel1 = 0
                if pixel2 < 0:
                    pixel2 = 0

                pixelMap[i,j] = (pixel0, pixel1, pixel2)

        self.updateImage(self.workingImage)

    def decreaseBrightness(self):
        self.brightnessCount -= 1
        self.changeBrightness()

    def increaseBrightness(self):
        self.brightnessCount += 1
        self.changeBrightness()

    def changeContrast(self):
        if self.isCurrentlyGray:
            originalPixelMap = self.getGreyImageMap(self.originalImage)
        else:
            originalPixelMap = self.originalImage.load()
        pixelMap = self.workingImage.load()

        for i in range(0, self.originalImage.size[0]):
            for j in range(0, self.originalImage.size[1]):
                pixel = originalPixelMap[i,j]
                pixel0 = pow(pixel[0], (1 + (self.brightnessCount * 0.05)))
                pixel1 = pow(pixel[1], (1 + (self.brightnessCount * 0.05)))
                pixel2 = pow(pixel[2], (1 + (self.brightnessCount * 0.05)))
                if pixel0 < 0:
                    pixel0 = 0
                if pixel1 < 0:
                    pixel1 = 0
                if pixel2 < 0:
                    pixel2 = 0

                pixelMap[i,j] = (int(pixel0), int(pixel1), int(pixel2))

        self.updateImage(self.workingImage)
        
    def decreaseContrast(self):
        self.brightnessCount -= 1
        self.changeContrast()

    def increaseContrast(self):
        self.brightnessCount += 1
        self.changeContrast()

    def negativeImage(self):
        pixelMap = self.workingImage.load()

        for i in range(0, self.workingImage.size[0]):
            for j in range(0, self.workingImage.size[1]):
                pixel = pixelMap[i,j]
                pixelMap[i,j] = (255 - pixel[0], 255 - pixel[1], 255 - pixel[2])

        self.updateImage(self.workingImage)

    def greyHistogramEqualization(self):
        grayImage = self.getGreyImage(self.workingImage)
        copiedImage = self.workingImage.copy()
        scalingFactor = 255 / (copiedImage.size[0] * copiedImage.size[1])
        r,g,b = grayImage.split()
        histogram = r.histogram()
        cummulativeHistogram = [scalingFactor * histogram[0]]

        for i in range(1, len(histogram)):
            cummulativeHistogram.append(scalingFactor * histogram[i] + cummulativeHistogram[i - 1])

        pixelMap = copiedImage.load()
        grayPixelMap = grayImage.load()

        for i in range(0, copiedImage.size[0]):
            for j in range(0, copiedImage.size[1]):
                grayPixel = grayPixelMap[i,j]
                grayShade = int(cummulativeHistogram[grayPixel[0]])
                pixelMap[i,j] = (grayShade, grayShade, grayShade)

        self.openNewWindow(copiedImage, "Histograma Equalizado", False)

    def openNewWindow(self, displayedImage, windowTitle, isBigWindow):
        windowTkImage = ImageTk.PhotoImage(displayedImage)

        newWindow = Toplevel(self)
        newWindow.title(windowTitle)
        if isBigWindow:
            newCanvas = Canvas(newWindow, width = 1100, height = 1100)
        else:
            newCanvas = Canvas(newWindow, width = 550, height = 450)
        
        newCanvas.pack()
        newCanvas.create_image(10, 30, anchor = 'nw', image = windowTkImage)
        newCanvas.currentImage = windowTkImage

    def histogramMatching(self):
        originalImagePath = "./test_images/Space_187k.jpg"
        targetImagePath = "./test_images/Gramado_72k.jpg"

        originalImage = Image.open(originalImagePath).convert('RGB')
        targetImage = Image.open(targetImagePath).convert('RGB')

        originalImageMap = originalImage.load()
        grayOriginalMap = self.getGreyImageMap(originalImage)
        targetImageMap = targetImage.load()
        grayTargetMap = self.getGreyImageMap(targetImage)

        for i in range(0, originalImage.size[0]):
            for j in range(0, originalImage.size[1]):
                originalImageMap[i,j] = grayOriginalMap[i,j]

        for i in range(0, targetImage.size[0]):
            for j in range(0, targetImage.size[1]):
                targetImageMap[i,j] = grayTargetMap[i,j]

        originalImage.thumbnail((512, 512))
        targetImage.thumbnail((512, 512))

        editedImage = originalImage.copy()

        r,g,b = originalImage.split()
        originalHistogram = r.histogram()
        originalScalingFactor = 255 / (originalImage.size[0] * originalImage.size[1])
        originalCummulativeHistogram = [originalScalingFactor * originalHistogram[0]]

        for i in range(1, len(originalHistogram)):
            originalCummulativeHistogram.append(originalScalingFactor * originalHistogram[i] + originalCummulativeHistogram[i - 1])

        r,g,b = targetImage.split()
        targetHistogram = r.histogram()
        targetScalingFactor = 255 / (targetImage.size[0] * targetImage.size[1])
        targetCummulativeHistogram = [targetScalingFactor * targetHistogram[0]]

        for i in range(1, len(targetHistogram)):
            targetCummulativeHistogram.append(targetScalingFactor * targetHistogram[i] + targetCummulativeHistogram[i - 1])

        editedHistogram = []
        editedImageMap = editedImage.load()

        for i in range(0, len(targetCummulativeHistogram)):
            editedHistogram.append(self.find_nearest(targetCummulativeHistogram, originalCummulativeHistogram[i]))

        for i in range(0, originalImage.size[0]):
            for j in range(0, originalImage.size[1]):
                grayShade = int(editedHistogram[originalImageMap[i,j][0]])
                editedImageMap[i,j] = (grayShade, grayShade, grayShade)

        self.openNewWindow(originalImage, "Original Image", False)
        self.openNewWindow(editedImage, "HM Image", False)
        self.openNewWindow(targetImage, "Target", False)

    # Source: https://stackoverflow.com/questions/2566412/find-nearest-value-in-numpy-array
    def find_nearest(self, array, value):
        n = [abs(i-value) for i in array]
        idx = n.index(min(n))
        return array[idx]

    def zoomIn(self):
        sx = 2
        sy = 2
        newWidth, newHeight = int(self.workingImage.size[0] * sx), int(self.workingImage.size[1] * sy)
        copiedImg = Image.new('RGB', (newWidth, newHeight))
        copiedImgMap = copiedImg.load()

        j = 0
        while (j < newHeight):
            for i in range(0, newWidth):
                if i % 2 == 0:
                    r,g,b = self.workingImage.getpixel((i / 2, j / 2))
                    copiedImgMap[i,j] = (int(r / (sx * sy)), int(g / (sx * sy)), int(b / (sx * sy)))
                elif (i + 1) / 2 < self.workingImage.size[0]:
                    prevR, prevG, prevB = self.workingImage.getpixel(((i-1) / 2, j / 2))
                    nextR, nextG, nextB = self.workingImage.getpixel(((i+1) / 2, j / 2))
                    prevR, prevG, prevB = int((prevR + nextR) / 2), int((prevG + nextG) / 2), int((prevB + nextB) / 2)
                    copiedImgMap[i,j] = (prevR, prevG, prevB)
                else:
                    r,g,b = self.workingImage.getpixel(((i-1) / 2, j / 2))
                    copiedImgMap[i,j] = (r, g, b)
            j += 2

        for i in range(0, newWidth):
            j = 1
            while (j < newHeight - 1):
                if (j + 1) / 2 < self.workingImage.size[1]:
                    prevR, prevG, prevB = self.workingImage.getpixel((i/2, (j-1)/2))
                    nextR, nextG, nextB = self.workingImage.getpixel((i/2, (j+1)/2))
                    prevR, prevG, prevB = int((prevR + nextR) / 2), int((prevG + nextG) / 2), int((prevB + nextB) / 2)
                    copiedImgMap[i,j] = (prevR, prevG, prevB)
                else:
                    r,g,b = self.workingImage.getpixel((i/2, (j-1)/2))
                    copiedImgMap[i,j] = (r, g, b) 
                j += 2

        self.openNewWindow(copiedImg, "Imagem com zoom in", True)

    def zoomOut(self):
        sx = 2
        sy = 2
        newWidth, newHeight = int(self.workingImage.size[0] / sx), int(self.workingImage.size[1] / sy)
        copiedImg = Image.new('RGB', (newWidth, newHeight))
        copiedImgMap = copiedImg.load()
        for i in range(0, newWidth):
            for j in range(0, newHeight):
                i_old = i * sx
                currentColor = [0, 0, 0]
                while i_old < sx * (i + 1) and i_old < self.workingImage.size[0] - 1:
                    i_old += 1
                    j_old = j * sy
                    while j_old < sy * (j + 1) and j_old < self.workingImage.size[1] - 1:
                        j_old += 1
                        r,g,b = self.workingImage.getpixel((i_old, j_old))
                        currentColor[0] += r
                        currentColor[1] += g
                        currentColor[2] += b
                copiedImgMap[i,j] = (int(currentColor[0] / (sx * sy)), int(currentColor[1] / (sx * sy)), int(currentColor[2] / (sx * sy)))

        self.openNewWindow(copiedImg, 'Imagem com zoom out', False)

    def clockwiseRotation(self):
        newWidth, newHeight = self.workingImage.size[1], self.workingImage.size[0]
        copiedImg = Image.new('RGB', (newWidth, newHeight))
        copiedImgMap = copiedImg.load()

        for i in range(0, self.workingImage.size[0]):
            for j in range(0, self.workingImage.size[1]):
                yPosition = copiedImg.size[0] - j - 1
                r, g, b = self.workingImage.getpixel((i, j))
                copiedImgMap[yPosition, i] = (r, g, b)

        self.workingImage = copiedImg
        self.updateImage(self.workingImage)

    def counterClockwiseRotation(self):
        newWidth, newHeight = self.workingImage.size[1], self.workingImage.size[0]
        copiedImg = Image.new('RGB', (newWidth, newHeight))
        copiedImgMap = copiedImg.load()

        for i in range(0, self.workingImage.size[0]):
            for j in range(0, self.workingImage.size[1]):
                xPosition = copiedImg.size[1] - i - 1
                r, g, b = self.workingImage.getpixel((i, j))
                copiedImgMap[j, xPosition] = (r, g, b)

        self.workingImage = copiedImg
        self.updateImage(self.workingImage)
        
    def updateScaleValue(self, v):
        self.scaleValue = v
        # print(self.menuValue.get())



imageProcessor = ImageProcessor()
imageProcessor.mainloop()
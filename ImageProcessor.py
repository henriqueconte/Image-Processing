from tkinter import * 
from PIL import Image, ImageTk, ImageDraw, ImageOps, ImageEnhance
import matplotlib.pyplot as plt 

class ImageProcessor(Tk):

    brightnessCount = 0
    contrastCount = 0
    isCurrentlyGray = False

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

        # Setups buttons on canvas
        self.decreaseConstrastButton.pack(side='left')
        self.increaseConstrastButton.pack(side='left')
        self.negativeImageButton.pack(side='left')
        self.histogramEqualizationButton.pack(side='left')
        self.histogramMatchingButton.pack(side = 'left')

        secondRowButtonFrame.pack(fill = 'x', pady = 1)

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

        self.openNewWindow(copiedImage, "Histograma Equalizado")

    def openNewWindow(self, displayedImage, windowTitle):
        windowTkImage = ImageTk.PhotoImage(displayedImage)

        newWindow = Toplevel(self)
        newWindow.title(windowTitle)

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

        self.openNewWindow(originalImage, "Original Image")
        self.openNewWindow(editedImage, "HM Image")
        self.openNewWindow(targetImage, "Target")

    # Source: https://stackoverflow.com/questions/2566412/find-nearest-value-in-numpy-array
    def find_nearest(self, array, value):
        n = [abs(i-value) for i in array]
        idx = n.index(min(n))
        return array[idx]

imageProcessor = ImageProcessor()
imageProcessor.mainloop()
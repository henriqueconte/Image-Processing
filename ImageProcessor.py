from tkinter import * 
from PIL import Image, ImageTk, ImageDraw, ImageOps, ImageEnhance

class ImageProcessor(Tk):
    
    def __init__(self):
        Tk.__init__(self)
        self.setupInterface()

    def setupInterface(self):
        buttonFrame = Frame(self, bd=3)        

        # Creates interface buttons
        self.saveButton = Button(buttonFrame, text = "Salvar", command = self.save)
        self.horizontalMirrorButton = Button(buttonFrame, text="Espelhamento horizontal", command = self.horizontalMirror)
        self.verticalMirrorButton = Button(buttonFrame, text="Espelhamento vertical", command = self.verticalMirror)
        self.greyImageButton = Button(buttonFrame, text="Tons de cinza", command = self.greyImage)
        self.quantizationButton = Button(buttonFrame, text = "Quantização", command = self.quantization)

        # Setups buttons on canvas
        self.saveButton.pack(side = 'left')
        self.horizontalMirrorButton.pack(side='left')
        self.verticalMirrorButton.pack(side='left')
        self.greyImageButton.pack(side='left')
        self.quantizationButton.pack(side='left')
        buttonFrame.pack(fill = 'x')

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

    def greyImage(self):
        pixelMap = self.workingImage.load()

        for i in range(0, self.workingImage.size[0]):
            for j in range(0, self.workingImage.size[1]):
                pixel = pixelMap[i,j]
                luminance = int(pixel[0] * 0.299 + pixel[1] * 0.587 + pixel[2] * 0.114)
                pixelMap[i,j] = (luminance, luminance, luminance, 0)

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

imageProcessor = ImageProcessor()
imageProcessor.mainloop()
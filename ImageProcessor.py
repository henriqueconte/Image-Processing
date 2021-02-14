'''
from tkinter import * 
#from PIL import Image, ImageTk, ImageDraw, ImageOps, ImageEnhance
from PIL import Image

imagePath = "./test_images/Gramado_22k.jpg"
image = Image.open(imagePath)
image.show()
print(image)
'''
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
        imagePath = "./test_images/Gramado_22k.jpg"
        originalImage = Image.open(imagePath)
        originalImage.thumbnail((512, 512))

        # Adds image to canvas
        self.tkImage = ImageTk.PhotoImage(originalImage)
        self.canvasItem = self.canvas.create_image(0, 0, anchor = 'nw', image = self.tkImage)
        self.canvas.config(width = originalImage.size[0], height = originalImage.size[1] * 2)

        self.currentImage = originalImage
        self.workingImage = originalImage.copy()

    def save(self):
        print("")

    def horizontalMirror(self):
        print("")

    def verticalMirror(self):
        print("")

    def greyImage(self):
        print('')

    def quantization(self):
        print("")

class ImageButcher(Tk):
    def __init__(self):
        Tk.__init__(self)

        #create ui
        f = Frame(self, bd=2)

        self.colour = StringVar(self)
        self.colourMenu = OptionMenu(f, self.colour,
                                     *('red','green','blue','white'))
        self.colourMenu.config(width=5)
        self.colour.set('red')
        self.colourMenu.pack(side='left')

        self.rectangleButton = Button(f, text='Rectangle',
                                    command=self.draw_rectangle)
        self.rectangleButton.pack(side='left')

        self.brightenButton = Button(f, text='Brighten',
                                    command=self.on_brighten)
        self.brightenButton.pack(side='left')

        self.mirrorButton = Button(f, text='Mirror',
                                    command=self.on_mirror)
        self.mirrorButton.pack(side='left')
        f.pack(fill='x')

        self.c = Canvas(self, bd=0, highlightthickness=0,
                        width=100, height=100)
        self.c.pack(fill='both', expand=1)

        #load image
        im = Image.open('./test_images/Gramado_22k.jpg')
        im.thumbnail((512,512))

        self.tkphoto = ImageTk.PhotoImage(im)
        self.canvasItem = self.c.create_image(0,0,anchor='nw',image=self.tkphoto)
        self.c.config(width=im.size[0], height=im.size[1])

        self.img = im
        self.temp = im.copy() # 'working' image

    def display_image(self, aImage):
        self.tkphoto = pic = ImageTk.PhotoImage(aImage)
        self.c.itemconfigure(self.canvasItem, image=pic)

    def on_mirror(self):
        im = ImageOps.mirror(self.temp)
        self.display_image(im)
        self.temp = im

    def on_brighten(self):
        brightener = ImageEnhance.Brightness(self.temp)
        self.temp = brightener.enhance(1.1) # +10%
        self.display_image(self.temp)

    def draw_rectangle(self):
        bbox = 9, 9, self.temp.size[0] - 11, self.temp.size[1] - 11        
        draw = ImageDraw.Draw(self.temp)
        draw.rectangle(bbox, outline=self.colour.get())
        self.display_image(self.temp)


#app = ImageButcher()
#app.mainloop()

imageProcessor = ImageProcessor()
imageProcessor.mainloop()
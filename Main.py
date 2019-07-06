from tkinter import *
from tkinter.ttk import Progressbar, Style

from PIL import ImageFont, Image, ImageDraw
import os
import barcode
from barcode.writer import ImageWriter

getDefaults = []

if(os.path.exists("conf.ini")):
    file = open("conf.ini", "r")
    for i in file:
        getDefaults.append(i)
    file.close()
else:
    getDefaults = ["","","","000001"]

class BarcodeGenerator:
    def __init__(self):
        self.n = 0
        self.window = Tk()
        self.window.title("BarcodeGenerator")
        self.window.resizable(False, False)
        try:
            self.topText = StringVar(value=getDefaults[0].strip("\n"))
        except:
            self.topText = StringVar(value="")
        self.topText.trace_add('write', self.val2)
        try:
            self.bottomText = StringVar(value=getDefaults[1].strip("\n"))
        except:
            self.bottomText = StringVar(value="")
        self.bottomText.trace_add('write', self.val3)
        try:
            self.tcode = StringVar(value=getDefaults[2].strip("\n"))
        except:
            self.tcode = StringVar(value="")
        self.tcode.trace_add('write', self.val0)
        try:
            self.code = StringVar(value=getDefaults[3].strip("\n"))
        except:
            self.code = StringVar(value="000001")
        self.code.trace_add('write', self.val1)
        self.numToMake = StringVar(value='1')
        self.numToMake.trace_add('write', self.val4)


        Label(self.window, text="").grid(row=4, column=2)
        Label(self.window, text="Top Line 1:", justify=LEFT).grid(row=0, column=0, sticky=W)
        Entry(self.window, textvariable=self.topText, justify=CENTER).grid(row=0, column=1, columnspan=5, sticky=E+W)

        Label(self.window, text="Top Line 2:", justify=LEFT).grid(row=1, column=0, sticky=W)
        Entry(self.window, textvariable=self.bottomText, justify=CENTER).grid(row=1, column=1, columnspan=5, sticky=E+W)

        Label(self.window, text="Herbarium Code: ", justify=LEFT).grid(row=2, column=0, sticky=W)
        Entry(self.window, textvariable=self.tcode, justify=CENTER).grid(row=2, column=1, sticky=W)
        self.ent = Entry(self.window, textvariable=self.code, justify=CENTER).grid(row=2, column=2, sticky=W)

        self.makeNum = Label(self.window, text=f"{int(self.numToMake.get())*52} barcodes will be generated", justify=LEFT).grid(row=3, column=3, columnspan=2, sticky=E)

        Label(self.window, text="Number of Pages: ").grid(row=2, column=3, sticky=W)
        Entry(self.window, textvariable=self.numToMake, justify=CENTER).grid(row=2, column=4, sticky=W)

        Button(self.window, text="Generate", command=self.generate).grid(row=3, column=2)

        self.p = Progressbar(self.window, orient="horizontal", length=100, mode='determinate')#, style="LabeledProgressbar")
        self.p.grid(row=4, column=0, columnspan=99, sticky=E + W)
        self.progressbar = Progressbar(self.window, orient=HORIZONTAL, length=100, mode='determinate')
        self.progressbar.grid(row=5, column=0, columnspan=5, sticky=E + W)
        self.progressbar["value"] = 0
        self.progressbar["maximum"] = 100

        mainloop()

    def val0(self, *args):
        valid = ''.join(filter(str.isalpha, self.tcode.get()))
        self.tcode.set(valid.upper()[:6])

    def val1(self, *args):
        valid = ''.join(filter(str.isnumeric, self.code.get()))
        toadd = '0' * (7 - len(self.code.get()))
        valid = toadd + valid
        self.code.set(valid[1:7])
        if(len(self.code.get()) != 6):
            self.code.set('0'+self.code.get())

    def val2(self, *args):
        var = self.topText.get()
        self.topText.set(var[:50])

    def val3(self, *args):
        var = self.bottomText.get()
        self.bottomText.set(var[:50])

    def val4(self, *args):
        valid = ''.join(filter(str.isnumeric, self.numToMake.get()))
        self.numToMake.set(valid[:3])
        try:
            self.makeNum = Label(self.window, text=f"   {int(self.numToMake.get())*52} barcodes will be generated", justify=LEFT).grid(row=3, column=3, columnspan=2, sticky=E)
        except:
            self.makeNum = Label(self.window, text=f"     0 barcodes will be generated", justify=LEFT).grid(row=3, column=3, columnspan=2, sticky=E)
        self.window.update()

    def increment_code(self, num):
        codenum = str(int(self.code.get()) + num)
        if(len(codenum) == 1):
            newcode = '00000' + codenum
        elif(len(codenum) == 2):
            newcode = '0000' + codenum
        elif(len(codenum) == 3):
            newcode = '000' + codenum
        elif(len(codenum) == 4):
            newcode = '00' + codenum
        elif (len(codenum) == 5):
            newcode = '0' + codenum
        else:
            return '999999'
        self.maxcode = newcode
        return newcode

    def generate(self):
        self.n = 0
        self.p["value"] = 0
        for m in range(int(self.numToMake.get())):
            self.generate_work(m)
            self.p["value"] = (int(((m+1) / int(self.numToMake.get())) * 100))
            self.window.update()
        self.saveconf()

    def generate_work(self, k):
        code39 = barcode.get_barcode_class('code39')

        BarImage = code39("THISISATEMPORARYBARCODEUSEDFORGETTINGTEXT", add_checksum=False, writer=ImageWriter())
        BarImage.save('top+bottom', text=(self.topText.get()))
        im = Image.open("top+bottom.png")
        pix = im.load()
        first = 1
        for i in range(1682):
            if(pix[i,255] != (255,255,255)):
                if(first == 1):
                    first = 0
                    minpix = i
                maxpix = i

        topBox = (minpix-5, 245, maxpix+7, 267)

        topSize = ((maxpix + 7) - (minpix - 5))

        BarImage = code39("THISISATEMPORARYBARCODEUSEDFORGETTINGTEXT", add_checksum=False, writer=ImageWriter())
        BarImage.save('top+bottom', text=(self.bottomText.get()))
        im2 = Image.open("top+bottom.png")
        pix = im2.load()

        first = 1
        for i in range(1682):
            if(pix[i, 255] != (255, 255, 255)):
                if(first == 1):
                    first = 0
                    minpix = i
                maxpix = i

        bottomBox = (minpix - 5, 245, maxpix + 7, 267)
        bottomSize = ((maxpix + 7) - (minpix - 5))

        im2.save("top+bottom.png")

        tboxc = im.crop(topBox)
        bboxc = im2.crop(bottomBox)
        image = Image.new('RGBA', (max(topSize, bottomSize), 48), "white")
        if(topSize>=bottomSize):
            sizeDif = int((topSize - bottomSize) / 2)
            image.paste(tboxc, (0, 0, topSize, 22))
            image.paste(bboxc, (sizeDif, 23, bottomSize+sizeDif, 45))
        else:
            sizeDif = int((bottomSize - topSize) / 2)
            image.paste(tboxc, (sizeDif, 0, topSize+sizeDif, 22))
            image.paste(bboxc, (0, 23, bottomSize, 45))

        image.save('testsavepastewords.png')
        im.close()

        sizex,sizey = image.size
        bx = (1,1,sizex,48)
        rgn = image.crop(bx)
        fullImg = Image.new('RGBA', (2750, 2125), "white")

        progcount = 0
        for i in range(13):
            for j in range(4):
                strcode = self.increment_code(self.n)
                code39 = barcode.get_barcode_class('code39')
                BarImage = code39((self.tcode.get() + strcode), add_checksum=False, writer=ImageWriter())
                BarImage.save('tmp')
                BarImage = Image.open("tmp.png")
                xoff = 650
                yoff = 150
                x,y = BarImage.size
                tmpbox = (1, y-35, x, y-15)
                tmptoPaste = (50 + (xoff * j), 185 + (yoff*i), x+49 + (xoff * j), 205 + (yoff*i))
                tmpregion = BarImage.crop(tmpbox)
                fullImg.paste(tmpregion, tmptoPaste)

                box = (1, 1, x, 54)
                toPaste = (60 + (xoff * j), 130 + (yoff*i), x+59 + (xoff * j), 183 + (yoff*i))
                region = BarImage.crop(box)
                fullImg.paste(region, toPaste)

                startx = int((x-sizex)/2)

                pst = (startx+60 + (xoff * j), 90 + (yoff * i), sizex + startx+59 + (xoff * j), 137 + (yoff * i))
                fullImg.paste(rgn, pst)

                self.progressbar["value"] = int((progcount / (13*4))*100)
                self.window.update()
                progcount += 1
                self.n += 1
        self.progressbar["value"] = 100
        self.window.update()

        file = f'{self.tcode.get()}{self.code.get()}({k}) barcodes.png'
        fullImg.save(file)

    def saveconf(self):
        file = open("conf.ini", "w+")
        self.code.set(self.increment_code(self.n))
        file.write(f"{self.topText.get()}\n{self.bottomText.get()}\n{self.tcode.get()}\n{self.code.get()}")
        file.close()

BarcodeGenerator()
from tkinter import *
from tkinter.ttk import Progressbar, Style

from showinfm import show_in_file_manager

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


        self.fileNames = []
        ########## CONFIG VARIABLES ##########
        self.textScale = 2.5
        self.topTextOffset = 15
        self.bottomTextOffsetX = 235
        self.deleteTempFiles = True
        self.lowerCharacters = {'g', 'j', 'q', 'p', 'y'}

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
        self.saveAsPdf()

    def containsLower(self, text):
        for char in text:
            if(char in self.lowerCharacters):
                return True
        return False

    def generate_work(self, k):
        code39 = barcode.get_barcode_class('code39')

        BarImage = code39("THISISATEMPORARYBARCODEUSEDFORGETTINGTEXT", add_checksum=False, writer=ImageWriter())
        
        BarImage.save('top+bottomtop', text=(self.topText.get()))
        im = Image.open("top+bottomtop.png")
        try:
            if(self.deleteTempFiles):
                os.remove("top+bottomtop.png")
        except Exception as e:
            print(e)
        pix = im.load()
        first = 1
        for i in range(1682):
            if(pix[i,230] != (255,255,255)):
                if(first == 1):
                    first = 0
                    minpix = i
                maxpix = i

        ############## ADD CONDITIONAL SIZING ? POSITIONING BASED OFF TEXT INCLUDED (I AM CURRENTLY ASSUMING THE POSITION IS GETTING ADJUSTED BASED OFF IF THE TEXT GOES ABOVE OR BELOW TO KEEP IT CENTERED AT THE SAME POINT)
        topBoxOffset = 215
        topBoxYSize = 40
        topContainsLower = self.containsLower(self.topText.get())
        if(topContainsLower):
            topBoxOffset -= 8
        topBox = (minpix-10, topBoxOffset, maxpix+10, topBoxOffset+topBoxYSize)
        topSize = ((maxpix + 10) - (minpix - 10))

        BarImage = code39("THISISATEMPORARYBARCODEUSEDFORGETTINGTEXT", add_checksum=False, writer=ImageWriter())
        BarImage.save('top+bottombottom', text=(self.bottomText.get()))
        im2 = Image.open("top+bottombottom.png")
        try:
            if(self.deleteTempFiles):
                os.remove("top+bottombottom.png")
        except Exception as e:
            print(e)
        pix = im2.load()

        first = 1
        for i in range(1682):
            if(pix[i, 230] != (255, 255, 255)):
                if(first == 1):
                    first = 0
                    minpix = i
                maxpix = i

        bottomBoxOffset = 215
        bottomBoxYSize = 40
        bottomContainsLower = self.containsLower(self.bottomText.get())
        if(bottomContainsLower):
            bottomBoxOffset -= 8
        bottomBox = (minpix-10, bottomBoxOffset, maxpix+10, bottomBoxOffset+bottomBoxYSize)
        bottomSize = ((maxpix + 10) - (minpix - 10))

        if(not self.deleteTempFiles):
            im2.save("top+bottom.png")

        tboxc = im.crop(topBox)
        tboxc = tboxc.resize((int(topSize/self.textScale), int(40/self.textScale)))
        bboxc = im2.crop(bottomBox)
        bboxc = bboxc.resize((int(bottomSize/self.textScale), int(40/self.textScale)))
        image = Image.new('RGB', (int(max(topSize, bottomSize)/self.textScale), int(40/self.textScale)*2), "white")
        if(topSize>=bottomSize):
            sizeDif = int((topSize - bottomSize) // 2)
            image.paste(tboxc, (0, 0)) #, topSize, 22))
            image.paste(bboxc, (int(sizeDif/self.textScale), int(40/self.textScale))) #, bottomSize+sizeDif, 45))
        else:
            sizeDif = int((bottomSize - topSize) // 2)
            image.paste(tboxc, (int(sizeDif/self.textScale), 0))#, topSize+sizeDif, 22))
            image.paste(bboxc, (0, int(40/self.textScale)))#, bottomSize, 45))

        if(not self.deleteTempFiles):
            image.save("top+bottom.png")
        im.close()

        sizex, sizey = image.size
        bx = (1,1,sizex,sizey)
        rgn = image.crop(bx)
        fullImg = Image.new('RGB', (2750, 2125), "white")

        progcount = 0
        for i in range(13):
            for j in range(4):
                strcode = self.increment_code(self.n)
                code39 = barcode.get_barcode_class('code39')
                BarImage = code39((self.tcode.get() + strcode), add_checksum=False, writer=ImageWriter())
                BarImage.save('tmp')
                BarImage = Image.open("tmp.png")
                try:
                    os.remove("tmp.png")
                except Exception as e:
                    print(e)
                xoff = 650
                yoff = 150
                x,y = BarImage.size
                tmpbox = (1, y-75, x, y-15)
                tmptoPaste = (self.bottomTextOffsetX + (xoff * j), 185 + (yoff*i), int(x/self.textScale)+self.bottomTextOffsetX + (xoff * j), int(60/self.textScale)+185 + (yoff*i))
                tmpregion = BarImage.crop(tmpbox)
                tmpregion = tmpregion.resize((int(x/self.textScale), int(60/self.textScale)))
                fullImg.paste(tmpregion, tmptoPaste)

                box = (1, 1, x, 54)
                toPaste = (60 + (xoff * j), 130 + (yoff*i), x+59 + (xoff * j), 183 + (yoff*i))
                region = BarImage.crop(box)
                fullImg.paste(region, toPaste)

                startx = int((x-sizex)/2)

                pst = (startx+60 + (xoff * j), 90+self.topTextOffset + (yoff * i), sizex + startx+59 + (xoff * j), 89+sizey+self.topTextOffset + (yoff * i))
                fullImg.paste(rgn, pst)

                self.progressbar["value"] = int((progcount / (13*4))*100)
                self.window.update()
                progcount += 1
                self.n += 1
        self.progressbar["value"] = 100
        self.window.update()

        file = f'{self.tcode.get()}{self.code.get()}({k}) barcodes.png'
        self.fileNames.append(file)
        fullImg.save(file)

    def saveconf(self):
        file = open("conf.ini", "w+")
        self.code.set(self.increment_code(self.n))
        a = f"{self.topText.get()}\n{self.bottomText.get()}\n{self.tcode.get()}\n{self.code.get()}"
        file.write(f"{self.topText.get()}\n{self.bottomText.get()}\n{self.tcode.get()}\n{self.code.get()}")
        file.close()

    def saveAsPdf(self):
        images = [Image.open(f) for f in self.fileNames]
        images[0].save(
            self.topText.get() + "_" + self.bottomText.get() + "_" + self.code.get() + '.pdf', "PDF" ,resolution=100.0, save_all=True, append_images=images[1:]
        )
        for file in self.fileNames:
            if os.path.exists(file):
                os.remove(file)
        self.showFileLocation()

    def showFileLocation(self):
        show_in_file_manager(self.topText.get() + "_" + self.bottomText.get() + "_" + self.code.get() + '.pdf')

BarcodeGenerator()
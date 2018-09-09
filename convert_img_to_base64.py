import base64 

class ImgToBase64():
    def __init__(self):
        pass

    def convertToBase64(self, imageFileName):
        image = open(imageFileName, 'rb', -1)
        imageBytes = image.read() 
        imageBase64 = base64.encodestring(imageBytes)
        image.close()
        return imageBase64.decode("UTF-8")

if __name__ == "__main__":
    print(ImgToBase64().convertToBase64("visor_erro_formatacao.png"))
import os
from machine import Pin,I2C,SPI,PWM,Timer,ADC
import framebuf
import time
Vbat_Pin = 29

#Pin definition  引脚定义
I2C_SDA = 6
I2C_SDL = 7
I2C_INT = 17
I2C_RST = 16

DC = 8
CS = 9
SCK = 10
MOSI = 11
MISO = 12
RST = 13

BL = 25

#LCD Driver  LCD驱动
class LCD_1inch28(framebuf.FrameBuffer):
    def __init__(self): #SPI initialization  SPI初始化
        self.width = 240
        self.height = 240

        self.cs = Pin(CS,Pin.OUT)
        self.rst = Pin(RST,Pin.OUT)

        self.cs(1)
        self.spi = SPI(1,100_000_000,polarity=0, phase=0,bits= 8,sck=Pin(SCK),mosi=Pin(MOSI),miso=None)
        self.dc = Pin(DC,Pin.OUT)
        self.dc(1)
        self.buffer = bytearray(self.height * self.width * 2)
        super().__init__(self.buffer, self.width, self.height, framebuf.RGB565)
        self.init_display()

        #Define color, Micropython fixed to BRG format  定义颜色，Micropython固定为BRG格式
        self.red   =   0x07E0
        self.green =   0x001f
        self.blue  =   0xf800
        self.white =   0xffff
        self.black =   0x0000
        self.brown =   0X8430

        self.fill(self.white) #Clear screen  清屏
        self.show()#Show  显示

        self.pwm = PWM(Pin(BL))
        self.pwm.freq(5000) #Turn on the backlight  开背光

    def write_cmd(self, cmd): #Write command  写命令
        self.cs(1)
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([cmd]))
        self.cs(1)

    def write_data(self, buf): #Write data  写数据
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(bytearray([buf]))
        self.cs(1)

    def set_bl_pwm(self,duty): #Set screen brightness  设置屏幕亮度
        self.pwm.duty_u16(duty)#max 65535

    def init_display(self): #LCD initialization  LCD初始化
        """Initialize dispaly"""
        self.rst(1)
        time.sleep(0.01)
        self.rst(0)
        time.sleep(0.01)
        self.rst(1)
        time.sleep(0.05)

        self.write_cmd(0xEF)
        self.write_cmd(0xEB)
        self.write_data(0x14)

        self.write_cmd(0xFE)
        self.write_cmd(0xEF)

        self.write_cmd(0xEB)
        self.write_data(0x14)

        self.write_cmd(0x84)
        self.write_data(0x40)

        self.write_cmd(0x85)
        self.write_data(0xFF)

        self.write_cmd(0x86)
        self.write_data(0xFF)

        self.write_cmd(0x87)
        self.write_data(0xFF)

        self.write_cmd(0x88)
        self.write_data(0x0A)

        self.write_cmd(0x89)
        self.write_data(0x21)

        self.write_cmd(0x8A)
        self.write_data(0x00)

        self.write_cmd(0x8B)
        self.write_data(0x80)

        self.write_cmd(0x8C)
        self.write_data(0x01)

        self.write_cmd(0x8D)
        self.write_data(0x01)

        self.write_cmd(0x8E)
        self.write_data(0xFF)

        self.write_cmd(0x8F)
        self.write_data(0xFF)


        self.write_cmd(0xB6)
        self.write_data(0x00)
        self.write_data(0x20)

        self.write_cmd(0x36)
        self.write_data(0x98)

        self.write_cmd(0x3A)
        self.write_data(0x05)


        self.write_cmd(0x90)
        self.write_data(0x08)
        self.write_data(0x08)
        self.write_data(0x08)
        self.write_data(0x08)

        self.write_cmd(0xBD)
        self.write_data(0x06)

        self.write_cmd(0xBC)
        self.write_data(0x00)

        self.write_cmd(0xFF)
        self.write_data(0x60)
        self.write_data(0x01)
        self.write_data(0x04)

        self.write_cmd(0xC3)
        self.write_data(0x13)
        self.write_cmd(0xC4)
        self.write_data(0x13)

        self.write_cmd(0xC9)
        self.write_data(0x22)

        self.write_cmd(0xBE)
        self.write_data(0x11)

        self.write_cmd(0xE1)
        self.write_data(0x10)
        self.write_data(0x0E)

        self.write_cmd(0xDF)
        self.write_data(0x21)
        self.write_data(0x0c)
        self.write_data(0x02)

        self.write_cmd(0xF0)
        self.write_data(0x45)
        self.write_data(0x09)
        self.write_data(0x08)
        self.write_data(0x08)
        self.write_data(0x26)
        self.write_data(0x2A)

        self.write_cmd(0xF1)
        self.write_data(0x43)
        self.write_data(0x70)
        self.write_data(0x72)
        self.write_data(0x36)
        self.write_data(0x37)
        self.write_data(0x6F)


        self.write_cmd(0xF2)
        self.write_data(0x45)
        self.write_data(0x09)
        self.write_data(0x08)
        self.write_data(0x08)
        self.write_data(0x26)
        self.write_data(0x2A)

        self.write_cmd(0xF3)
        self.write_data(0x43)
        self.write_data(0x70)
        self.write_data(0x72)
        self.write_data(0x36)
        self.write_data(0x37)
        self.write_data(0x6F)

        self.write_cmd(0xED)
        self.write_data(0x1B)
        self.write_data(0x0B)

        self.write_cmd(0xAE)
        self.write_data(0x77)

        self.write_cmd(0xCD)
        self.write_data(0x63)


        self.write_cmd(0x70)
        self.write_data(0x07)
        self.write_data(0x07)
        self.write_data(0x04)
        self.write_data(0x0E)
        self.write_data(0x0F)
        self.write_data(0x09)
        self.write_data(0x07)
        self.write_data(0x08)
        self.write_data(0x03)

        self.write_cmd(0xE8)
        self.write_data(0x34)

        self.write_cmd(0x62)
        self.write_data(0x18)
        self.write_data(0x0D)
        self.write_data(0x71)
        self.write_data(0xED)
        self.write_data(0x70)
        self.write_data(0x70)
        self.write_data(0x18)
        self.write_data(0x0F)
        self.write_data(0x71)
        self.write_data(0xEF)
        self.write_data(0x70)
        self.write_data(0x70)

        self.write_cmd(0x63)
        self.write_data(0x18)
        self.write_data(0x11)
        self.write_data(0x71)
        self.write_data(0xF1)
        self.write_data(0x70)
        self.write_data(0x70)
        self.write_data(0x18)
        self.write_data(0x13)
        self.write_data(0x71)
        self.write_data(0xF3)
        self.write_data(0x70)
        self.write_data(0x70)

        self.write_cmd(0x64)
        self.write_data(0x28)
        self.write_data(0x29)
        self.write_data(0xF1)
        self.write_data(0x01)
        self.write_data(0xF1)
        self.write_data(0x00)
        self.write_data(0x07)

        self.write_cmd(0x66)
        self.write_data(0x3C)
        self.write_data(0x00)
        self.write_data(0xCD)
        self.write_data(0x67)
        self.write_data(0x45)
        self.write_data(0x45)
        self.write_data(0x10)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0x00)

        self.write_cmd(0x67)
        self.write_data(0x00)
        self.write_data(0x3C)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0x01)
        self.write_data(0x54)
        self.write_data(0x10)
        self.write_data(0x32)
        self.write_data(0x98)

        self.write_cmd(0x74)
        self.write_data(0x10)
        self.write_data(0x85)
        self.write_data(0x80)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0x4E)
        self.write_data(0x00)

        self.write_cmd(0x98)
        self.write_data(0x3e)
        self.write_data(0x07)

        self.write_cmd(0x35)
        self.write_cmd(0x21)

        self.write_cmd(0x11)

        self.write_cmd(0x29)

    #设置窗口
    def setWindows(self,Xstart,Ystart,Xend,Yend):
        self.write_cmd(0x2A)
        self.write_data(0x00)
        self.write_data(Xstart)
        self.write_data(0x00)
        self.write_data(Xend-1)

        self.write_cmd(0x2B)
        self.write_data(0x00)
        self.write_data(Ystart)
        self.write_data(0x00)
        self.write_data(Yend-1)

        self.write_cmd(0x2C)

    #Show  显示
    def show(self):
        self.setWindows(0,0,self.width,self.height)

        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(self.buffer)
        self.cs(1)
        

    def show_image(self, image_path):
        # Open the BMP file
        with open(image_path, 'rb') as f:
            # Read the BMP header (54 bytes)
            header = f.read(54)

            # Extract width and height from the header
            width = header[18] + (header[19] << 8)
            height = header[22] + (header[23] << 8)

            # Check if the image size matches the display size
            if width != self.width or height != self.height:
                raise ValueError("Image must be 240x240 pixels.")

            # Create a buffer for the image
            buffer = bytearray(self.height * self.width * 2)  # 2 bytes per pixel for RGB565

            # Read pixel data
            for y in range(height):
                for x in range(width):
                    # Read 3 bytes for each pixel (BGR format)
                    pixel_data = f.read(3)  # Read Blue, Green, Red

                    # Check if we read 3 bytes
                    if len(pixel_data) < 3:
                        raise ValueError("Unexpected end of file while reading pixel data.")

                    b = pixel_data[0]  # Blue
                    g = pixel_data[1]  # Green
                    r = pixel_data[2]  # Red

                    # Convert RGB to RGB565 format
                    rgb565 = ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)

                    # Write to buffer (2 bytes per pixel)
                    buffer[(y * width + x) * 2] = (rgb565 >> 8) & 0xFF  # High byte
                    buffer[(y * width + x) * 2 + 1] = rgb565 & 0xFF      # Low byte

            # Set the buffer to the LCD's buffer
            self.buffer = buffer  # Update the LCD's buffer
            self.setWindows(0, 0, self.width, self.height)  # Set the window for the display

            # Send the buffer to the display
            self.cs(1)
            self.dc(1)
            self.cs(0)
            self.spi.write(self.buffer)
            self.cs(1)

    '''
        Partial display, the starting point of the local
        display here is reduced by 10, and the end point
        is increased by 10
    '''
    #Partial display, the starting point of the local display here is reduced by 10, and the end point is increased by 10
    #局部显示，这里的局部显示起点减少10，终点增加10
    def Windows_show(self,Xstart,Ystart,Xend,Yend):
        if Xstart > Xend:
            data = Xstart
            Xstart = Xend
            Xend = data

        if (Ystart > Yend):
            data = Ystart
            Ystart = Yend
            Yend = data

        if Xstart <= 10:
            Xstart = 10
        if Ystart <= 10:
            Ystart = 10

        Xstart -= 10;Xend += 10
        Ystart -= 10;Yend += 10

        self.setWindows(Xstart,Ystart,Xend,Yend)
        self.cs(1)
        self.dc(1)
        self.cs(0)
        for i in range (Ystart,Yend-1):
            Addr = (Xstart * 2) + (i * 240 * 2)
            self.spi.write(self.buffer[Addr : Addr+((Xend-Xstart)*2)])
        self.cs(1)

    #Write characters, size is the font size, the minimum is 1
    #写字符，size为字体大小,最小为1
    def write_text(self,text,x,y,size,color):
        ''' Method to write Text on OLED/LCD Displays
            with a variable font size

            Args:
                text: the string of chars to be displayed
                x: x co-ordinate of starting position
                y: y co-ordinate of starting position
                size: font size of text
                color: color of text to be displayed
        '''
        background = self.pixel(x,y)
        info = []
        # Creating reference charaters to read their values
        self.text(text,x,y,color)
        for i in range(x,x+(8*len(text))):
            for j in range(y,y+8):
                # Fetching amd saving details of pixels, such as
                # x co-ordinate, y co-ordinate, and color of the pixel
                px_color = self.pixel(i,j)
                info.append((i,j,px_color)) if px_color == color else None
        # Clearing the reference characters from the screen
        self.text(text,x,y,background)
        # Writing the custom-sized font characters on screen
        for px_info in info:
            self.fill_rect(size*px_info[0] - (size-1)*x , size*px_info[1] - (size-1)*y, size, size, px_info[2])

def load_image_to_buffer(image_path):
    # Open the BMP file
    with open(image_path, 'rb') as f:
        # Read the BMP header (54 bytes)
        header = f.read(54)
        
        # Extract width and height from the header
        width = header[18] + (header[19] << 8)
        height = header[22] + (header[23] << 8)

        # Check if the image size matches the display size
        if width != 240 or height != 240:
            raise ValueError("Image must be 240x240 pixels.")

        # Create a buffer for the image
        buffer = bytearray(240 * 240)  # Assuming 16-bit color depth (RGB565)

        # Read pixel data
        for y in range(height):
            for x in range(width):
                # Each pixel is represented by 3 bytes (BGR)
                b = ord(f.read(1))  # Blue
                g = ord(f.read(1))  # Green
                r = ord(f.read(1))  # Red

                # Convert RGB to RGB565 format
                rgb565 = ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)
                print(rgb565)

                # Write to buffer (2 bytes per pixel)
                buffer[(y * width + x) * 2] = (rgb565 >> 8) & 0xFF  # High byte
                buffer[(y * width + x) * 2 + 1] = rgb565 & 0xFF     # Low byte

        # Set the buffer to the LCD's buffer
        LCD.buffer = buffer  # Assuming LCD has a buffer attribute

    return buffer


def load_images(folder):
    images = []
    try:
        for filename in os.listdir(folder):
            if filename.endswith('.bmp'):  # Assuming BMP format for images
                images.append(folder + '/' + filename)
        images.sort()  # Sort images alphabetically
    except OSError as e:
        print(f"Error accessing folder '{folder}': {e}")
    return images

# Function to show images in a slideshow
def slideshow(images, dwell):
    while True:
        for image in images:
            LCD.show_image(image)  # Show the image directly
            time.sleep(dwell)  # Wait for the specified dwell time
            
# Main execution block
if __name__ == '__main__':
    # Initialize the display
    LCD = LCD_1inch28()  # Create an instance of the LCD
    LCD.set_bl_pwm(65535)  # Set backlight to maximum brightness

    # Initialize the touch controller, passing the LCD instance
    #Touch = Touch_CST816T(mode=1, LCD=LCD)  # Adjust mode as necessary

    # Load images from the folder
    image_folder = "/images"
    images = load_images(image_folder)

    # Start the slideshow with a dwell time of 60 seconds
    slideshow(images, 5)




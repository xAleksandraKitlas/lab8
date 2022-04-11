#innowacyjnosc:
#jako pierwszy modul zrobilam prosta wersje painta
# mozna wybrac kolor i grubosc pena, a takze kolor tla
# jako drugi projekt wybralam gre na podstawie retro gry tron
# gracz pierwszy(czerwony) -> sterowanie WASD
# gracz drugi(zolty) -> sterowanie strzalki


from tkinter import *
import pygame
import sys
from tkinter import ttk, colorchooser

def button1Action():
    window.destroy()
    pygame.init()
    width = 600
    height = 500
    display = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Tron 2D")
    clock = pygame.time.Clock()

    background = (27, 79, 114)
    black = (0, 0, 0)
    yellow = (241, 196, 15)
    darkYellow = (247, 220, 111)
    red = (231, 76, 60)
    darkRed = (241, 148, 138)
    darkBlue = (40, 116, 166)

    font = pygame.font.SysFont("comicsansms", 35)

    w = 10

    # klasa naszego motoru
    class tronBike:
        def __init__(self, number, color, darkColor, side):
            self.w = w
            self.h = w
            self.x = abs(side - 100)
            self.y = height / 2 - self.h
            self.speed = 10
            self.color = color
            self.darkColor = darkColor
            self.history = [[self.x, self.y]]
            self.number = number
            self.length = 1

        # rysujemy motor na planszy
        def draw(self):
            for i in range(len(self.history)):
                if i == self.length - 1:
                    pygame.draw.rect(display, self.darkColor, (self.history[i][0], self.history[i][1], self.w, self.h))
                else:
                    pygame.draw.rect(display, self.color, (self.history[i][0], self.history[i][1], self.w, self.h))

        # poruszanie sie
        def move(self, xdir, ydir):
            self.x += xdir * self.speed
            self.y += ydir * self.speed
            self.history.append([self.x, self.y])
            self.length += 1
            if self.x < 0 or self.x > width or self.y < 0 or self.y > height:
                gameOver(self.number)

        # sprawdzamy kolizje
        def checkIfHit(self, opponent):
            if abs(opponent.history[opponent.length - 1][0] - self.history[self.length - 1][0]) < self.w and abs(
                    opponent.history[opponent.length - 1][1] - self.history[self.length - 1][1]) < self.h:
                gameOver(0)
            for i in range(opponent.length):
                if abs(opponent.history[i][0] - self.history[self.length - 1][0]) < self.w and abs(
                        opponent.history[i][1] - self.history[self.length - 1][1]) < self.h:
                    gameOver(self.number)

            for i in range(len(self.history) - 1):
                if abs(self.history[i][0] - self.x) < self.w and abs(
                        self.history[i][1] - self.y) < self.h and self.length > 2:
                    gameOver(self.number)

    # kiedy bedzie koniec gry
    def gameOver(number):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    close()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        close()
                    if event.key == pygame.K_r:
                        tron()
            if number == 0:
                text = font.render("Gacze zdezyli sie!", True, black)
            else:
                text = font.render("Gracz %d przegral!" % (number), True, black)

            display.blit(text, (50, height / 2))

            pygame.display.update()
            clock.tick(60)

    def drawGrid():
        squares = 50
        for i in range(int(width / squares)):
            pygame.draw.line(display, darkBlue, (i * squares, 0), (i * squares, height))
            pygame.draw.line(display, darkBlue, (0, i * squares), (width, i * squares))

    def close():
        pygame.quit()
        sys.exit()

    def tron():
        loop = True

        bike1 = tronBike(1, red, darkRed, 0)
        bike2 = tronBike(2, yellow, darkYellow, width)

        x1 = 1
        y1 = 0
        x2 = -1
        y2 = 0

        while loop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    close()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        close()
                    if event.key == pygame.K_UP:
                        if not (x2 == 0 and y2 == 1):
                            x2 = 0
                            y2 = -1
                    if event.key == pygame.K_DOWN:
                        if not (x2 == 0 and y2 == -1):
                            x2 = 0
                            y2 = 1
                    if event.key == pygame.K_LEFT:
                        if not (x2 == 1 and y2 == 0):
                            x2 = -1
                            y2 = 0
                    if event.key == pygame.K_RIGHT:
                        if not (x2 == -1 and y2 == 0):
                            x2 = 1
                            y2 = 0
                    if event.key == pygame.K_w:
                        if not (x1 == 0 and y1 == 1):
                            x1 = 0
                            y1 = -1
                    if event.key == pygame.K_s:
                        if not (x1 == 0 and y1 == -1):
                            x1 = 0
                            y1 = 1
                    if event.key == pygame.K_a:
                        if not (x1 == 1 and y1 == 0):
                            x1 = -1
                            y1 = 0
                    if event.key == pygame.K_d:
                        if not (x1 == -1 and y1 == 0):
                            x1 = 1
                            y1 = 0

            display.fill(background)
            drawGrid()
            bike1.draw()
            bike2.draw()

            bike1.move(x1, y1)
            bike2.move(x2, y2)

            bike1.checkIfHit(bike2)
            bike2.checkIfHit(bike1)

            pygame.display.update()
            clock.tick(10)

    tron()

def button2Action():
    window.destroy()
    class main:
        def __init__(self, master):
            self.master = master
            self.color_fg = 'black'
            self.color_bg = 'white'
            self.old_x = None
            self.old_y = None
            self.penwidth = 5
            self.drawWidgets()
            self.c.bind('<B1-Motion>', self.paint)  # rysowanie linii
            self.c.bind('<ButtonRelease-1>', self.reset)

        def paint(self, e):
            if self.old_x and self.old_y:
                self.c.create_line(self.old_x, self.old_y, e.x, e.y, width=self.penwidth, fill=self.color_fg,
                                   capstyle=ROUND, smooth=True)

            self.old_x = e.x
            self.old_y = e.y

        def reset(self, e):  # czyscimy nasz obrazek
            self.old_x = None
            self.old_y = None

        def changeW(self, e):  # zmiana grubosci dlugopisu
            self.penwidth = e

        def clear(self):
            self.c.delete(ALL)

        def change_fg(self):  # zmiana koloru dlugopisu
            self.color_fg = colorchooser.askcolor(color=self.color_fg)[1]

        def change_bg(self):  # zmiana koloru tla
            self.color_bg = colorchooser.askcolor(color=self.color_bg)[1]
            self.c['bg'] = self.color_bg

        def drawWidgets(self):
            self.controls = Frame(self.master, padx=5, pady=5)
            Label(self.controls, text='Grubosc Pena:', font=('arial 18')).grid(row=0, column=0)
            self.slider = ttk.Scale(self.controls, from_=5, to=100, command=self.changeW, orient=HORIZONTAL)
            self.slider.set(self.penwidth)
            self.slider.grid(row=0, column=1, ipadx=30)
            self.controls.pack(side=LEFT)

            self.c = Canvas(self.master, width=500, height=500, bg=self.color_bg, )
            self.c.pack(fill=BOTH, expand=True)

            menu = Menu(self.master)
            self.master.config(menu=menu)
            filemenu = Menu(menu)
            colormenu = Menu(menu)
            menu.add_cascade(label='Kolory', menu=colormenu)
            colormenu.add_command(label='Kolor Pena', command=self.change_fg)
            colormenu.add_command(label='Kolor tla', command=self.change_bg)
            optionmenu = Menu(menu)
            menu.add_cascade(label='Opcje', menu=optionmenu)
            optionmenu.add_command(label='Czysc rysunek', command=self.clear)
            optionmenu.add_command(label='Wyjdz', command=self.master.destroy)

    if __name__ == '__main__':
        root = Tk()
        main(root)
        root.title('Mini Paint')
        root.mainloop()

'''
ALGORYTM RYSOWANIA KRZYWYCH BEZIERA
    for(double t =0.0; t<1.0; t+=0.005)
        {
            double xt = Math.pow(1-t, 3)*x[0]+3*t*Math.pow(1-t,2)*x[1] + 3 *Math.pow(t,2)*(1-t)*x[2] + Math.pow(t,3)*x[3];
            double yt = Math.pow(1-t, 3)*y[0]+3*t*Math.pow(1-t,2)*y[1] + 3 *Math.pow(t,2)*(1-t)*y[2]+ Math.pow(t,3)*y[3];
            putpoint(xt,yt);
        }
'''



def closeWindow():
    window.destroy()

# #
window = Tk()
window.title("PROJEKT 1")
window.geometry("500x400")
window.configure(bg= "white")
label1 = Label(window, text="Gra TRON", fg="blue", height=1, width=10, bg= "white")
label1.pack()
button1 = Button(window, text ="Zagraj!", fg="blue", command = button1Action, height=2, width=10)
button1.pack()

label2 = Label(window, text="Mini Paint", fg="red", height=1, width=10, bg= "white")
label2.pack()
button2 = Button(window, text ="Narysuj cos!", fg="red", command = button2Action, height=2, width=10)
button2.pack()

label3 = Label(window, text="Bezier curves", fg="black", height=1, width=10, bg= "white")
label3.pack()
button3 = Button(window, text ="Zobacz!", fg="black", height=2, width=10)
button3.pack()

label4 = Label(window, text="Bezier surfaces", fg="green", height=1, width=10, bg= "white")
label4.pack()
button4 = Button(window, text ="Zobacz!", fg="green", height=2, width=10)
button4.pack()

label5 = Label(window, text="", fg="green", height=1,  width=10, bg= "white")
label5.pack()
button5 = Button(window, text ="wyjdz!", fg="grey", height=2, width=6, command=closeWindow)
button5.pack()

window.mainloop()

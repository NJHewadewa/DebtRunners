from SimpleGUICS2Pygame import simpleguics2pygame as simplegui

class hud():
    def __init__(self,visible=False,canvasHeight=700):
        self.visible = visible
        self.canvasHeight = canvasHeight

    def draw(self,canvas,lives,health,score,gun,money):
        offset = 100
        image = simplegui.load_image('https://raw.githubusercontent.com/NJHewadewa/DebtRunners/master/Sprites/HRT.png')
        if self.visible == True:
            for x in range(lives):
                canvas.draw_image(image, (896 / 2, 896 / 2), (896, 896), [offset+(50*x),self.canvasHeight-68], (64, 64))
            canvas.draw_polygon([[250,620],[(250+health),620],[(250+health),645],[250,645]], 1, 'Black', 'Red')
            canvas.draw_text(str(health), [250,670], 15, 'Red')
            StringScore = "Score: " + str(score)
            canvas.draw_text(StringScore,[1050,635],20,'Yellow')
            CurrentGun = "Gun: " + gun
            canvas.draw_text(CurrentGun, [850, 635], 20, 'Yellow')
            CurrentMoney = "£ " + str(money)
            canvas.draw_text(CurrentMoney, [750, 635], 20, 'Yellow')

    def setVisible(self,newVisiblility):
        self.visible = newVisiblility




class hud():
    def __init__(self,visible=False,canvasHeight=700):
        self.visible = visible
        self.canvasHeight = canvasHeight

    def draw(self,canvas,lives,health):
        offset = 100
        if self.visible == True:
            for x in range(lives):
                canvas.draw_circle([offset+(50*x),self.canvasHeight-90],15,10,'Black','Red')
            canvas.draw_polygon([[250,600],[(250+health),600],[(250+health),625],[250,625]], 1, 'Black', 'Red')
            canvas.draw_text(str(health), [250,650], 15, 'Red')

    def setVisible(self,newVisiblility):
        self.visible = newVisiblility

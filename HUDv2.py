class hud():
    def __init__(self,visible=False,canvasHeight=700):
        self.visible = visible
        self.canvasHeight = canvasHeight

    def draw(self,canvas,lives,health):
        offset = 100
        if self.visible == True:
            for x in range(lives):
		
                canvas.draw_circle([offset+(50*x),self.canvasHeight-40],15,10,'Black','Red')
	    canvas.draw_text(("Lives: "), (20,670), 20, 'Green')
            canvas.draw_polygon([[250,650],[(250+100),650],[(250+100),675],[250,675]], 1, 'Black', 'Green')
            canvas.draw_text(("HP: "), [215,670], 20, 'Green')

    def setVisible(self,newVisiblility):
self.visible = newVisiblility
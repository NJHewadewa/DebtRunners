try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

levelname = "startmenu"
title = "Debt Runners"
maintext = ""
background = simplegui.load_image("https://businessfirstfamily.com/wp-content/uploads/2017/12/consider-debt-consolidation.jpg")
background2 = simplegui.load_image("https://ksr-ugc.imgix.net/assets/014/840/017/401808e191e0c25e8577d7d7d2c49251_original.png?crop=faces&w=1552&h=873&fit=crop&v=1496716514&auto=format&q=92&s=2c65f0228772a91c7de95531eed647c2")
sound = simplegui.load_sound("https://youtu.be/GGXzlRoNtHU")
sound.set_volume(1)

def draw(canvas):  # Drawing objects
    if levelname == "instructions":
        canvas.draw_image(background2, (1553 / 2, 873 / 2), (1552, 873), (1200 / 2, 720 / 2), (1200, 720))
        canvas.draw_text(title, [440, 112], 69, "Black", "monospace")
        canvas.draw_text("Instructions go here", [450, 200], 48, "Black")
        canvas.draw_text("", [10, 320], 46, "Green")
        canvas.draw_text(maintext, [10, 100], 52, "Orange")


    elif levelname == "startmenu":
        canvas.draw_image(background, (2200/2, 1125/2), (2200, 1125), (1200/2, 720/2), (1200, 720))
        canvas.draw_text(title, [380, 112], 69, "Black", "monospace")
        canvas.draw_text("Start", [470, 340], 52, "Black")
        canvas.draw_text("Instructions", [470, 400], 52, "Black")
        canvas.draw_text("Quit", [470, 460], 52, "Black")
        sound.play()

def mouse_handler(position):  # Buttons activity
    global levelname
    x, y = position

    if 450 < x < 580 and 360 < y < 400:
        levelname = "instructions"
        instructions()

    elif 400 < x < 640 and 420 < y < 460:
        levelname = "quit"
        quit()

    elif 5 < x < 200 and 50 < y < 300 and levelname == "instructions":
        levelname = "startmenu"
        startmenu()


    elif levelname == "":
        return
    elif levelname == "":
        return


# Running the stuff
def instructions():
    global title, levelname, maintext
    title = "Instructions"
    maintext = "Back"


def startmenu():
    global title, levelname, maintext
    title = "Debt Runners"

frame = simplegui.create_frame("Dept Runners", 1200, 720)
frame.set_canvas_background('White')
frame.set_draw_handler(draw)
frame.set_mouseclick_handler(mouse_handler)
frame.start()
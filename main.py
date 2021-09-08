import math

from browser import document, bind, window, ajax
from browser.widgets.dialog import InfoDialog

head_radius = 20/320
body_length = 40/320
arm_length = 40/320
leg_length = 40/320
word = ""

class Panel:

    def __init__(self, canvas):
        self.ctx = canvas.getContext("2d")
        self.x = canvas.width / 2
        self.y = canvas.height / 2
        self.score = 0
        self.guesses = 10

    def drawGallows(self):
        self.ctx.clearRect(0, 0, canvas.width, canvas.height)
        ctx = self.ctx
        ctx.beginPath()
        ctx.moveTo(self.x - canvas.width/4, canvas.height * 0.99)
        ctx.lineTo(self.x + canvas.width/4, canvas.height * 0.99)
        ctx.moveTo(self.x , canvas.height * 0.99)
        ctx.lineTo(self.x , canvas.height * 0.25)
        ctx.lineTo(self.x + head_radius*canvas.height * 2, canvas.height*0.25)
        ctx.lineTo(self.x + head_radius*canvas.height * 2, self.y - head_radius*canvas.height)
        ctx.stroke()
        ctx.closePath()
    
    def drawHangman(self, counter):
        if counter == 1:
            self.drawHead()
        if counter == 2:
            self.drawBody()
        if counter == 3:
            self.drawLeftArm()
        if counter == 4:
            self.drawRightArm()
        if counter == 5:
            self.drawLeftLeg()
        if counter == 6:
            self.drawRightLeg()
            
    def drawHead(self):
        ctx = self.ctx
        ctx.beginPath()
        ctx.arc(self.x + head_radius*canvas.height * 2, self.y, head_radius*canvas.height, 0, math.pi * 2)
        ctx.stroke()
        ctx.closePath()
    
    def drawBody(self):
        ctx = self.ctx
        ctx.beginPath()
        ctx.moveTo(self.x+ head_radius*canvas.height * 2, self.y + head_radius*canvas.height)
        ctx.lineTo(self.x+ head_radius*canvas.height * 2, self.y + head_radius*canvas.height + body_length*canvas.height)
        ctx.stroke()
        ctx.closePath()
 
    def drawLeftArm(self):
        ctx = self.ctx
        ctx.beginPath()
        ctx.moveTo(self.x+ head_radius*canvas.height * 2, self.y + head_radius*canvas.height + 0.2*body_length*canvas.height)
        ctx.lineTo(self.x+ head_radius*canvas.height * 2 - arm_length*canvas.height/math.sqrt(2), self.y + head_radius*canvas.height + arm_length*canvas.height/math.sqrt(2))
        ctx.stroke()
        ctx.closePath()

    def drawRightArm(self):
        ctx = self.ctx
        ctx.beginPath()
        ctx.moveTo(self.x+ head_radius*canvas.height * 2, self.y + head_radius*canvas.height+ 0.2*body_length*canvas.height)
        ctx.lineTo(self.x+ head_radius*canvas.height * 2 + arm_length*canvas.height/math.sqrt(2), self.y + head_radius*canvas.height + arm_length*canvas.height/math.sqrt(2))
        ctx.stroke()
        ctx.closePath()
        
    def drawLeftLeg(self):
        ctx = self.ctx
        ctx.beginPath()
        ctx.moveTo(self.x+ head_radius*canvas.height * 2, self.y + head_radius*canvas.height + body_length*canvas.height)
        ctx.lineTo(self.x+ head_radius*canvas.height * 2 - leg_length*canvas.height/math.sqrt(2), self.y + head_radius*canvas.height + body_length*canvas.height + leg_length*canvas.height/math.sqrt(2))
        ctx.stroke()
        ctx.closePath()
        
    def drawRightLeg(self):
        ctx = self.ctx
        ctx.beginPath()
        ctx.moveTo(self.x+ head_radius*canvas.height * 2, self.y + head_radius*canvas.height + body_length*canvas.height)
        ctx.lineTo(self.x+ head_radius*canvas.height * 2 + leg_length*canvas.height/math.sqrt(2), self.y + head_radius*canvas.height + body_length*canvas.height + leg_length*canvas.height/math.sqrt(2))
        ctx.stroke()
        ctx.closePath()
        




    
def get_word():
    ajax.get("https://random-word-api.herokuapp.com/word?number=1",
              timeout=5,
              cache = True,
             oncomplete=show_word)


def show_word(req):
    global word 
    word = req.text[2:-2]
    display = "_ "*len(word)
    top.html = display
    

def new_game():
    global guessed_set
    global counter
    global panel
    global guessed_text
    
    guessed_text = document["guessed_letters"]
    guessed_text.text = ""
    guessed_set = set()
    get_word()
    counter = 0
    panel = Panel(document["myCanvas"])
    panel.drawGallows()
  

# the entry field has the id "guess"
def charCode(ev):
    global word
    global guessed_set
    global guessed_text
    global counter
    global panel
    global top
    
    word_set = set([letter for letter in word])
    if ev.keyCode == 13:
        input_field = document["input"]
        warning = document["warning"]
        if input_field.value.lower() in "abcdefghijklmnopqrstuvwxyz":
            warning.text = ""
            char = input_field.value.lower()
            if char not in guessed_set:
                guessed_set.add(char)
                guessed_text.text += char 
                if char not in word:
                    counter += 1
                    panel.drawHangman(counter)
                    if counter == 6:
                        message = "You Lose!"
                        InfoDialog("", message, ok="Play again?")
                        new_game()
                        top.html = word
                else:
                    display = "".join(["_ " if letter not in guessed_set else letter for letter in word])
                    top.html = display
                    if counter < 6 and "_" not in display:
                        InfoDialog("", "You win!", ok="Play again?")
            else:
                warning.text = "Your already guessed the letter " + char
                    
        else:
            warning.text = "Please type a letter that's in the English alphabet!"
        input_field.value = ""  # reset input filed value after last input



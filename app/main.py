import math
from browser import document, bind, window, ajax
from browser.widgets.dialog import InfoDialog





class Panel:

    def __init__(self, canvas):
        self.ctx = canvas.getContext("2d")
        self.center_x = canvas.width / 2
        self.center_y = canvas.height / 2
        self.score = 0
        self.guesses = 10
        self.head_radius = 0.1
        self.body_length = 0.2
        self.arm_length = 0.2
        self.leg_length = 0.2
        self.gallows_height = 0.8

    def draw_gallows(self, canvas):
        self.ctx.clearRect(0, 0, canvas.width, canvas.height)
        ctx = self.ctx
        ctx.beginPath()
        ctx.moveTo(self.center_x - canvas.width/4, canvas.height * 0.99)
        ctx.lineTo(self.center_x + canvas.width/4, canvas.height * 0.99)
        ctx.moveTo(self.center_x , canvas.height * 0.99)
        ctx.lineTo(self.center_x , self.gallows_height)
        ctx.lineTo(self.center_x + self.head_radius*canvas.height * 2, self.gallows_height)
        ctx.lineTo(self.center_x + self.head_radius*canvas.height * 2, self.center_y - self.head_radius*canvas.height)
        ctx.stroke()
        ctx.closePath()
    
    def draw_hangman(self, counter):
        ctx = self.ctx
        ctx.beginPath()
        if counter == 1: # draw head
            ctx.arc(self.center_x + self.head_radius*canvas.height * 2, self.center_y, self.head_radius*canvas.height, 0, math.pi * 2)
            ctx.stroke()
        if counter == 2: # draw body
            ctx.moveTo(self.center_x+ self.head_radius*canvas.height * 2, self.center_y + self.head_radius*canvas.height)
            ctx.lineTo(self.center_x+ self.head_radius*canvas.height * 2, self.center_y + self.head_radius*canvas.height + self.body_length*canvas.height)
            ctx.stroke()
        if counter == 3: # draw left arm
            ctx.moveTo(self.center_x+ self.head_radius*canvas.height * 2, self.center_y + self.head_radius*canvas.height + 0.2*self.body_length*canvas.height)
            ctx.lineTo(self.center_x+ self.head_radius*canvas.height * 2 - self.arm_length*canvas.height/math.sqrt(2), self.center_y + self.head_radius*canvas.height + self.arm_length*canvas.height/math.sqrt(2))
            ctx.stroke()
        if counter == 4: # draw right arm
            ctx.moveTo(self.center_x+ self.head_radius*canvas.height * 2, self.center_y + self.head_radius*canvas.height+ 0.2*self.body_length*canvas.height)
            ctx.lineTo(self.center_x+ self.head_radius*canvas.height * 2 + self.arm_length*canvas.height/math.sqrt(2), self.center_y + self.head_radius*canvas.height + self.arm_length*canvas.height/math.sqrt(2))
            ctx.stroke()
        if counter == 5: # draw left leg
            ctx.moveTo(self.center_x+ self.head_radius*canvas.height * 2, self.center_y + self.head_radius*canvas.height + self.body_length*canvas.height)
            ctx.lineTo(self.center_x+ self.head_radius*canvas.height * 2 - self.leg_length*canvas.height/math.sqrt(2), self.center_y + self.head_radius*canvas.height + self.body_length*canvas.height + self.leg_length*canvas.height/math.sqrt(2))
            ctx.stroke()        
        if counter == 6: # draw right leg
            ctx.moveTo(self.center_x+ self.head_radius*canvas.height * 2, self.center_y + self.head_radius*canvas.height + self.body_length*canvas.height)
            ctx.lineTo(self.center_x+ self.head_radius*canvas.height * 2 - self.leg_length*canvas.height/math.sqrt(2), self.center_y + self.head_radius*canvas.height + self.body_length*canvas.height + self.leg_length*canvas.height/math.sqrt(2))
            ctx.stroke()
            
 
    
def get_word():
    "get a random word from the random word API"
    ajax.get("https://random-word-api.herokuapp.com/word?number=1",
              timeout=5,
              cache = True,
             oncomplete=show_word)


def show_word(req):
    global word 
    global top
    word = req.text[2:-2]
    display = "_ "*len(word)
    top.html = display
    

def new_game():
    global guessed_set
    global counter
    global panel
    global guessed_text
    global word 
    global top
    global canvas
    
    word = ""
    
    guessed_text = document["guessed_letters"]
    guessed_text.text = ""
    guessed_set = set()
    get_word()
    counter = 0
    
    canvas = document["myCanvas"]
    panel = Panel(canvas)
    panel.draw_gallows(canvas)
    document["input"].bind("keypress", check)
    top = document["top"]

# the entry field has the id "guess"
def check(ev):
    global word
    global guessed_set
    global guessed_text
    global counter
    global panel
    global top
    
    word_set = set([letter for letter in word])
    if ev.keyCode == 13:
        input_field = document["input"]
        message = document["message"]
        if input_field.value.lower() in "abcdefghijklmnopqrstuvwxyz":
            message.text = ""
            char = input_field.value.lower()
            if char not in guessed_set:
                guessed_set.add(char)
                if len(guessed_set) == 1:
                    guessed_text.text += char
                else:
                    guessed_text.text += (', ' +char) 
                if char not in word:
                    counter += 1
                    panel.draw_hangman(counter)
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
                message.text = 'You already guessed the letter "' + char + '"!'
                    
        else:
            message.text = "Please type a letter that's in the English alphabet!"
        input_field.value = ""  # reset input filed value after last input


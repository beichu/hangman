import math
from browser import document, bind, window, ajax, html
from browser.widgets.dialog import Dialog
import json


class Panel:

    def __init__(self, canvas):
        self.ctx = canvas.getContext("2d")
        self.ctx.clearRect(0, 0, canvas.width, canvas.height)

    def draw_gallows(self, canvas):
        ctx = self.ctx
        ctx.beginPath()
        ctx.moveTo(canvas.width*0.25, canvas.height)
        ctx.lineTo(canvas.width*0.75, canvas.height)
        ctx.moveTo(canvas.width*0.5, canvas.height)
        ctx.lineTo(canvas.width*0.5, 0)
        ctx.lineTo(canvas.width*0.6, 0)
        ctx.lineTo(canvas.width*0.6, canvas.height*0.25)
        ctx.stroke()

    
    def draw_hangman(self, canvas, counter):
        ctx = self.ctx
        ctx.beginPath()
        if counter == 1: # draw head
            ctx.arc(canvas.width*0.6, 
                    canvas.height*0.35, 
                    0.1 * canvas.height, 
                    0, math.pi * 2)
            ctx.stroke()
        if counter == 2: # draw body
            ctx.moveTo(canvas.width*0.6, 
                       canvas.height*0.45)
            ctx.lineTo(canvas.width*0.6, 
                       canvas.height*0.65)
            ctx.stroke()
        if counter == 3: # draw left arm
            ctx.moveTo(canvas.width*0.6, 
                       canvas.height*0.55)
            ctx.lineTo(canvas.width*0.6-canvas.height*0.14, 
                       canvas.height*0.41)
            ctx.stroke()
        if counter == 4: # draw right arm
            ctx.moveTo(canvas.width*0.6, 
                       canvas.height*0.55)
            ctx.lineTo(canvas.width*0.6+canvas.height*0.14, 
                       canvas.height*0.41)
            ctx.stroke()
        if counter == 5: # draw left leg
            ctx.moveTo(canvas.width*0.6, 
                       canvas.height*0.65)
            ctx.lineTo(canvas.width*0.6-canvas.height*0.14, 
                       canvas.height*0.8)
            ctx.stroke()        
        if counter == 6: # draw right leg
            ctx.moveTo(canvas.width*0.6, 
                       canvas.height*0.65)
            ctx.lineTo(canvas.width*0.6+canvas.height*0.14, 
                       canvas.height*0.8)
            ctx.stroke()
            
 
class Game:

    def __init__(self):
        "initialize the game"
        self.canvas = document["my_canvas"]       
        self.panel = Panel(self.canvas)
        self.panel.draw_gallows(self.canvas)
        
        self.message_div = document["message"]
        self.guessed_div = document["guessed_letters"]
        self.message_div.text = ""
        self.guessed_div.text = ""
        self.top_div = document["top_word"]
        
        self.guessed_set = set()

        self.counter = 0
        self.word = self.get_word()
        
        document["input"].bind("keypress", self.check)      
        document["hint"].bind("click", self.get_def)

    
    def get_def(self, ev):
        "get word def from the free dictionary api"
        print('here')
        url = "https://api.dictionaryapi.dev/api/v2/entries/en/{word}".format(word = self.word)
        ajax.get(url, timeout = 15, cache = True, oncomplete=self.show_hint)

    
    def get_word(self):
        "get a random word from the random word API"
        ajax.get("https://random-word-api.herokuapp.com/word?number=1",
                  timeout=5,
                  cache = True,
                 oncomplete=self.show_word)
    



    def show_word(self, req):
        "display the word as a series of underscores"
        self.word = req.text[2:-2]
        self.top_div.html = "_ "*len(self.word)

    
    def show_hint(self, req):
        print(req.text)
        try:
            if "No Definitions Found" in req.text:
                word_def = "Sorry, no hint available."
            else:
                word_def = str(json.loads(req.text[1:-1])['meanings'][0]['definitions'][0]['definition'])
            self.message_div.text = 'Hint: ' + word_def
        except:
            pass
    
    def show_dialogue(self, status):
        d = Dialog('', default_css=False, ok_cancel=True)
        @bind(d.ok_button, "click")
        def ok(ev):
            "Event handler for ok button"
            self.__init__()
            document["input"].unbind("keypress", self.check)
            d.close()
                
        
        if status == 'lose':
            d.panel <= html.DIV("You Lose!<br>Play Again?")
        else:
            d.panel <= html.DIV("You Win!<br>Play Again?")



    def check(self, ev):
        input_field = document["input"]
        if ev.keyCode == 13: # 13 is the code for the "Enter" key    
            letter = input_field.value.lower() # convert to lower case where possible
            if (not (letter.isalpha()) or (len(letter) != 1)): 
                self.message_div.text = "Please type a valid English letter!"
            else: # input is valid
                self.message_div.text = ""
                if letter not in self.guessed_set:
                    self.guessed_set.add(letter)
                    if len(self.guessed_set) == 1:
                        self.guessed_div.text = letter
                    else:
                        self.guessed_div.text += (', ' + letter)
                    if letter not in self.word:
                        self.counter += 1
                        self.panel.draw_hangman(self.canvas, self.counter)
                        if self.counter == 6:
                            self.top_div.html = self.word
                            self.show_dialogue('lose')  
                    else: # letter in word
                        display = "".join(["_ " if letter not in self.guessed_set else letter for letter in self.word]) 
                        self.top_div.html = display
                        if self.counter < 6 and "_" not in display:
                            self.show_dialogue('win')
                
                else:
                    self.message_div.text = 'You already guessed the letter "' + letter + '"!'    
            
            input_field.value = ""  # reset input filed value after last input


game = Game()
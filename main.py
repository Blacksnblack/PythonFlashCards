import tkinter as tk
from tkinter import filedialog
from PyQt5.QtWidgets import QApplication

fullCard = False
cardIndex = 0
fbIndex = 0
cards = []
card, fileLabel = None, None
filename = ""
# Constants
horizontalRule = "-" * 40
WIDTH = 400
HEIGHT = 400
openingMessage = "To begin, click the \n\"Open File\" button above and \nselect a file formatted for " \
                 "\nflashcards " \
                 "\n\n私は猫です。\n あなたも猫ですか？"


def center(topLevel):
    topLevel.update_idletasks()

    app = QApplication([])
    screen_width = app.desktop().screenGeometry().width()
    screen_height = app.desktop().screenGeometry().height()

    x = int(screen_width/2 - WIDTH/2)
    y = int(screen_height/2 - HEIGHT/2)

    topLevel.geometry(f"+{x}+{y}")

def resetVars():
    global fullCard, cardIndex, fbIndex, cards
    fullCard = False
    cardIndex = 0
    fbIndex = 0
    cards = []


def formatText(text):
    # Word Wrap
    temp = text.split("\n")
    pos = 0
    for i, item in enumerate(temp):
        if len(item) > 20 and item != horizontalRule:  # ignore horizontal rule
            if " " in text[pos+20:]:
                while not text[pos+20] == " ":
                    pos += 1
            elif " " in text[:pos+20]:
                while not text[pos+20] == " ":
                    pos -= 1
            text = text[:pos+20] + "\n" + text[pos+20:]
        pos += len(item) + 1
    # dynamic vertical center (better way to do this?)
    num = text.count("\n")
    if num <= 2:
        return "\n" * 3 + text
    elif num <= 4:
        return "\n" * 2 + text
    else:
        return "\n" + text


def doFullCard():
    fullText = cards[cardIndex][0] + "\n" + horizontalRule + "\n" + cards[cardIndex][1]
    fullText = formatText(fullText)
    card.config(text=fullText)


def showFullCard():
    global card, cards, cardIndex, fullCard
    if len(cards) == 0:
        return
    fullCard = not fullCard
    if fullCard:
        doFullCard()
    else:
        updateCard()


def updateCard():
    global card, cards, cardIndex, fbIndex
    card.config(text=formatText(cards[cardIndex][fbIndex]))


def nextCard():
    global cardIndex, cards, fullCard
    if cardIndex < len(cards) - 1:
        cardIndex += 1
        if fullCard:
            doFullCard()
        else:
            updateCard()


def previousCard():
    global cardIndex, cards, fullCard
    if cardIndex > 0:
        cardIndex -= 1
        if fullCard:
            doFullCard()
        else:
            updateCard()


def flipCard():
    global fbIndex, fullCard, cards
    if len(cards) == 0:
        return
    if fullCard:
        return
    fbIndex += 1
    if fbIndex > 1:
        fbIndex = 0
    updateCard()


def generateCards():
    resetVars()
    with open(filename, "r", encoding="utf8") as f:
        data = f.read().split("\n\n")
        for item in data:
            cardData = item.split("~")
            if len(cardData) > 1:
                cards.append(cardData)


def openFile():
    global filename, fileLabel
    filename = filedialog.askopenfilename(
        initialdir= ".",
        title="Select A File",
        filetype=(("Txt", "*.txt"), ("All Files", "*.*")),
    )
    if filename and len(filename) > 1:
        generateCards()
        updateCard()
        fileLabel.config(text=filename.split("/")[-1])


root = tk.Tk()
root.iconbitmap(default='transparent.ico')
root.geometry(f"{WIDTH}x{HEIGHT}")
root.title("Python FlashCard Application")
root.resizable(False, False)
center(root)

mainFrame = tk.Frame(root)
mainFrame.grid()


# Very Top
topFrame = tk.Frame(mainFrame, width=WIDTH, height=50)
topFrame.grid(row=0, column=0)
topFrame.columnconfigure(0, weight=10)

fileLabel = tk.Label(topFrame, text="No File", padx=50)
fileLabel.grid(row=0, column=0)

fileButton = tk.Button(topFrame, text="Open File", padx=50, command=openFile)
fileButton.grid(row=0, column=1)


# Top
secondFrame = tk.Frame(mainFrame, width=WIDTH, height=50)
secondFrame.grid(row=1, column=0)
secondFrame.columnconfigure(0, weight=10)

optionButton = tk.Button(secondFrame, text="Show Both Sides", command=showFullCard)
optionButton.grid()

# Center
thirdFrame = tk.Frame(mainFrame, width=WIDTH, height=HEIGHT - 150)
thirdFrame.grid(row=2, column=0)
thirdFrame.columnconfigure(0, weight=10)
thirdFrame.grid_propagate(False)
card = tk.Label(thirdFrame, text=openingMessage, font=("Arial", 20))  # , width=42, height=10)
card.grid(row=0, column=0, columnspan=3)

# generateCards()
# updateCard()

# Bottom
bottomFrame = tk.Frame(mainFrame, width=WIDTH, height=50)
bottomFrame.grid(row=3, column=0)
bottomFrame.columnconfigure(0, weight=10)

back_button = tk.Button(bottomFrame, text="<--", command=previousCard, padx=15)
flip_button = tk.Button(bottomFrame, text="Flip", command=flipCard, padx=15)
forward_button = tk.Button(bottomFrame, text="-->", command=nextCard, padx=15)

back_button.grid(row=1, column=0)
flip_button.grid(row=1, column=1)
forward_button.grid(row=1, column=2)

# mainloop
root.mainloop()

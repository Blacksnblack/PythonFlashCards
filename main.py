import tkinter as tk
from tkinter import filedialog


fullCard = False
cardIndex = 0
fbIndex = 0
cards = []
card, fileLabel = None, None
filename = "../vocab/verbs.txt" #  "../vocab/test.txt"
horizontalRule = "-" * 40


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

    # dynamic vertical center
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
    global fbIndex, fullCard
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
        # print(data)
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
    generateCards()
    updateCard()
    fileLabel.config(text=filename.split("/")[-1])


WIDTH = 400
HEIGHT = 400

root = tk.Tk()
root.geometry(f"{WIDTH}x{HEIGHT}")
root.resizable(False, False)

mainFrame = tk.Frame(root)
mainFrame.grid()

# Very Top
veryTopFrame = tk.Frame(mainFrame, width=WIDTH, height=50)
veryTopFrame.grid(row=0, column=0)
veryTopFrame.columnconfigure(0, weight=10)

fileLabel = tk.Label(veryTopFrame, text="No File", padx=50)
fileLabel.grid(row=0, column=0)

fileButton = tk.Button(veryTopFrame, text="Open File", padx=50, command=openFile)
fileButton.grid(row=0, column=1)


# Top
topFrame = tk.Frame(mainFrame, width=WIDTH, height=50)
topFrame.grid(row=1, column=0)
topFrame.columnconfigure(0, weight=10)

optionButton = tk.Button(topFrame, text="Show Both Sides", command=showFullCard)
optionButton.grid()

# Center
entryFrame = tk.Frame(mainFrame, width=WIDTH, height=HEIGHT - 150)
entryFrame.grid(row=2, column=0)
entryFrame.columnconfigure(0, weight=10)
entryFrame.grid_propagate(False)

card = tk.Label(entryFrame, text="私は猫です。\n あなたも猫ですか？", font=("Arial", 20))  # , width=42, height=10)
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

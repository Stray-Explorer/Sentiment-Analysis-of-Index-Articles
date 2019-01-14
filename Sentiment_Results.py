#!/usr/bin/python3
import os
from tkinter import *
import textwrap



os.environ["DISPLAY"] = ":1.0"


dexres = open('DEXresults.txt', 'r')
lines = dexres.readlines()
content = []
for line in range((len(lines)-9), len(lines)-1):
    content.append(lines[line])
#print(content[1:7])
#print(content[2])
#print(content[3])

#mostwords = ' '.join(content[5:6])
mostwords = content[0]
#print(mostwords)
sentres = ' '.join(content[1:7])# + ' '.join(content[-2:])
#sentres = ' '.join(content[0:4]) + ' '.join(content[-2:])
mostwords_wrapped = textwrap.fill(mostwords, width = 45) 
sentres_wrapped = textwrap.fill(sentres, width = 45)


DexRs = Tk()

DexRs.title('Sentiment Analysis of Index Articles')
DexRsContentWords = Label(DexRs, text= mostwords_wrapped)
DexRsContentRes = Label(DexRs, text= sentres_wrapped)

DexRsContentWords['bd'] = 16
#DexRsContentWords['relief'] = 'ridge'
DexRsContentWords['font'] = 'Mistral 17 bold'
DexRsContentWords['bg'] = 'black'
DexRsContentWords['fg'] = 'green'
DexRsContentWords['text'] = mostwords_wrapped
DexRsContentWords['padx'] = 16


DexRsContentRes['bd'] = 16
DexRsContentRes['relief'] = 'ridge'
DexRsContentRes['font'] = 'Mistral 17 bold'
DexRsContentRes['bg'] = 'black'
DexRsContentRes['fg'] = 'green'
DexRsContentRes['text'] = sentres_wrapped
DexRsContentRes['padx'] = 16

DexRs.after(885000, lambda: DexRs.destroy())

DexRsContentWords.pack()
DexRsContentRes.pack(expand=True)
DexRs.mainloop()
dexres.close()








          


from PIL import Image
import pytesseract
import cv2
import pandas as pd
import nltk
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
import firebase

from flask import Blueprint
from firebase_admin import firestore

db = firestore.client()
user_Ref = db.collection('Images')
userAPI = Blueprint('userAPI',__name__)

storage = firebase.storage()

@userAPI.route("/pattern",methods=["get"])
def pattern():    
    pytesseract.pytesseract.tesseract_cmd = r'E:\Tesseract-OCR\tesseract.exe'
    for i in range(0,2):
        image=cv2.imread('bill{}.png'.format(i),0)


        text=(pytesseract.image_to_string(image)).lower()
    #   print("All TEXT")
    #    print(text)



    #    match=re.findall(r'\d+[/.-]\d+[/.-]\d+', text)

    #    st=" "
    #    st=st.join(match)
    #    print("\n\n Date")
    #    print(st)



        #lets try to extract title
        sent_tokens=nltk.sent_tokenize(text)
        #print(sent_tokens)
        sent_tokens[0].splitlines()[0]
        #print(sent_tokens[0].splitlines()[0])
        head=sent_tokens[0].splitlines()[0]

        price=re.findall(r'[\$\£\€](\d+(?:\.\d{1,2})?)',text)
        price = list(map(float,price)) 
        #print(max(price))
        x=max(price) 

        #print(word_tokenize(text))

        tokenizer = nltk.RegexpTokenizer(r"\w+")
        new_words = tokenizer.tokenize(text)
        #print(new_words)

        stop_words = set(nltk.corpus.stopwords.words('english')) 

        #there is the filetred list
        filtered_list=[w for w in new_words if w not in stop_words ]
        #print(filtered_list)


        entertainment = [] 
        for syn in wordnet.synsets("entertainment"): 
            for l in syn.lemmas(): 
                entertainment.append(l.name()) 
            
        l=['happy','restaurant','food','kitchen','hotel','room','park','movie','cinema','popcorn','combo meal']
        entertainment=entertainment+l

        home_utility=[] 
        for syn in wordnet.synsets("home"): 
            for l in syn.lemmas(): 
                home_utility.append(l.name()) 
        l2=['internet','telephone','elecricity','meter','wifi','broadband','consumer','reading','gas','water','postpaid','prepaid']
        home_utility+=l2

        grocery=[] 
        for syn in wordnet.synsets("grocery"): 
            for l in syn.lemmas(): 
                grocery.append(l.name())
        l3=['bigbasket','milk','atta','sugar','bottle','suflower','oil','bread','vegetabe','fruit','salt','paneer']
        grocery+=l3

        transport=[]
        for syn in wordnet.synsets("car"): 
            for l in syn.lemmas(): 
                transport.append(l.name()) 
        l4=['cab','ola','uber','autorickshaw','railway','air','emirates','aerofloat','taxi','booking','road','highway']
        transport+=l4

        shopping=[]
        for syn in wordnet.synsets("dress"): 
            for l in syn.lemmas(): 
                shopping.append(l.name()) 
        l4=['iphone','laptop','saree','max','pantaloons','westside','vedic','makeup','lipstick','cosmetics','mac','facewash','heels','crocs','footwear','purse']
        shopping+=l4

        e=False
        g=False
        s=False
        t=False
        h=False

        for word in filtered_list:
            if word in entertainment:
                e=True
                break
            elif word in grocery:
                g=True
                break
            elif word in shopping:
                s=True
                break
            elif word in transport:
                t=True
                break
            elif word in home_utility:
                h=True
                break


        if(e):
            #print("entertainment category")
            filename='{}.csv'.format('entertainment')           
        elif(s):
            #print("shopping category")
            filename='{}.csv'.format('shopping')
        elif(g):
            #print("grocery category")
            filename='{}.csv'.format('grocery')
        elif(t):
            #print("transport category")
            filename='{}.csv'.format('transport')
        elif(h):
            #print("home utility category")
            filename='{}.csv'.format('home')
        else:
            #print("others")
            filename='{}.csv'.format('others')

                

        row_contents = [head,x]
        from csv import writer

        def append_list_as_row(file, list_of_elem):
            
            with open(file, 'a+', newline='') as write_obj:
                
                csv_writer = writer(write_obj)
                
                csv_writer.writerow(list_of_elem)
        append_list_as_row(filename, row_contents)


    entertainment=pd.read_csv('entertainment.csv')
    shopping=pd.read_csv('shopping.csv')
    grocery=pd.read_csv('grocery.csv')
    transport=pd.read_csv('transport.csv')
    other=pd.read_csv('others.csv')
    home=pd.read_csv('home.csv')



    category=['entertainment','shopping','grocery','transport','home','others']
    #lets sum all the expenditure category wise
    total_entertainment=entertainment['amount'].sum()
    total_shopping=shopping['amount'].sum()
    total_grocery=grocery['amount'].sum()
    total_transport=transport['amount'].sum()
    total_home=home['amount'].sum()
    total_others=other['amount'].sum()
    total_amount=total_entertainment+total_shopping+total_grocery+total_transport+total_home+total_others




    print("\n\n\n")
    print("Spent Money on Entertainment Rs:",total_entertainment)
    print("Spent Money on Shopping Rs:     ",total_shopping)
    print("Spent Money on grocery Rs:      ",total_grocery)
    print("Spent Money on transport Rs:    ",total_transport)
    print("Spent Money on home Rs:         ",total_home)
    print("Spent Money on others Rs:       ",total_others)

    print("\n")
    print(int((total_entertainment/total_amount)*100),"% ependiture in Entertainment categorty")
    print(int((total_shopping/total_amount)*100),"% ependiture in shopping categorty")
    print(int((total_grocery/total_amount)*100),"% ependiture in grocery categorty")
    print(int((total_transport/total_amount)*100),"% ependiture in transport categorty")
    print(int((total_home/total_amount)*100),"% ependiture in home categorty")
    print(int((total_others/total_amount)*100),"% ependiture in others categorty")


    print("\n")    
    return {"name":total_entertainment,"name2":total_grocery}


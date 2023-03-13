import pytesseract
import cv2
import re
import nltk

pytesseract.pytesseract.tesseract_cmd = r'E:\Tesseract-OCR\tesseract.exe'

for i in range(0,2):
    image=cv2.imread('bill{}.png'.format(i),0)


    text=(pytesseract.image_to_string(image)).lower()

    print("\n\n")


    print("************************ Bill",i+1,"**************************\n")

    print("/////////////All TEXT////////////\n")
    print(text)
    print("///////////////////////////////////\n\n")
    


    #To extract title        
    tokens=nltk.sent_tokenize(text)
    print("............Tokens..............\n")    
    print(tokens)    
    print("................................\n\n") 
    print("#######Oraganization of Bill(Title)########\n")               
    print(tokens[0].splitlines()[0])
    print("\n########################################\n\n")     
    

    price=re.findall(r'[\$\£\€](\d+(?:\.\d{1,2})?)',text)
    price = list(map(float,price))  
    print('Total Expense of Bill:',max(price))
    print("\n\n")
    

#    match=re.findall(r'\d+[/.-]\d+[/.-]\d+', text)
#    st=" "
#    st=st.join(match)
#    print("\n\n Date")
#    print(st)






"""
print(new_words)
for i in range(len(new_words)):
    if new_words[i]=='grand' and new_words[i+1]=='total':
        break
price=new_words[i+2]
print(price) 
"""

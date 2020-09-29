
# coding: utf-8

# In[43]:


def imgtotext(url):
    import numpy as np
    import pytesseract
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    import cv2
    import sys
    print("in the function")
    sys.stdout.flush()
    # Load the image
    #img = cv2.imread(url)
    img = url_to_image(url)
    (H, W) = img.shape[:2]
    # set the new width and height and then determine the ratio in change
    # for both the width and height
    (newW, newH) = (800, 400)
    rW = W / float(newW)
    rH = H / float(newH)
    # resize the image and grab the new image dimensions
    img = cv2.resize(img, (newW, newH))
    (H, W) = img.shape[:2]
    # convert to grayscale
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    # smooth the image to avoid noises
    gray = cv2.medianBlur(gray,5)

    # Apply adaptive threshold
    thresh = cv2.adaptiveThreshold(gray,255,1,1,11,2)
    thresh_color = cv2.cvtColor(thresh,cv2.COLOR_GRAY2BGR)

    # apply some dilation and erosion to join the gaps - change iteration to detect more or less area's

    thresh = cv2.dilate(thresh,None,iterations = 3)
    thresh = cv2.erode(thresh,None,iterations = 3)

    # Find the contours
    contours = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)[0]

    im2 = img.copy()
    file = open("recognised.txt", "w+")
    file.write("")
    file.close()

    # For each contour, find the bounding rectangle and draw it
    
    print("Running iterations now. Please wait.")
    sys.stdout.flush()
    for cnt in contours:
        # sys.stdout.flush()
        x,y,w,h = cv2.boundingRect(cnt)
        cv2.rectangle(thresh_color,(x,y),(x+w,y+h),(0,255,0),2)
        rect = cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
        cropped = im2[y:y+h, x:x+w]
        file = open("recognised.txt", "a")
        text = pytesseract.image_to_string(cropped) 
        #print('found : ' + text)
        if (text == " " or text=="\n" or text==""):
            #print("no text")
            continue

        else:
            file.write(text.encode("utf-8"))
            file.write("\n")
            file.close       
    
    print("Done. Result stored in recognised.txt")
    sys.stdout.flush()
    with open('recognised.txt', 'r') as myfile:
          data = myfile.read()
            
    #Print the passport number:
    print(find_id_number(data))
    sys.stdout.flush()

    # Finally show the image. Disabled for server purposes.
    # cv2.imshow('img',img)
    # cv2.imshow('res',thresh_color)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()


# In[44]:


# METHOD #1: OpenCV, NumPy, and urllib
def url_to_image(url):
    import urllib
    import numpy as np
    import cv2
    resp = urllib.urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)

    return image

def is_number(num):
    if num=='0' or '1' or '2' or '3' or '4' or '5' or '6' or '7' or '8' or '9' or '0':
        return True
    else:
        return False
    
def find_id_number(rec):
    for i,char in enumerate(rec):
        if char.isupper() and is_number(rec[i+1]) and is_number(rec[i+7]):
            return rec[i:i+7]
            break
    return 'No number found.'


import sys
imgtotext(sys.argv[1])
# In[42]:





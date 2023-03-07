
import os   
# removes all the images in the folder
def clear_pngs():
    for x in os.listdir('./images/'):
        if not x.startswith('.') and not x.startswith('1'):
            for files in os.listdir('./images/'+x):
                if files.endswith('.png'):
                    os.remove('./images/'+ x + '/' + files) 

def clear_pdfs():
    for subdirs in os.listdir('./images/'):
        if not subdirs.startswith('.') and not subdirs.startswith('1'):
            for files in os.listdir('./images/'+subdirs):
                if files.endswith('.pdf'):
                    os.remove('./images/'+subdirs + '/' +files) 


import os   
# removes all the images in the folder
def clear_pngs():
    for file in os.listdir('./images/'):
        if file.endswith('.png'):
            os.remove('./images/'+file) 
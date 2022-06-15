
import os

# removes all the images in the folder
for file in os.listdir('./images/'):
    if file.endswith('.png'):
        os.remove(file) 
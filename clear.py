
import os

# removes all the images in the folder
for file in os.listdir('./'):
    if file.endswith('.png'):
        os.remove(file) 
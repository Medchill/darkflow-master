import os
path = '/Users/Kaden/Desktop/darkflow-master/new_model_data/images'
files = os.listdir(path)
i = 1

for file in files:
    os.rename(os.path.join(path, file), os.path.join(path, str(i)+'.png'))
    i = i+1
import os
import time




def path2DictIndex(locPath,basePath,types=['png','jpg','jpeg','gif']):

    dirs=os.listdir(basePath+locPath)

    xr=[]

    for i in dirs:

        fileName,ext=os.path.splitext(i)
        xr.append([fileName[3:],i])

    return xr

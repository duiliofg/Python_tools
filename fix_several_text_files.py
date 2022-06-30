#original writted by Shine Vision
 
#import this
import os
from IPython.display import clear_output
#Text to find  
texttofind='here'
#Text to replace
texttoreplace='here'
#Your source path
sourcepath=os.listdir('your_source_path/')
for file in sourcepath:
    inputfile='your_source_path/'+file
    clear_output(wait=True)
    print('Conversion is ongoing for:' + inputfile)
    with open(inputfile,'r') as inputfile:
          filedata=inputfile.read()
          freq=0
          freq=filedata.count(texttofind)
    destinationpath='your_ouput_path/'+file
    filedata=filedata.replace(texttofind,texttoreplace)      
    with open(destinationpath,'w') as file:
          file.write(filedata)
    print('Total %d Record Replaced' %freq)      

### simplevideo

```
usage: simplevideo.py [-h] [-n FILENAME] [-c CAMERANUMBER]
                      [-d DIRECTORYFORSAVING]

Records continuously from a specified camera and saves to file. Stops after
pressing [Escape]. (written by Pieter Goltstein - December 2020)

optional arguments:
  -h, --help            show this help message and exit
  -n FILENAME, --filename FILENAME
                        Filename-stem for storing video (date and time will be
                        added automatically)
  -c CAMERANUMBER, --cameranumber CAMERANUMBER
                        Number of the camera device that openCV will use
                        (default=0)
  -d DIRECTORYFORSAVING, --directoryforsaving DIRECTORYFORSAVING
                        The path of the directory where the videos will be
                        saved

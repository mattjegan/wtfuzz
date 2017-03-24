# wtfuzz - What The Fuzz
Wtfuzz is a cli tool used for checking the existance of different types of web resources including webpages, files, api endpoints and more.

# Installation
Requires Python 3.5+
```
pip install wtfuzz
```

# Usage
Try find resources from some url
```
wtfuzz http://your-url-here.com
```
Use a particular file as the list of resources to try.
```
wtfuzz http://your-url-here.com -f myList.txt
```
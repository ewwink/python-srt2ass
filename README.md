# python-srt2ass
Python Script to Convert Subtitle formats from .srt to .ass. By default it will add black background (opaque) with yellow font color, useful to hide hardsub foreign subtitle

## Requirements ##

* [Python 2.7](https://www.python.org/downloads/) (recommend)
* Windows/Linux/Mac/Android

## How to use ##

```python srt2ass.py "file"```

## Sample ##
using command line

    python srt2ass.py file1.srt
    or
    python srt2ass.py file1.srt file2.srt file3.srt

using as module

    from srt2ass import srt2ass
    
    assSub = srt2ass("file.srt")
    print 'ASS subtitle saved as: ' + assSub
    # ASS subtitle saved as: file.ass



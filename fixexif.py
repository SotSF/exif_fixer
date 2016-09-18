import os
import os.path
import sys
import piexif
from datetime import datetime, timedelta

#Approximate offset from temple burn time
OFFSET = timedelta(4257, 62400)
EXIFFMT = "%Y:%m:%d %H:%M:%S"
DATEKEY = 36867

def main():
    picdir = sys.argv[1]
    if not os.path.isdir(picdir):
        print '"%s" is not a valid directory' % picdir
        return 1
    for pic in os.listdir(picdir):
        try:
            path = os.path.join(picdir, pic)
            exifdata = piexif.load(path)
            taken = None
            try:
                taken = datetime.strptime(exifdata['Exif'][DATEKEY], EXIFFMT)
            except:
                taken = datetime.strptime(exifdata['Exif'][DATEKEY+1], EXIFFMT)
            if taken and taken.year < 2016:
                corrected = taken + OFFSET
                print "Found improperly tagged photo '%s', updating '%s' => '%s'..." % (pic, taken, corrected)
                exifdata['Exif'][DATEKEY] = corrected.strftime(EXIFFMT)
                exifdata['Exif'][DATEKEY+1] = corrected.strftime(EXIFFMT)
                piexif.insert(piexif.dump(exifdata), path)
        except Exception as e:
            print "Failed to process '%s':" % pic, e.message
    print "Done."
    return 0

sys.exit(main())

import xml.dom.minidom as xdom
import os

def procXml(gpxPath):
    print(gpxPath)
    dom_tree = xdom.parse(os.path.join(filePath, gpxPath))
    collection = dom_tree.documentElement
    trkpts = collection.getElementsByTagName("trkpt")
    eles = collection.getElementsByTagName("ele")
    times = collection.getElementsByTagName("time")
    cads = collection.getElementsByTagName("gpxtpx:cad")

    lats, lons = [], []
    alt, time, RunCadence = [], [], []

    for t in times:
        time.append(t.firstChild.data)

    for ele in eles:
        alt.append(ele.firstChild.data)

    for cad in cads:
        RunCadence.append(float(cad.firstChild.data) / 2)

    for trkpt in trkpts:
        lat = trkpt.getAttribute("lat")
        lon = trkpt.getAttribute("lon")
        if lat == '0' or lon == '0':
            continue
        lats.append(float(lat))
        lons.append(float(lon))

    M = input('Minutes:')
    S = input('Seconds:')
    TotalTimeSeconds = 60 * int(M) + int(S)

    data = '<?xml version="1.0"?>\n' \
           '<TrainingCenterDatabase xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2">\n' \
           '<Activities>\n' \
           '<Activity Sport="Running">\n' \
           '<Id>' + time[0] + '</Id>\n' \
            '<Lap StartTime="' + time[0] + '">\n' \
            '<TotalTimeSeconds>' + str(TotalTimeSeconds) + '</TotalTimeSeconds>\n' \
            '<DistanceMeters>' + input('Distance:') + '</DistanceMeters>\n' \
            '<Calories>' + input('Calories:') + '</Calories>\n' \
            '<Intensity>Active</Intensity>\n' \
            '<TriggerMethod>Manual</TriggerMethod>\n' \
            '<Track>\n'

    for i in range(len(alt)):
        data = data + '<Trackpoint>\n' \
                      '<Time>' + time[i+1] + '</Time>\n' \
                        '<Position>\n' \
                        '<LatitudeDegrees>' + str(lats[i]) + '</LatitudeDegrees>\n' \
                        '<LongitudeDegrees>' + str(lons[i]) + '</LongitudeDegrees>\n' \
                        '</Position>\n' \
                        '<AltitudeMeters>' + alt[i] + '</AltitudeMeters>\n' \
                        '</Trackpoint>\n'

    data = data + '</Track>\n' \
                  '</Lap>\n' \
                  '</Activity>\n' \
                  '</Activities>\n' \
                  '</TrainingCenterDatabase>'

    tcxDir = os.path.abspath('./tcxs')
    if not os.path.exists(tcxDir):
        os.mkdir(tcxDir)
    tcxPath = os.path.join(tcxDir, gpxPath) + '.tcx'
    with open(tcxPath, 'w') as f:
        f.write(data)
        f.close()

filePath = os.path.abspath('./gpxs')
fileList = os.listdir(filePath)
for gpxPath in fileList:
    procXml(gpxPath)
input('按任意键结束')
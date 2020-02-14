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

    data = '<?xml version="1.0" encoding="UTF-8"?>\n' \
           '<!-- Created by FitnessSyncer.com -->\n' \
           '<TrainingCenterDatabase xsi:schemaLocation="' \
           'http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2 ' \
           'http://www.garmin.com/xmlschemas/TrainingCenterDatabasev2.xsd" xmlns:ns5="' \
           'http://www.garmin.com/xmlschemas/ActivityGoals/v1" xmlns:ns3="' \
           'http://www.garmin.com/xmlschemas/ActivityExtension/v2" xmlns:ns2="' \
           'http://www.garmin.com/xmlschemas/UserProfile/v2" xmlns="' \
           'http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2" xmlns:xsi="' \
           'http://www.w3.org/2001/XMLSchema-instance">\n' \
           '<Activities>\n' \
           '<Activity Sport="Running"><Id>' + time[0] + '</Id><Lap StartTime="' + time[0] + '"><TotalTimeSeconds>'\
           + str(TotalTimeSeconds) + '</TotalTimeSeconds><DistanceMeters>'\
           + input('Distance:') + '</DistanceMeters><Intensity>Active</Intensity><Cadence>'\
           + str(RunCadence[len(RunCadence)-1]) + '</Cadence><TriggerMethod>Manual</TriggerMethod><Track>'

    for i in range(len(alt)):
        data = data + '<Trackpoint><Time>' + time[i+1] + '</Time><Position><LatitudeDegrees>'\
           + str(lats[i]) + '</LatitudeDegrees><LongitudeDegrees>' \
           + str(lons[i]) + '</LongitudeDegrees></Position><AltitudeMeters>' \
           + alt[i] + '</AltitudeMeters></Trackpoint>'

        # if i > 0:
        #    data = data + '<Extensions><TPX xmlns="http://www.garmin.com/xmlschemas/ActivityExtension/v2"><RunCadence>'\
        #           + str(RunCadence[i-1]) + '</RunCadence></TPX></Extensions></Trackpoint>'

    data = data + '</Track></Lap>\n' \
                  '</Activity></Activities>\n' \
                  '<Author xsi:type="Application_t"><Name>FitnessSyncer.com</Name><Build><Version><VersionMajor>1</VersionMajor><VersionMinor>0</VersionMinor><BuildMajor>0</BuildMajor><BuildMinor>0</BuildMinor></Version></Build><LangID>en</LangID><PartNumber>000-00000-00</PartNumber></Author>\n' \
                  '</TrainingCenterDatabase>'

    tcxDir = os.path.abspath('./tcxs')
    if not os.path.exists(tcxDir):
        os.mkdir(tcxDir)
    tcxPath = os.path.join(tcxDir, gpxPath[:7]) + '.tcx'
    with open(tcxPath, 'w') as f:
        f.write(data)
        f.close()

filePath = os.path.abspath('./gpxs')
fileList = os.listdir(filePath)
for gpxPath in fileList:
    procXml(gpxPath)
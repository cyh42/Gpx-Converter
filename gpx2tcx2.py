import re
import os

def procXml(gpxPath):
    print(gpxPath)
    filePath = './gpxs/' + gpxPath
    f = open(filePath, 'r')
    data = f.readlines()
    f.close()

    time = re.findall('<time>(.*)</time>', data[3])
    M = input('Minutes:')
    S = input('Seconds:')
    TotalTimeSeconds = 60 * int(M) + int(S)
    text = '<?xml version="1.0"?>\n' \
        '<TrainingCenterDatabase xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2">\n' \
        '<Activities>\n' \
        '<Activity Sport="Running">\n' \
        '<Id>' + time[0] + '</Id>\n' \
        '<Lap StartTime="' + time[0] + '">\n' \
        '<TotalTimeSeconds>' + str(TotalTimeSeconds) + '</TotalTimeSeconds>\n' \
        '<DistanceMeters>' + input('Distance:') + '</DistanceMeters>\n' \
        '<AverageHeartRateBpm><Value>' + input('AverageHeartRateBpm:') + '</Value></AverageHeartRateBpm>\n' \
        '<MaximumHeartRateBpm><Value>' + input('MaximumHeartRateBpm:') + '</Value></MaximumHeartRateBpm>\n' \
        '<Calories>' + input('Calories:') + '</Calories>\n' \
        '<Intensity>Active</Intensity>\n' \
        '<TriggerMethod>Manual</TriggerMethod>\n' \
        '<Track>\n'

    i = 0
    lat, lon = '', ''
    for line in data:
        i = i + 1
        if re.match('<trkpt', line):
            text = text + '<Trackpoint>\n'
            lat = re.findall('lat="(.*)" lon', line)[0]
            lon = re.findall('lon="(.*)">', line)[0]

        if re.findall('<time>(.*)</time>', line) and i > 8:
            text = text + '<Time>' + re.findall('<time>(.*)</time>', line)[0] + '</Time>\n' \
                            '<Position>\n' \
                            '<LatitudeDegrees>' + str(lat) + '</LatitudeDegrees>\n' \
                            '<LongitudeDegrees>' + str(lon) + '</LongitudeDegrees>\n' \
                            '</Position>\n'
            lat, lon = '', ''

        if re.match('<ele>', line):
            text = text + '<AltitudeMeters>' + re.findall('<ele>(.*)</ele>', line)[0] + '</AltitudeMeters>\n'

        if re.match('<gpxtpx:hr>', line):
            text = text + '<HeartRateBpm xsi:type="HeartRateInBeatsPerMinute_t"><Value>' + re.findall('<gpxtpx:hr>(.*)</gpxtpx:hr>', line)[0] + '</Value></HeartRateBpm>\n'

        if re.match('</trkpt>', line):
            text = text + '</Trackpoint>\n'
    
    text = text + '</Track>\n' \
                  '</Lap>\n' \
                  '</Activity>\n' \
                  '</Activities>\n' \
                  '</TrainingCenterDatabase>\n'

    tcxDir = os.path.abspath('./tcxs')
    if not os.path.exists(tcxDir):
        os.mkdir(tcxDir)
    tcxPath = os.path.join(tcxDir, gpxPath) + '.tcx'
    with open(tcxPath, 'w') as f:
        f.write(text)
        f.close()

filePath = os.path.abspath('./gpxs')
fileList = os.listdir(filePath)
for gpxPath in fileList:
    procXml(gpxPath)
input('按任意键结束')

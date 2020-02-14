import xml.dom.minidom as xdom
import os
import math

x_pi = 3.14159265358979324 * 3000.0 / 180.0
pi = 3.1415926535897932384626  # π
a = 6378245.0  # 长半轴
ee = 0.00669342162296594323  # 偏心率平方

def wgs84_to_gcj02(lng, lat):
    """
    WGS84转GCJ02(火星坐标系)
    :param lng:WGS84坐标系的经度
    :param lat:WGS84坐标系的纬度
    :return:

    if out_of_china(lng, lat):  # 判断是否在国内
        return [lng, lat]
    """
    dlat = _transformlat(lng - 105.0, lat - 35.0)
    dlng = _transformlng(lng - 105.0, lat - 35.0)
    radlat = lat / 180.0 * pi
    magic = math.sin(radlat)
    magic = 1 - ee * magic * magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * pi)
    dlng = (dlng * 180.0) / (a / sqrtmagic * math.cos(radlat) * pi)
    mglat = lat + dlat
    mglng = lng + dlng
    return [mglng, mglat]
def _transformlat(lng, lat):
    ret = -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat + \
          0.1 * lng * lat + 0.2 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 *
            math.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lat * pi) + 40.0 *
            math.sin(lat / 3.0 * pi)) * 2.0 / 3.0
    ret += (160.0 * math.sin(lat / 12.0 * pi) + 320 *
            math.sin(lat * pi / 30.0)) * 2.0 / 3.0
    return ret
def _transformlng(lng, lat):
    ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + \
          0.1 * lng * lat + 0.1 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 *
            math.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lng * pi) + 40.0 *
            math.sin(lng / 3.0 * pi)) * 2.0 / 3.0
    ret += (150.0 * math.sin(lng / 12.0 * pi) + 300.0 *
            math.sin(lng / 30.0 * pi)) * 2.0 / 3.0
    return ret
def out_of_china(lng, lat):
    """
    判断是否在国内，不在国内不做偏移
    :param lng:
    :param lat:
    :return:
    """
    return not (lng > 73.66 and lng < 135.05 and lat > 3.86 and lat < 53.55)

def procXml(filePath, gpxPath):
    dom_tree = xdom.parse(os.path.join(filePath, gpxPath))
    collection = dom_tree.documentElement
    trkpts = collection.getElementsByTagName("trkpt")
    data = '{"line_id":"' + gpxPath[31:39] + '","lnglat":['
    i = 0
    for trkpt in trkpts:
        i = i + 1
        lat = trkpt.getAttribute("lat")
        lon = trkpt.getAttribute("lon")
        if lat == '0' or lon == '0':
            continue
        ret = wgs84_to_gcj02(float(lon), float(lat))
        data = data + '[' + str(ret[0]) + ',' + str(ret[1]) + ']'
        if(i < len(trkpts)):
            data = data + ','
    data = data + ']},'

    jsonDir = os.path.abspath('./jsons')
    if not os.path.exists(jsonDir):
        os.mkdir(jsonDir)
    jsonPath = os.path.join(jsonDir, gpxPath) + '.json'
    with open(jsonPath, 'w') as f:
        f.write(data)
        f.close()


def main():
    filePath = os.path.abspath('./gpxs')
    fileList = os.listdir(filePath)
    for gpxPath in fileList:
        print('Processing ' + str(gpxPath))
        procXml(filePath, gpxPath)
        print('Coresponding JSON file was generated.')

if __name__ == '__main__':
    main()
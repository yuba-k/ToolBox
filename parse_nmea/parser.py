import matplotlib.pyplot as plt
from matplotlib import colors
import math


def parser(nmealine:str):
    satelites = []
    latlon = []
    lines = nmealine.split("\n")
    for line in lines:
        token = line.split(",")
        token[-1] = token[-1].split("*")[0]
        match token[0]:
            case "$GPRMC":
                UTC = token[1]
                latdeg = float(token[3]) / 100
                latdeg = int(latdeg)
                latmin = float(token[3]) % 100
                LAT = latdeg + latmin / 60.0
                londeg = float(token[5]) / 100
                londeg = int(londeg)
                lonmin = float(token[5]) % 100
                LON = londeg + lonmin / 60.0
                latlon.append([LAT,LON])
                UTCDATE = token[9]
                MODE = token[12][0]
            case "$GPGGA":
                SATELITES = token[7]
                HDOP = token[8]
            case "$GPGSA":
                TYPE = token[2]
                PRN = token[3:15]
                PDOP = token[15]
            case "$GPGSV":
                num = len(token[4:])
                for i in range(num//4):
                    satelites.append({"PRN":token[4+4*i],"ELEVATION":float(token[5+4*i] if token[5+4*i] != "" else "0"),"AZIMUTH":float(token[6+4*i] if token[6+4*i] != "" else "0"),"SIGNAL_STREGNTH":float(token[7+4*i] if token[7+4*i] != "" else "0")})
            case "$GPVTG":
                pass
            case "GPZDA":
                pass
    return f"UTC:{UTC},LAT:{LAT},LON:{LON},UTCDATE:{UTCDATE},MODE:{MODE},SATELITES:{SATELITES},HDOP:{HDOP},TYPE:{TYPE},PRN:{PRN},PDOP:{PDOP}",satelites,latlon

def show_plt(satelites, latlon):
    theta = []
    r = []
    c = []
    lat = []
    lon = []
    for element in satelites:
        theta.append(math.radians(element["AZIMUTH"]))
        r.append(90-element["ELEVATION"])
        c.append(float(element["SIGNAL_STREGNTH"]))
    fig = plt.figure(figsize=(6,6))
    ax = fig.add_subplot(1,2,1,projection="polar")
    sc = ax.scatter(theta,r,alpha=0.4,s=5,c=c,cmap="plasma",norm=colors.Normalize(vmin=min(c),vmax=max(c)))
    ax.set_rlim(0,90)
    ax.set_rlabel_position(180)
    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)
    plt.colorbar(sc, ax=ax,label="SNR")
    for element in latlon:
        lat.append(element[0])
        lon.append(element[1])
    ax2 = fig.add_subplot(1,2,2)
    ax2.scatter(lat,lon)
    plt.show()

def testmain():
    testNMEA = ("$GPRMC,123519,A,3135.1234,N,13033.5678,E,0.13,309.62,140326,,,A*6C\n"
        "$GPGGA,123519,3135.1234,N,13033.5678,E,1,08,0.9,12.3,M,39.0,M,,*47\n"
        "$GPGSA,A,3,07,08,10,13,15,18,20,23,,,,,1.8,1.0,1.5*33\n"
        "$GPGSV,2,1,08,07,79,048,42,08,62,273,43,10,51,120,41,13,45,312,42*70\n"
        "$GPGSV,2,2,08,15,34,220,39,18,29,085,37,20,18,310,35,23,10,140,30*71\n")
    parsed, satelites, latlon = parser(testNMEA)
    show_plt(satelites, latlon)
    
def main():
    with open("parse_nmea/nmeaLog.csv",mode="r") as f:
        alllines = f.read()
        parsed, satelites, latlon = parser(alllines)
        show_plt(satelites, latlon)

if __name__ == "__main__":
    main()

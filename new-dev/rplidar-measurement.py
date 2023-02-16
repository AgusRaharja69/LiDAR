from datetime import datetime
import json

from rplidar import RPLidar

PORT_NAME = 'COM14'
BAUDRATE: int = 115200
TIMEOUT: int = 1
DMAX: int = 4000
IMIN: int = 0
IMAX: int = 50
raw = True

def run():
    lidar = RPLidar(PORT_NAME, baudrate=BAUDRATE, timeout=TIMEOUT)
    try:
        if not raw:
            print('Print measurements - Press Crl+C to stop.')
            now = datetime.now()
            date_time = now.strftime("%d/%m/%Y %H:%M:%S")
            print('Date & Time  : {0}'.format(date_time))
        for val in lidar.iter_scans():
            # print(val)
            lidarData = {}
            lidarData["data"] = val
            with open('../../object-distance-detection/lidarJson.json','w') as outfile :                    
                json.dump(lidarData, outfile, indent=2)
                lidarData["data"] = []
    except KeyboardInterrupt:
        lidar.stop()
        lidar.stop_motor()
        lidar.disconnect()

if __name__ == '__main__':
    run()


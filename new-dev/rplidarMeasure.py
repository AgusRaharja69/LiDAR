from rplidar import RPLidar
import json
# import time

PORT_NAME = 'COM14'
BAUDRATE: int = 115200
TIMEOUT: int = 1

def runLidar():
    lidar = RPLidar(PORT_NAME, baudrate=BAUDRATE, timeout=TIMEOUT)
    try:
        lidarData = {}
        lidarData["angle"] = []
        lidarData["distance"] = []
        i=0   
        angle = -1     
        for val in lidar.iter_measures(scan_type='express', max_buf_meas=False):
            ''' Save in fix number of data '''
            # if val[3] != 0:  
            #     lidarData["angle"].append(val[2])
            #     lidarData["distance"].append(val[3]) 
            #     i+=1
            #     if i == 150:
            #         with open('lidarJson.json','w') as outfile :                    
            #             json.dump(lidarData, outfile, indent=3)
            #         lidarData = {}
            #         lidarData["angle"] = []
            #         lidarData["distance"] = []
            #         i=0   

            ''' Save for one LiDAR cycle '''
            if val[3] != 0:
                if angle < val[2]:                
                    lidarData["angle"].append(val[2])
                    lidarData["distance"].append(val[3])
                else :
                    # print(len(lidarData["angle"]))
                    with open('../../../object-distance-detection/lidarJson.json','w') as outfile :                    
                        json.dump(lidarData, outfile, indent=2)
                    lidarData["angle"] = []
                    lidarData["distance"] = []
                    angle = -1
                angle = val[2]

    except KeyboardInterrupt:
        lidar.stop()
        lidar.stop_motor()
        lidar.disconnect()

if __name__ == '__main__':
    runLidar()

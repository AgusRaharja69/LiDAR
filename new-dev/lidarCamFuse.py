import json
import cv2
import numpy as np

# Connect to the webcam
cap = cv2.VideoCapture(1)
jsonLidarPath = '../lidarJson.json'
angle, lidarDist = [], []

while True:
    # Get a frame from the webcam
    ret, frame = cap.read()

    # Load the camera intrinsic parameters
    fx = 823.91511051
    cx = 298.20819386
    fy = 817.78038047
    cy = 305.53945851
    K = np.array([[fx, 0, cx], [0, fy, cy], [0, 0, 1]])

    # Load the camera extrinsic parameters
    R = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    t = np.array([0, 0, 0])

    
    # Convert the RPLidar scan to a point cloud
    with open(jsonLidarPath, 'r') as j:
        try :
            lidarData = json.loads(j.read())
            # angle = lidarData['angle']
            # lidarDist = lidarData['distance']
            lidarAngle = [a[1] for a in lidarData['data']]
            lidarDist = [b[2] for b in lidarData['data']]
            
        except :
            print("error")
            lidarAngle, lidarDist = lidarAngle, lidarDist    

    point_cloud = []    
    for s in scan:
        for quality, angle, distance in s:
            if quality > 0:
                x = distance * np.cos(angle)
                y = distance * np.sin(angle)
                z = 0
                point_cloud.append((x, y, z))

    # Convert the point cloud to a numpy array
    point_cloud = np.array(point_cloud)

    # Transform the point cloud to the camera coordinate frame
    point_cloud_cam = R.dot(point_cloud.T) + t

    # Project the point cloud onto the image plane
    point_cloud_image = K.dot(point_cloud_cam)
    point_cloud_image /= point_cloud_image[2,:]
    point_cloud_image = point_cloud_image[:2,:].T

    # Draw the point cloud on the image
    for p in point_cloud_image:
        cv2.circle(frame, (int(p[0]), int(p[1])), 2, (255, 0, 0), -1)

    # Display the image
    cv2.imshow("Frame", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam
cap.release()
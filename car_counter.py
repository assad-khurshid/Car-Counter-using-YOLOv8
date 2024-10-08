from ultralytics import YOLO
import cv2
import cvzone
import numpy as np
import math
from sort import *


# Load the YOLO model
model = YOLO('../Yolo-weights/yolov8n.pt')

classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
              "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
              "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
              "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
              "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
              "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
              "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
              "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
              "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
              "teddy bear", "hair drier", "toothbrush"
              ]


mask = cv2.imread("mask.png")

# Tracking
tracker = Sort(max_age=20, min_hits=3, iou_threshold=0.3)

limits = [400, 297, 700, 297]  # Line for counting
totalCount = []

# For videos
cap = cv2.VideoCapture("../videos/cars.mp4")

while True:  # To ensure screen is on by rotating the loop
    success, img = cap.read()  # Read a frame from the webcam
    if not success:
        break  # Exit if no frame is read (end of video)

    imgRegion = cv2.bitwise_and(img, mask)

    imgGraphics = cv2.imread("graphics.png", cv2.IMREAD_UNCHANGED)
    img = cvzone.overlayPNG(img, imgGraphics,(0,0))

    results = model(imgRegion, stream=True)  # Perform object detection

    detections = np.empty((0, 5))

    # Loop through the detections
    for r in results:
        boxes = r.boxes
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0]  # Ensure only one value
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)  # Convert to integers

            w, h = x2 - x1, y2 - y1

            # For confidence
            conf = math.ceil((box.conf[0] * 100)) / 100  # Round confidence to 2 decimal places

            # For bounding box
            cls = int(box.cls[0])
            currentClass = classNames[cls]
            if currentClass in ["car", "truck", "bus", "motorbike"] and conf > 0.3:
                currentArray = np.array([x1, y1, x2, y2, conf])
                detections = np.vstack((detections, currentArray))

    resultTrackers = tracker.update(detections)

    # Draw the counting line
    cv2.line(img, (limits[0], limits[1]), (limits[2], limits[3]), (0, 0, 255), 5)

    # Process each tracked object
    for result in resultTrackers:
        x1, y1, x2, y2, Id = result
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)  # Convert to integers

        w, h = x2 - x1, y2 - y1
        cx, cy = x1 + w // 2, y1 + h // 2  # Calculate the center of the bounding box

        cvzone.cornerRect(img, (x1, y1, w, h), l=9, rt=2, colorR=(255, 0, 255))
        cvzone.putTextRect(img, f'{int(Id)}', (max(0, x1), max(35, y1)), scale=2, thickness=3, offset=10)

        # Draw a circle at the center of the tracked object
        cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

        # Check if the object's center crosses the counting line
        if limits[0] < cx < limits[2] and limits[1] - 15 < cy < limits[1] + 15:
            if totalCount.count(Id) == 0:
               totalCount.append(Id)
               cv2.line(img, (limits[0], limits[1]), (limits[2], limits[3]), (0, 255, 0), 5)


    # Display the count
    #cvzone.putTextRect(img, f'Count: {len(totalCount)}', (50, 50), scale=2, thickness=2, offset=5)
    cv2.putText(img, str(len(totalCount)), (255, 100), cv2.FONT_HERSHEY_PLAIN, 5, (50, 50, 255), 8)
    # Display the image with bounding boxes
    cv2.imshow('Image', img)
    cv2.imshow('ImageRegion', imgRegion)

    if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to exit
        break

cap.release()
cv2.destroyAllWindows()

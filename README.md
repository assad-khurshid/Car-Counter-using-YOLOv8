
# Car Counter using YOLOv8

This project implements a real-time vehicle counting system using the YOLOv8 model. It is designed to detect and count cars, trucks, buses, and motorbikes in a given video feed. The counting is based on the objects crossing a predefined line in the frame.

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Methodology](#methodology)
- [Technologies Used](#technologies-used)
-[Contribution](#Contribution)

## Project Overview

This project leverages the YOLOv8 model for real-time object detection, combined with SORT for object tracking. The system processes video frames to detect vehicles and tracks them until they cross a counting line. A mask is applied to the video feed to ensure that only relevant parts of the frame are analyzed for object detection, improving accuracy and performance.

## Features

- **Real-Time Detection and Counting**: Detects and counts vehicles such as cars, trucks, buses, and motorbikes in real-time.
- **Customizable Counting Line**: You can adjust the line for counting vehicles to suit your specific use case.
- **Accurate Object Tracking**: The SORT algorithm is used to ensure objects are tracked consistently across frames.
- **High Confidence Filtering**: Only objects with a confidence score above a threshold (e.g., 30%) are considered for counting.
- **Masked Region Detection**: A mask is used to ensure only the main areas of the frame are selected for vehicle detection.

  ![YOLOv8 Model Diagram](https://github.com/assad-khurshid/Car-Counter-using-YOLOv8/blob/main/Screenshot%202024-08-24%20202142.png)


## Installation

### Prerequisites

- Python 3.8+
- Anaconda (optional, but recommended)
- OpenCV
- YOLOv8 (Ultralytics)
- cvzone
- numpy
- SORT (Simple Online and Realtime Tracking)

### Steps

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/Car-Counter-YOLOv8.git
   cd Car-Counter-YOLOv8
   ```

2. **Set Up the Environment**:
   ```bash
   conda create --name car-counter python=3.8
   conda activate car-counter
   ```

3. **Install Required Libraries**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Download YOLOv8 Weights**:
   Download YOLOv8 weights from [Ultralytics' official site](https://github.com/ultralytics/ultralytics) and place them in the `Yolo-weights` folder.

5. **Run the Application**:
   ```bash
   python car_counter.py
   ```

## Usage

1. Ensure that you have a video source (either a live camera feed or a video file) placed in the appropriate directory.
2. Customize the `limits` variable in the code to define the line where vehicles will be counted.
3. Run the `car_counter.py` script to start counting vehicles.
4. The system will display the video feed with detected objects, bounding boxes, and the count of vehicles.

## Methodology

### Detection and Tracking

The YOLOv8 model is used for object detection, which identifies vehicles in the frame. SORT (Simple Online and Realtime Tracking) is then used to track each object across multiple frames. Once an object crosses a predefined line in the video frame, it is counted.

### Masking

A mask is applied to the video frames to ensure that only the relevant portions of the image are processed by the detection model. This improves the efficiency of the system and ensures that the detection focuses on the primary areas of interest, such as the road.

### Counting Logic

The system uses a line defined by the `limits` variable. When the center of a detected object crosses this line, the object is counted, and a unique ID is assigned to prevent double counting.

## Technologies Used

- **Python 3.8**: The programming language used for the project.
- **YOLOv8 (Ultralytics)**: Primary object detection model used.
- **OpenCV**: Used for video processing and image manipulation.
- **cvzone**: Helper library to draw bounding boxes and manage object detection visuals.
- **SORT**: Algorithm used for object tracking.

## Contributing

Contributions are welcome! Please fork the repository, create a new branch, and submit a pull request.


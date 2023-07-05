# yolo_video_detect

This program is used for YOLO model detection video, you can use the Realsense camera to view the recognition results in real time



## Building
```bash
git clone https://github.com/TKUwengkunduo/yolo_video_detect.git

cd yolo_video_detect
```

## Get file
1. Put `.weights` in the `/cfg/weights` folder
2. Replace the original files with your own `.cfg`, `.data` and `.name`

## Get darknet file
Please put the following two files in your darknet folder into this folder to replace the original files
`darknet`
`libdarknet.so`

## Modify path
In the `YOLO_Detect.py` file, modify the following lines according to the path and name of your file:
```bash
data_path = 'cfg/yolov4.data'
cfg_path = 'cfg/yolov4.cfg'
weights_path = 'cfg/weights/yolov4.weights'
```

## Run
```bash
python3 YOLO_Detect.py
```

## other
`.data` may need to be changed according to the situation

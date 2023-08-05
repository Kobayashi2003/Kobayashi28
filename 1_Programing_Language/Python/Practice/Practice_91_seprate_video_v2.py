import cv2
import os
import threading

def video_to_frames(video_path, outPutDirName):
    times = 0

    frame_frequency = 300

    if not os.path.exists(outPutDirName):
        os.makedirs(outPutDirName)

    camera = cv2.VideoCapture(video_path)

    while True:
        times = times + 1
        res, image = camera.read()
        if not res:
            print('not res, not image')
            break
        if times % frame_frequency == 0:
            cv2.imwrite(outPutDirName + '/' + str(times) + '.jpg', image)
            print('Saved frame%d.jpg' % (times / frame_frequency))
    print('over')
    camera.release()

if __name__ == '__main__':
    video_path = 'C:\\Users\\KOBAYASHI\\Desktop\\test\\test.mp4'
    outPutDirName = 'C:\\Users\\KOBAYASHI\\Desktop\\test'
    video_to_frames(video_path, outPutDirName)
    
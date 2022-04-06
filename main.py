import cv2
import threading


class CamThread(threading.Thread):

    def __init__(self, preview_name, cam_id):
        threading.Thread.__init__(self)
        self.preview_name = preview_name
        self.cam_id = cam_id

    def run(self):
        print(f'Starting... {self.preview_name}')
        preview_cam(self.preview_name, self.cam_id)


def preview_cam(preview_name, cam_id):
    frame = None

    cv2.namedWindow(preview_name)
    cam = cv2.VideoCapture(cam_id)

    if cam.isOpened():
        success, frame = cam.read()
    else:
        success = False

    while success:
        cv2.imshow(preview_name, frame)
        success, frame = cam.read()
        key = cv2.waitKey(20)

        if key == 27:
            break

    cv2.destroyWindow(preview_name)


if __name__ == '__main__':
    thread1 = CamThread("Canal 01", 'rtsp://admin:agility10@192.168.2.11:554/cam/realmonitor?channel=1&subtype=1')
    thread1.start()

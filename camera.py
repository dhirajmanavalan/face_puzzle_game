import cv2

def capture_image():
    cam = cv2.VideoCapture(0)

    while True:
        ret, frame = cam.read()
        cv2.imshow("Press SPACE to Capture", frame)

        if cv2.waitKey(1) & 0xFF == 32:
            cv2.imwrite("captured.jpg", frame)
            break

    cam.release()
    cv2.destroyAllWindows()
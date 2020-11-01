import cv2


cam = cv2.VideoCapture("Lane Detection Test Video 01.mp4")


while True:
    ret, frame = cam.read()
    if ret is False:
        break
        cv2.imshow("Original", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
cam.release()
cv2.destroyAllwindows()
new_width = frame.shape (tuple of (height, width))
new_height =
cv2.resize(frame, (new_width, new_height)))


upper_left =
upper_right =
lower_left =
lower_right =

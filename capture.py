from datetime import datetime

import cv2
import pandas

first_frame = None
status_list = [0, 0]
times = []
df = pandas.DataFrame(columns=["Start Time", "End Time"])

video = cv2.VideoCapture(0, cv2.CAP_DSHOW)

while True:
    check, frame = video.read()
    status = 0

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    if first_frame is None:
        first_frame = gray
        continue

    delta_frame = cv2.absdiff(first_frame, gray)

    thresh_frame = cv2.threshold(delta_frame, 35, 255, cv2.THRESH_BINARY)[1]

    thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)

    (cnts,_) = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in cnts:
        if cv2.contourArea(contour) < 10000:
            continue

        status = 1
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
    status_list.append(status)
    if status_list[-1] != status_list[-2]:
        if status_list[-1]:
            times.append(datetime.now())
            print('x')
        else:
            times.append(datetime.now())
            print('y')
    cv2.imshow("Capturing", gray)
    cv2.imshow("delta", delta_frame)
    cv2.imshow("delta frame", thresh_frame)
    cv2.imshow("Color Frame", frame)

    key = cv2.waitKey(1)

    if key == ord('q'):
        if status:
            times.append(datetime.now())
        break
print(times)

for i in range(0, len(times), 2):
    df = df.append({"Start Time" : times[i], "End Time" : times[i+1]}, ignore_index=True)

df.to_csv("Times.csv")

video.release()

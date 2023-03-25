import cv2
import numpy as np
import matplotlib.pyplot as plt


MAX_DETECTORS = 2
coord = []
all_aver_gray1 = []
all_aver_gray2 = []
size_of_decorator = 10
time_proshlo = 0
time_first_detector = 0
time_second_detector = 0


def discret(arr):
    listt = []
    for i in range(len(arr)):
        if i == 0:
            listt.append(0)
        elif (arr[0] - arr[i]) > arr[0] * 3 / 100:
            listt.append(1)
        else:
            listt.append(0)

    for i in range(0, len(listt) - 2):
        if listt[i] == 1 and listt[i + 2] == 1:
            listt[i + 1] = 1

    for i in range(0, len(listt) - 3):
        if listt[i] == 1 and listt[i + 3] == 1:
            listt[i + 1] = 1
            listt[i + 2] = 1

    for i in range(0, len(listt) - 3):
        if listt[i] == 0 and listt[i + 3] == 0:
            listt[i + 1] = 0
            listt[i + 2] = 0

    return listt


def add_coord(event, x, y, flags, param):

    global MAX_DETECTORS, ghf, time_first_detector, time_proshlo, time_second_detector

    if event == cv2.EVENT_LBUTTONDOWN:

        if len(coord) == 0 and time_first_detector == 0:
            time_first_detector = time_proshlo
        elif time_second_detector == 0:
            time_second_detector = time_proshlo

        if len(coord) >= MAX_DETECTORS:
            coord[0] = coord[1]
            del coord[1]
            coord.append((x, y))
        else:
            coord.append((x, y))

        ghf = True


def frame_capture(path):

    global coord, time_proshlo, time_first_detector, time_second_detector

    fig1, (ax1, ax2) = plt.subplots(nrows=1, ncols=2)
    ax1.set_title("first")
    ax1.set_ylim(80, 160)
    ax1.set_xlabel("Кадры")
    ax1.set_ylabel("Значение серого")

    ax2.set_title("second")
    ax2.set_ylim(80, 160)
    ax2.set_xlabel("Кадры")
    ax2.set_ylabel("")
    fig1.suptitle("График среднего серого цвета")

    fig2, (ax3, ax4) = plt.subplots(nrows=1, ncols=2)
    ax3.set_title("first")
    ax3.set_ylim(80, 160)
    ax3.set_xlabel("Секунды")
    ax3.set_ylabel("Значение серого")

    ax4.set_title("second")
    ax4.set_ylim(80, 160)
    ax4.set_xlabel("Секунды")
    ax4.set_ylabel("Значение серого")
    fig2.suptitle("График значения серого цвета по времени")

    fig3, (ax5, ax6) = plt.subplots(nrows=1, ncols=2)
    ax5.set_title("first")
    ax5.set_ylim(0, 2)
    ax5.set_xlabel("кадры")
    ax5.set_ylabel("")

    ax6.set_title("second")
    ax6.set_ylim(0, 2)
    ax6.set_xlabel("кадры")
    ax6.set_ylabel("")

    fig3.suptitle("Бинаризированный график для каждого детектора")

    capture = cv2.VideoCapture(path) # path = video.mp4

    if capture:
        count_of_frame = 0
        while True:
            ret, frame = capture.read()  # Получаем сам кадр
            if ret:
                count_of_frame += 1
                cv2.namedWindow('Track')
                cv2.setMouseCallback('Track', add_coord)  # Связываем нажатие мыши с функцией

                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                for i in range(len(coord)):  # Рисуем прямоугольник от нажатия мыши
                    cv2.rectangle(gray, (coord[i][0] - size_of_decorator, coord[i][1] - size_of_decorator),
                                  (coord[i][0] + size_of_decorator, coord[i][1] + size_of_decorator), (255, 0, 255), 2)

                    crop_image = gray[coord[i][1] - size_of_decorator:coord[i][1] + size_of_decorator, coord[i][0] - size_of_decorator:coord[i][0] + size_of_decorator]
                    average_color_row = np.average(crop_image, axis=0)
                    average_color = int(np.average(average_color_row, axis=0))

                    if i == 0:
                        aver_gray1 = average_color
                        all_aver_gray1.append(aver_gray1)
                    else:
                        aver_gray2 = average_color
                        all_aver_gray2.append(aver_gray2)

                cv2.imshow("Track", gray)

            key = cv2.waitKey(60)
            time_proshlo += 1
            if key == ord('q'):
                length1 = min(count_of_frame, len(all_aver_gray1))
                length2 = min(count_of_frame, len(all_aver_gray2))

                ax1.plot(list(range(length1)), all_aver_gray1[:length1])
                ax2.plot(list(range(length2)), all_aver_gray2[:length2])

                len_1 = list()
                for i in range(time_proshlo):
                    if i < time_first_detector:
                        len_1.append(0)
                    elif (i - time_first_detector) < len(all_aver_gray1):
                        len_1.append(all_aver_gray1[i - time_first_detector])
                    else:
                        len_1.append(0)

                len_2 = list()
                for i in range(time_proshlo):
                    if i < time_second_detector:
                        len_2.append(0)
                    elif (i - time_second_detector) < len(all_aver_gray2):
                        len_2.append(all_aver_gray2[i - time_second_detector])
                    else:
                        len_2.append(0)

                ax3.plot(list(map(lambda x: float(float(x) * 0.06), list(range(time_proshlo)))),
                         len_1)
                ax4.plot(list(map(lambda x: float(float(x) * 0.06), list(range(time_proshlo)))),
                         len_2)

                arr1 = discret(all_aver_gray1)
                arr2 = discret(all_aver_gray2)

                ax5.plot(list(range(length1)), arr1[:length1])
                ax6.plot(list(range(length2)), arr2[:length2])

                plt.show()


                count_of_car_1 = 0
                k1 = 0
                while k1 < len(arr1):
                    if arr1[k1] == 1:
                        count_of_car_1 += 1
                        while k1 < len(arr1):
                            if arr1[k1] != 1:
                                break
                            k1 += 1
                    k1 += 1

                count_of_car_2 = 0
                k2 = 0
                while k2 < len(arr2):
                    if arr2[k2] == 1:
                        count_of_car_2 += 1
                        while k2 < len(arr2):
                            if arr2[k2] != 1:
                                break
                            k2 += 1
                    k2 += 1

                print("Count of cars in first detector is " + str(count_of_car_1))
                print("Count of cars in second detector is " + str(count_of_car_2))

                print()

                print("Intensity for first detector is " + str(count_of_car_1 / (time_proshlo * 0.06 - time_first_detector * 0.06)))
                print("Intensity for second detector is " + str(count_of_car_2 / (time_proshlo * 0.06 - time_second_detector * 0.06)))


                bigger = "first detector" if all_aver_gray1[0] > all_aver_gray2[0] else "second detector"
                print("\nBigger grey scale in " + bigger)

                break


if __name__ == '__main__':
    frame_capture("video.mp4")

import cv2


def decode_fourcc(v):
    v = int(v)
    return "".join([chr((v >> 8 * i) & 0xFF) for i in range(4)])


def rplc(a, b):
    return a.replace("1", b)


def get_keys_location(filepath):
    cap = cv2.VideoCapture(filepath)
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

    frame = cap.read()[1]
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = cv2.threshold(frame, 100, 255, cv2.THRESH_BINARY)[1]
    watch_line = frame[int(950 / 1080 * height)]
    sound = {}
    key_name0 = ["D0", "Ds0", "E0", "F0",
                 "Fs0", "G0", "Gs0", "A0", "As0", "B0"]
    key_name1 = ["C1", "Cs1", "D1", "Ds1", "E1",
                 "F1", "Fs1", "G1", "Gs1", "A1", "As1", "B1"]
    key_name2 = [rplc(i, "2") for i in key_name1]
    key_name3 = [rplc(i, "3") for i in key_name1]
    key_name4 = [rplc(i, "4") for i in key_name1]
    key_name5 = [rplc(i, "5") for i in key_name1]
    key_name6 = [rplc(i, "6") for i in key_name1[0:8]]
    key_names = key_name0 + key_name1 + key_name2 + \
                key_name3 + key_name4 + key_name5 + key_name6
    key_number = 10 + 12 * 5 + 8
    left = 15
    right = 15
    Black = 0
    center = 0
    key = 0
    # for k in range(key_number):
    #     print(key_names[k])
    for k in range(int(width) - 15):
        i = k + 15
        if (key <= key_number - 1):
            if (watch_line[i] >= 150) and (Black == 1):
                Black = 0
                left = right
                right = i
                center = int((left + right) / 2)
                print(i)
                print(key_names[key])
                sound[key_names[key]] = [950, center]
                if (watch_line[i + 5] >= 150):
                    sound[key_names[key]] = [950, center - 7]
                print(key, sound[key_names[key]])
                key += 1

            elif (watch_line[i] <= 20) and (Black == 0):
                Black = 1
                left = right
                right = i
                center = int((left + right) / 2)
                print(i)
                print(key_names[key])
                sound[key_names[key]] = [950, center]
                print(key, sound[key_names[key]])
                key += 1
                if (watch_line[i + 10] >= 150):
                    Black = 2
                    key -= 1
            elif (watch_line[i] >= 150) and (Black == 2):
                Black = 1
    # frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
    # for i in range(key_number):
    #     watch_line[int(sound[key_names[i]][1])] = [0, 0, 255]
    # cv2.imwrite("gray_dot.jpg", frame)
    # cv2.destroyAllWindows()
    return sound

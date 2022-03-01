from math import sqrt
import cv2

pt_x, pt_y = None, None
pt1_x, pt1_y = None, None
pt2_x, pt2_y = None, None
full_count = 0
empty_count = 0
line_count = 0
parking_width = 46

font = cv2.FONT_HERSHEY_SIMPLEX


def full_counter():
    global full_count
    full_count += 1
    return full_count


def empty_counter():
    global empty_count
    empty_count += 1
    return empty_count


def line_counter():
    global line_count
    line_count = int((sqrt((pt2_x - pt1_x) ** 2 + (pt2_y - pt1_y) ** 2)) / parking_width)
    return line_count


def search_window(event, x, y, flags, param):
    global pt_x, pt_y, pt1_x, pt1_y, pt2_x, pt2_y

    if event == cv2.EVENT_LBUTTONDOWN:
        pt_x, pt_y = x, y
        pt1_x, pt1_y = x, y

    elif event == cv2.EVENT_LBUTTONUP:
        pt2_x, pt2_y = x, y
        ptm_x = int((pt2_x + pt1_x) / 2)
        ptm_y = int((pt2_y + pt1_y) / 2)
        parking_spaces = line_counter()
        if parking_spaces == 0:
            full_spaces = full_counter()
            cv2.putText(img, f'{full_spaces}', (pt_x - 15, pt_y + 5), font, 1, (0, 0, 255), 2, cv2.LINE_AA)
        else:
            cv2.line(img, (pt1_x, pt1_y), (pt2_x, pt2_y), (0, 0, 0), 2, cv2.LINE_AA)
            cv2.putText(img, f'{parking_spaces}', (ptm_x - 15, ptm_y + 7), font, 1, (0, 0, 255), 2, cv2.LINE_AA)
            for i in range(parking_spaces):
                full_counter()

    if event == cv2.EVENT_RBUTTONDOWN:
        pt_x, pt_y = x, y
        pt1_x, pt1_y = x, y

    elif event == cv2.EVENT_RBUTTONUP:
        pt2_x, pt2_y = x, y
        ptm_x = int((pt2_x + pt1_x) / 2)
        ptm_y = int((pt2_y + pt1_y) / 2)
        parking_spaces = line_counter()
        if parking_spaces == 0:
            full_spaces = empty_counter()
            cv2.putText(img, f'{full_spaces}', (pt_x - 15, pt_y + 5), font, 1, (0, 255, 0), 2, cv2.LINE_AA)
        else:
            cv2.line(img, (pt1_x, pt1_y), (pt2_x, pt2_y), (0, 0, 0), 2, cv2.LINE_AA)
            cv2.putText(img, f'{parking_spaces}', (ptm_x - 15, ptm_y + 7), font, 1, (0, 255, 0), 2, cv2.LINE_AA)
            for i in range(parking_spaces):
                empty_counter()


name = "carpark.jpg"
img = cv2.imread("input/" + name)
img_copy = img.copy()

while True:

    cv2.namedWindow('Image')
    cv2.setMouseCallback('Image', search_window)

    cv2.rectangle(img, (0, 0), (70, 80), (255, 255, 255), -1)
    cv2.putText(img, f'{full_count}', (5, 30), font, 1, (0, 0, 255), 2, cv2.LINE_AA)
    cv2.putText(img, f'{empty_count}', (5, 70), font, 1, (0, 255, 0), 2, cv2.LINE_AA)

    cv2.imshow('Image', img)

    if cv2.waitKey(10) & 0xFF == ord('s'):
        cv2.imwrite("output/" + name, img)

    if cv2.waitKey(10) & 0xFF == 27:
        break

cv2.destroyAllWindows()

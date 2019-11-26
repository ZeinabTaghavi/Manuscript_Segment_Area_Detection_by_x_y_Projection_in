# zeinab Taghavi
#
# time: 2.64
#
# its better image be threshed once before usage
# 1 - correct rotation to more accurately find lines
# 2 - find the high compression vertical area
# 3 - in vertical high compression areas, make all horizontal high compression areas
#

import cv2
import numpy as np


def find_segment_area_by_x_y_projection(img_file, horizontal_percent, vertical_percent):

    def correct_rotation(img):
        edges = cv2.Canny(img, 50, 150, apertureSize=3)
        lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)
        num = 0
        sum = 0

        # if there is no line, or OCR could not find
        try:
            for i in lines:
                for rho, theta in i:
                    if np.degrees(theta) > 60 and np.degrees(theta) < 120:
                        sum += np.degrees(theta)
                        num += 1

            rows, cols = img.shape[0], img.shape[1]
            if num != 0:
                M = cv2.getRotationMatrix2D((cols / 2, rows / 2), (sum / num) - 90, 1)
                img = cv2.warpAffine(img, M, (cols, rows))
                theta_radian = np.radians((sum / num) - 90)
                y = int(np.sin(theta_radian) / np.cos(theta_radian) * img.shape[0])
                img[0:abs(y), :] = 255
                img[img.shape[0] - abs(y):, :] = 255
                x = int(np.sin(theta_radian) / np.cos(theta_radian) * img.shape[1])
                img[:, 0:abs(y)] = 255
                img[:, img.shape[1] - abs(y):] = 255
        except:
            pass

        return img

    img = cv2.imread(img_file)

    # 1 - correct rotation to more accurately find lines

    corrected_rotation = correct_rotation(img)
    gray_corrected_rotation = cv2.cvtColor(img , cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray_corrected_rotation, (5, 5), 0)
    ret, otsu = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    gray_env = cv2.bitwise_not(otsu)
    gray_corrected_rotation = otsu

    # 2 - find the high compression vertical area

    vertical_hist = [sum(gray_env[i,:]) for i in range(corrected_rotation.shape[0])]
    vertical_temp = gray_corrected_rotation.copy()
    vertical_limit = gray_env.shape[1] * 255 * horizontal_percent *.01
    for i in range(len(vertical_hist)):
        if vertical_hist[i] > vertical_limit:
            vertical_temp[i,:] = 255
        else:
            vertical_temp[i,:] = 0

    cv2.imwrite(img_file+'_find_segment_area_by_x_y_projection_1_vertical_line_detected.jpg' , vertical_temp)
    contour , _ = cv2.findContours(vertical_temp , cv2.RETR_TREE , cv2.CHAIN_APPROX_SIMPLE)
    # cv2.drawContours(corrected_rotation , contour , -1 , 100 , 3)

    # 3 - in vertical high compression areas, make all horizontal high compression areas

    vertical_lines_positions = []  # they are vertical high compression areas
    for cnt in contour:
        x , y , w , h = cv2.boundingRect(cnt)
        vertical_lines_positions.append([y,y+h])
        # corrected_rotation = cv2.rectangle(corrected_rotation , (x,y) , (x+w , y+h) , (0,0,200) ,-1)

    gray_corrected_rotation_env = cv2.bitwise_not(otsu)
    line_location_image = np.zeros((otsu.shape[0],otsu.shape[1]),np.uint8)
    line_location_image.fill(255)

    for y1,y2 in vertical_lines_positions:
        temp_img_env = gray_corrected_rotation_env[y1:y2,:]
        horizontal_limit = (y2-y1) * 255 * vertical_percent * .01
        for j in range(temp_img_env.shape[1]):
            if sum(temp_img_env[:,j]) > horizontal_limit:
                line_location_image[y1:y2, j] = 0

    dilate_kernel = np.array((1, 10), np.uint8)
    line_location_image = cv2.erode(line_location_image , kernel=dilate_kernel , iterations=1)
    cv2.imwrite(img_file + '_find_segment_area_by_x_y_projection_2_just_lines.jpg', line_location_image)


if __name__ == '__main__':

    n1 = 1
    n2 = 2

    avg_time = []

    for i in range(n1,n2):

        e1 = cv2.getTickCount()

        img_file = str(i) + '.jpg'

        # vertical_percent , horizontal_percent
        vertical_percent = 11 # if 11 percent of a column is black -> main column
        horizontal_percent = 11  # if 11 percent of a column is black -> main column
        find_segment_area_by_x_y_projection(img_file,horizontal_percent,vertical_percent)

        e2 = cv2.getTickCount()
        print('time:' , str((e2-e1)/cv2.getTickFrequency()) , )



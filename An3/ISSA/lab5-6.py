import cv2
import numpy as np


def solve_linear_eq(y, a, b):
    return (y - b) / a


cam = cv2.VideoCapture('Lane Detection Test Video 01.mp4')
ret, frame = cam.read()

# ex1
# Calculate height and weight for resizing
height, width, channels = frame.shape
height, width = height // 3, width // 3

# Calculate frame points
frame_points = np.array([(width - 1, 0), (0, 0), (0, height - 1), (width - 1, height - 1)])

# Make greyscale image
black_image = np.zeros((height, width), dtype=np.uint8)

# Calculate trapezoid points
top_left = (int(0.45 * width), int(0.75 * height))
top_right = (int(0.55 * width), int(0.75 * height))
bottom_left = (0, height - 1)
bottom_right = (width, height - 1)

# Make trapezoid
trapezoid_points = np.array([top_right, top_left, bottom_left, bottom_right], dtype=np.int32)
cv2.fillConvexPoly(black_image, trapezoid_points, 1)

# Filters
sobel_vertical = np.float32([[-1, -2, -1],
                             [0, 0, 0],
                             [1, 2, 1]])
sobel_horizontal = np.transpose(sobel_vertical)

# point coords for lines
left_top_x = 0
left_top_y = 0

left_bottom_x = 0
left_bottom_y = 0

right_top_x = 0
right_top_y = 0

right_bottom_x = 0
right_bottom_y = 0

left_top_x2 = 0
left_top_y2 = 0

left_bottom_x2 = 0
left_bottom_y2 = 0

right_top_x2 = 0
right_top_y2 = 0

right_bottom_x2 = 0
right_bottom_y2 = 0


#
if __name__ == '__main__':
    while ret:
        # Resizing
        # ex2
        frame = cv2.resize(frame, (width, height))
        frame2 = frame.copy()
        cv2.imshow('ex2-Original', frame2)

        # ex3
        # Converting color
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow('ex3-Grayscale', frame)

        # ex4
        # Highlighting road
        cv2.imshow('Trapezoid', black_image * 255)
        frame = frame * black_image
        cv2.imshow('ex4-Road', frame)

        # ex 5
        # Top-Down
        trapezoid_bounds = np.float32(trapezoid_points)
        frame_bounds = np.float32(frame_points)
        stretch_matrix = cv2.getPerspectiveTransform(trapezoid_bounds, frame_bounds)
        frame = cv2.warpPerspective(frame, stretch_matrix, (width, height))
        cv2.imshow('ex5-Top-Down', frame)

        # ex 6
        # Add blur
        frame = cv2.blur(frame, ksize=(7, 7))
        cv2.imshow('ex6-Blur', frame)

        # ex 7
        # Applying filters
        frame = np.float32(frame)
        frame_vf = cv2.filter2D(frame, -1, sobel_vertical)
        # cv2.imshow('sobel1', cv2.convertScaleAbs(frame_vf))
        frame_hf = cv2.filter2D(frame, -1, sobel_horizontal)
        # cv2.imshow('sobel2', np.float32(frame_vf))

        frame = np.sqrt(frame_hf ** 2 + frame_vf ** 2)
        # Converting back to uint
        frame = cv2.convertScaleAbs(frame)
        cv2.imshow('ex7-Sobel', frame)

        # ex 8
        # 0 or 255 for each pixel
        retur, frame = cv2.threshold(frame, 255 // 3, 255, cv2.THRESH_BINARY)
        # Turn to binary
        cv2.imshow('ex8-Binary', frame)

        # ex 9
        cpy = frame.copy()
        # aici calculez procentaj si dupa ma folosesc de python
        percentage = int(5 / 100 * width)
        frame[:, 0:percentage] = 0
        frame[:, width - percentage:] = 0
        cv2.imshow('Black edges', frame)
        # Left and right white points
        left_xs = []
        left_ys = []
        right_xs = []
        right_ys = []
        left_xs2 = []
        left_ys2 = []
        right_xs2 = []
        right_ys2 = []
        # argwhere
        left_points = np.argwhere(frame[:, :width // 2] == 255)
        right_points = np.argwhere(frame[:, width // 2:] == 255)

        for index in left_points:
            left_xs.append(index[1])
            left_ys.append(index[0])

        for index in right_points:
            right_xs.append(index[1] + width // 2)
            right_ys.append(index[0])
        left_xs = np.array(left_xs)
        left_ys = np.array(left_ys)
        right_xs = np.array(right_xs)
        right_ys = np.array(right_ys)
        # print("Coord ex 9: ", left_xs, left_ys, right_xs2, right_ys2)

        # ex 10
        # Lines that go through them
        left_line = np.polyfit(left_xs, left_ys, deg=1)
        right_line = np.polyfit(right_xs, right_ys, deg=1)
        # Getting points for the lines
        if -10 ** 8 < int(solve_linear_eq(0, left_line[0], left_line[1])) < 10 ** 8 and \
                -10 ** 8 < int(solve_linear_eq(height - 1, left_line[0], left_line[1])) < 10 ** 8 and\
                -10 ** 8 < int(solve_linear_eq(0, right_line[0], right_line[1])) < 10 ** 8 and \
                -10 ** 8 < int(solve_linear_eq(height - 1, right_line[0], right_line[1])) < 10 ** 8:
            left_top_x = int(solve_linear_eq(0, left_line[0], left_line[1]))
            left_top_y = 0

            left_bottom_x = int(solve_linear_eq(height - 1, left_line[0], left_line[1]))
            left_bottom_y = height - 1

            right_top_x = int(solve_linear_eq(0, right_line[0], right_line[1]))
            right_top_y = 0

            right_bottom_x = int(solve_linear_eq(height - 1, right_line[0], right_line[1]))
            right_bottom_y = height - 1

        # Drawing lines
        cv2.line(frame, (left_top_x, left_top_y), (left_bottom_x, left_bottom_y), (200, 0, 0), 5)
        cv2.line(frame, (right_top_x, right_top_y), (right_bottom_x, right_bottom_y), (255, 0, 0), 5)

        cv2.imshow('ex9-10-Lines', frame)

        # BONUS
        # blank_left = frame2.copy()

        blank = np.zeros((height, width), dtype=np.uint8)

        retur, blank1 = cv2.threshold(blank, 255 // 2, 255, cv2.THRESH_BINARY)

        cv2.line(blank, (left_top_x, left_top_y), (left_bottom_x, left_bottom_y), (255, 0, 0), 3)
        cv2.line(blank, (right_top_x, right_top_y), (right_bottom_x, right_bottom_y), (255, 0, 0), 5)

        new_matrix = cv2.getPerspectiveTransform(frame_bounds, trapezoid_bounds)
        blank = cv2.warpPerspective(blank, new_matrix, (width, height))

        # cv2.imshow('Bonus', blank)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        ret, frame = cam.read()

    cam.release()
    cv2.destroyAllWindows()

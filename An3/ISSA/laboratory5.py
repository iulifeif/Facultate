import cv2
import numpy as np


def solve_linear_eq(y, a, b):
    return (y - b) / a


cam = cv2.VideoCapture('Lane Detection Test Video 01.mp4')
ret, frame = cam.read()

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

while ret:
    # Resizing
    frame = cv2.resize(frame, (width, height))
    frame2 = frame.copy()

    # Converting color
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('Grayscale', frame)
    # Highlighting road
    frame = frame * black_image

    cv2.imshow('Road', frame)
    # Birds-eye-view
    trapezoid_bounds = np.float32(trapezoid_points)
    frame_bounds = np.float32(frame_points)
    stretch_matrix = cv2.getPerspectiveTransform(trapezoid_bounds, frame_bounds)
    frame = cv2.warpPerspective(frame, stretch_matrix, (width, height))

    cv2.imshow('Bird eye view', frame)
    # Add blur
    frame = cv2.blur(frame, ksize=(3, 3))
    cv2.imshow('Blur', frame)
    # Applying filters
    frame = np.float32(frame)
    frame_vf = cv2.filter2D(frame, -1, sobel_vertical)
    frame_hf = cv2.filter2D(frame, -1, sobel_horizontal)
    frame = np.sqrt(frame_hf ** 2 + frame_vf ** 2)
    # Converting back to uint
    frame = cv2.convertScaleAbs(frame)
    cv2.imshow('Filters', frame)
    # 0 or 255 for each pixel
    retur, frame = cv2.threshold(frame, 255 // 2, 255, cv2.THRESH_BINARY)
    # Turn to binary
    cv2.imshow('Binary', frame)
    cpy = frame.copy()
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
    left_points = np.argwhere(frame[:, :width // 2] == 255)
    right_points = np.argwhere(frame[:, width // 2:] == 255)

    for p in left_points:
        left_xs.append(p[1])
        left_ys.append(p[0])

    for p in right_points:
        right_xs.append(p[1] + width // 2)
        right_ys.append(p[0])

    left_xs = np.array(left_xs)
    left_ys = np.array(left_ys)
    right_xs = np.array(right_xs)
    right_ys = np.array(right_ys)
    # Lines that go through them
    left_line = np.polyfit(left_xs, left_ys, deg=1)
    right_line = np.polyfit(right_xs, right_ys, deg=1)
    # Getting points for the lines
    if -10 ** 8 < int(solve_linear_eq(0, left_line[0], left_line[1])) < 10 ** 8 and -10 ** 8 < int(
            solve_linear_eq(height - 1, left_line[0], left_line[1])) < 10 ** 8 and -10 ** 8 < int(
        solve_linear_eq(0, right_line[0], right_line[1])) < 10 ** 8 and -10 ** 8 < \
            int(solve_linear_eq(height - 1, right_line[0], right_line[1])) < 10 ** 8:
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
    cv2.line(frame, (right_top_x, right_top_y), (right_bottom_x, right_bottom_y), (100, 0, 0), 5)

    # 11

    blank1 = np.zeros((height, width), dtype=np.uint8)
    cv2.line(blank1, (left_top_x, left_top_y), (left_bottom_x, left_bottom_y), (255, 0, 0), 3)
    cv2.line(blank1, (right_top_x, right_top_y), (right_bottom_x, right_bottom_y), (100, 0, 0), 5)

    new_matrix = cv2.getPerspectiveTransform(frame_bounds, trapezoid_bounds)
    blank1 = cv2.warpPerspective(blank1, new_matrix, (width, height))

    # left_points2 = np.argwhere(blank1[:, :width // 2] == 255)
    # right_points2 = np.argwhere(blank1[:, width // 2:] == 255)
    #
    # for p in left_points2:
    #     left_xs2.append(p[1])
    #     left_ys2.append(p[0])
    # for p in right_points2:
    #     right_xs2.append(p[1] + width // 2)
    #     right_ys2.append(p[0])
    #
    # left_xs2 = np.array(left_xs2)
    # left_ys2 = np.array(left_ys2)
    # right_xs2 = np.array(right_xs2)
    # right_ys2 = np.array(right_ys2)
    #
    # left_line2 = np.polyfit(left_xs2, left_ys2, deg=1)
    # right_line2 = np.polyfit(right_xs2, right_ys2, deg=1)
    #
    # left_top_x2 = int(solve_linear_eq(0, left_line2[0], left_line2[1]))
    # left_top_y2 = 0
    #
    # left_bottom_x2 = int(solve_linear_eq(height - 1, left_line2[0], left_line2[1]))
    # left_bottom_y2 = height - 1
    #
    # right_top_x2 = int(solve_linear_eq(0, right_line2[0], right_line2[1]))
    # right_top_y2 = 0
    #
    # right_bottom_x2 = int(solve_linear_eq(height - 1, right_line2[0], right_line2[1]))
    # right_bottom_y2 = height - 1
    #
    # cv2.line(frame2, (left_top_x2, left_top_y2), (left_bottom_x2, left_bottom_y2), (255, 0, 0), 3)
    # cv2.line(frame2, (right_top_x2, right_top_y2), (right_bottom_x2, right_bottom_y2), (100, 0, 0), 5)

    cv2.imshow('Done', frame)
    #cv2.imshow('PLEASE PLEASE', frame2)
    cv2.imshow('Final', blank1)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    ret, frame = cam.read()

cam.release()
cv2.destroyAllWindows()

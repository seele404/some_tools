import cv2
import mediapipe as mp
import numpy as np
import pygame
from pygame.locals import DOUBLEBUF, OPENGL
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
# 切换摄像头可以改成1，2，3...
capture_dev = 0
# 初始化 Pygame 和 OpenGL
pygame.init()
display = (800, 600)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
glTranslatef(0.0, 0.0, -5)
thumb_gl_point = 0
indexfinger_gl_point = 0
# 初始化旋转角度和鼠标状态
rot_x, rot_y = 0.0, 0.0
mouse_down = False
last_mouse_pos = (0, 0)

# 视频捕获和处理函数
def video_capture():
    global rot_x, rot_y, mouse_down, last_mouse_pos
    cap = cv2.VideoCapture(capture_dev)
    if not cap.isOpened():
        print("无法打开摄像头")
        exit()

    while True:
        # 处理 Pygame 事件以保持窗口响应
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cap.release()
                pygame.quit()
                cv2.destroyAllWindows()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 左键按下
                    mouse_down = True
                    last_mouse_pos = pygame.mouse.get_pos()
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # 左键释放
                    mouse_down = False
            elif event.type == pygame.MOUSEMOTION:
                if mouse_down:
                    x, y = pygame.mouse.get_pos()
                    dx, dy = x - last_mouse_pos[0], y - last_mouse_pos[1]
                    last_mouse_pos = (x, y)
                    rot_x += dy * 0.1  # 调整这些值以改变旋转速度
                    rot_y += dx * 0.1

        # 读取和处理 OpenCV 帧
        ret, frame = cap.read()
        if not ret:
            print("无法接收帧(视频流已结束？)")
            break
        frame = cv2.flip(frame, 1)
        # 调用detect_and_draw_hand_landmarks函数
        hand_landmarks = detect_and_draw_hand_landmarks(frame) 
        # 调用draw_palm_points函数
        draw_palm_points(frame, hand_landmarks)
        cv2.imshow('Frame', frame)

        # 如果按下 'q' 或关闭窗口，则退出
        if cv2.waitKey(1) == ord('q') or cv2.getWindowProperty('Frame', cv2.WND_PROP_VISIBLE) < 1:
            break

    cap.release()
    pygame.quit()
    cv2.destroyAllWindows()

# 测量手部区域上的关键点和边缘，并呈现关键点
def detect_and_draw_hand_landmarks(frame):
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=False, 
                           max_num_hands=2, 
                           min_detection_confidence=0.5)

    mp_drawing = mp.solutions.drawing_utils
    rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_image)

    hand_landmarks = None
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks)
            for id, landmark in enumerate(hand_landmarks.landmark):
                print(f'Landmark {id}: x={landmark.x}, y={landmark.y}, z={landmark.z}')
                
    hands.close()
    return hand_landmarks

# 描绘手指捏合时的轨迹点跟踪与显示
def draw_palm_points(frame, hand_landmarks, history_palm_points=[]):
    if not hand_landmarks:
        history_palm_points.clear()
        return
    thumb_index = 4
    indexfinger_index = 8

    indexfinger_point = hand_landmarks.landmark[indexfinger_index]
    thumb_point = hand_landmarks.landmark[thumb_index]

    # 转换坐标并绘制到opengl
    thumb_gl_point = mediapipe_to_opengl_coords(thumb_point, display[0], display[1])
    indexfinger_gl_point = mediapipe_to_opengl_coords(indexfinger_point, display[0], display[1])
    # 处理和绘制 OpenGL 窗口
    draw_opengl_points([thumb_gl_point, indexfinger_gl_point])

    finger_distance = np.sqrt((thumb_point.x - indexfinger_point.x) ** 2 
                + (thumb_point.y - indexfinger_point.y) ** 2)
    if finger_distance < 0.1:
        palm_point = [int((thumb_point.x + indexfinger_point.x) * frame.shape[1] // 2),
                                    int((thumb_point.y + indexfinger_point.y) * frame.shape[0] // 2)]
        history_palm_points.append(palm_point)
    
    if len(history_palm_points) < 2:
        pass
    else:
        for i in range(1, len(history_palm_points)):
            cv2.line(frame, tuple(history_palm_points[i-1][:2]), tuple(history_palm_points[i][:2]), (0, 255, 255), 5) 

def mediapipe_to_opengl_coords(mp_point, screen_width, screen_height):
    # 将 MediaPipe 归一化坐标转换为屏幕坐标
    screen_x = mp_point.x * screen_width
    screen_y = screen_height - mp_point.y * screen_height  # Y坐标翻转

    # 将屏幕坐标转换为 OpenGL 坐标
    gl_x = (screen_x - screen_width / 2) / (screen_width / 2)
    gl_y = (screen_y - screen_height / 2) / (screen_height / 2)
    gl_z = mp_point.z  # Z坐标可直接使用或需要调整比例

    return (gl_x, gl_y, gl_z)
# OpenGL 绘制函数
def draw_opengl_points(points):
    global rot_x, rot_y
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    # glTranslatef(0.0, 0.0, -5)
    glRotatef(rot_x, 1, 0, 0)
    glRotatef(rot_y, 0, 1, 0)
    
    # 设置点的大小
    glPointSize(10.0)

    # 绘制点
    glBegin(GL_POINTS)
    glColor3f(1, 1, 1)  # 设置为白色
    for point in points:
        glVertex3fv(point)
    glEnd()

    # 绘制坐标轴线
    glBegin(GL_LINES)
    # X 轴 - 红色
    glColor3f(1, 0, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(1, 0, 0)

    # Y 轴 - 绿色
    glColor3f(0, 1, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(0, 1, 0)

    # Z 轴 - 蓝色
    glColor3f(0, 0, 1)
    glVertex3f(0, 0, 0)
    glVertex3f(0, 0, 1)
    glEnd()

    pygame.display.flip()





# 调用video_capture函数
if __name__ == '__main__':
    video_capture()




import numpy as np

# 定义四元数
def create_quaternion(w, x, y, z):
    return np.array([w, x, y, z])

# 四元数乘法
def quaternion_multiply(q1, q2):
    w1, x1, y1, z1 = q1
    w2, x2, y2, z2 = q2
    w = w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2
    x = w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2
    y = w1 * y2 + y1 * w2 + z1 * x2 - x1 * z2
    z = w1 * z2 + z1 * w2 + x1 * y2 - y1 * x2
    return np.array([w, x, y, z])

# 四元数共轭
def quaternion_conjugate(q):
    w, x, y, z = q
    return np.array([w, -x, -y, -z])

# 使用四元数旋转一个点
def rotate_point(p, q):
    p_quat = np.insert(p, 0, 0)  # 将点p转换为四元数形式,索引0插入值0
    q_conj = quaternion_conjugate(q)
    return quaternion_multiply(quaternion_multiply(q, p_quat), q_conj)[1:]  # 返回旋转后的坐标（忽略w）

# 创建表示绕Z轴旋转90度的四元数
q = create_quaternion(0.707, 0, 0, 0.707)

# 定义要旋转的点（例如：(1,0,0)表示沿x轴）
point = np.array([1, 1, 1])

# 使用四元数旋转这个点
rotated_point = rotate_point(point, q)

print("原始点:", point)
print("旋转后的点:", rotated_point)
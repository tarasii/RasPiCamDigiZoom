import cv2

def draw_label(img, text, pos, bg_color):
    font_face = cv2.FONT_HERSHEY_SIMPLEX
    scale = 0.4
    color = (0, 0, 0)
    thickness = cv2.FILLED
    margin = 2

    txt_size = cv2.getTextSize(text, font_face, scale, thickness)

    end_x = pos[0] + txt_size[0][0] + margin
    end_y = pos[1] - txt_size[0][1] - margin

    #cv2.rectangle(img, pos, (end_x, end_y), bg_color, thickness)
    cv2.putText(img, text, pos, font_face, scale, color, 1, cv2.LINE_AA)


class xy(object):
    """docstring for xy"""
    def __init__(self, x, y):
        super(xy, self).__init__()
        self.x = x
        self.y = y

    def point():
        return (self.x, self.y)
        


def draw_lines(img, lines):
    for p0, p1, color in lines:
        cv2.line(img, p0, p1, color)


class colors():
    white = (255, 255, 255)
    black = (0,0,0)

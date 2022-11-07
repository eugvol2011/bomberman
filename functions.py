def point_in_area(px, py, x, y, w, h):
    if x <= px <= x + w and y <= py <= y + h:
        return True
    else:
        return False


def in_contact(px, py, pw, ph, x, y, w, h, sensitive):
    if (point_in_area(px + sensitive, py + sensitive, x, y, w, h) or
            point_in_area(px + sensitive, py + ph - sensitive, x, y, w, h) or
            point_in_area(px + pw - sensitive, py + ph - sensitive, x, y, w,
                          h) or
            point_in_area(px + pw - sensitive, py + sensitive, x, y, w, h) or
            (point_in_area(x, y + h, px + sensitive, py + sensitive, pw - sensitive,
                           ph - sensitive) and point_in_area(x + w, y + h,
                                                             px + sensitive, py + sensitive,
                                                             pw - sensitive, ph - sensitive)) or
            (point_in_area(x + w, y + h, px + sensitive, py + sensitive, pw - sensitive,
                           ph - sensitive) and point_in_area(x + w, y,
                                                             px + sensitive, py + sensitive,
                                                             pw - sensitive,
                                                             ph - sensitive)) or
            (point_in_area(x, y, px + sensitive, py + sensitive, pw - sensitive,
                           ph - sensitive) and point_in_area(x + w, y, px + sensitive,
                                                             py + sensitive, pw - sensitive,
                                                             ph - sensitive)) or
            (point_in_area(x, y, px + sensitive, py + sensitive, pw - sensitive,
                           ph - sensitive) and point_in_area(x, y + h, px + sensitive,
                                                             py + sensitive, pw - sensitive,
                                                             ph - sensitive))):
        return True

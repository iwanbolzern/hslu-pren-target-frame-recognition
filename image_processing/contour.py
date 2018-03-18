import cv2
from typing import Tuple, List


class Contour:

    def __init__(self, points):
        self._points = points
        self._center = None
        self._area = None

    @property
    def center(self) -> Tuple[int, int]:
        if not self._center:
            M = cv2.moments(self._points)
            divider = max(M["m00"], 0.001)
            self._center = (int(M["m10"] / divider), int(M["m01"] / divider))
        return self._center

    @property
    def area(self) -> float:
        if not self._area:
            self._area = cv2.contourArea(self._points)
        return self._area

    @property
    def points(self) -> List[Tuple[float, float]]:
        return self._points

    @points.setter
    def points(self, value):
        self.__init__(value)

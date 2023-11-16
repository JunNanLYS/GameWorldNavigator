import unittest

import cv2

from gamenavigator.ocr_recognition import text_in_img

apex = cv2.imread(r".\images\Apex Legends.png")
star_rail = cv2.imread(r".\images\StarRail.png")


class TestInImage(unittest.TestCase):

    def test_1(self) -> None:
        self.assertEqual(True, text_in_img(apex, "万蒂奇"))
        self.assertEqual(False, text_in_img(apex, "亡灵"))
        self.assertEqual(True, text_in_img(apex, "侦察"))
        self.assertEqual(True, text_in_img(apex, "突击"))

    def test_2(self) -> None:
        self.assertEqual(True, text_in_img(star_rail, "开始游戏"))
        self.assertEqual(True, text_in_img(star_rail, "版本热点"))
        self.assertEqual(False, text_in_img(star_rail, "霍霍"))
        self.assertEqual(True, text_in_img(star_rail, "银河铁道之声"))
        self.assertEqual(True, text_in_img(star_rail, "1.5"))
        self.assertEqual(False, text_in_img(star_rail, "迷惑之谈"))


if __name__ == '__main__':
    unittest.main()

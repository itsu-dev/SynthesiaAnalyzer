from get_keys_location import get_keys_location
import movie_analyzer


def export_as_score(elements, channel_count):
    text = ""
    for k, v in elements.items():
        t = "M"
        if v.__class__.__name__ == "Stop":
            t = "S"

        key = ""
        for i in range(0, channel_count):
            key = k.replace("_s_" + str(i), "").replace("_m_" + str(i), "")

        text += \
            key + " " + \
            t + " " + \
            ",".join(v.sounds) + " " + \
            k.split("_")[2] + "\n"

    print(text)


# よく使われる色
color_yellow = [[30, 40], [220, 255], [220, 255]]  # 色の範囲（黄色）
color_red = [[220, 240], [170, 230], [220, 255]]  # 色の範囲（赤色）
color_blue = [[140, 220], [180, 240], [220, 255]]  # TODO 色の範囲（青色）
color_green = [[140, 220], [180, 240], [220, 255]]  # TODO 色の範囲（緑色）


class Channel:
    def __init__(self, color, program, velocity=100, name=''):
        self.color = color  # 検出する色の範囲
        self.program = program  # 楽器ID
        self.velocity = velocity  # 強さ
        self.name = name  # チャンネル名


keys = get_keys_location('test.mp4')
elements = movie_analyzer.analyze(
    keys,
    'test.mp4',  # 読み込む動画ファイル
    [
        Channel(color=color_yellow, program=11, velocity=100, name='Piano1'),  # チャンネル0
        Channel(color=color_red, program=11, velocity=100, name='Piano2')  # チャンネル1
    ],   'test.mid',  # MIDI出力先
    120  # テンポ
)


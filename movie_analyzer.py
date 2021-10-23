import cv2
import numpy as np

from midi_exporter import MIDIExporter


class Element:
    def __init__(self, channel: int, sounds: list):
        self.channel = channel
        self.sounds = sounds


class Music(Element):
    def __init__(self, channel: int, sounds: list):
        super(Music, self).__init__(channel, sounds)


class Stop(Element):
    def __init__(self, channel: int, sounds: list):
        super(Stop, self).__init__(channel, sounds)


def analyze(keys: dict, target_file: str, channels: list, midi_file: str = None, tempo: int = 120):
    debug = False  # デバッグモード

    # その時点で押されているキーの辞書（キー名[str]:ms[int]）
    available_keys = [{} for _ in range(0, len(channels))]

    # 結果の辞書（ms[int]:要素[Element]）
    result = {}

    # 画像認識関連
    cap = cv2.VideoCapture(target_file)
    fps = cap.get(cv2.CAP_PROP_FPS)  # fps
    frame_rate = int((1 / fps) * 1000)  # 1フレーム当たりのミリ秒
    ms = 0  # その時点での時間

    # MIDI関連
    export_as_midi = midi_file is not None
    midi: MIDIExporter
    tick: float

    if export_as_midi:
        midi = MIDIExporter(midi_file, tempo)
        tick = (60 / tempo) / 480  # 1拍=480tick

    while True:
        ret, frame = cap.read()
        if not ret:
            break  # 映像取得に失敗

        # すべてのキーの座標に対して
        for k, v in keys.items():
            bgr = np.uint8([[frame[int(v[0]), int(v[1])]]])  # キーの位置の色を取得
            hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)  # 色空間の変換: BGR -> HSV
            hsv_h = hsv[0, 0, 0]
            hsv_s = hsv[0, 0, 1]
            hsv_v = hsv[0, 0, 2]

            # 識別対象の色に対して
            for i in range(0, len(channels)):
                # 現時点でキーが押されていたら...
                if channels[i].color[1][0] <= hsv_s <= channels[i].color[1][1]\
                        and channels[i].color[2][0] <= hsv_v <= channels[i].color[2][1]:
                    if debug:
                        frame = cv2.circle(frame, [v[1], v[0]], 3, [255, 0, 0], 3)  # 押されているキーに色を付ける

                    if export_as_midi:
                        midi.create_instrument(i, channels[i].program, channels[i].name)  # MIDIにチャンネルが登録されていなければ生成する

                    # この時間に初めてキーが押されているならば
                    if k not in available_keys[i].keys():
                        available_keys[i][k] = ms  # キーが押されたとして登録する
                        print(ms, k)

                # ひとつ前の時間では押されていたがこの時点でキーが離されたならば
                elif k in available_keys[i].keys():
                    # MIDIに音符を登録
                    if export_as_midi:
                        midi.append_note(i, channels[i].velocity, k, available_keys[i][k] * tick, ms * tick)

                    if str(available_keys[i][k]) + "_m_" + str(i) in result.keys():
                        result[str(available_keys[i][k]) + "_m_" + str(i)].sounds.append(k)
                    else:
                        result[str(available_keys[i][k]) + "_m_" + str(i)] = Music(i, [k])

                    if str(ms) + "_s_" + str(i) in result.keys():
                        result[str(ms) + "_s_" + str(i)].sounds.append(k)
                    else:
                        result[str(ms) + "_s_" + str(i)] = Stop(i, [k])

                    available_keys[i].pop(k)  # キーが押されていない状態に戻す

        if debug:
            cv2.imshow('f', frame)
            cv2.waitKey(1)

        ms += frame_rate

    cap.release()

    # MIDIファイルとして保存する
    if export_as_midi:
        midi.export()

    return result

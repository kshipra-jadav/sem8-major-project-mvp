import time

import cv2

from utils import play_audio, setup_camera, sceneDetection
from stt import speech_to_text
from tts import text_to_speech


TIMES_EXEC = 0


def main():
    cv2.namedWindow("Frame")  # Remove after porting to Linux
    while True:
        global TIMES_EXEC

        if TIMES_EXEC == 0:
            play_audio(filename="greeting_openai.mp3")

            TIMES_EXEC += 1

        key = cv2.waitKey(1)

        if key == ord('s'):
            play_audio("sd_openai.mp3", bg=False)

            # cap = setup_camera()

            # for _ in range(10):
            #     ret, frame = cap.read()

            # _, frame = cap.read()

            frame = cv2.imread("test.jpg")  # Remove after porting to Linux.

            text = speech_to_text()
            print(text)

            play_audio("processing_openai.mp3")

            response = sceneDetection(frame, text)

            print(f"\nResponse - {response}\n")

            text_to_speech(response)

        if key == ord('o'):
            play_audio("ocr_openai.mp3")

            # cap = setup_camera()

            # for _ in range(10):
            #     ret, frame = cap.read()

            # time.sleep(2)

            # _, frame = cap.read()

            frame = cv2.imread("snap1.jpg")

            text = "Please perform OCR on this image. Only return exactly what is written in the image and nothing else."

            response = sceneDetection(frame, text)

            print(f"\nResponse - {response}\n")

            text_to_speech(response)

        if key == ord('q'):  # Remove after porting to Linux.
            cv2.destroyAllWindows()
            break


if __name__ == "__main__":
    main()

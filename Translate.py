from google.cloud import translate
from google.cloud import vision
import anki_vector
import time

def main():
    client = vision.ImageAnnotatorClient()
    translate_client = translate.Client()
    target = 'en'
    with anki_vector.Robot(enable_camera_feed=True) as robot:
        for _ in range(30):
            while not robot.camera.latest_image:
                time.sleep(1.0)
            image = robot.camera.latest_image
            response = client.text_detection(image=image)
            texts = response.text_annotations
            translation = translate_client.translate(texts,target_language=target)
            print(u'Text: {}'.format(texts))
            print(u'Translation: {}'.format(translation['translatedText']))
            image.show()
            robot.say_text(translation)


if __name__ == "__main__":
    main()

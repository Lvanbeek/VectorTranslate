import os
import io
from google.cloud import translate
from google.cloud import vision
import anki_vector
import time
from PIL import Image
from google.protobuf.json_format import MessageToJson

def main():
    client = vision.ImageAnnotatorClient()
    translate_client = translate.Client()
    target = 'en'
    with anki_vector.Robot() as robot:
        robot.camera.init_camera_feed()
        for _ in range(30):
            while not robot.camera.latest_image:
                time.sleep(1.0)
            photo = robot.camera.latest_image.raw_image
            imgByteArr = io.BytesIO()
            photo.save(imgByteArr, format='PNG')
            content = imgByteArr.getvalue()
            image = vision.types.Image(content=content)
            response = client.document_text_detection(image=image)
            texts = response.full_text_annotation.text
            translation = translate_client.translate(texts, target_language=target)
            print(u'Text: {}'.format(texts))
            print(u'Translation: {}'.format(translation['translatedText']))
            say = u'{}'.format(translation['translatedText'])
            robot.behavior.say_text(say)


if __name__ == "__main__":
    main()

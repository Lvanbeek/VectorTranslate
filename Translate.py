import io
from google.cloud import translate
from google.cloud import vision
import anki_vector
import time
from anki_vector.events import Events
from anki_vector.util import degrees
import functools
import threading



def main():
    client = vision.ImageAnnotatorClient()
    translate_client = translate.Client()
    target = 'en'
    evt = threading.Event()

    def on_tapped_cube(robot, event_type, event, evt):
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

    args = anki_vector.util.parse_command_args()
    with anki_vector.Robot(args.serial) as robot:
        robot.conn.request_control()
        robot.camera.init_camera_feed()
        robot.behavior.set_head_angle(degrees(0.0))
        robot.world.connect_cube()
        on_tapped_cube = functools.partial(on_tapped_cube, robot)
        robot.events.subscribe(on_tapped_cube, Events.object_tapped)
        print("ready")
        j = 0
        while j < 600:
            time.sleep(1)
            j += 1
        robot.behavior.say_text("My head hurts, I need to rest")


if __name__ == "__main__":
    main()

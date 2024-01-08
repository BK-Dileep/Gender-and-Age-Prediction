import cv2
import dlib

from os.path import join
def load_model(model_path, caffemodel, prototxt):
    caffemodel_path = join(model_path, caffemodel)
    prototxt_path = join(model_path, prototxt)
    model = cv2.dnn.readNet(prototxt_path, caffemodel_path)

    return model


def predict(model, img, height, width):
    face_blob = cv2.dnn.blobFromImage(img, 1.0, (height, width), (0.485, 0.456, 0.406))
    model.setInput(face_blob)
    predictions = model.forward()
    class_num = predictions[0].argmax()
    confidence = predictions[0][class_num]

    return class_num, confidence
detector = dlib.get_frontal_face_detector()
font, fontScale, fontColor, lineType = cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2

input_height = 224
input_width = 224

# load gender model
gender_model_path = 'models/gender'
gender_caffemodel = 'gender.caffemodel'
gender_prototxt = 'gender.prototxt'
gender_model = load_model(gender_model_path, gender_caffemodel, gender_prototxt)

# load age model
age_model_path = 'models/age'
age_caffemodel = 'dex_chalearn_iccv2015.caffemodel'
age_prototxt = 'age.prototxt'
age_model = load_model(age_model_path, age_caffemodel, age_prototxt)

cap = cv2.VideoCapture(0)


while cap.isOpened():
        _, frame_bgr = cap.read()

        if frame_bgr is not None:
            frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
            faces = detector(frame_rgb, 1)

            for d in faces:
                left = int(1.0 * d.left())     # + 40% margin
                top = int(1.0 * d.top())       # + 40% margin
                right = int(1.7 * d.right())   # + 40% margin
                bottom = int(1.7 * d.bottom()) # + 40% margin
                face_segm = frame_rgb[top:bottom, left:right]
                gender, gender_confidence = predict(gender_model, face_segm, input_height, input_width)
                age, age_confidence = predict(age_model, face_segm, input_height, input_width)
                gender = 'male' if gender == 1 else 'female'
                text = '{} ({:.2f}%) {} ({:.2f}%)'.format(gender, gender_confidence*100, age-5, age_confidence*100)
                cv2.putText(frame_bgr, text, (d.left(), d.top() - 20), font, fontScale, fontColor, lineType)
                cv2.rectangle(frame_bgr, (d.left(), d.top()), (d.right(), d.bottom()), fontColor, 2)
                cv2.imshow('frame', frame_bgr)
                
                
                if cv2.waitKey(33) & 0xFF == ord('\n'):
                    break
        
cv2.destroyAllWindows()
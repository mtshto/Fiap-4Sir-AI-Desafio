import cv2
import numpy as np
from ultralytics import YOLO

model = YOLO('weights/yolov8n-football.pt')

# Carregar o arquivo de texto com os nomes das classes
class_names = []
with open("weights/classes.txt", "r") as file:
    class_names = [line.strip() for line in file.readlines()]

#cap = cv2.VideoCapture("videos/spfc560p")
cap = cv2.VideoCapture("videos/spfc560p-editado.mp4")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    #TODO: Implementar aqui lógica para pegar somente parte do campo
    #Fazer isso com o vídeo spfc560p.mp4, o editado é um vídeo com a torcida cortada no editor...
    #Houve uma melhoria de uns 15~20% perfomance com isso.

    #Em Windows altere o device para gpu, no Mac (M1+) mantenha mps
    results = model(source=frame, conf=0.25, device="mps", task="detect", mode="predict")
    result = results[0]

    bboxes = np.array(result.boxes.xyxy.cpu(), dtype="int")
    classes = np.array(result.boxes.cls.cpu(), dtype="int")

    print (classes)

    for cls, bbox in zip(classes, bboxes):
        (x, y, x2, y2) = bbox
        class_name = class_names[cls]
        cv2.rectangle(frame, (x,y), (x2,y2), (0,0,255), 2)
        cv2.putText(frame, class_name, (x,y-5), cv2.FONT_HERSHEY_PLAIN, 2, (0,0,255), 2)


    cv2.imshow("", frame)

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
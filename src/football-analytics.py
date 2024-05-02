import cv2
import numpy as np
from ultralytics import YOLO

# Função para calcular IoU entre duas caixas delimitadoras
def calculate_iou(box1, box2):
    # Coordenadas para interseção
    x1 = max(box1[0], box2[0])
    y1 = max(box1[1], box2[1])
    x2 = min(box1[2], box2[2])
    y2 = min(box1[3], box2[3])

    # Área de interseção
    inter_area = max(0, x2 - x1) * max(0, y2 - y1)

    # Área de cada caixa delimitadora
    box1_area = (box1[2] - box1[0]) * (box1[3] - box1[1])
    box2_area = (box2[2] - box2[0]) * (box2[3] - box2[1])

    # Área de união
    union_area = box1_area + box2_area - inter_area

    # IoU
    iou = inter_area / union_area

    return iou


model = YOLO('weights/yolov8n-football.pt')

# Carregar o arquivo de texto com os nomes das classes
class_names = []
with open("weights/classes.txt", "r") as file:
    class_names = [line.strip() for line in file.readlines()]

cap = cv2.VideoCapture("videos/mciXrma22.mp4")

# Manter o estado do frame anterior
previous_message = ""

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(source=frame, conf=0.1, device="mps", task="detect", mode="predict")
    result = results[0]

    bboxes = np.array(result.boxes.xyxy.cpu(), dtype="int")
    classes = np.array(result.boxes.cls.cpu(), dtype="int")

    # Encontre a caixa delimitadora para a bola e jogadores
    ball_bbox = None
    player_bboxes = []

    for cls, bbox in zip(classes, bboxes):
        (x, y, x2, y2) = bbox
        class_name = class_names[cls]

        cv2.rectangle(frame, (x, y), (x2, y2), (0, 0, 255), 2)
        cv2.putText(frame, class_name, (x, y - 5), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)

        if class_name == "Bola":
            ball_bbox = bbox
        elif class_name == "Jogador":
            player_bboxes.append(bbox)

    # Mensagem para indicar posse da bola
    current_message = ""

    # Se a bola foi detectada, verificar a posse da bola
    if ball_bbox is not None:
        possession = False
        for player_bbox in player_bboxes:
            iou = calculate_iou(ball_bbox, player_bbox)
            if iou > 0:  # Limite para indicar posse da bola
                current_message = "Um jogador tem a posse da bola"
                possession = True
                break
        
        if not possession:
            current_message = "Nenhum jogador tem posse da bola"
            
        # Verificar se houve um passe
        if previous_message == "Um jogador tem a posse da bola" and current_message == "Nenhum jogador tem posse da bola":
            current_message = "Passe detectado"

    else:
        # Se a bola não foi detectada, mantenha o estado do frame anterior
        current_message = previous_message

    # Mostre a mensagem no frame
    if current_message:
        cv2.putText(frame, current_message, (400, 40), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

    previous_message = current_message  # Atualize o estado para o próximo frame

    cv2.imshow("Football Detection", frame)

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()

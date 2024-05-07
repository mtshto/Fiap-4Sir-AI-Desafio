import cv2
import numpy as np
from ultralytics import YOLO
import time

# Função para calcular a distância euclidiana entre dois pontos
def euclidean_distance(p1, p2):
    return np.linalg.norm(np.array(p1) - np.array(p2))

# Criar janela para o vídeo e painel de status
cv2.namedWindow("Football Detection", cv2.WINDOW_NORMAL)

model = YOLO('weights/yolov8n-football.pt')

class_names = []
with open("weights/classes.txt", "r") as file:
    class_names = [line.strip() for line in file.readlines()]

#Vídeos para teste:
cap = cv2.VideoCapture("videos/mciXrma22gol.mp4")
#cap = cv2.VideoCapture("videos/barXbay20gol.mp4")

# Status para posse, passe e gol
possession = False
pass_detected = False
goal_detected = False
goal_time = None  # Controlador do tempo para manter a indicação de gol
pass_timer = None
goal_timeout = 5  # Manter a indicação de gol por 5 segundos

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(source=frame, conf=0.1, device="mps", task="detect", mode="predict")
    result = results[0]

    bboxes = np.array(result.boxes.xyxy.cpu(), dtype="int")
    classes = np.array(result.boxes.cls.cpu(), dtype="int")

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

    # Calcular posição central das caixas
    ball_center = ((ball_bbox[0] + ball_bbox[2]) / 2, (ball_bbox[1] + bbox[3]) / 2) if ball_bbox is not None else None
    player_centers = [((bbox[0] + bbox[2]) / 2, ((bbox[1] + bbox[3]) / 2)) for bbox in player_bboxes]

    # Detecção de posse
    if ball_center:
        possession = False
        for player_center in player_centers:
            if euclidean_distance(ball_center, player_center) < 50:
                possession = True
                break

    # Detecção de passe
    if possession:
        pass_timer = None
        pass_detected = False
    else:
        if pass_timer is None:
            pass_timer = time.time()

        if (time.time() - pass_timer) > 1:
            pass_detected = True
            pass_timer = None

    # Detecção de gol - MELHORA OU PIORA A VALIDAÇÂO, IDEAL SERIA TROCAR POR UMA DETECÇÃO DA TRAVE.
    goal_line = frame.shape[1] - 100

    if ball_center and ball_center[0] > goal_line:
        goal_time = time.time()  # Atualiza o tempo para manter a indicação de gol
        goal_detected = True

    # Manter o indicador de gol por 5 segundos após detecção
    if goal_time is not None and (time.time() - goal_time) > goal_timeout:
        goal_detected = False
        goal_time = None

    # Painel de status
    status_frame = np.zeros((frame.shape[0], 100, 3), dtype=np.uint8)
    status_frame.fill(255)  # Branco para contraste

    # Caixa para posse
    cv2.putText(status_frame, "POSSE", (10, 30), 2, cv2.FONT_HERSHEY_PLAIN, (0, 0, 0), 2)
    cv2.rectangle(status_frame, (10, 40), (90, 80), (0, 255, 0) if possession else (0, 0, 0), 2)
    if possession:
        cv2.putText(status_frame, "X", (50, 65), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

    # Caixa para passe
    cv2.putText(status_frame, "PASSE", (10, 110), 2, cv2.FONT_HERSHEY_PLAIN, (0, 0, 0), 2)
    cv2.rectangle(status_frame, (10, 120), (90, 160), (0, 255, 0) if pass_detected else (0, 0, 0), 2)
    if pass_detected:
        cv2.putText(status_frame, "X", (50, 135), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

    # Caixa para gol
    cv2.putText(status_frame, "GOL", (10, 190), 2, cv2.FONT_HERSHEY_PLAIN, (0, 0, 0), 2)
    cv2.rectangle(status_frame, (10, 200), (90, 240), (0, 255, 0) if goal_detected else (0, 0, 0), 2)
    if goal_detected:
        cv2.putText(status_frame, "X", (50, 215), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

    combined_frame = np.hstack((frame, status_frame))
    cv2.imshow("Football Detection", combined_frame)

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
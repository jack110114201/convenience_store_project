import cv2
class yolo_mask():
    def __init__(self):
        self.CONFIDENCE_THRESHOLD = 0.3
        self.NMS_THRESHOLD = 0.4
        self.net= cv2.dnn.readNetFromDarknet("./cfg_mask/yolov4-tiny-custom.cfg",
                                         "./cfg_mask/weights/yolov4-tiny-custom_last.weights")
        self.model = cv2.dnn_DetectionModel(self.net)
        self.model.setInputParams(size=(320, 320), scale=1 / 255, swapRB=True)
        # self.model.setInputParams(size=(416, 416), scale=1 / 255, swapRB=True)
        # self.model.setInputParams(size=(608, 608), scale=1 / 255, swapRB=True)
        self.label = [line.strip() for line in open('./cfg_mask/obj.names')]
        self.colors = [(0, 0, 255), (0, 255, 0)]

    def request_yolo(self , img):
        classes, scores, boxes = self.model.detect(img, self.CONFIDENCE_THRESHOLD, self.NMS_THRESHOLD)
        for i in range(len(boxes)):
            x, y, w, h = boxes[i]
            class_int = int(classes[i])
            score = round(float(scores[i]) * 100, 2)
            color = self.colors[class_int]
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
            cv2.putText(img, str(self.label[class_int]), (x, y - 15), cv2.FONT_HERSHEY_COMPLEX, 1, color, 2)
            cv2.putText(img, 'score:' + str(score) + '%', (x, y - 35), cv2.FONT_HERSHEY_COMPLEX, 1, color, 2)
        return img

if __name__ == '__main__':
    yolo_model = yolo_mask()
    cap = cv2.VideoCapture(0)
    cap.set(3 ,600)
    cap.set(4 ,400)

    while True :
        _ , img = cap.read()
        img = yolo_model.request_yolo(img)

        cv2.imshow('video', img)
        if cv2.waitKey(10) & 0xFF == ord('p'):
            break


    cap.release()
    cv2.destroyAllWindows()
    cv2.waitKey(1)


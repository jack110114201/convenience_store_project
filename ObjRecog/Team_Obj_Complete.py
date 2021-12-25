import cv2, time, datetime
import customerinfo

# DB index of each porduct
db_num = {'0':18203921, '1':1007796, '2':12385416, '3':892838}



class yolo_obj():
    def __init__(self):
        self.CONFIDENCE_THRESHOLD = 0.3
        self.NMS_THRESHOLD = 0.4
        self.net= cv2.dnn.readNetFromDarknet("./cfg_mask/yolov4-tiny-custom.cfg",
                                         "./cfg_mask/weights/yolov4-tiny-custom_last.weights")
        self.model = cv2.dnn_DetectionModel(self.net)
#         self.model.setInputParams(size=(320, 320), scale=1 / 255, swapRB=True)
        # self.model.setInputParams(size=(416, 416), scale=1 / 255, swapRB=True)
        self.model.setInputParams(size=(608, 608), scale=1 / 255, swapRB=True)
        self.label = [line.strip() for line in open('./cfg_mask/obj.names')]
        self.colors = [(0, 0, 255), (0, 255, 0) , (255,0,0) , (0,255,255)]
        

    def request_yolo(self , img):
        classes, scores, boxes = self.model.detect(img, self.CONFIDENCE_THRESHOLD, self.NMS_THRESHOLD)
#         print(len(boxes))
        if len(boxes) == 1 :
            x, y, w, h = boxes[0]
            class_int = int(classes[0])
            score = round(float(scores[0]) * 100, 2)
            if score >= 97.00 :
                color = self.colors[class_int]
                cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
                cv2.putText(img, str(self.label[class_int]), (x, y - 15), cv2.FONT_HERSHEY_COMPLEX, 1, color, 2)
                cv2.putText(img, 'score:' + str(score) + '%', (x, y - 35), cv2.FONT_HERSHEY_COMPLEX, 1, color, 2)

                predict = db_num.get(str(classes[0][0]))
    #             print(predict)
                return predict


if __name__ == '__main__':
    yolo_model = yolo_obj()
    cap = cv2.VideoCapture(1)
    cap.set(3 ,600)
    cap.set(4 ,400)
    count = 0
    product = None
    while True :
        _ , img = cap.read()
        predict = yolo_model.request_yolo(img)
        
        if predict != None and product != predict :
            # date time
            datetime_dt = datetime.datetime.today() # 獲得當地時間
            time = datetime_dt.strftime("%Y/%m/%d %H:%M:%S") # 轉 str
        
            # customer ID
            UID = customerinfo.check_register('A')
            product = predict
            checkout = [(UID, product, 1, time)]
            customerinfo.add_barsket(checkout)
            
        cv2.imshow('Scanner', img)
             
        key=cv2.waitKey(1)
        if key == 27:
            break


    cap.release()
    cv2.destroyAllWindows()
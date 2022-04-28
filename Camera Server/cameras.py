import cv2

def usb_cam():
    cam = cv2.VideoCapture(0)
    while 1 :
        try:
            check,frame = cam.read()
            #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            if(check):
                imgencode = cv2.imencode('.jpg',frame)[1]
                strinData = imgencode.tostring()
                yield (b'--frame\r\n'b'Content-Type: text/plain\r\n\r\n'+strinData+b'\r\n')
        except:
            cam.release()
            break
    return 'Closed'

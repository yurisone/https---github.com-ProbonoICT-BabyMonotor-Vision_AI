from camera_stream import Flask, Response
import cv2

app = Flask(__name__)

# 카메라를 초기화합니다 (기본 카메라 사용)
camera = cv2.VideoCapture(0)

def generate_frames():
    while True:
        # 카메라에서 프레임을 읽습니다
        success, frame = camera.read()
        if not success:
            break
        else:
            # YOLOv5를 여기서 적용할 수 있습니다 (선택 사항)
            # 예: frame = yolov5_inference(frame)

            # 프레임을 JPEG로 인코딩합니다
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            
            # 프레임을 전송합니다
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from ultralytics import YOLO
import cv2
import numpy as np
from message_filters import ApproximateTimeSynchronizer, Subscriber

class YOLOv8Node(Node):
    def __init__(self):
        super().__init__('depth_aware_detector')
        
        self.bridge = CvBridge()
        rgb_sub = Subscriber(self, Image, '/ascamera/camera_publisher/rgb0/image')
        depth_sub = Subscriber(self, Image, '/ascamera/camera_publisher/depth0/image_raw')
        
        self.ts = ApproximateTimeSynchronizer(
            [rgb_sub, depth_sub], 
            queue_size=10, 
            slop=0.1
        )
        self.ts.registerCallback(self.sync_callback)
        
        self.publisher = self.create_publisher(Image, '/yolov8/detections', 10)
            # yol0v8n模型的位置
        self.model = YOLO('/src/yolov8_ros/models/yolov8n.pt')
        
           
            # 定义监控区域参数（需要根据实际相机参数调整）
        self.monitor_region = np.array([
            [320, 320],  # 左上
            [480, 320],  # 右上
            [560, 476],  # 右下
            [240, 476]   # 左下
        ], dtype=np.int32)  
        
         
            # COCO 类别名称（80类）
        self.class_names = [
            'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train',
            'truck', 'boat', 'traffic light', 'fire hydrant', 'stop sign',
            'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep',
            'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella',
            'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard',
            'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard',
            'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup', 'fork',
            'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich', 'orange',
            'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair',
            'couch', 'potted plant', 'bed', 'dining table', 'toilet', 'tv',
            'laptop', 'mouse', 'remote', 'keyboard', 'cell phone', 'microwave',
            'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase',
            'scissors', 'teddy bear', 'hair drier', 'toothbrush'
        ]

    def sync_callback(self, rgb_msg, depth_msg):
        try:
            # 转换RGB图像
            rgb_image = self.bridge.imgmsg_to_cv2(rgb_msg, 'bgr8')
            
            # 转换RAW16深度图像（单位为毫米）
            depth_image = self.bridge.imgmsg_to_cv2(depth_msg, '16UC1')
            depth_image = depth_image.astype(np.float32) / 1000.0  # 转换为米
        except Exception as e:
            self.get_logger().error(f'Image conversion failed: {e}')
            return

        results = self.model.predict(rgb_image, conf=0.5)
        annotated_frame = results[0].plot()

            # 绘制监控区域
        cv2.polylines(annotated_frame, [self.monitor_region], 
                     isClosed=True, color=(0, 0, 255), thickness=2)

        for box in results[0].boxes:
            cls_id = int(box.cls)
            conf = float(box.conf)
            class_name = self.class_names[cls_id]
            
            x1, y1, x2, y2 = map(int, box.xyxy[0].cpu().numpy())
            
            # 计算中心点坐标
            center_x = int((x1 + x2) / 2)
            center_y = int((y1 + y2) / 2)
            center_x = np.clip(center_x, 0, depth_image.shape[1]-1)
            center_y = np.clip(center_y, 0, depth_image.shape[0]-1)
            
            # 获取深度值（处理无效值）
            depth_roi = depth_image[
                max(center_y-2, 0):min(center_y+3, depth_image.shape[0]),
                max(center_x-2, 0):min(center_x+3, depth_image.shape[1])
            ]
            valid_depths = depth_roi[(depth_roi > 0.1) & (depth_roi < 10.0)]
            
            if valid_depths.size > 0:
                distance = np.median(valid_depths)
            else:
                distance = 0.0
                self.get_logger().warn(f"Invalid depth at ({center_x}, {center_y})")

            # 绘制带深度信息的标签
            label = f"{class_name} {conf:.2f} | {distance:.2f}m"
            cv2.putText(annotated_frame, label, 
                        (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX,
                        0.6, (0, 255, 0), 2)

        try:
            self.publisher.publish(
                self.bridge.cv2_to_imgmsg(annotated_frame, 'bgr8'))
        except Exception as e:
            self.get_logger().error(f'Image publish failed: {e}')

def main(args=None):
    rclpy.init(args=args)
    detector = YOLOv8Node()
    rclpy.spin(detector)
    detector.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

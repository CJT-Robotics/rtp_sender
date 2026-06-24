#!/usr/bin/env python3
import rospy
import subprocess
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

class RosToFFmpeg:
    def __init__(self):
        rospy.init_node('ros_to_ffmpeg', anonymous=True)
        
        self.image_topic = rospy.get_param('~image_topic', 'cam_front/image_raw')
        self.receiver_ip = rospy.get_param('~receiver_ip', '192.168.0.5')
        self.port = rospy.get_param('~port', 5000)
        self.fps = rospy.get_param('~fps', 30)
        
        self.stream_width = rospy.get_param('~stream_width', 1280)
        self.stream_height = rospy.get_param('~stream_height', 720)
        self.bitrate = rospy.get_param('~bitrate', '2.5M')
        
        self.bridge = CvBridge()
        self.ffmpeg_process = None
        
        ffmpeg_cmd = [
            'ffmpeg',
            '-y',
            '-f', 'rawvideo',
            '-vcodec', 'rawvideo',
            '-pix_fmt', 'bgr24',
            '-s', f"{self.stream_width}x{self.stream_height}",
            '-r', str(self.fps),
            '-i', '-',
            '-c:v', 'libx264',
            '-preset', 'ultrafast',
            '-tune', 'zerolatency',
            '-g', str(self.fps),
            '-b:v', self.bitrate,
            '-maxrate', self.bitrate,
            '-bufsize', self.bitrate,
            '-f', 'rtp', f"rtp://{self.receiver_ip}:{self.port}"
        ]
        
        rospy.loginfo(f"Starte FFmpeg Stream für {self.image_topic} auf Port {self.port}...")
        self.ffmpeg_process = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE, stderr=subprocess.STDOUT)
        
        self.sub = rospy.Subscriber(self.image_topic, Image, self.image_callback, queue_size=1)

    def image_callback(self, msg):
        if self.ffmpeg_process is None or self.ffmpeg_process.poll() is not None:
            return
            
        try:
            cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")
            
            if cv_image.shape[1] != self.stream_width or cv_image.shape[0] != self.stream_height:
                cv_image = cv2.resize(cv_image, (self.stream_width, self.stream_height), interpolation=cv2.INTER_LINEAR)
            
            self.ffmpeg_process.stdin.write(cv_image.tobytes())
            
        except Exception as e:
            rospy.logerr(f"Fehler beim Streamen: {e}")

    def shutdown(self):
        if self.ffmpeg_process:
            rospy.loginfo("Schließe FFmpeg Stream...")
            self.ffmpeg_process.stdin.close()
            self.ffmpeg_process.wait()

if __name__ == '__main__':
    node = RosToFFmpeg()
    rospy.on_shutdown(node.shutdown)
    rospy.spin()
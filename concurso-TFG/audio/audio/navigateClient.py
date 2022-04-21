import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node

import time  # Time library
 
from geometry_msgs.msg import PoseStamped # Pose with ref frame and timestamp
from rclpy.duration import Duration # Handles time for ROS 2
import rclpy # Python client library for ROS 2
 
from audio.robot_navigator import BasicNavigator, NavigationResult
from nav2_msgs.action import NavigateToPose, FollowWaypoints, ComputePathToPose



class navigateClient(Node):

    def __init__(self):
        super().__init__('navigate_action_client')
        self._action_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')

    def send_goal(self, x, y):
        #goal_msg = NavigateToPose.Goal()
        #goal_msg.order = order

        navigator = BasicNavigator()

        # Set the robot's initial pose if necessary
        #initial_pose = PoseStamped()
        #initial_pose.header.frame_id = 'map'
        #initial_pose.header.stamp = navigator.get_clock().now().to_msg()
        #initial_pose.pose.position.x = 0.0
        #initial_pose.pose.position.y = 0.0
        #initial_pose.pose.position.z = 0.0
        #initial_pose.pose.orientation.x = 0.0
        #initial_pose.pose.orientation.y = 0.0
        #initial_pose.pose.orientation.z = 0.0
        #initial_pose.pose.orientation.w = 1.0
        #navigator.setInitialPose(initial_pose)
        #self._action_client.wait_for_server()

        navigator.waitUntilNav2Active()


        # Set the robot's goal pose
        goal_pose = PoseStamped()
        
        goal_pose.header.frame_id = 'map'
        goal_pose.header.stamp = navigator.get_clock().now().to_msg()
        #goal_msg.goal_pose.position.x = 4.67
        goal_pose.pose.position.x = 4.67
        goal_pose.pose.position.y = 3.86
        goal_pose.pose.position.z = 0.0
        goal_pose.pose.orientation.x = 4.67
        goal_pose.pose.orientation.y = 3.86
        goal_pose.pose.orientation.z = 0.0
        goal_pose.pose.orientation.w = 1.0

        navigator.goToPose(goal_pose)
        #return self._action_client.send_goal_async(goal_msg)


def main(args=None):
    rclpy.init(args=args)

    action_client = navigateClient()

    future = action_client.send_goal(4.67, 3.86)

    rclpy.spin_until_future_complete(action_client, future)


if __name__ == '__main__':
    main()

/**
 * @file      ascamera_node.cpp
 * @brief     angstrong ros2 camera publisher node.
 *
 * Copyright (c) 2023 Angstrong Tech.Co.,Ltd
 *
 * @author    Angstrong SDK develop Team
 * @date      2023/03/27
 * @version   1.0

 */

#include "rclcpp/rclcpp.hpp"
#include "rclcpp/node.hpp"

#include "CameraPublisher.h"

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto logger = rclcpp::get_logger("as_logger");
    RCLCPP_INFO(logger, "hello world angstrong camera ros2 node");

    auto node = std::make_shared<CameraPublisher>();
    // rclcpp::spin(std::make_shared<CameraPublisher>());

    node->start();
    rclcpp::WallRate loop_rate(25);

    while (rclcpp::ok()) {
        rclcpp::spin_some(node);
        loop_rate.sleep();
    }
    node->stop();

    RCLCPP_INFO(logger, "angstrong camera ros2 node shutdown");

    rclcpp::shutdown();
    return 0;
}

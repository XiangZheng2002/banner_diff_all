/*
Navicat MySQL Data Transfer

Source Server         : X
Source Server Version : 50743
Source Host           : localhost:3306
Source Database       : banner_diffusion

Target Server Type    : MYSQL
Target Server Version : 50743
File Encoding         : 65001

Date: 2024-05-05 19:38:32
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for alembic_version
-- ----------------------------
DROP TABLE IF EXISTS `alembic_version`;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of alembic_version
-- ----------------------------
INSERT INTO `alembic_version` VALUES ('138442f00582');

-- ----------------------------
-- Table structure for image_style
-- ----------------------------
DROP TABLE IF EXISTS `image_style`;
CREATE TABLE `image_style` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `original_image_id` int(11) DEFAULT NULL,
  `style` varchar(20) CHARACTER SET utf8 DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `original_image_id` (`original_image_id`),
  CONSTRAINT `image_style_ibfk_1` FOREIGN KEY (`original_image_id`) REFERENCES `original_image` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of image_style
-- ----------------------------
INSERT INTO `image_style` VALUES ('1', '1', '温馨风');
INSERT INTO `image_style` VALUES ('2', '2', '温馨风');
INSERT INTO `image_style` VALUES ('3', '3', '温馨风');
INSERT INTO `image_style` VALUES ('4', '4', '温馨风');
INSERT INTO `image_style` VALUES ('5', '5', '温馨风');
INSERT INTO `image_style` VALUES ('6', '6', '温馨风');
INSERT INTO `image_style` VALUES ('7', '7', '温馨风');
INSERT INTO `image_style` VALUES ('8', '8', '温馨风');
INSERT INTO `image_style` VALUES ('9', '9', '温馨风');
INSERT INTO `image_style` VALUES ('10', '10', '温馨风');
INSERT INTO `image_style` VALUES ('11', '11', '温馨风');

-- ----------------------------
-- Table structure for image_type
-- ----------------------------
DROP TABLE IF EXISTS `image_type`;
CREATE TABLE `image_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `original_image_id` int(11) DEFAULT NULL,
  `type` varchar(20) CHARACTER SET utf8 DEFAULT NULL,
  `category` varchar(20) CHARACTER SET utf8 DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `original_image_id` (`original_image_id`),
  CONSTRAINT `image_type_ibfk_1` FOREIGN KEY (`original_image_id`) REFERENCES `original_image` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of image_type
-- ----------------------------
INSERT INTO `image_type` VALUES ('1', '1', '主体物', '美妆');
INSERT INTO `image_type` VALUES ('2', '2', '主体物', '美妆');
INSERT INTO `image_type` VALUES ('3', '3', '主体物', '美妆');
INSERT INTO `image_type` VALUES ('4', '4', '装饰物', null);
INSERT INTO `image_type` VALUES ('5', '5', '装饰物', null);
INSERT INTO `image_type` VALUES ('6', '6', '装饰物', null);
INSERT INTO `image_type` VALUES ('7', '7', '装饰物', null);
INSERT INTO `image_type` VALUES ('8', '8', '装饰物', null);
INSERT INTO `image_type` VALUES ('9', '9', '装饰物', null);
INSERT INTO `image_type` VALUES ('10', '10', '标语', null);
INSERT INTO `image_type` VALUES ('11', '11', '背景', null);

-- ----------------------------
-- Table structure for original_image
-- ----------------------------
DROP TABLE IF EXISTS `original_image`;
CREATE TABLE `original_image` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) CHARACTER SET utf8 DEFAULT NULL,
  `img_url` varchar(80) CHARACTER SET utf8 NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `last_mod` char(19) CHARACTER SET utf8 DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `img_url` (`img_url`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `original_image_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of original_image
-- ----------------------------
INSERT INTO `original_image` VALUES ('1', '_01_粉色主体物', 'backend/static/input/2/_01_粉色主体物.png', '2', '2024-04-19T22:17:00');
INSERT INTO `original_image` VALUES ('2', '_02_橘色主体物', 'backend/static/input/2/_02_橘色主体物.png', '2', '2024-04-19T22:17:00');
INSERT INTO `original_image` VALUES ('3', '_03_绿色主体物', 'backend/static/input/2/_03_绿色主体物.png', '2', '2024-04-19T22:17:00');
INSERT INTO `original_image` VALUES ('4', '_04_花瓣', 'backend/static/input/2/_04_花瓣.png', '2', '2024-04-19T22:17:00');
INSERT INTO `original_image` VALUES ('5', '_05_花瓣', 'backend/static/input/2/_05_花瓣.png', '2', '2024-04-19T22:17:00');
INSERT INTO `original_image` VALUES ('6', '_07_石头', 'backend/static/input/2/_07_石头.png', '2', '2024-04-19T22:22:22');
INSERT INTO `original_image` VALUES ('7', '_08_垫石', 'backend/static/input/2/_08_垫石.png', '2', '2024-04-19T22:22:22');
INSERT INTO `original_image` VALUES ('8', '_09_布料', 'backend/static/input/2/_09_布料.png', '2', '2024-04-19T22:22:22');
INSERT INTO `original_image` VALUES ('9', '_10_标语', 'backend/static/input/2/_10_标语.png', '2', '2024-04-19T22:22:22');
INSERT INTO `original_image` VALUES ('10', '_11_背景', 'backend/static/input/2/_11_背景.png', '2', '2024-04-19T22:22:22');
INSERT INTO `original_image` VALUES ('11', '1', 'backend/static/input/1/1.jpg', '1', '2024-04-27T06:41:07');

-- ----------------------------
-- Table structure for output_image
-- ----------------------------
DROP TABLE IF EXISTS `output_image`;
CREATE TABLE `output_image` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) CHARACTER SET utf8 DEFAULT NULL,
  `img_url` varchar(80) CHARACTER SET utf8 NOT NULL,
  `project_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `last_mod` char(19) CHARACTER SET utf8 DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `img_url` (`img_url`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of output_image
-- ----------------------------
INSERT INTO `output_image` VALUES ('1', '1_0419-22-27-21-097988', 'backend/static/output/1_0419-22-27-21-097988.png', '1', '2', '2024-04-19T22:27:42');

-- ----------------------------
-- Table structure for processed_image
-- ----------------------------
DROP TABLE IF EXISTS `processed_image`;
CREATE TABLE `processed_image` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `pos_x` int(11) DEFAULT NULL,
  `pos_y` int(11) DEFAULT NULL,
  `layer` int(11) DEFAULT NULL,
  `rotate_deg` int(11) DEFAULT NULL,
  `width` int(11) DEFAULT NULL,
  `height` int(11) DEFAULT NULL,
  `w_pos` decimal(2,1) DEFAULT NULL,
  `w_neg` decimal(2,1) DEFAULT NULL,
  `t_i` decimal(2,1) DEFAULT NULL,
  `project_id` int(11) DEFAULT NULL,
  `img_id` int(11) DEFAULT NULL,
  `last_mod` char(19) CHARACTER SET utf8 DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `img_id` (`img_id`),
  KEY `project_id` (`project_id`),
  CONSTRAINT `processed_image_ibfk_1` FOREIGN KEY (`img_id`) REFERENCES `original_image` (`id`),
  CONSTRAINT `processed_image_ibfk_2` FOREIGN KEY (`project_id`) REFERENCES `project` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of processed_image
-- ----------------------------
INSERT INTO `processed_image` VALUES ('1', '0', '0', '9', '0', '750', '380', '0.5', '1.0', '0.6', '1', '1', '2024-04-19T22:24:45');
INSERT INTO `processed_image` VALUES ('2', '0', '0', '8', '0', '750', '380', '0.5', '1.0', '0.5', '1', '2', '2024-04-19T22:24:45');
INSERT INTO `processed_image` VALUES ('3', '0', '0', '7', '0', '750', '380', '0.5', '1.0', '0.5', '1', '3', '2024-04-19T22:24:45');
INSERT INTO `processed_image` VALUES ('4', '0', '0', '6', '0', '750', '380', '0.5', '1.0', '0.2', '1', '4', '2024-04-19T22:24:45');
INSERT INTO `processed_image` VALUES ('5', '0', '0', '5', '0', '750', '380', '0.5', '1.0', '0.2', '1', '5', '2024-04-19T22:24:45');
INSERT INTO `processed_image` VALUES ('6', '0', '0', '4', '0', '750', '380', '0.5', '1.0', '0.2', '1', '6', '2024-04-19T22:24:45');
INSERT INTO `processed_image` VALUES ('7', '0', '0', '3', '0', '750', '380', '0.5', '1.0', '0.0', '1', '7', '2024-04-19T22:24:45');
INSERT INTO `processed_image` VALUES ('8', '0', '0', '2', '0', '750', '380', '0.5', '1.0', '0.0', '1', '8', '2024-04-19T22:24:45');
INSERT INTO `processed_image` VALUES ('9', '0', '0', '1', '0', '750', '380', '0.5', '1.0', '0.0', '1', '9', '2024-04-19T22:24:45');
INSERT INTO `processed_image` VALUES ('10', '0', '0', '0', '0', '750', '380', '0.5', '1.0', '0.6', '1', '10', '2024-04-19T22:24:45');

-- ----------------------------
-- Table structure for project
-- ----------------------------
DROP TABLE IF EXISTS `project`;
CREATE TABLE `project` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) CHARACTER SET utf8 DEFAULT NULL,
  `width` int(11) DEFAULT NULL,
  `height` int(11) DEFAULT NULL,
  `style` json DEFAULT NULL,
  `type` json DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `last_mod` char(19) CHARACTER SET utf8 DEFAULT NULL,
  `thumbnail_url` varchar(80) CHARACTER SET utf8 DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `project_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of project
-- ----------------------------
INSERT INTO `project` VALUES ('1', '测试工程', '750', '600', '[\"可爱风\"]', '[\"节日\"]', '2');
INSERT INTO `project` VALUES ('2', '1测试工程', '750', '600', '[\"唯美风\"]', '[\"节日\"]', '2');
INSERT INTO `project` VALUES ('3', '2测试工程', '750', '600', '[\"唯美风\"]', '[\"节日\"]', '2');
INSERT INTO `project` VALUES ('4', 'Untitled Project1', '400', '600', '[\"科技风\"]', '[\"运动类\"]', '2');
INSERT INTO `project` VALUES ('5', '0505测试', '600', '600', '[\"温馨风\"]', '[\"美妆类\"]', '2');

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `name` varchar(80) CHARACTER SET utf8 DEFAULT NULL,
  `password` varchar(80) CHARACTER SET utf8 DEFAULT NULL,
  `avatar_url` varchar(80) CHARACTER SET utf8 DEFAULT NULL,
  `is_admin` tinyint(1) DEFAULT NULL,
  `last_mod` char(19) CHARACTER SET utf8 DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES ('1', 'admin', 'admin', 'backend/static/avatar/1.jpg', '1', null);
INSERT INTO `user` VALUES ('2', 'test1', '123456', 'backend/static/avatar/doggy.jpg', '0', '2024-04-02T11:17:16');
INSERT INTO `user` VALUES ('3', 'test2', '123456', 'backend/static/avatar/doggy.jpg', '0', '2024-04-13T20:16:08');

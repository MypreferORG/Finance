-- 用户设备数据表建表语句
-- 执行顺序：按依赖关系，先创建主表

-- 1. 用户短信记录表
CREATE TABLE IF NOT EXISTS `user_sms_record` (
    `id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    `user_id` INT NOT NULL COMMENT '关联用户ID',
    `telphone` VARCHAR(50) NULL COMMENT '发送者号码',
    `content` TEXT NOT NULL COMMENT '短信内容',
    `send_date` DATETIME NULL COMMENT '短信发送时间',
    `sms_type` VARCHAR(20) DEFAULT 'received' COMMENT '短信类型: received/sent',
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '记录创建时间',
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '记录更新时间',
    INDEX `idx_user_sms_user` (`user_id`),
    INDEX `idx_user_sms_telphone` (`telphone`),
    CONSTRAINT `fk_user_sms_user` FOREIGN KEY (`user_id`) REFERENCES `user_auth` (`index`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户短信记录表';

-- 2. 用户应用列表记录表
CREATE TABLE IF NOT EXISTS `user_app_record` (
    `id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    `user_id` INT NOT NULL COMMENT '关联用户ID',
    `name` VARCHAR(200) NOT NULL COMMENT '应用名称',
    `pkg_name` VARCHAR(200) NULL COMMENT '包名',
    `version_name` VARCHAR(50) NULL COMMENT '版本名',
    `version_code` INT NULL COMMENT '版本号',
    `is_system_app` TINYINT(1) DEFAULT 0 COMMENT '是否系统应用',
    `install_time` DATETIME NULL COMMENT '安装时间',
    `last_update_time` DATETIME NULL COMMENT '最后更新时间',
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '记录创建时间',
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '记录更新时间',
    INDEX `idx_user_app_user` (`user_id`),
    INDEX `idx_user_app_name` (`name`),
    INDEX `idx_user_app_pkg` (`pkg_name`),
    CONSTRAINT `fk_user_app_user` FOREIGN KEY (`user_id`) REFERENCES `user_auth` (`index`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户应用列表记录表';

-- 3. 用户通讯录记录表
CREATE TABLE IF NOT EXISTS `user_contact_record` (
    `id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    `user_id` INT NOT NULL COMMENT '关联用户ID',
    `display_name` VARCHAR(100) NULL COMMENT '联系人姓名',
    `phone_number` VARCHAR(50) NOT NULL COMMENT '电话号码(归一化后)',
    `phone_number_raw` VARCHAR(50) NULL COMMENT '原始电话号码',
    `phone_type` VARCHAR(20) NULL COMMENT '号码类型: mobile/home/work等',
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '记录创建时间',
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '记录更新时间',
    INDEX `idx_user_contact_user` (`user_id`),
    INDEX `idx_user_contact_phone` (`phone_number`),
    CONSTRAINT `fk_user_contact_user` FOREIGN KEY (`user_id`) REFERENCES `user_auth` (`index`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户通讯录记录表';

-- 4. 用户图片记录表
CREATE TABLE IF NOT EXISTS `user_image_record` (
    `id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    `user_id` INT NOT NULL COMMENT '关联用户ID',
    `image_type` VARCHAR(50) NULL COMMENT '图片类型: id_card_front/id_card_back/face/other',
    `image_url` VARCHAR(500) NULL COMMENT '图片URL或路径',
    `file_name` VARCHAR(255) NULL COMMENT '上传的文件名',
    `file_size` INT NULL COMMENT '文件大小（字节）',
    `mime_type` VARCHAR(64) NULL COMMENT 'MIME 类型，例如 image/jpeg',
    `image_data` LONGTEXT NULL COMMENT '图片Base64数据(可选)',
    `ocr_result` JSON NULL COMMENT 'OCR识别结果',
    `verify_status` VARCHAR(20) DEFAULT 'pending' COMMENT '验证状态: pending/passed/failed',
    `verify_message` TEXT NULL COMMENT '验证消息',
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '记录创建时间',
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '记录更新时间',
    INDEX `idx_user_image_user` (`user_id`),
    INDEX `idx_user_image_type` (`image_type`),
    CONSTRAINT `fk_user_image_user` FOREIGN KEY (`user_id`) REFERENCES `user_auth` (`index`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户图片记录表';

-- 5. 用户设备数据批量上传记录表
CREATE TABLE IF NOT EXISTS `user_device_data_batch` (
    `id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    `user_id` INT NOT NULL COMMENT '关联用户ID',
    `batch_id` VARCHAR(64) NOT NULL UNIQUE COMMENT '批次ID',
    `data_type` VARCHAR(20) NOT NULL COMMENT '数据类型: sms/app/contact/image/all',
    `total_count` INT DEFAULT 0 COMMENT '数据总条数',
    `success_count` INT DEFAULT 0 COMMENT '成功导入条数',
    `failed_count` INT DEFAULT 0 COMMENT '失败条数',
    `status` VARCHAR(20) DEFAULT 'processing' COMMENT '状态: processing/completed/failed',
    `error_message` TEXT NULL COMMENT '错误信息',
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '记录创建时间',
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '记录更新时间',
    INDEX `idx_batch_user` (`user_id`),
    INDEX `idx_batch_id` (`batch_id`),
    INDEX `idx_batch_type` (`data_type`),
    CONSTRAINT `fk_batch_user` FOREIGN KEY (`user_id`) REFERENCES `user_auth` (`index`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户设备数据批量上传记录表';

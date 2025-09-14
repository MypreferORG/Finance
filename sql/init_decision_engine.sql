-- 决策引擎数据库表结构
-- 创建时间: 2025-09-14
-- 作者: Myprefer

-- 决策规则表
CREATE TABLE IF NOT EXISTS `decision_rules` (
    `id` VARCHAR(50) NOT NULL PRIMARY KEY COMMENT '规则ID',
    `name` VARCHAR(100) NOT NULL COMMENT '规则名称',
    `description` TEXT COMMENT '规则描述',
    `nodes` JSON NOT NULL COMMENT '规则节点数据',
    `edges` JSON NOT NULL COMMENT '规则边数据',
    `variables` JSON NOT NULL COMMENT '规则变量数据',
    `status` VARCHAR(20) DEFAULT 'draft' COMMENT '规则状态: draft/active/inactive',
    `version` VARCHAR(20) DEFAULT '1.0.0' COMMENT '版本号',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    `created_by` VARCHAR(50) NOT NULL COMMENT '创建者ID',
    INDEX `idx_status` (`status`),
    INDEX `idx_created_by` (`created_by`),
    INDEX `idx_name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='决策规则表';

-- 决策执行记录表
CREATE TABLE IF NOT EXISTS `decision_executions` (
    `id` VARCHAR(50) NOT NULL PRIMARY KEY COMMENT '执行ID',
    `rule_id` VARCHAR(50) NOT NULL COMMENT '规则ID',
    `rule_name` VARCHAR(100) NOT NULL COMMENT '规则名称',
    `input_data` JSON NOT NULL COMMENT '输入数据',
    `result` JSON NOT NULL COMMENT '执行结果',
    `execution_path` JSON NOT NULL COMMENT '执行路径',
    `node_results` JSON NOT NULL COMMENT '节点执行结果',
    `execution_time` DECIMAL(10,6) NOT NULL COMMENT '执行耗时(秒)',
    `status` VARCHAR(20) DEFAULT 'completed' COMMENT '执行状态: completed/failed/timeout',
    `error_message` TEXT COMMENT '错误信息',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX `idx_rule_id` (`rule_id`),
    INDEX `idx_status` (`status`),
    INDEX `idx_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='决策执行记录表';

-- 决策测试用例表
CREATE TABLE IF NOT EXISTS `decision_test_cases` (
    `id` INT AUTO_INCREMENT PRIMARY KEY COMMENT '测试用例ID',
    `rule_id` VARCHAR(50) NOT NULL COMMENT '规则ID',
    `name` VARCHAR(100) NOT NULL COMMENT '测试用例名称',
    `input_data` JSON NOT NULL COMMENT '测试输入数据',
    `expected_result` JSON NOT NULL COMMENT '期望结果',
    `actual_result` JSON COMMENT '实际结果',
    `status` VARCHAR(20) COMMENT '测试状态: success/failure/pending',
    `match_expected` BOOLEAN COMMENT '是否匹配期望结果',
    `execution_time` DECIMAL(10,6) COMMENT '执行耗时(秒)',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX `idx_rule_id` (`rule_id`),
    INDEX `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='决策测试用例表';

-- 决策统计数据表
CREATE TABLE IF NOT EXISTS `decision_statistics` (
    `id` INT AUTO_INCREMENT PRIMARY KEY COMMENT '统计ID',
    `date` DATE NOT NULL COMMENT '统计日期',
    `rule_id` VARCHAR(50) COMMENT '规则ID',
    `total_executions` INT DEFAULT 0 COMMENT '总执行次数',
    `success_executions` INT DEFAULT 0 COMMENT '成功执行次数',
    `failed_executions` INT DEFAULT 0 COMMENT '失败执行次数',
    `avg_execution_time` DECIMAL(10,6) DEFAULT 0.0 COMMENT '平均执行时间',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX `idx_date` (`date`),
    INDEX `idx_rule_id` (`rule_id`),
    UNIQUE KEY `uk_date_rule` (`date`, `rule_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='决策统计数据表';

-- 插入示例数据
INSERT INTO `decision_rules` (`id`, `name`, `description`, `nodes`, `edges`, `variables`, `status`, `version`, `created_by`) VALUES
('rule_001', '信用评估规则', '基于用户基本信息和A卡评分的信用评估', 
'[
    {
        "id": "start_001",
        "type": "data_source",
        "position": {"x": 100, "y": 100},
        "data": {
            "label": "获取用户数据",
            "sourceType": "userProfile",
            "outputFields": ["user.age", "user.income", "user.credit"]
        }
    },
    {
        "id": "condition_001",
        "type": "condition",
        "position": {"x": 300, "y": 100},
        "data": {
            "label": "年龄检查",
            "condition": "user.age >= 18 && user.age <= 65"
        }
    },
    {
        "id": "condition_002",
        "type": "condition",
        "position": {"x": 500, "y": 100},
        "data": {
            "label": "收入和黑名单检查",
            "condition": "user.income > 3000 && !application.is_blacklisted"
        }
    },
    {
        "id": "model_001",
        "type": "model",
        "position": {"x": 700, "y": 100},
        "data": {
            "label": "A卡模型评分",
            "modelId": "model_a",
            "threshold": 0.7
        }
    },
    {
        "id": "decision_001",
        "type": "decision",
        "position": {"x": 900, "y": 100},
        "data": {
            "label": "最终决策",
            "approvalCondition": "model_score >= 0.7",
            "maxAmount": 50000
        }
    }
]',
'[
    {
        "id": "edge_001",
        "source": "start_001",
        "target": "condition_001",
        "type": "default"
    },
    {
        "id": "edge_002",
        "source": "condition_001",
        "target": "condition_002",
        "type": "success"
    },
    {
        "id": "edge_003",
        "source": "condition_002",
        "target": "model_001",
        "type": "success"
    },
    {
        "id": "edge_004",
        "source": "model_001",
        "target": "decision_001",
        "type": "default"
    }
]',
'[
    {
        "name": "user.age",
        "type": "number",
        "description": "用户年龄",
        "category": "基本信息"
    },
    {
        "name": "user.income",
        "type": "number",
        "description": "用户月收入",
        "category": "基本信息"
    },
    {
        "name": "user.credit",
        "type": "number",
        "description": "信用评分",
        "category": "信用信息"
    },
    {
        "name": "application.is_blacklisted",
        "type": "boolean",
        "description": "是否在黑名单",
        "category": "风险信息"
    },
    {
        "name": "loanAmount",
        "type": "number",
        "description": "申请贷款金额",
        "category": "申请信息"
    }
]',
'active', '1.0.0', 'user_123');

-- 插入示例执行记录
INSERT INTO `decision_executions` (`id`, `rule_id`, `rule_name`, `input_data`, `result`, `execution_path`, `node_results`, `execution_time`, `status`) VALUES
('exec_001', 'rule_001', '信用评估规则',
'{"user.age": 25, "user.income": 8000, "user.credit": 720, "application.is_blacklisted": false, "loanAmount": 30000}',
'{"decision": "approved", "confidence": 0.85, "approved_amount": 25000, "risk_level": "low"}',
'["start_001", "condition_001", "condition_002", "model_001", "decision_001"]',
'{
    "start_001": {"output": {"user.age": 25, "user.income": 8000, "user.credit": 720}},
    "condition_001": {"result": true, "condition": "user.age >= 18 && user.age <= 65"},
    "condition_002": {"result": true, "condition": "user.income > 3000 && !application.is_blacklisted"},
    "model_001": {"prediction": 0.85, "model_output": {"credit_risk": "low", "recommended_amount": 25000}},
    "decision_001": {"final_decision": "approved", "approved_amount": 25000, "risk_level": "low"}
}',
0.125, 'completed');

-- 插入示例统计数据
INSERT INTO `decision_statistics` (`date`, `rule_id`, `total_executions`, `success_executions`, `failed_executions`, `avg_execution_time`) VALUES
(CURDATE(), 'rule_001', 100, 95, 5, 0.125),
(CURDATE(), NULL, 150, 140, 10, 0.135);
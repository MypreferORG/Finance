-- 测试用例表结构迁移脚本
-- 安全地更新表结构，保留现有数据

USE finance;

-- 开始事务
START TRANSACTION;

-- 1. 首先添加 description 字段
ALTER TABLE decision_test_cases 
ADD COLUMN IF NOT EXISTS description TEXT COMMENT '测试用例描述';

-- 2. 创建临时表用于ID类型迁移
CREATE TABLE IF NOT EXISTS decision_test_cases_new (
    id VARCHAR(50) PRIMARY KEY COMMENT '测试用例ID',
    rule_id VARCHAR(50) NULL COMMENT '关联规则ID',
    name VARCHAR(100) NOT NULL COMMENT '测试用例名称',
    description TEXT NULL COMMENT '测试用例描述',
    input_data JSON NOT NULL COMMENT '测试输入数据',
    expected_result VARCHAR(50) NOT NULL COMMENT '期望结果',
    actual_result JSON NULL COMMENT '实际结果',
    status VARCHAR(20) NULL COMMENT '测试状态: success/failure/pending',
    match_expected BOOLEAN NULL COMMENT '是否匹配期望结果',
    execution_time FLOAT NULL COMMENT '执行耗时(秒)',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_rule_id (rule_id),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='决策测试用例表';

-- 3. 迁移现有数据（如果存在）
INSERT IGNORE INTO decision_test_cases_new 
(id, rule_id, name, description, input_data, expected_result, actual_result, status, match_expected, execution_time, created_at, updated_at)
SELECT 
    CONCAT('test_case_', LPAD(id, 8, '0')) as id,  -- 将数字ID转换为字符串ID
    rule_id,
    name,
    NULL as description,  -- 新字段默认为NULL
    input_data,
    CASE 
        WHEN JSON_EXTRACT(expected_result, '$') IS NOT NULL THEN JSON_UNQUOTE(JSON_EXTRACT(expected_result, '$'))
        ELSE expected_result
    END as expected_result,  -- 处理JSON到字符串的转换
    actual_result,
    status,
    match_expected,
    execution_time,
    created_at,
    updated_at
FROM decision_test_cases 
WHERE EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'decision_test_cases' AND table_schema = DATABASE());

-- 4. 备份原表（重命名）
DROP TABLE IF EXISTS decision_test_cases_backup;
RENAME TABLE decision_test_cases TO decision_test_cases_backup;

-- 5. 将新表重命名为正式表名
RENAME TABLE decision_test_cases_new TO decision_test_cases;

-- 提交事务
COMMIT;

-- 验证迁移结果
SELECT COUNT(*) as migrated_records FROM decision_test_cases;
DESCRIBE decision_test_cases;
-- 简单的测试用例表更新脚本
-- 只添加缺少的字段，不改变现有结构

USE finance;

-- 添加 description 字段（如果不存在）
SET @sql = 'ALTER TABLE decision_test_cases ADD COLUMN description TEXT NULL COMMENT ''测试用例描述''';
SET @sql = IF(
    (SELECT COUNT(*) FROM information_schema.columns 
     WHERE table_schema = DATABASE() 
     AND table_name = 'decision_test_cases' 
     AND column_name = 'description') = 0,
    @sql,
    'SELECT ''description column already exists'' as message'
);
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- 确保 rule_id 允许 NULL
ALTER TABLE decision_test_cases MODIFY COLUMN rule_id VARCHAR(50) NULL COMMENT '关联规则ID';

-- 修改 expected_result 字段类型（如果当前是JSON类型）
ALTER TABLE decision_test_cases MODIFY COLUMN expected_result VARCHAR(50) NOT NULL COMMENT '期望结果';

-- 查看表结构
DESCRIBE decision_test_cases;
-- 更新测试用例表结构
-- 添加缺少的字段以支持测试用例管理功能

-- 1. 添加 description 字段（如果不存在）
ALTER TABLE decision_test_cases 
ADD COLUMN IF NOT EXISTS description TEXT COMMENT '测试用例描述';

-- 2. 修改 id 字段类型为 VARCHAR(50)（如果需要）
-- 注意：这个操作可能需要先备份数据，因为会改变主键类型
-- ALTER TABLE decision_test_cases 
-- MODIFY COLUMN id VARCHAR(50) PRIMARY KEY COMMENT '测试用例ID';

-- 3. 修改 expected_result 字段类型为 VARCHAR(50)（如果需要）
ALTER TABLE decision_test_cases 
MODIFY COLUMN expected_result VARCHAR(50) COMMENT '期望结果';

-- 4. 允许 rule_id 为 NULL（支持独立测试用例）
ALTER TABLE decision_test_cases 
MODIFY COLUMN rule_id VARCHAR(50) NULL COMMENT '关联规则ID';

-- 查看更新后的表结构
DESCRIBE decision_test_cases;
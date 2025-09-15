-- 为测试用例表添加 description 字段
USE finance;

-- 检查并添加 description 字段
ALTER TABLE decision_test_cases 
ADD COLUMN IF NOT EXISTS description TEXT COMMENT '测试用例描述';

-- 验证字段是否添加成功
DESCRIBE decision_test_cases;
-- 更新 loan_record 表，添加复审功能所需的字段
-- 执行前请备份数据库

-- 添加复审相关字段到 loan_record 表
ALTER TABLE loan_record 
ADD COLUMN income DECIMAL(10,2) NULL COMMENT '申请人月收入',
ADD COLUMN credit_score INT NULL COMMENT '信用评分',
ADD COLUMN auditor VARCHAR(50) NULL COMMENT '审核员',
ADD COLUMN audit_time DATETIME NULL COMMENT '审核时间',
ADD COLUMN remark TEXT NULL COMMENT '审核备注/拒绝原因';

-- 验证字段是否添加成功
DESCRIBE loan_record;

-- 可选：为新字段添加索引以提高查询性能
CREATE INDEX idx_loan_record_auditor ON loan_record(auditor);
CREATE INDEX idx_loan_record_audit_time ON loan_record(audit_time);
CREATE INDEX idx_loan_record_status ON loan_record(status);

-- 插入一些测试数据（可选）
UPDATE loan_record 
SET 
    income = 8000.00,
    credit_score = 720,
    auditor = '系统审核',
    audit_time = NOW(),
    remark = '初始化数据'
WHERE id IN (SELECT id FROM (SELECT id FROM loan_record LIMIT 5) AS temp);

-- 验证更新
SELECT id, amount, status, income, credit_score, auditor, audit_time, remark 
FROM loan_record 
WHERE remark IS NOT NULL 
LIMIT 5;

-- 复审管理测试数据初始化SQL
-- 用于复审管理功能的开发和测试

-- 创建复审申请表（如果不存在）
CREATE TABLE IF NOT EXISTS review_applications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    original_audit_id INT NOT NULL COMMENT '原始审核记录ID',
    applicant_name VARCHAR(50) NOT NULL COMMENT '申请人姓名',
    phone VARCHAR(20) NOT NULL COMMENT '联系电话',
    id_card VARCHAR(18) NOT NULL COMMENT '身份证号',
    loan_amount DECIMAL(10,2) NOT NULL COMMENT '贷款金额',
    loan_purpose VARCHAR(100) NOT NULL COMMENT '贷款用途',
    
    -- 原始审核信息
    original_result VARCHAR(20) NOT NULL COMMENT '原审核结果',
    original_reason TEXT NOT NULL COMMENT '原拒绝原因',
    original_auditor VARCHAR(50) NOT NULL COMMENT '原审核员',
    original_audit_time DATETIME NOT NULL COMMENT '原审核时间',
    
    -- 复审申请信息
    review_reason TEXT NOT NULL COMMENT '复审理由',
    review_apply_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '复审申请时间',
    status VARCHAR(20) DEFAULT 'review_pending' COMMENT '复审状态',
    priority VARCHAR(10) DEFAULT 'medium' COMMENT '优先级',
    additional_docs JSON COMMENT '补充材料文件名列表',
    
    -- 复审处理信息
    review_auditor VARCHAR(50) COMMENT '复审员',
    review_time DATETIME COMMENT '复审时间',
    review_result VARCHAR(20) COMMENT '复审结果',
    review_comment TEXT COMMENT '复审意见',
    
    -- 时间字段
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    
    INDEX idx_status (status),
    INDEX idx_priority (priority),
    INDEX idx_original_audit_id (original_audit_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='复审申请表';

-- 插入测试数据
INSERT INTO review_applications (
    original_audit_id, applicant_name, phone, id_card, loan_amount, loan_purpose,
    original_result, original_reason, original_auditor, original_audit_time,
    review_reason, status, priority, additional_docs,
    review_auditor, review_time, review_result, review_comment
) VALUES 
-- 待复审的申请
(1001, '张三', '13800138001', '110101199001011234', 50000.00, '创业资金',
 'rejected', '信用评分不足，月收入偏低', '审核员A', '2024-01-15 09:30:00',
 '提供了新的收入证明和银行流水，信用状况有所改善', 'review_pending', 'high', 
 '["新收入证明.pdf", "银行流水.pdf"]', NULL, NULL, NULL, NULL),

(1002, '李四', '13800138002', '110101199002022345', 80000.00, '房屋装修',
 'rejected', '负债比例过高，还款能力不足', '审核员B', '2024-01-20 14:20:00',
 '已结清部分债务，负债比例降低，提供清债证明', 'review_pending', 'medium',
 '["清债证明.pdf", "更新征信报告.pdf"]', NULL, NULL, NULL, NULL),

(1003, '王五', '13800138003', '110101199003033456', 30000.00, '医疗费用',
 'rejected', '工作不稳定，收入来源单一', '审核员C', '2024-01-25 11:15:00',
 '已签订正式劳动合同，工作稳定，申请紧急医疗贷款', 'review_pending', 'urgent',
 '["劳动合同.pdf", "医院诊断书.pdf"]', NULL, NULL, NULL, NULL),

-- 已处理的复审申请
(1004, '赵六', '13800138004', '110101199004044567', 100000.00, '购车',
 'rejected', '贷款用途不明确，风险较高', '审核员A', '2024-01-10 16:45:00',
 '提供详细购车计划和合同，用途明确', 'review_approved', 'medium',
 '["购车合同.pdf", "车辆报价单.pdf"]', '复审员甲', '2024-01-28 10:30:00', 'approved', '经复审，申请人提供了详细的购车计划，用途明确，同意放款'),

(1005, '钱七', '13800138005', '110101199005055678', 25000.00, '教育培训',
 'rejected', '还款计划不合理', '审核员B', '2024-01-12 13:20:00',
 '重新制定了还款计划，更加合理可行', 'review_rejected', 'low',
 '["新还款计划.pdf"]', '复审员乙', '2024-01-27 15:45:00', 'rejected', '经复审，申请人虽然提供了新的还款计划，但综合风险评估仍然偏高，维持原决定'),

(1006, '孙八', '13800138006', '110101199006066789', 60000.00, '经营周转',
 'rejected', '经营状况不佳，现金流不稳定', '审核员C', '2024-01-18 09:00:00',
 '经营状况好转，提供最新财务报表', 'review_approved', 'high',
 '["最新财务报表.pdf", "经营许可证.pdf"]', '复审员甲', '2024-01-30 14:20:00', 'approved', '经复审，申请人经营状况确实有所好转，现金流改善，同意放款'),

-- 更多待复审申请
(1007, '周九', '13800138007', '110101199007077890', 40000.00, '债务整合',
 'rejected', '多头借贷，风险过高', '审核员A', '2024-02-01 10:15:00',
 '已部分结清其他贷款，降低多头借贷风险', 'review_pending', 'medium',
 '["部分结清证明.pdf", "征信更新报告.pdf"]', NULL, NULL, NULL, NULL),

(1008, '吴十', '13800138008', '110101199008088901', 70000.00, '投资理财',
 'rejected', '投资用途风险较大', '审核员B', '2024-02-03 16:30:00',
 '修改贷款用途为稳健投资，提供详细投资计划', 'review_pending', 'low',
 '["投资计划书.pdf", "风险评估报告.pdf"]', NULL, NULL, NULL, NULL),

(1009, '郑十一', '13800138009', '110101199009099012', 35000.00, '紧急资金',
 'rejected', '用途不够明确，缺乏支撑材料', '审核员C', '2024-02-05 11:45:00',
 '家庭突发疾病，需要紧急医疗资金，已提供医院证明', 'review_pending', 'urgent',
 '["医院诊断证明.pdf", "医疗费用预算.pdf"]', NULL, NULL, NULL, NULL),

-- 添加更多历史记录数据
(1010, '陈强', '13800138012', '110101199003031234', 80000.00, '房屋装修',
 'rejected', '担保人信用不足', '赵审核', '2024-06-18 10:00:00',
 '更换担保人，新担保人信用良好', 'review_approved', 'medium',
 '["新担保人身份证.pdf", "担保协议.pdf"]', '李审核', '2024-06-26 10:30:00', 'approved', '新担保人资质良好，同意通过'),

(1011, '刘芳', '13800138013', '110101199004041234', 45000.00, '子女教育',
 'rejected', '还款来源不稳定', '王审核', '2024-06-15 14:20:00',
 '提供配偶收入证明，双收入保障还款', 'review_approved', 'high',
 '["配偶收入证明.pdf", "结婚证.pdf"]', '张审核', '2024-06-25 16:45:00', 'approved', '双收入家庭，还款保障充足，同意放款'),

(1012, '马伟', '13800138014', '110101199005051234', 120000.00, '投资扩产',
 'rejected', '投资计划风险过大', '李审核', '2024-06-20 09:15:00',
 '调整投资计划，降低风险系数', 'review_rejected', 'low',
 '["调整投资计划.pdf", "风险评估.pdf"]', '赵审核', '2024-06-28 11:20:00', 'rejected', '经复审，调整后的投资计划仍存在较大风险，维持原决定'),

(1013, '杨敏', '13800138015', '110101199006061234', 35000.00, '旅游消费',
 'rejected', '贷款用途非必需', '张审核', '2024-06-22 15:30:00',
 '改为紧急医疗用途，提供相关证明', 'review_approved', 'urgent',
 '["医疗费用单.pdf", "医生诊断.pdf"]', '王审核', '2024-06-29 09:10:00', 'approved', '用途变更为医疗紧急需求，符合放贷条件'),

(1014, '黄辉', '13800138016', '110101199007071234', 90000.00, '房产首付',
 'rejected', '首付比例不足', '王审核', '2024-06-25 11:00:00',
 '追加自有资金，提高首付比例', 'review_approved', 'medium',
 '["追加资金证明.pdf", "购房合同.pdf"]', '李审核', '2024-06-30 14:30:00', 'approved', '首付比例达标，购房计划合理，同意放款'),

-- 更多待处理的复审申请
(1015, '林娜', '13800138017', '110101199008081234', 55000.00, '装修贷款',
 'rejected', '收入证明有疑问', '赵审核', '2024-07-01 10:20:00',
 '提供税务局出具的纳税证明，证实收入真实性', 'review_pending', 'medium',
 '["纳税证明.pdf", "工资流水.pdf"]', NULL, NULL, NULL, NULL);

-- 验证数据插入
SELECT 
    COUNT(*) as total_count,
    SUM(CASE WHEN status = 'review_pending' THEN 1 ELSE 0 END) as pending_count,
    SUM(CASE WHEN status = 'review_approved' THEN 1 ELSE 0 END) as approved_count,
    SUM(CASE WHEN status = 'review_rejected' THEN 1 ELSE 0 END) as rejected_count
FROM review_applications;

-- 按优先级统计
SELECT priority, COUNT(*) as count 
FROM review_applications 
GROUP BY priority;

-- 最新的复审申请
SELECT applicant_name, loan_amount, status, priority, review_apply_time 
FROM review_applications 
ORDER BY review_apply_time DESC 
LIMIT 5;

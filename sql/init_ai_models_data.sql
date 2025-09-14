-- 模型管理系统初始化数据SQL脚本
-- 创建时间: 2025-06-27
-- 描述: 为ai_models表添加示例数据

-- 首先确保表存在（如果使用Tortoise ORM，通常会自动创建）
-- CREATE TABLE IF NOT EXISTS ai_models (
--     id INT AUTO_INCREMENT PRIMARY KEY,
--     name VARCHAR(100) NOT NULL COMMENT '模型名称',
--     version VARCHAR(20) NOT NULL COMMENT '版本号',
--     file_path VARCHAR(255) NOT NULL COMMENT '文件路径',
--     description TEXT NOT NULL COMMENT '模型描述',
--     technical_details TEXT NULL COMMENT '技术说明',
--     file_size INT NOT NULL COMMENT '文件大小(字节)',
--     file_extension VARCHAR(10) NOT NULL COMMENT '文件扩展名',
--     status VARCHAR(20) NOT NULL DEFAULT 'testing' COMMENT '模型状态: active/current/testing',
--     ks_value FLOAT NULL COMMENT 'KS值',
--     bad_rate FLOAT NULL COMMENT '坏账率',
--     accuracy FLOAT NULL COMMENT '准确率',
--     recall FLOAT NULL COMMENT '召回率',
--     `precision` FLOAT NULL COMMENT '精确率',
--     created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
--     updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
--     INDEX idx_name_version (name, version),
--     INDEX idx_status (status)
-- ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='AI模型信息表';

-- 插入示例数据
INSERT INTO ai_models (
    name, 
    version, 
    file_path, 
    description, 
    technical_details, 
    file_size, 
    file_extension, 
    status, 
    ks_value, 
    bad_rate, 
    accuracy, 
    recall, 
    `precision`, 
    created_at, 
    updated_at
) VALUES 
-- 当前使用的模型
(
    '风控评分模型v2.0', 
    '2.0.0', 
    './ai/risk_model_v2.0_current.pkl', 
    '基于深度学习的风控评分模型，采用神经网络架构，具有更高的准确率和更低的误判率。适用于个人信贷风险评估。', 
    '使用TensorFlow 2.8构建，包含3层全连接层，dropout=0.3，batch_size=256，训练样本100万条，验证集20万条。特征工程包含用户基础信息、行为数据、征信记录等45个维度。', 
    15728640, 
    '.pkl', 
    'current', 
    0.38, 
    0.065, 
    0.91, 
    0.87, 
    0.89, 
    '2024-05-15 10:30:00', 
    '2024-06-20 14:20:00'
),

-- 活跃状态的历史模型
(
    '风控评分模型v1.5', 
    '1.5.0', 
    './ai/risk_model_v1.5_active.pkl', 
    '基于随机森林的风控评分模型，稳定性较好，在生产环境中表现优异。', 
    '使用Scikit-learn RandomForest，n_estimators=200，max_depth=15，特征数量38个。训练时间2小时，模型大小适中。', 
    8912345, 
    '.pkl', 
    'active', 
    0.34, 
    0.078, 
    0.86, 
    0.82, 
    0.84, 
    '2024-03-10 15:20:00', 
    '2024-05-15 09:45:00'
),

-- 另一个活跃模型
(
    '风控评分模型v1.2', 
    '1.2.0', 
    './ai/risk_model_v1.2_active.pkl', 
    '基于逻辑回归的轻量级风控模型，推理速度快，资源消耗低。', 
    '使用逻辑回归算法，L2正则化，C=0.1，特征标准化处理。模型文件小，适合高并发场景。', 
    2457890, 
    '.pkl', 
    'active', 
    0.31, 
    0.085, 
    0.83, 
    0.79, 
    0.81, 
    '2024-01-20 11:15:00', 
    '2024-03-08 16:30:00'
),

-- 测试中的新模型
(
    '风控评分模型v3.0-beta', 
    '3.0.0-beta', 
    './ai/risk_model_v3.0_testing.pth', 
    '基于Transformer架构的新一代风控模型，引入注意力机制，正在测试阶段。', 
    '使用PyTorch 1.12构建，Transformer编码器，8个注意力头，隐藏层维度512。训练数据150万条，采用对抗训练提升鲁棒性。GPU训练时间48小时。', 
    45123456, 
    '.pth', 
    'testing', 
    0.42, 
    0.055, 
    0.93, 
    0.91, 
    0.92, 
    '2024-06-10 09:00:00', 
    '2024-06-25 18:30:00'
),

-- 另一个测试模型
(
    '风控评分模型-XGBoost', 
    '2.1.0', 
    './ai/risk_model_xgboost_testing.pkl', 
    '基于XGBoost的梯度提升模型，具有良好的特征重要性解释能力。', 
    'XGBoost 1.6，n_estimators=500，learning_rate=0.05，max_depth=8。支持特征重要性分析，便于业务理解。', 
    12345678, 
    '.pkl', 
    'testing', 
    0.36, 
    0.072, 
    0.88, 
    0.85, 
    0.86, 
    '2024-06-05 14:00:00', 
    '2024-06-22 10:15:00'
),

-- ONNX格式的模型
(
    '风控评分模型-轻量版', 
    '1.8.0', 
    './ai/risk_model_lite.onnx', 
    '专为移动端和边缘计算优化的轻量级风控模型。', 
    '转换为ONNX格式，模型量化压缩，支持CPU推理，延迟<10ms。适合移动APP集成。', 
    3456789, 
    '.onnx', 
    'active', 
    0.29, 
    0.092, 
    0.80, 
    0.76, 
    0.78, 
    '2024-04-18 16:45:00', 
    '2024-06-01 12:20:00'
),

-- TensorFlow SavedModel格式
(
    '风控评分模型-TF版', 
    '2.2.0', 
    './ai/risk_model_tf_serving.pb', 
    '专为TensorFlow Serving部署优化的模型版本。', 
    'TensorFlow 2.9 SavedModel格式，支持GPU推理，可通过TF Serving提供REST API服务。包含完整的预处理图。', 
    23456789, 
    '.pb', 
    'testing', 
    0.37, 
    0.068, 
    0.90, 
    0.86, 
    0.88, 
    '2024-06-12 11:30:00', 
    '2024-06-24 15:45:00'
),

-- 另一个历史模型
(
    '风控评分模型v1.0', 
    '1.0.0', 
    './ai/risk_model_v1.0_legacy.joblib', 
    '第一代风控评分模型，使用传统机器学习方法构建。', 
    '使用Scikit-learn构建，包含数据预处理、特征选择、模型训练的完整pipeline。joblib格式保存。', 
    5678901, 
    '.joblib', 
    'active', 
    0.28, 
    0.095, 
    0.78, 
    0.74, 
    0.76, 
    '2023-12-05 13:20:00', 
    '2024-01-15 09:30:00'
);

-- 验证插入的数据
SELECT 
    id,
    name,
    version,
    status,
    ks_value,
    bad_rate,
    accuracy,
    created_at
FROM ai_models 
ORDER BY created_at DESC;

-- 统计各状态的模型数量
SELECT 
    status,
    COUNT(*) as count,
    AVG(accuracy) as avg_accuracy,
    AVG(ks_value) as avg_ks_value
FROM ai_models 
GROUP BY status;

-- 查看当前使用的模型
SELECT 
    id,
    name,
    version,
    ks_value,
    bad_rate,
    accuracy,
    recall,
    `precision`
FROM ai_models 
WHERE status = 'current';

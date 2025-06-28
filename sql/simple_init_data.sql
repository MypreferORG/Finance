-- 简化版模型数据初始化SQL
-- 适用于快速测试和开发环境

-- 插入基础示例数据
INSERT INTO ai_models (
    name, version, file_path, description, file_size, file_extension, status, 
    ks_value, bad_rate, accuracy, recall, `precision`
) VALUES 
-- 当前使用的模型
('风控模型v2.0', '2.0.0', './ai/model_v2_current.pkl', '当前生产环境使用的风控评分模型', 15728640, '.pkl', 'current', 0.38, 0.065, 0.91, 0.87, 0.89),

-- 活跃的备用模型
('风控模型v1.5', '1.5.0', './ai/model_v1_5_active.pkl', '稳定的备用风控模型', 8912345, '.pkl', 'active', 0.34, 0.078, 0.86, 0.82, 0.84),
('风控模型v1.2', '1.2.0', './ai/model_v1_2_active.pkl', '轻量级风控模型', 2457890, '.pkl', 'active', 0.31, 0.085, 0.83, 0.79, 0.81),

-- 测试中的模型
('风控模型v3.0-beta', '3.0.0', './ai/model_v3_testing.pth', '新一代测试模型', 45123456, '.pth', 'testing', 0.42, 0.055, 0.93, 0.91, 0.92),
('XGBoost风控模型', '2.1.0', './ai/xgboost_model.pkl', 'XGBoost算法测试模型', 12345678, '.pkl', 'testing', 0.36, 0.072, 0.88, 0.85, 0.86);

-- 快速验证
SELECT name, version, status, accuracy FROM ai_models;

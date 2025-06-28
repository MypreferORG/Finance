/*
 Navicat Premium Data Transfer

 Source Server         : localhost_3306
 Source Server Type    : MySQL
 Source Server Version : 50726
 Source Host           : localhost:3306
 Source Schema         : finance

 Target Server Type    : MySQL
 Target Server Version : 50726
 File Encoding         : 65001

 Date: 28/06/2025 17:18:48
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for ai_models
-- ----------------------------
DROP TABLE IF EXISTS `ai_models`;
CREATE TABLE `ai_models`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '模型名称',
  `version` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '版本号',
  `file_path` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '文件路径',
  `description` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '模型描述',
  `technical_details` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '技术说明',
  `file_size` int(11) NOT NULL COMMENT '文件大小(字节)',
  `file_extension` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '文件扩展名',
  `status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'testing' COMMENT '模型状态: active/current/testing',
  `ks_value` double NULL DEFAULT NULL COMMENT 'KS值',
  `bad_rate` double NULL DEFAULT NULL COMMENT '坏账率',
  `accuracy` double NULL DEFAULT NULL COMMENT '准确率',
  `recall` double NULL DEFAULT NULL COMMENT '召回率',
  `precision` double NULL DEFAULT NULL COMMENT '精确率',
  `created_at` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) COMMENT '创建时间',
  `updated_at` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6) COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_ai_models_name_8d5f82`(`name`, `version`) USING BTREE,
  INDEX `idx_ai_models_status_c881b8`(`status`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 17 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '模型文件信息' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of ai_models
-- ----------------------------
INSERT INTO `ai_models` VALUES (1, '风控评分模型v2.0', '2.0.0', './ai/risk_model_v2.0_current.pkl', '基于深度学习的风控评分模型，采用神经网络架构，具有更高的准确率和更低的误判率。适用于个人信贷风险评估。', '使用TensorFlow 2.8构建，包含3层全连接层，dropout=0.3，batch_size=256，训练样本100万条，验证集20万条。特征工程包含用户基础信息、行为数据、征信记录等45个维度。', 15728640, '.pkl', 'active', 0.38, 0.065, 0.91, 0.87, 0.89, '2024-05-15 10:30:00.000000', '2025-06-27 19:19:50.971154');
INSERT INTO `ai_models` VALUES (2, '风控评分模型v1.5', '1.5.0', './ai/risk_model_v1.5_active.pkl', '基于随机森林的风控评分模型，稳定性较好，在生产环境中表现优异。', '使用Scikit-learn RandomForest，n_estimators=200，max_depth=15，特征数量38个。训练时间2小时，模型大小适中。', 8912345, '.pkl', 'active', 0.34, 0.078, 0.86, 0.82, 0.84, '2024-03-10 15:20:00.000000', '2024-05-15 09:45:00.000000');
INSERT INTO `ai_models` VALUES (3, '风控评分模型v1.2', '1.2.0', './ai/risk_model_v1.2_active.pkl', '基于逻辑回归的轻量级风控模型，推理速度快，资源消耗低。', '使用逻辑回归算法，L2正则化，C=0.1，特征标准化处理。模型文件小，适合高并发场景。', 2457890, '.pkl', 'active', 0.31, 0.085, 0.83, 0.79, 0.81, '2024-01-20 11:15:00.000000', '2024-03-08 16:30:00.000000');
INSERT INTO `ai_models` VALUES (4, '风控评分模型v3.0-beta', '3.0.0-beta', './ai/risk_model_v3.0_testing.pth', '基于Transformer架构的新一代风控模型，引入注意力机制，正在测试阶段。', '使用PyTorch 1.12构建，Transformer编码器，8个注意力头，隐藏层维度512。训练数据150万条，采用对抗训练提升鲁棒性。GPU训练时间48小时。', 45123456, '.pth', 'testing', 0.42, 0.055, 0.93, 0.91, 0.92, '2024-06-10 09:00:00.000000', '2024-06-25 18:30:00.000000');
INSERT INTO `ai_models` VALUES (5, '风控评分模型-XGBoost', '2.1.0', './ai/risk_model_xgboost_testing.pkl', '基于XGBoost的梯度提升模型，具有良好的特征重要性解释能力。', 'XGBoost 1.6，n_estimators=500，learning_rate=0.05，max_depth=8。支持特征重要性分析，便于业务理解。', 12345678, '.pkl', 'testing', 0.36, 0.072, 0.88, 0.85, 0.86, '2024-06-05 14:00:00.000000', '2024-06-22 10:15:00.000000');
INSERT INTO `ai_models` VALUES (6, '风控评分模型-轻量版', '1.8.0', './ai/risk_model_lite.onnx', '专为移动端和边缘计算优化的轻量级风控模型。', '转换为ONNX格式，模型量化压缩，支持CPU推理，延迟<10ms。适合移动APP集成。', 3456789, '.onnx', 'active', 0.29, 0.092, 0.8, 0.76, 0.78, '2024-04-18 16:45:00.000000', '2024-06-01 12:20:00.000000');
INSERT INTO `ai_models` VALUES (7, '风控评分模型-TF版', '2.2.0', './ai/risk_model_tf_serving.pb', '专为TensorFlow Serving部署优化的模型版本。', 'TensorFlow 2.9 SavedModel格式，支持GPU推理，可通过TF Serving提供REST API服务。包含完整的预处理图。', 23456789, '.pb', 'testing', 0.37, 0.068, 0.9, 0.86, 0.88, '2024-06-12 11:30:00.000000', '2024-06-24 15:45:00.000000');
INSERT INTO `ai_models` VALUES (8, '风控评分模型v1.0', '1.0.0', './ai/risk_model_v1.0_legacy.joblib', '第一代风控评分模型，使用传统机器学习方法构建。', '使用Scikit-learn构建，包含数据预处理、特征选择、模型训练的完整pipeline。joblib格式保存。', 5678901, '.joblib', 'active', 0.28, 0.095, 0.78, 0.74, 0.76, '2023-12-05 13:20:00.000000', '2024-01-15 09:30:00.000000');
INSERT INTO `ai_models` VALUES (9, '风控评分模型v2.1', '1.0.0', 'D:\\ML\\finance\\Finance\\ai\\风控评分模型v2.1_1.0.0_b3df6fc5467040e4b65411f3993a05b7.pth', '风控评分模型v2.1', NULL, 438406567, '.pth', 'active', NULL, NULL, NULL, NULL, NULL, '2025-06-27 19:17:47.405137', '2025-06-27 19:30:45.154096');
INSERT INTO `ai_models` VALUES (10, '风控评分模型v2.2', '1.0.1', '/ai/model/风控评分模型v2.2_1.0.1_41493ca79db6468bb29f8d56b4602bcd.pth', '风控评分模型v2.2', NULL, 438406567, '.pth', 'active', NULL, NULL, NULL, NULL, NULL, '2025-06-27 19:24:55.475668', '2025-06-27 19:53:46.374728');
INSERT INTO `ai_models` VALUES (11, '风控评分模型v2.3', '1.0.3', 'D:\\ML\\finance\\Finance\\ai\\风控评分模型v2.3_1.0.3_cd89f3b4a2454403b3634c6d4d09b84f.pth', '风控评分模型v2.3', NULL, 438406567, '.pth', 'active', 0.35, 0.08, 0.85, 0.78, 0.82, '2025-06-27 19:53:35.527037', '2025-06-27 20:04:25.136053');
INSERT INTO `ai_models` VALUES (12, '风控评分模型v2.4', '1.0.4', 'D:\\ML\\finance\\Finance\\ai\\风控评分模型v2.4_1.0.4_84e8f15c9e5b4e1386bcef463a3e29a2.pth', '风控评分模型v2.4', NULL, 438406567, '.pth', 'testing', 0.4, 0.072, 0.9, 0.81, 0.84, '2025-06-27 19:57:52.482004', '2025-06-27 19:57:52.482004');
INSERT INTO `ai_models` VALUES (13, '风控评分模型v2.5', '2.0.5', 'D:\\ML\\finance\\Finance\\ai\\风控评分模型v2.5_2.0.5_6b4585738f5b4a33a2af48da668b208d.pth', '风控评分模型v2.5', NULL, 438406567, '.pth', 'testing', 0.35, 0.08, 0.85, 0.78, 0.82, '2025-06-27 19:59:38.548432', '2025-06-27 19:59:38.548432');
INSERT INTO `ai_models` VALUES (14, '风控评分模型v2.6', '1.0.0', 'D:\\ML\\finance\\Finance\\ai\\风控评分模型v2.6_1.0.0_ce2d780522e6450e83ab4414f2980126.pth', '风控评分模型v2.6', NULL, 438406567, '.pth', 'testing', 0.35, 0.08, 0.85, 0.78, 0.82, '2025-06-27 20:00:29.882852', '2025-06-27 20:00:29.882852');
INSERT INTO `ai_models` VALUES (15, '风控评分模型v2.7', '1.0.0', 'd:\\ML\\finance\\Finance\\ai\\风控评分模型v2.7_1.0.0_6c59069c80664a5882f2ae78775a3d96.pth', '风控评分模型v2.7', NULL, 438406567, '.pth', 'testing', 0.35, 0.08, 0.85, 0.78, 0.82, '2025-06-27 20:01:15.974073', '2025-06-27 20:01:15.974073');
INSERT INTO `ai_models` VALUES (16, '风控评分模型v2.8', '1.0.0', 'D:\\ML\\finance\\Finance\\ai\\model\\风控评分模型v2.8_1.0.0_59c53236df384087b84671e3ded067cb.pth', '风控评分模型v2.8', NULL, 438406567, '.pth', 'current', 0.35, 0.08, 0.85, 0.78, 0.82, '2025-06-27 20:03:46.175750', '2025-06-27 20:04:25.138941');

-- ----------------------------
-- Table structure for announcement
-- ----------------------------
DROP TABLE IF EXISTS `announcement`;
CREATE TABLE `announcement`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '公告标题',
  `content` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '公告内容，支持Markdown或HTML格式',
  `publish_date` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) COMMENT '公告发布时间',
  `updated_at` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6) COMMENT '公告最后更新时间',
  `status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'active' COMMENT '公告状态（如：active、inactive、archived等）',
  `author` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '公告发布者姓名或昵称',
  `expiration_date` datetime(6) NULL DEFAULT NULL COMMENT '公告过期时间（可选）',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_announcemen_title_df0aa9`(`title`, `publish_date`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '公告表：用于记录系统公告和通知的信息' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of announcement
-- ----------------------------

-- ----------------------------
-- Table structure for article
-- ----------------------------
DROP TABLE IF EXISTS `article`;
CREATE TABLE `article`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `link` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '文章链接',
  `title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '文章标题',
  `publish_date` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) COMMENT '记录时间',
  `summary` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '文章摘要或简介',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `link`(`link`) USING BTREE,
  INDEX `idx_article_link_c12f67`(`link`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 38 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '文章表：用于记录文章的链接信息' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of article
-- ----------------------------
INSERT INTO `article` VALUES (1, 'https://zhuanlan.zhihu.com/p/411427024', '银行贷款具体流程是什么？主要有这5大环节! - 知乎', '2024-07-07 23:31:25.850653', '银行贷款总的流程可以分为 贷款的受理与调查 、贷款的审查与审批、 贷款的签收与发放 、贷款的支付、 贷后管理 5大环节。. 申请银行贷款过程中的具体流程分别是什么样的，以及申请银行贷款过程中具体有哪些需要注意的点，已经集中为大家整理好了，绝对干货! 一、贷款的受理与调查');
INSERT INTO `article` VALUES (2, 'https://zhuanlan.zhihu.com/p/308778621', '各银行信用贷款申请条件以及流程 - 知乎 - 知乎专栏', '2024-03-03 23:31:25.855899', '本文章更新于 2021年7月16日 现目前已统计7家银行，后期会覆盖更多银行。 现在想要申请银行的贷款其实很简单，全程app 申请，资料都不需要准备。 附上具体操作流程。 工商银行-融e借1.额度:600块-80万（手机银行最…');
INSERT INTO `article` VALUES (3, 'https://baijiahao.baidu.com/s?id=1819934343041841750', '贷款审批流程解析：从申请到放款，贷款的各个环节如何进行？', '2024-11-14 23:31:25.859948', '贷款是许多人解决资金问题的常见方式，无论是购房、购车、创业，还是应急周转，贷款都能有效满足我们的资金需求。然而，许多人对贷款的审批流程并不清楚，甚至不知道每个环节如何操作，申请贷款需要准备哪些材料。');
INSERT INTO `article` VALUES (4, 'https://zh.wikihow.com/提高你的信用评分', '如何提高你的信用评分: 11 步骤 - zh.wikihow.com', '2024-07-08 23:31:25.864678', '如何提高你的信用评分. 通常信贷公司会通过信用报告来判断客户的信用风险是否良好、是否有能力偿还贷款。你可以采取一些简单的措施来提高自己的信用评级。其中许多措施是禁止类的事项。 注意：这篇文章适用于美国。同时部分信息与其他管辖权相关，请首先核对与你所在区域是否有关。');
INSERT INTO `article` VALUES (5, 'https://www.csai.cn/loan/1410637.html', '信用评分怎么提高？爆改信用评分的八招 - 希财网', '2024-06-21 23:31:25.867123', '信用评分提高的方法如下：1、征信不良：尽快还清逾期的欠款，后续持续保持良好的信用状态。2、征信查询次数过多：确保半年内不办理任何信贷业务。3、贷款次数较多：尽可能地结清部分贷款，可以优先结清小额贷款。4、负债率过高：提前结清大额贷款。5、工作不稳定：连续工作3个月以上再 ...');
INSERT INTO `article` VALUES (6, 'https://zhuanlan.zhihu.com/p/349557694', '秒拒到秒批!5步教你快速提高综合信用评分~ - 知乎专栏', '2024-12-17 23:31:25.870629', '除此之外，还有这些可以有效提升综合信用分。 如何完善综合信用评分？ 1确保资料的完整性和真实性. 申请信息一定要如实填写，尽量填写完整。如果身份证号和姓名对不上，基本上就不会再进入下一步了。');
INSERT INTO `article` VALUES (7, 'https://zhuanlan.zhihu.com/p/667347012', '如何选择一个适合自己的贷款产品？ - 知乎专栏', '2024-06-04 23:46:54.706556', '如果对 贷款市场 不熟悉，是很难找到跟自己完全匹配的产品的，所以我们家今天就来给大家讲讲如何选择一款适合自己的贷款产品。 一、明确贷款的用途和期限 . 贷款必须要有一个明确的目的，千万不要盲目。');
INSERT INTO `article` VALUES (8, 'https://zhuanlan.zhihu.com/p/29138518562', '普通人如何选择最适合自己的贷款方式？2025年避坑指南与实操策略 - 知乎', '2024-05-23 23:46:54.711556', '在金融产品日益丰富的当下，贷款已成为普通人解决资金需求的重要工具。然而，面对复杂的贷款类型和潜在的陷阱，如何科学选择并规避风险？本文结合2025年最新政策与市场动态，从需求分析、产品匹配、风险防范等维度，提供一份实用指南。');
INSERT INTO `article` VALUES (9, 'https://www.zhihu.com/question/14025659998', '如何选择适合自己的贷款产品？避免这些常见误区，让贷款更顺利!? - 知乎', '2024-11-07 23:46:54.715555', '在贷款的过程中，许多人都遇到过各种问题——从选择合适的贷款产品到审批过程中的一些\"陷阱\"。作为一名从事贷款中介多年的专业人士，今天我就来为大家解答如何避免这些常见误区，选择最适合自己的贷款方案。');
INSERT INTO `article` VALUES (10, 'https://zhuanlan.zhihu.com/p/91911632', '征信报告怎么看？个人征信报告教学试解读（详细版） - 知乎', '2024-08-19 23:46:54.717837', '今天呆呆就来详细解读个人征信报告里都有哪些内容，有哪些需要注意的事项，详细版征信报告包含以下5项个人信息： ... 主要是通过之前本人在某申请过的贷款、或者信用卡类业务，申请银行主动向央行提交的。 ...');
INSERT INTO `article` VALUES (11, 'https://zhuanlan.zhihu.com/p/345565948', '个人详细版征信报告解读(两万字长文) - 知乎 - 知乎专栏', '2024-11-01 23:46:54.720247', '九、报告说明. 十、编制说明. 十一、总结. 以上内容是关于个人信用报告（详细版）的详细解读，你的信用价值百万，这并不是一句空话，而信用的起步在于征信报告，一份好的征信报告可以让你在金融界自由驰骋，为个人发展插上起飞的翅膀。');
INSERT INTO `article` VALUES (12, 'https://zhuanlan.zhihu.com/p/695629989', '人民银行详版个人征信报告解读（保姆级1万5千字） - 知乎', '2024-03-17 23:46:54.724151', '从《个人信用报告（自主查询版）解读》的定义强调\"其他还款责任\"和进行的列举来看，\"相关还款责任\"指的是个人为第三方提供保证而可能承担的或有负债或已经成立的保证责任。 ... 然后上报给征信系统，最后记录在我们的征信报告上面，所以在信用卡 ...');
INSERT INTO `article` VALUES (13, 'https://www.fangdailixi.com/', '房贷计算器 房贷计算器2025年最新版 房贷利率计算器 房贷利息', '2024-07-17 23:57:31.094479', '房贷计算器提供LPR利率和固定利率两种计算方式，以及等额本息和等额本金两种还款方式，方便对比查看房贷利息和月供明细。输入贷款金额、房价、首付比例、期限等信息，即可得到最新的房贷利率和还款结果。');
INSERT INTO `article` VALUES (14, 'https://fin.paas.cmbchina.com/fininfo/calloanper', '招商银行 -- 个人贷款计算器 - cmbchina.com', '2024-09-01 23:57:31.103791', '输入贷款金额、期限、年利率和还款方式，可计算按揭贷款和固定利率贷款的等额本息还款和等额本金还款的月供和总利息。数据仅供参考，以办理业务或交易实际结果为准。');
INSERT INTO `article` VALUES (15, 'https://ccb.com/chn/personal/interestv3/calculator_dk.shtml', '中国建设银行-个人贷款计算器', '2025-01-20 23:57:31.107315', '初始化栏目：个人贷款计算器 中国建设银行，在全球范围内为台湾、香港、美国、澳大利亚等国家或地区提供全面金融服务，主要经营公司银行业务、个人银行业务和资金业务，包括居民储蓄存款、信贷资金贷款、住房类贷款、外汇、信用卡，以及投资理财等多种业务。');
INSERT INTO `article` VALUES (16, 'https://zhuanlan.zhihu.com/p/62115136', '房贷提前还款，到底好不好？ - 知乎 - 知乎专栏', '2024-11-16 23:57:31.110312', '三、你适合提前还款吗？ 1、适合提前还款的人. ①对负债非常敏感，一想到负债就超大压力。 ②没有合适的投资渠道，理财赚的钱远不如提前还贷省下的银行利息。 ③想拿房子去做抵押投资。这种情况下，你可以提前还清贷款，解除房子在银行的抵押，再拿 ...');
INSERT INTO `article` VALUES (17, 'https://baijiahao.baidu.com/s?id=1807236736318451531', '提前还房贷，到底是\"聪明\"还是\"糊涂\"？银行员工算了一笔账', '2024-05-12 23:57:31.113365', '首先，我们不得不提的是提前还贷最直观的效益——节省利息。房贷的利息是根据剩余本金和利率计算的，本金越少，利息自然就越少。以一笔100万、30年期限、年利率5%的房贷为例，如果采用等额本息还款方式，每月还款额约为5368元，其中利息占比较大。');
INSERT INTO `article` VALUES (18, 'https://zhuanlan.zhihu.com/p/327773911', '房贷可以提前还款吗？带你分析房贷提前还款的\"利与弊\"？ - 知乎', '2024-09-17 23:57:31.115365', '享有折扣利率不适合提前还款 在银行政策里，银行所给出的房贷优惠是不一样的，房奴可能享受到7折或者8折的利率优惠，此时你正在享受折扣利率，那么一旦你选择了提前还贷，你就是自己选择弃权了这份福利，因此，享有折扣利率的房奴最好别选择提前还贷 ...');
INSERT INTO `article` VALUES (19, 'https://www.jiemian.com/article/1666739.html', '拿到个人征信报告读不懂？看完这篇解析，你也能成专家|界面新闻 · JMedia', '2024-09-18 23:57:31.123191', '手把手教你读懂信用报告. 今天我们要解读的对象就是个人版信用报告。 先来看看个人版信用报告的组成结构： 下面详细介绍各个部分该如何解读。 （1）报告头。直接看下图相信大家都能懂。');
INSERT INTO `article` VALUES (20, 'https://zhuanlan.zhihu.com/p/11783157276', '征信有逾期按着以下4个步骤去申诉，就不用再等五年了! - 知乎', '2024-04-29 23:57:31.124960', '如果发现征信报告上有逾期记录，想要申诉消除，可参考以下步骤： 1. 打印详版征信报告：仔细查看报告上的逾期记录，包括逾期的机构、金额、时间、原因等，以便做出对应的处理方案。需要注意的是，征信报告上显示的逾期金额可能并非真实的欠款金额，有 ...');
INSERT INTO `article` VALUES (21, 'https://www.zhihu.com/question/640224619', '银行对贷款逾期的处理方式有哪些？ - 知乎', '2025-01-19 23:57:31.127460', '坐标郑州，郑州贷款行业从事 6 年的资深信贷员，给你分析解答。 银行的贷款逾期以后，肯定要面临催收!首先就是短信通知，电话通知，然后就是给联系人打电话协助通知还款，上门通知还款，然后就是起诉至法院，强制执行!');
INSERT INTO `article` VALUES (22, 'https://www.csai.cn/loan/1420266.html', '信用贷款逾期怎么处理？不要慌，补救措施有很多 - 希财网', '2024-12-10 23:57:31.129465', '信用贷款逾期后的处理办法有很多，这里介绍一些常见的，希望能帮到大家。 一、及时还款. 正规贷款平台都接入了征信中心，所以逾期后会影响征信，对后续生活借贷都有不良影响。');
INSERT INTO `article` VALUES (23, 'https://zhuanlan.zhihu.com/p/93629044', '一份超详细的理财入门指南 - 知乎 - 知乎专栏', '2024-10-22 23:57:31.132907', '理财作为一种技能，和学习任何知识一样遵循刻意练习的法则。 多学、多练、多思考，和比自己掌握的更好的人讨论，这些都是提高学习效果的通路。 正如在文章一开始说的，我学理财更多的是思维层面的收获。');
INSERT INTO `article` VALUES (24, 'https://www.zhihu.com/tardis/bd/art/437691372', '理财小白如何高效理财？（含新手入门时机+风险规避+养鸡经验）', '2024-08-22 23:57:31.135908', '之前对于理财都是无头苍蝇，直到之前上了一位老师的课，我才有种醍醐灌醒的感觉，他就把关于基金理财讲得非常详细，而且还边教边实操。 有需要的朋友不妨点进去听一听，而且老师有15年以上的基金、股票投资实战经验总结，学完之后你对投资理财的认知 ...');
INSERT INTO `article` VALUES (25, 'https://zhuanlan.zhihu.com/p/82696752', '投资理财基础知识 你一定要懂得7大理财知识 - 知乎', '2025-02-12 23:57:31.137906', '总觉得投资理财是\"别人的事\"?总想着钱不多不用理财?你这样想就亏大了!理财能帮助你实现财富稳健增长，每个人都应该学习一些理财知识。 投资理财基础知识：你一定要懂得7大理财知识 一、理财的三个环节 一个中心…');
INSERT INTO `article` VALUES (26, 'https://www.zhihu.com/question/631412958', '如何合理规划和管理个人财务？ - 知乎', '2025-01-04 23:57:31.139907', '1.3 净现金流 每月的盈余（或赤字）情况，是判断个人或家庭是否需要调整消费结构的重要依据。. 确定财务目标 目标是财务规划的指南针。 根据时间维度，财务目标可分为： 短期目标（1-3年）：偿还信用卡欠款、购买家电、组建紧急储备金。 中期目标（3-10年）：子女教育、购房、事业发展。');
INSERT INTO `article` VALUES (27, 'https://zhuanlan.zhihu.com/p/374115506', '手把手教你做个人财务分析 - 知乎 - 知乎专栏', '2024-10-11 23:57:31.143427', '个人（家庭）的财务分析，用的是：资产负债表、 收入支出表 ，两张表格。通过表格中不同数据之间的比率关系，来分析个人（家庭）的财务状况，然后再进行合理的理财规划。 资产负债表：反应的是个人（家庭）资产和负债在某一个时点的基本情况。');
INSERT INTO `article` VALUES (28, 'https://zhuanlan.zhihu.com/p/28627291', '学会个人财务规划（入门） - 知乎专栏', '2024-05-03 23:57:31.145426', '如果大学时期你是个月光族，那么现在你就要开始改变你的花费习惯。将要从事公司财务管理的你，可以通过管理个人资金开始培养财务意识。（以下内容只是为初入职场的新人提供入门理财规划建议，没有深入的理财规划和投资的知识。');
INSERT INTO `article` VALUES (29, 'https://zhuanlan.zhihu.com/p/706182378', '贷款逾期该怎么办？别怕!自救指南!（5000字长文收藏备用） - 知乎', '2024-06-26 00:02:09.392977', '关于如何把网贷置换成银行贷款可以参考这篇文章，详细介绍了置换的流程： 最后，详细介绍了贷款逾期后该怎么办，而且已经细致到了每个环节的实操，希望能够解开你关于贷款逾期的所有疑惑。如果实际还遇到了难以解决的问题，还可以来找杭州贷款菲姐。');
INSERT INTO `article` VALUES (30, 'https://www.zhihu.com/question/641383644', '有什么方法可以提高个人信用评分？ - 知乎', '2024-09-14 00:06:14.503610', '提高个人信用评分做好下面几点! 【1】保持个人信息的稳定性，准确性. 手机号信息. 个人工作信息. 居住地址信息 【2】按时履约. 名下贷款，信用卡及时还款，切勿逾期，及时还款是守信的表现，也是能力的体现! 【3】网贷账户还清记得注销!');
INSERT INTO `article` VALUES (31, 'https://www.zhihu.com/question/283685807', '公务员怎样合法合规的理财？ - 知乎', '2024-10-28 00:12:51.990910', '理财的话其实很多方式都可以，比如基金，黄金，股票，炒房。合不合规一是取决于你的理财时间。上班时间理财都是不合规。二是取决于是否涉嫌内幕，比如你所在行政区域有一两家a股上市企业，但你又非要频繁交易这几只股票。如果真查的话，你是说不清的。');
INSERT INTO `article` VALUES (32, 'https://www.ctax.org.cn/zt/learn20th/benshebaodao/xinwen/202301/t20230116_1127332.shtml', '中国税务网 - ctax.org.cn', '2024-10-08 00:12:51.994907', '由于高收入群体收入中财产性收入和资本性收入占较大比重，因此应逐步将财产性收入和资本性收入等非综合所得项目纳入综合所得的征收范围之中，这样做不仅有利于提高个人所得税对高收入群体的调节力度，还可以提升个人所得税的收入规模，改进个人所得 ...');
INSERT INTO `article` VALUES (33, 'https://zhuanlan.zhihu.com/p/689848192', '养老金并轨后，公务员如何理智规划财务？ - 知乎专栏', '2025-02-08 00:12:51.996912', '在养老金并轨政策实施后，公务员群体的养老福利模式发生了重大变化。这一改革意味着所有职业将按照统一的标准进行 养老保险 缴费和领取，从而结束了公务员过去依赖单位福利的特殊待遇。 这样的政策变动，无疑对公务员的个人财务规划提出了更高的要求。');
INSERT INTO `article` VALUES (34, 'https://book.douban.com/subject/3891587/', '北京居民理财指南 - 豆瓣读书', '2024-03-20 00:12:52.001629', '《北京居民理财指南》是一本针对北京居民理财类的实用工具书《北京居民理财指南》和大家见面了。 基于全球金融危机爆发，国内资本市场持续低迷，广大投资者损失惨重，特别需要了解理财知识，提高理财技能：同时，也是基于目前国内缺乏一本系统普及居民理财知识，提高居民理财水平 ...');
INSERT INTO `article` VALUES (35, 'https://zhuanlan.zhihu.com/p/26291915853', '2025有哪些适合高收入人群的税收优惠政策？ - 知乎专栏', '2024-12-07 00:12:52.005140', '到2025年，还是很多人对税务一窍不通，甚至个税申报扣除也是一知半解，多交的税从几千到几十万都有。 对高净值（收入）个人来说其实不需要太高的抗风险性，因为相较于企业，个人的历史遗留问题更多，但又没有一个可参考的税率去评判，只能在统计范畴上做问询，因此可操作的空间相对更大。');
INSERT INTO `article` VALUES (36, 'https://www.csai.cn/loan/1422075.html', '如何提高综合信用评分？做到这七点，不愁分数不提升 - 希财网', '2024-10-04 17:22:05.537413', '如何提高综合信用评分？要从\"信用分\"和\"综合分\"两方面下功夫，通常只要做到以下几点，就不愁分数不提升：还清逾期欠款、积累良好信用、优化信贷账户、控制申贷频率、定期检查征信、稳定工作收入、避免违法欠税。');
INSERT INTO `article` VALUES (37, 'https://www.hefeilaws.com/hf/505395.html', '银行贷款逾期了怎么办？最新处理办法一文看懂 - 合飞律师', '2024-12-27 18:13:38.000002', '银行贷款逾期处理的核心步骤与法律依据生活中难免遇到资金周转困难，导致银行贷款逾期，面对这种情况，如何合法合规应对，避免陷入更大危机？本文将结合法律规定与实操经验，为您解析关键处理办法，逾期后果：违约金与征信的双重压力银行通常会在贷款合同中明确逾期罚息和违约金的计算 ...');

-- ----------------------------
-- Table structure for article_userauth
-- ----------------------------
DROP TABLE IF EXISTS `article_userauth`;
CREATE TABLE `article_userauth`  (
  `article_id` int(11) NOT NULL,
  `userauth_id` int(11) NOT NULL,
  INDEX `article_id`(`article_id`) USING BTREE,
  INDEX `userauth_id`(`userauth_id`) USING BTREE,
  CONSTRAINT `article_userauth_ibfk_1` FOREIGN KEY (`article_id`) REFERENCES `article` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `article_userauth_ibfk_2` FOREIGN KEY (`userauth_id`) REFERENCES `userauth` (`index`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '推荐该文章的用户' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of article_userauth
-- ----------------------------

-- ----------------------------
-- Table structure for loan_record
-- ----------------------------
DROP TABLE IF EXISTS `loan_record`;
CREATE TABLE `loan_record`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `amount` decimal(10, 2) NOT NULL COMMENT '借款金额',
  `interest_rate` decimal(5, 2) NOT NULL COMMENT '年利率',
  `loan_term` int(11) NOT NULL COMMENT '贷款期限（以月为单位）',
  `status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'defaulted' COMMENT '贷款状态（如：active、completed、defaulted、overdue等）',
  `repayment_method` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '还款方式(等额本金/等额本息)',
  `repayment_amount` decimal(10, 2) NOT NULL DEFAULT 0.00 COMMENT '已还款金额',
  `repayment_schedule` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '还款计划（如每期还款金额、还款日期等）',
  `usage` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '借款用途',
  `bank_account` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '收款/还款银行账户',
  `created_at` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) COMMENT '贷款申请时间',
  `updated_at` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6) COMMENT '贷款信息更新时间',
  `user_id` int(11) NOT NULL COMMENT '关联的用户',
  `income` decimal(10, 2) NULL DEFAULT NULL COMMENT '申请人月收入',
  `credit_score` int(11) NULL DEFAULT NULL COMMENT '信用评分',
  `auditor` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '审核员',
  `audit_time` datetime NULL DEFAULT NULL COMMENT '审核时间',
  `remark` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '审核备注/拒绝原因',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_loan_record_user_id_5235c2`(`user_id`, `created_at`) USING BTREE,
  INDEX `idx_loan_record_auditor`(`auditor`) USING BTREE,
  INDEX `idx_loan_record_audit_time`(`audit_time`) USING BTREE,
  INDEX `idx_loan_record_status`(`status`) USING BTREE,
  CONSTRAINT `fk_loan_rec_userauth_b20ed31a` FOREIGN KEY (`user_id`) REFERENCES `userauth` (`index`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '贷款记录表：用于记录所有用户的借款信息' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of loan_record
-- ----------------------------
INSERT INTO `loan_record` VALUES (1, 1000.00, 0.05, 10, 'active', '等额本金', 0.00, '[{\"installment_number\": 1, \"amount_due\": 104.17, \"due_date\": \"2025-05-10\"}, {\"installment_number\": 2, \"amount_due\": 103.75, \"due_date\": \"2025-06-09\"}, {\"installment_number\": 3, \"amount_due\": 103.33, \"due_date\": \"2025-07-09\"}, {\"installment_number\": 4, \"amount_due\": 102.92, \"due_date\": \"2025-08-08\"}, {\"installment_number\": 5, \"amount_due\": 102.5, \"due_date\": \"2025-09-07\"}, {\"installment_number\": 6, \"amount_due\": 102.08, \"due_date\": \"2025-10-07\"}, {\"installment_number\": 7, \"amount_due\": 101.67, \"due_date\": \"2025-11-06\"}, {\"installment_number\": 8, \"amount_due\": 101.25, \"due_date\": \"2025-12-06\"}, {\"installment_number\": 9, \"amount_due\": 100.83, \"due_date\": \"2026-01-05\"}, {\"installment_number\": 10, \"amount_due\": 100.42, \"due_date\": \"2026-02-04\"}]', '生意周转', '16468979746466464', '2025-04-10 13:42:54.690481', '2025-06-27 22:32:13.167816', 13, 8000.00, 720, '系统审核', '2025-06-27 22:32:13', '初始化数据');
INSERT INTO `loan_record` VALUES (2, 1000.00, 0.05, 10, 'active', '等额本金', 0.00, '[{\"installment_number\": 1, \"amount_due\": 104.17, \"due_date\": \"2025-05-10\"}, {\"installment_number\": 2, \"amount_due\": 103.75, \"due_date\": \"2025-06-09\"}, {\"installment_number\": 3, \"amount_due\": 103.33, \"due_date\": \"2025-07-09\"}, {\"installment_number\": 4, \"amount_due\": 102.92, \"due_date\": \"2025-08-08\"}, {\"installment_number\": 5, \"amount_due\": 102.5, \"due_date\": \"2025-09-07\"}, {\"installment_number\": 6, \"amount_due\": 102.08, \"due_date\": \"2025-10-07\"}, {\"installment_number\": 7, \"amount_due\": 101.67, \"due_date\": \"2025-11-06\"}, {\"installment_number\": 8, \"amount_due\": 101.25, \"due_date\": \"2025-12-06\"}, {\"installment_number\": 9, \"amount_due\": 100.83, \"due_date\": \"2026-01-05\"}, {\"installment_number\": 10, \"amount_due\": 100.42, \"due_date\": \"2026-02-04\"}]', '生意周转', '16468979746466464', '2025-04-10 17:53:26.913602', '2025-06-27 22:32:13.167816', 13, 8000.00, 720, '系统审核', '2025-06-27 22:32:13', '初始化数据');
INSERT INTO `loan_record` VALUES (3, 10000.00, 0.05, 12, 'active', '等额本金', 0.00, '[{\"installment_number\": 1, \"amount_due\": 875.0, \"due_date\": \"2025-05-23\"}, {\"installment_number\": 2, \"amount_due\": 871.53, \"due_date\": \"2025-06-22\"}, {\"installment_number\": 3, \"amount_due\": 868.06, \"due_date\": \"2025-07-22\"}, {\"installment_number\": 4, \"amount_due\": 864.58, \"due_date\": \"2025-08-21\"}, {\"installment_number\": 5, \"amount_due\": 861.11, \"due_date\": \"2025-09-20\"}, {\"installment_number\": 6, \"amount_due\": 857.64, \"due_date\": \"2025-10-20\"}, {\"installment_number\": 7, \"amount_due\": 854.17, \"due_date\": \"2025-11-19\"}, {\"installment_number\": 8, \"amount_due\": 850.69, \"due_date\": \"2025-12-19\"}, {\"installment_number\": 9, \"amount_due\": 847.22, \"due_date\": \"2026-01-18\"}, {\"installment_number\": 10, \"amount_due\": 843.75, \"due_date\": \"2026-02-17\"}, {\"installment_number\": 11, \"amount_due\": 840.28, \"due_date\": \"2026-03-19\"}, {\"installment_number\": 12, \"amount_due\": 836.81, \"due_date\": \"2026-04-18\"}]', '生意周转', '16468979746466464', '2025-04-24 00:25:41.182574', '2025-06-27 22:32:13.167816', 13, 8000.00, 720, '系统审核', '2025-06-27 22:32:13', '初始化数据');
INSERT INTO `loan_record` VALUES (4, 1000.00, 0.05, 5, 'active', '等额本息', 0.00, '[{\"installment_number\": 1, \"amount_due\": 202.51, \"due_date\": \"2025-05-23\"}, {\"installment_number\": 2, \"amount_due\": 202.51, \"due_date\": \"2025-06-22\"}, {\"installment_number\": 3, \"amount_due\": 202.51, \"due_date\": \"2025-07-22\"}, {\"installment_number\": 4, \"amount_due\": 202.51, \"due_date\": \"2025-08-21\"}, {\"installment_number\": 5, \"amount_due\": 202.51, \"due_date\": \"2025-09-20\"}]', '个人支出', '16468979746466464', '2025-04-24 00:39:47.970324', '2025-06-27 22:32:13.167816', 13, 8000.00, 720, '系统审核', '2025-06-27 22:32:13', '初始化数据');

-- ----------------------------
-- Table structure for notification
-- ----------------------------
DROP TABLE IF EXISTS `notification`;
CREATE TABLE `notification`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '通知标题',
  `content` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '通知内容',
  `type` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '通知类型（如：系统通知、推文通知、公告提醒等）',
  `is_read` tinyint(1) NOT NULL DEFAULT 0 COMMENT '是否已读',
  `created_at` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) COMMENT '通知创建时间',
  `status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'sent' COMMENT '通知状态（如：sent、failed）',
  `target_user_id` int(11) NOT NULL COMMENT '接收通知的用户',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_notificatio_target__afa622`(`target_user_id`, `created_at`) USING BTREE,
  CONSTRAINT `fk_notifica_userauth_8c65edb3` FOREIGN KEY (`target_user_id`) REFERENCES `userauth` (`index`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '通知表：用于记录系统发送给用户的通知信息' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of notification
-- ----------------------------

-- ----------------------------
-- Table structure for rate
-- ----------------------------
DROP TABLE IF EXISTS `rate`;
CREATE TABLE `rate`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `interest_rate` decimal(5, 2) NOT NULL COMMENT '年利率',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '储存贷款利率' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of rate
-- ----------------------------

-- ----------------------------
-- Table structure for repayment_record
-- ----------------------------
DROP TABLE IF EXISTS `repayment_record`;
CREATE TABLE `repayment_record`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `amount` decimal(10, 2) NOT NULL COMMENT '还款金额',
  `repayment_date` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) COMMENT '还款时间',
  `status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'successful' COMMENT '还款状态（如：successful、failed、overdue等）',
  `message` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '还款结果的附加信息（如失败原因等）',
  `loan_id` int(11) NOT NULL COMMENT '关联的贷款记录',
  `user_id` int(11) NOT NULL COMMENT '关联的用户',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `fk_repaymen_userauth_76efc83e`(`user_id`) USING BTREE,
  INDEX `idx_repayment_r_loan_id_cecd88`(`loan_id`, `repayment_date`) USING BTREE,
  CONSTRAINT `fk_repaymen_loan_rec_0c685516` FOREIGN KEY (`loan_id`) REFERENCES `loan_record` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `fk_repaymen_userauth_76efc83e` FOREIGN KEY (`user_id`) REFERENCES `userauth` (`index`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '还款记录表：用于记录所有用户的还款信息' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of repayment_record
-- ----------------------------

-- ----------------------------
-- Table structure for review_applications
-- ----------------------------
DROP TABLE IF EXISTS `review_applications`;
CREATE TABLE `review_applications`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `original_audit_id` int(11) NOT NULL COMMENT '原始审核记录ID',
  `applicant_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '申请人姓名',
  `phone` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '联系电话',
  `id_card` varchar(18) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '身份证号',
  `loan_amount` decimal(10, 2) NOT NULL COMMENT '贷款金额',
  `loan_purpose` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '贷款用途',
  `original_result` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '原审核结果',
  `original_reason` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '原拒绝原因',
  `original_auditor` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '原审核员',
  `original_audit_time` datetime(6) NOT NULL COMMENT '原审核时间',
  `review_reason` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '复审理由',
  `review_apply_time` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) COMMENT '复审申请时间',
  `status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'review_pending' COMMENT '复审状态',
  `priority` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'medium' COMMENT '优先级',
  `additional_docs` json NOT NULL COMMENT '补充材料文件名列表',
  `review_auditor` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '复审员',
  `review_time` datetime(6) NULL DEFAULT NULL COMMENT '复审时间',
  `review_result` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '复审结果',
  `review_comment` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '复审意见',
  `created_at` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) COMMENT '创建时间',
  `updated_at` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6) COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_review_appl_status_f75175`(`status`) USING BTREE,
  INDEX `idx_review_appl_priorit_37e47b`(`priority`) USING BTREE,
  INDEX `idx_review_appl_origina_d36e8d`(`original_audit_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 10 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '复审申请模型' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of review_applications
-- ----------------------------
INSERT INTO `review_applications` VALUES (1, 1001, '张三', '13800138001', '110101199001011234', 50000.00, '创业资金', 'rejected', '信用评分不足，月收入偏低', '审核员A', '2024-01-15 09:30:00.000000', '提供了新的收入证明和银行流水，信用状况有所改善', '2025-06-27 22:23:43.926180', 'review_approved', 'high', '[\"新收入证明.pdf\", \"银行流水.pdf\"]', '当前审核员', '2025-06-27 23:07:22.427783', 'approved', '111111111111', '2025-06-27 22:23:43.926180', '2025-06-27 23:07:22.427783');
INSERT INTO `review_applications` VALUES (2, 1002, '李四', '13800138002', '110101199002022345', 80000.00, '房屋装修', 'rejected', '负债比例过高，还款能力不足', '审核员B', '2024-01-20 14:20:00.000000', '已结清部分债务，负债比例降低，提供清债证明', '2025-06-27 22:23:43.926180', 'review_approved', 'medium', '[\"清债证明.pdf\", \"更新征信报告.pdf\"]', '当前审核员', '2025-06-27 23:07:49.942476', 'approved', 'qqqqqqqqqqqqq', '2025-06-27 22:23:43.926180', '2025-06-27 23:07:49.942476');
INSERT INTO `review_applications` VALUES (3, 1003, '王五', '13800138003', '110101199003033456', 30000.00, '医疗费用', 'rejected', '工作不稳定，收入来源单一', '审核员C', '2024-01-25 11:15:00.000000', '已签订正式劳动合同，工作稳定，申请紧急医疗贷款', '2025-06-27 22:23:43.926180', 'review_approved', 'urgent', '[\"劳动合同.pdf\", \"医院诊断书.pdf\"]', '当前审核员', '2025-06-27 23:07:49.948907', 'approved', 'qqqqqqqqqqqqq', '2025-06-27 22:23:43.926180', '2025-06-27 23:07:49.949905');
INSERT INTO `review_applications` VALUES (4, 1004, '赵六', '13800138004', '110101199004044567', 100000.00, '购车', 'rejected', '贷款用途不明确，风险较高', '审核员A', '2024-01-10 16:45:00.000000', '提供详细购车计划和合同，用途明确', '2025-06-27 22:23:43.926180', 'review_approved', 'medium', '[\"购车合同.pdf\", \"车辆报价单.pdf\"]', '复审员甲', '2024-01-28 10:30:00.000000', 'approved', '经复审，申请人提供了详细的购车计划，用途明确，同意放款', '2025-06-27 22:23:43.926180', '2025-06-27 22:23:43.926180');
INSERT INTO `review_applications` VALUES (5, 1005, '钱七', '13800138005', '110101199005055678', 25000.00, '教育培训', 'rejected', '还款计划不合理', '审核员B', '2024-01-12 13:20:00.000000', '重新制定了还款计划，更加合理可行', '2025-06-27 22:23:43.926180', 'review_rejected', 'low', '[\"新还款计划.pdf\"]', '复审员乙', '2024-01-27 15:45:00.000000', 'rejected', '经复审，申请人虽然提供了新的还款计划，但综合风险评估仍然偏高，维持原决定', '2025-06-27 22:23:43.926180', '2025-06-27 22:23:43.926180');
INSERT INTO `review_applications` VALUES (6, 1006, '孙八', '13800138006', '110101199006066789', 60000.00, '经营周转', 'rejected', '经营状况不佳，现金流不稳定', '审核员C', '2024-01-18 09:00:00.000000', '经营状况好转，提供最新财务报表', '2025-06-27 22:23:43.926180', 'review_approved', 'high', '[\"最新财务报表.pdf\", \"经营许可证.pdf\"]', '复审员甲', '2024-01-30 14:20:00.000000', 'approved', '经复审，申请人经营状况确实有所好转，现金流改善，同意放款', '2025-06-27 22:23:43.926180', '2025-06-27 22:23:43.926180');
INSERT INTO `review_applications` VALUES (7, 1007, '周九', '13800138007', '110101199007077890', 40000.00, '债务整合', 'rejected', '多头借贷，风险过高', '审核员A', '2024-02-01 10:15:00.000000', '已部分结清其他贷款，降低多头借贷风险', '2025-06-27 22:23:43.926180', 'review_approved', 'medium', '[\"部分结清证明.pdf\", \"征信更新报告.pdf\"]', '当前审核员', '2025-06-27 23:07:49.956416', 'approved', 'qqqqqqqqqqqqq', '2025-06-27 22:23:43.926180', '2025-06-27 23:07:49.956416');
INSERT INTO `review_applications` VALUES (8, 1008, '吴十', '13800138008', '110101199008088901', 70000.00, '投资理财', 'rejected', '投资用途风险较大', '审核员B', '2024-02-03 16:30:00.000000', '修改贷款用途为稳健投资，提供详细投资计划', '2025-06-27 22:23:43.926180', 'review_approved', 'low', '[\"投资计划书.pdf\", \"风险评估报告.pdf\"]', '当前审核员', '2025-06-27 23:07:49.961617', 'approved', 'qqqqqqqqqqqqq', '2025-06-27 22:23:43.926180', '2025-06-27 23:07:49.961617');
INSERT INTO `review_applications` VALUES (9, 1009, '郑十一', '13800138009', '110101199009099012', 35000.00, '紧急资金', 'rejected', '用途不够明确，缺乏支撑材料', '审核员C', '2024-02-05 11:45:00.000000', '家庭突发疾病，需要紧急医疗资金，已提供医院证明', '2025-06-27 22:23:43.926180', 'review_approved', 'urgent', '[\"医院诊断证明.pdf\", \"医疗费用预算.pdf\"]', '当前审核员', '2025-06-27 23:07:49.965617', 'approved', 'qqqqqqqqqqqqq', '2025-06-27 22:23:43.926180', '2025-06-27 23:07:49.965617');

-- ----------------------------
-- Table structure for user_application
-- ----------------------------
DROP TABLE IF EXISTS `user_application`;
CREATE TABLE `user_application`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `real_name_verified` tinyint(1) NOT NULL DEFAULT 0 COMMENT '用户实名制是否通过核实',
  `age` int(11) NULL DEFAULT NULL COMMENT '用户年龄',
  `is_student` tinyint(1) NOT NULL DEFAULT 0 COMMENT '是否大学生客户',
  `is_blacklisted` tinyint(1) NOT NULL DEFAULT 0 COMMENT '是否黑名单客户',
  `is_unhealthy_4g_user` tinyint(1) NOT NULL DEFAULT 0 COMMENT '是否4G不健康客户',
  `network_age_months` int(11) NULL DEFAULT NULL COMMENT '用户网龄（月）',
  `last_payment_months_ago` int(11) NULL DEFAULT NULL COMMENT '用户最近一次缴费距今时长（月）',
  `last_payment_amount` double NULL DEFAULT NULL COMMENT '最近一次缴费金额（元）',
  `avg_monthly_spending_6_months` double NULL DEFAULT NULL COMMENT '用户近6个月平均消费值（元）',
  `current_bill_total` double NULL DEFAULT NULL COMMENT '用户账单当月总费用（元）',
  `current_account_balance` double NULL DEFAULT NULL COMMENT '用户当月账户余额（元）',
  `has_outstanding_payment` tinyint(1) NOT NULL DEFAULT 0 COMMENT '当前是否欠费缴费',
  `call_fee_sensitivity` int(11) NULL DEFAULT NULL COMMENT '用户话费敏感度',
  `contacts_this_month` int(11) NULL DEFAULT NULL COMMENT '当月通话交往圈人数',
  `is_frequent_mall_visitor` tinyint(1) NOT NULL DEFAULT 0 COMMENT '是否经常逛商场的人',
  `avg_mall_visits_3_months` int(11) NULL DEFAULT NULL COMMENT '近三个月月均商场出现次数',
  `visited_fuzhou_cangshan_wanda` tinyint(1) NOT NULL DEFAULT 0 COMMENT '当月是否逛过福州仓山万达',
  `visited_fuzhou_sam_club` tinyint(1) NOT NULL DEFAULT 0 COMMENT '当月是否到过福州山姆会员店',
  `watched_movie` tinyint(1) NOT NULL DEFAULT 0 COMMENT '当月是否看电影',
  `visited_scenic_spot` tinyint(1) NOT NULL DEFAULT 0 COMMENT '当月是否景点游览',
  `used_sports_facility` tinyint(1) NOT NULL DEFAULT 0 COMMENT '当月是否体育场馆消费',
  `online_shopping_app_usage` int(11) NULL DEFAULT NULL COMMENT '当月网购类应用使用次数',
  `logistics_app_usage` int(11) NULL DEFAULT NULL COMMENT '当月物流快递类应用使用次数',
  `finance_app_usage` int(11) NULL DEFAULT NULL COMMENT '当月金融理财类应用使用总次数',
  `video_app_usage` int(11) NULL DEFAULT NULL COMMENT '当月视频播放类应用使用次数',
  `airplane_app_usage` int(11) NULL DEFAULT NULL COMMENT '当月飞机类应用使用次数',
  `train_app_usage` int(11) NULL DEFAULT NULL COMMENT '当月火车类应用使用次数',
  `travel_info_app_usage` int(11) NULL DEFAULT NULL COMMENT '当月旅游资讯类应用使用次数',
  `credit_score` double NULL DEFAULT NULL COMMENT '用户信用分',
  `created_at` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) COMMENT '记录创建时间',
  `updated_at` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6) COMMENT '记录更新时间',
  `user_id` int(11) NOT NULL COMMENT '关联的用户',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_user_applic_user_id_83c45c`(`user_id`) USING BTREE,
  CONSTRAINT `fk_user_app_userauth_834fe576` FOREIGN KEY (`user_id`) REFERENCES `userauth` (`index`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 29 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = 'A卡评分卡所需信息' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of user_application
-- ----------------------------
INSERT INTO `user_application` VALUES (1, 0, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2025-03-17 19:51:29.816222', '2025-03-17 19:51:29.816222', 1);
INSERT INTO `user_application` VALUES (2, 0, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2025-03-20 20:39:53.826669', '2025-03-20 20:39:53.826669', 2);
INSERT INTO `user_application` VALUES (3, 0, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2025-03-20 20:41:32.765454', '2025-03-20 20:41:32.765454', 3);
INSERT INTO `user_application` VALUES (4, 0, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2025-04-02 17:12:19.689022', '2025-04-02 17:12:19.689022', 4);
INSERT INTO `user_application` VALUES (5, 0, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2025-04-02 17:15:48.029317', '2025-04-02 17:15:48.029317', 5);
INSERT INTO `user_application` VALUES (6, 0, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2025-04-02 17:17:51.398902', '2025-04-02 17:17:51.398902', 6);
INSERT INTO `user_application` VALUES (7, 0, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2025-04-02 17:20:15.456223', '2025-04-02 17:20:15.456223', 7);
INSERT INTO `user_application` VALUES (8, 0, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2025-04-02 17:21:30.469506', '2025-04-02 17:21:30.469506', 8);
INSERT INTO `user_application` VALUES (9, 0, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2025-04-02 17:23:19.208651', '2025-04-02 17:23:19.208651', 9);
INSERT INTO `user_application` VALUES (10, 0, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2025-04-02 17:26:38.130684', '2025-04-02 17:26:38.130684', 10);
INSERT INTO `user_application` VALUES (11, 0, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2025-04-02 17:28:37.526661', '2025-04-02 17:28:37.526661', 11);
INSERT INTO `user_application` VALUES (12, 0, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2025-04-10 13:05:47.537463', '2025-04-10 13:05:47.537463', 12);
INSERT INTO `user_application` VALUES (13, 0, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2025-04-10 13:14:05.646480', '2025-04-10 13:14:05.646480', 13);
INSERT INTO `user_application` VALUES (14, 0, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2025-04-10 17:05:25.871718', '2025-04-10 17:05:25.871744', 14);
INSERT INTO `user_application` VALUES (15, 0, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2025-05-07 18:39:14.134422', '2025-05-07 18:39:14.134422', 15);
INSERT INTO `user_application` VALUES (16, 0, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2025-05-07 19:23:03.023844', '2025-05-07 19:23:03.024842', 16);
INSERT INTO `user_application` VALUES (17, 0, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2025-05-07 19:24:49.314063', '2025-05-07 19:24:49.314063', 17);
INSERT INTO `user_application` VALUES (18, 0, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2025-05-07 19:27:51.169469', '2025-05-07 19:27:51.169469', 18);
INSERT INTO `user_application` VALUES (19, 0, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2025-05-07 19:28:20.364997', '2025-05-07 19:28:20.364997', 19);
INSERT INTO `user_application` VALUES (20, 0, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2025-05-07 19:29:30.359379', '2025-05-07 19:29:30.359379', 20);
INSERT INTO `user_application` VALUES (21, 0, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2025-05-07 19:30:00.833999', '2025-05-07 19:30:00.833999', 21);
INSERT INTO `user_application` VALUES (22, 0, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2025-05-07 19:30:48.195215', '2025-05-07 19:30:48.196417', 22);
INSERT INTO `user_application` VALUES (23, 0, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2025-05-07 19:32:25.951052', '2025-05-07 19:32:25.951052', 23);
INSERT INTO `user_application` VALUES (24, 0, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2025-05-07 19:35:56.641532', '2025-05-07 19:35:56.641532', 24);
INSERT INTO `user_application` VALUES (25, 0, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2025-05-07 19:38:45.654641', '2025-05-07 19:38:45.654641', 25);
INSERT INTO `user_application` VALUES (26, 0, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2025-05-07 19:42:24.918750', '2025-05-07 19:42:24.918750', 26);
INSERT INTO `user_application` VALUES (27, 0, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2025-05-07 19:45:18.456886', '2025-05-07 19:45:18.456886', 27);
INSERT INTO `user_application` VALUES (28, 0, NULL, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 0, NULL, 0, 0, 0, 0, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2025-06-27 00:03:21.351192', '2025-06-27 00:03:21.351192', 28);

-- ----------------------------
-- Table structure for user_behavior
-- ----------------------------
DROP TABLE IF EXISTS `user_behavior`;
CREATE TABLE `user_behavior`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `age` int(11) NULL DEFAULT NULL COMMENT '用户年龄',
  `bank_cards_count` int(11) NULL DEFAULT NULL COMMENT '全国股份制商业银行卡片数',
  `remote_transaction_months` int(11) NULL DEFAULT NULL COMMENT '近6个月有异地交易的月份数',
  `internet_transaction_avg` double NULL DEFAULT NULL COMMENT '近6个月互联网交易笔数均值',
  `financial_transaction_months` int(11) NULL DEFAULT NULL COMMENT '近6个月有金融类交易的月份数',
  `financial_transaction_avg_amount` double NULL DEFAULT NULL COMMENT '近6个月金融类交易额均值',
  `max_loan_amount_180_days` double NULL DEFAULT NULL COMMENT '180天内单笔放款金额最大值',
  `min_loan_amount_180_days` double NULL DEFAULT NULL COMMENT '180天内单笔放款金额最小值',
  `apply_loan_company_number` int(11) NULL DEFAULT NULL COMMENT '申请贷款机构数',
  `created_at` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) COMMENT '记录创建时间',
  `updated_at` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6) COMMENT '记录更新时间',
  `user_id` int(11) NOT NULL COMMENT '关联的用户',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_user_behavi_user_id_2d3c82`(`user_id`) USING BTREE,
  CONSTRAINT `fk_user_beh_userauth_5af75cb1` FOREIGN KEY (`user_id`) REFERENCES `userauth` (`index`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 29 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = 'B卡评分卡所需信息' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of user_behavior
-- ----------------------------
INSERT INTO `user_behavior` VALUES (1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2025-03-17 19:51:29.826279', '2025-03-17 19:51:29.826279', 1);
INSERT INTO `user_behavior` VALUES (2, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2025-03-20 20:39:53.830732', '2025-03-20 20:39:53.831821', 2);
INSERT INTO `user_behavior` VALUES (3, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2025-03-20 20:41:32.767389', '2025-03-20 20:41:32.767389', 3);
INSERT INTO `user_behavior` VALUES (4, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2025-04-02 17:12:19.694209', '2025-04-02 17:12:19.694209', 4);
INSERT INTO `user_behavior` VALUES (5, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2025-04-02 17:15:48.032847', '2025-04-02 17:15:48.032847', 5);
INSERT INTO `user_behavior` VALUES (6, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2025-04-02 17:17:51.400002', '2025-04-02 17:17:51.400002', 6);
INSERT INTO `user_behavior` VALUES (7, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2025-04-02 17:20:15.457668', '2025-04-02 17:20:15.457668', 7);
INSERT INTO `user_behavior` VALUES (8, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2025-04-02 17:21:30.473112', '2025-04-02 17:21:30.473112', 8);
INSERT INTO `user_behavior` VALUES (9, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2025-04-02 17:23:19.210222', '2025-04-02 17:23:19.210222', 9);
INSERT INTO `user_behavior` VALUES (10, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2025-04-02 17:26:38.136671', '2025-04-02 17:26:38.136671', 10);
INSERT INTO `user_behavior` VALUES (11, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2025-04-02 17:28:37.527706', '2025-04-02 17:28:37.527706', 11);
INSERT INTO `user_behavior` VALUES (12, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2025-04-10 13:05:47.537463', '2025-04-10 13:05:47.537463', 12);
INSERT INTO `user_behavior` VALUES (13, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2025-04-10 13:14:05.648271', '2025-04-10 13:14:05.648271', 13);
INSERT INTO `user_behavior` VALUES (14, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2025-04-10 17:05:25.876779', '2025-04-10 17:05:25.876816', 14);
INSERT INTO `user_behavior` VALUES (15, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2025-05-07 18:39:14.136421', '2025-05-07 18:39:14.136421', 15);
INSERT INTO `user_behavior` VALUES (16, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2025-05-07 19:23:03.025843', '2025-05-07 19:23:03.025843', 16);
INSERT INTO `user_behavior` VALUES (17, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2025-05-07 19:24:49.316062', '2025-05-07 19:24:49.316062', 17);
INSERT INTO `user_behavior` VALUES (18, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2025-05-07 19:27:51.171470', '2025-05-07 19:27:51.171470', 18);
INSERT INTO `user_behavior` VALUES (19, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2025-05-07 19:28:20.367622', '2025-05-07 19:28:20.367622', 19);
INSERT INTO `user_behavior` VALUES (20, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2025-05-07 19:29:30.364889', '2025-05-07 19:29:30.364889', 20);
INSERT INTO `user_behavior` VALUES (21, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2025-05-07 19:30:00.837978', '2025-05-07 19:30:00.837978', 21);
INSERT INTO `user_behavior` VALUES (22, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2025-05-07 19:30:48.202441', '2025-05-07 19:30:48.202441', 22);
INSERT INTO `user_behavior` VALUES (23, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2025-05-07 19:32:25.957425', '2025-05-07 19:32:25.957425', 23);
INSERT INTO `user_behavior` VALUES (24, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2025-05-07 19:35:56.647535', '2025-05-07 19:35:56.647535', 24);
INSERT INTO `user_behavior` VALUES (25, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2025-05-07 19:38:45.657642', '2025-05-07 19:38:45.657642', 25);
INSERT INTO `user_behavior` VALUES (26, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2025-05-07 19:42:24.933377', '2025-05-07 19:42:24.933377', 26);
INSERT INTO `user_behavior` VALUES (27, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2025-05-07 19:45:18.460023', '2025-05-07 19:45:18.460023', 27);
INSERT INTO `user_behavior` VALUES (28, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2025-06-27 00:03:21.355191', '2025-06-27 00:03:21.355191', 28);

-- ----------------------------
-- Table structure for user_login_log
-- ----------------------------
DROP TABLE IF EXISTS `user_login_log`;
CREATE TABLE `user_login_log`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '用户操作类型, 登录/登出',
  `ip_address` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT 'IP地址（IPv4或IPv6）',
  `user_agent` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '用户设备信息（浏览器、操作系统等）',
  `success` tinyint(1) NOT NULL DEFAULT 1 COMMENT '操作是否成功',
  `message` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '额外的操作结果信息或错误消息',
  `created_at` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) COMMENT '操作发生的时间',
  `user_id` int(11) NOT NULL COMMENT '关联的用户',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_user_login__user_id_890a2a`(`user_id`, `action`) USING BTREE,
  CONSTRAINT `fk_user_log_userauth_89fc15b2` FOREIGN KEY (`user_id`) REFERENCES `userauth` (`index`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 70 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '用户登录日志表：记录用户的登录、登出操作' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of user_login_log
-- ----------------------------
INSERT INTO `user_login_log` VALUES (1, 'register', '', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0', 1, NULL, '2025-03-17 19:51:32.074669', 1);
INSERT INTO `user_login_log` VALUES (2, 'login', '', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0', 1, NULL, '2025-03-17 23:24:09.898414', 1);
INSERT INTO `user_login_log` VALUES (3, 'login', '', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0', 1, NULL, '2025-03-20 19:13:06.817676', 1);
INSERT INTO `user_login_log` VALUES (4, 'register', '', 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1 Edg/134.0.0.0', 1, NULL, '2025-03-20 20:40:33.501142', 2);
INSERT INTO `user_login_log` VALUES (5, 'register', '', 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1 Edg/134.0.0.0', 1, NULL, '2025-03-20 20:42:12.527900', 3);
INSERT INTO `user_login_log` VALUES (6, 'login', '', 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1 Edg/134.0.0.0', 1, NULL, '2025-03-20 20:42:25.905258', 3);
INSERT INTO `user_login_log` VALUES (7, 'login', '', 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1 Edg/134.0.0.0', 1, NULL, '2025-03-20 20:44:28.422199', 3);
INSERT INTO `user_login_log` VALUES (8, 'login', '', 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1 Edg/134.0.0.0', 1, NULL, '2025-03-20 20:51:04.784711', 1);
INSERT INTO `user_login_log` VALUES (9, 'login', '', 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1 Edg/134.0.0.0', 1, NULL, '2025-03-27 19:12:20.709201', 1);
INSERT INTO `user_login_log` VALUES (10, 'register', '', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0', 1, NULL, '2025-04-02 17:12:56.830593', 4);
INSERT INTO `user_login_log` VALUES (11, 'register', '', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0', 1, NULL, '2025-04-02 17:20:51.160852', 7);
INSERT INTO `user_login_log` VALUES (12, 'register', '', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0', 1, NULL, '2025-04-02 17:22:05.524368', 8);
INSERT INTO `user_login_log` VALUES (13, 'register', '', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0', 1, NULL, '2025-04-02 17:23:53.868478', 9);
INSERT INTO `user_login_log` VALUES (14, 'register', '', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0', 1, NULL, '2025-04-02 17:28:39.544536', 11);
INSERT INTO `user_login_log` VALUES (15, 'login', '', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0', 1, NULL, '2025-04-02 17:35:02.729783', 1);
INSERT INTO `user_login_log` VALUES (16, 'login', '', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0', 1, NULL, '2025-04-02 18:09:09.144785', 1);
INSERT INTO `user_login_log` VALUES (17, 'login', '', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0', 1, NULL, '2025-04-03 19:10:02.931766', 1);
INSERT INTO `user_login_log` VALUES (18, 'register', '', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36', 1, NULL, '2025-04-10 13:05:49.567641', 12);
INSERT INTO `user_login_log` VALUES (19, 'login', '', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36', 1, NULL, '2025-04-10 13:09:29.263951', 12);
INSERT INTO `user_login_log` VALUES (20, 'register', '', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36', 1, NULL, '2025-04-10 13:14:07.667224', 13);
INSERT INTO `user_login_log` VALUES (21, 'login', '', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36', 1, NULL, '2025-04-10 13:14:45.648342', 13);
INSERT INTO `user_login_log` VALUES (22, 'login', '', 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1 HBuilderX', 1, NULL, '2025-04-10 13:26:48.680697', 13);
INSERT INTO `user_login_log` VALUES (23, 'login', '', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0', 1, NULL, '2025-04-10 16:24:10.652134', 13);
INSERT INTO `user_login_log` VALUES (24, 'login', '', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0', 1, NULL, '2025-04-10 16:25:48.608035', 13);
INSERT INTO `user_login_log` VALUES (25, 'login', '', 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1 Edg/135.0.0.0', 1, NULL, '2025-04-10 16:30:27.087688', 13);
INSERT INTO `user_login_log` VALUES (26, 'login', '', 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1 Edg/135.0.0.0', 1, NULL, '2025-04-10 16:49:35.995011', 13);
INSERT INTO `user_login_log` VALUES (27, 'register', '', 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1 Edg/135.0.0.0', 1, NULL, '2025-04-10 17:05:25.885313', 14);
INSERT INTO `user_login_log` VALUES (28, 'login', '', 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1 Edg/135.0.0.0', 1, NULL, '2025-04-10 17:05:33.777962', 14);
INSERT INTO `user_login_log` VALUES (29, 'login', '', 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1 Edg/135.0.0.0', 1, NULL, '2025-04-10 17:47:22.697965', 14);
INSERT INTO `user_login_log` VALUES (30, 'login', '', 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1 Edg/135.0.0.0', 1, NULL, '2025-04-10 17:47:46.336449', 13);
INSERT INTO `user_login_log` VALUES (31, 'login', '', 'Mozilla/5.0 (Linux; Android 14; PHP110 Build/UKQ1.230924.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/132.0.6834.163 Mobile Safari/537.36 uni-app Html5Plus/1.0 (Immersed/31.428572)', 1, NULL, '2025-04-10 18:07:38.270239', 13);
INSERT INTO `user_login_log` VALUES (32, 'login', '', 'Mozilla/5.0 (Linux; Android 14; PHP110 Build/UKQ1.230924.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/132.0.6834.163 Mobile Safari/537.36 uni-app Html5Plus/1.0 (Immersed/31.428572)', 1, NULL, '2025-04-10 18:11:07.320063', 13);
INSERT INTO `user_login_log` VALUES (33, 'login', '', 'Mozilla/5.0 (Linux; Android 14; PHP110 Build/UKQ1.230924.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/132.0.6834.163 Mobile Safari/537.36 uni-app Html5Plus/1.0 (Immersed/31.428572)', 1, NULL, '2025-04-10 18:14:26.604722', 13);
INSERT INTO `user_login_log` VALUES (34, 'login', '', 'Mozilla/5.0 (Linux; Android 14; PHP110 Build/UKQ1.230924.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/132.0.6834.163 Mobile Safari/537.36 uni-app Html5Plus/1.0 (Immersed/31.428572)', 1, NULL, '2025-04-10 18:15:39.888470', 13);
INSERT INTO `user_login_log` VALUES (35, 'login', '', 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1 HBuilderX', 1, NULL, '2025-04-23 15:14:27.507645', 13);
INSERT INTO `user_login_log` VALUES (36, 'login', '', 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1 Edg/135.0.0.0', 1, NULL, '2025-04-23 15:15:09.278891', 13);
INSERT INTO `user_login_log` VALUES (37, 'login', '', 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1 Edg/135.0.0.0', 1, NULL, '2025-04-23 15:29:53.393951', 13);
INSERT INTO `user_login_log` VALUES (38, 'login', '', 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1 Edg/135.0.0.0', 1, NULL, '2025-04-23 15:47:39.181776', 13);
INSERT INTO `user_login_log` VALUES (39, 'login', '', 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1 Edg/135.0.0.0', 1, NULL, '2025-04-23 15:52:49.444691', 13);
INSERT INTO `user_login_log` VALUES (40, 'login', '', 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1 Edg/135.0.0.0', 1, NULL, '2025-04-23 15:54:07.953421', 13);
INSERT INTO `user_login_log` VALUES (41, 'login', '', 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1 Edg/135.0.0.0', 1, NULL, '2025-04-23 15:55:46.398378', 13);
INSERT INTO `user_login_log` VALUES (42, 'login', '', 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1 Edg/135.0.0.0', 1, NULL, '2025-04-23 16:29:28.289399', 13);
INSERT INTO `user_login_log` VALUES (43, 'login', '', 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1 Edg/135.0.0.0', 1, NULL, '2025-04-23 16:35:46.522669', 13);
INSERT INTO `user_login_log` VALUES (44, 'login', '', 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1 Edg/135.0.0.0', 1, NULL, '2025-04-23 17:05:43.348600', 13);
INSERT INTO `user_login_log` VALUES (45, 'login', '', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0', 1, NULL, '2025-04-23 17:08:06.667207', 13);
INSERT INTO `user_login_log` VALUES (46, 'login', '', 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1', 1, NULL, '2025-04-24 00:23:25.511622', 13);
INSERT INTO `user_login_log` VALUES (47, 'login', '', 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1 Edg/135.0.0.0', 1, NULL, '2025-04-24 00:33:25.042399', 13);
INSERT INTO `user_login_log` VALUES (48, 'register', '', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0', 1, NULL, '2025-05-07 18:39:16.208522', 15);
INSERT INTO `user_login_log` VALUES (49, 'register', '', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0', 1, NULL, '2025-05-07 19:23:05.066354', 16);
INSERT INTO `user_login_log` VALUES (50, 'register', '', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0', 1, NULL, '2025-05-07 19:27:53.213494', 18);
INSERT INTO `user_login_log` VALUES (51, 'register', '', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0', 1, NULL, '2025-05-07 19:28:22.407266', 19);
INSERT INTO `user_login_log` VALUES (52, 'register', '', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0', 1, NULL, '2025-05-07 19:29:54.388779', 20);
INSERT INTO `user_login_log` VALUES (53, 'register', '', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0', 1, NULL, '2025-05-07 19:37:18.355329', 24);
INSERT INTO `user_login_log` VALUES (54, 'register', '', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0', 1, NULL, '2025-05-07 19:44:24.652012', 26);
INSERT INTO `user_login_log` VALUES (55, 'register', '', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0', 1, NULL, '2025-05-07 19:45:54.487447', 27);
INSERT INTO `user_login_log` VALUES (56, 'register', '', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0', 1, NULL, '2025-06-27 00:03:23.434068', 28);
INSERT INTO `user_login_log` VALUES (57, 'login', '', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0', 1, NULL, '2025-06-27 00:04:56.522706', 28);
INSERT INTO `user_login_log` VALUES (58, 'login', '', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0', 1, NULL, '2025-06-27 00:36:42.729170', 28);
INSERT INTO `user_login_log` VALUES (59, 'login', '', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0', 1, NULL, '2025-06-27 17:10:55.826620', 28);
INSERT INTO `user_login_log` VALUES (60, 'login', '', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0', 1, NULL, '2025-06-27 17:48:40.085601', 28);
INSERT INTO `user_login_log` VALUES (61, 'login', '', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0', 1, NULL, '2025-06-27 18:45:39.681953', 28);
INSERT INTO `user_login_log` VALUES (62, 'login', '', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0', 1, NULL, '2025-06-27 18:54:31.568959', 28);
INSERT INTO `user_login_log` VALUES (63, 'login', '', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0', 1, NULL, '2025-06-28 00:03:05.371503', 28);
INSERT INTO `user_login_log` VALUES (64, 'login', '', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0', 1, NULL, '2025-06-28 01:13:41.731480', 28);
INSERT INTO `user_login_log` VALUES (65, 'login', '', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0', 1, NULL, '2025-06-28 01:18:09.012134', 28);
INSERT INTO `user_login_log` VALUES (66, 'login', '', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0', 1, NULL, '2025-06-28 01:26:03.775163', 28);
INSERT INTO `user_login_log` VALUES (67, 'login', '', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0', 1, NULL, '2025-06-28 14:46:49.349531', 28);
INSERT INTO `user_login_log` VALUES (68, 'login', '', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0', 1, NULL, '2025-06-28 16:29:41.159637', 28);
INSERT INTO `user_login_log` VALUES (69, 'login', '', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0', 1, NULL, '2025-06-28 17:08:16.330022', 28);

-- ----------------------------
-- Table structure for user_profile
-- ----------------------------
DROP TABLE IF EXISTS `user_profile`;
CREATE TABLE `user_profile`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '唯一用户名',
  `full_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '姓名',
  `phone_number` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '电话号码',
  `gender` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '性别',
  `id_card_number` varchar(18) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '身份证号',
  `id_card_expiry` date NULL DEFAULT NULL COMMENT '身份证有效期',
  `bank_account` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '银行卡号',
  `profession` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '职业类别',
  `address` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '住址',
  `date_of_birth` date NULL DEFAULT NULL COMMENT '出生年月',
  `student_verified` tinyint(1) NOT NULL DEFAULT 0 COMMENT '学信网认证，学生专属',
  `profile_picture` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '头像URL',
  `income` decimal(10, 2) NULL DEFAULT NULL COMMENT '月收入',
  `max_amount` decimal(10, 2) NOT NULL DEFAULT 10000.00 COMMENT '最大借款额度',
  `credit` decimal(10, 2) NOT NULL DEFAULT 100.00 COMMENT '信用分数',
  `loaned_amount` decimal(10, 2) NOT NULL DEFAULT 0.00 COMMENT '已经贷款金额',
  `is_profile_completed` tinyint(1) NOT NULL DEFAULT 0 COMMENT '是否已经完善个人信息',
  `created_at` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) COMMENT '记录创建时间',
  `updated_at` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6) COMMENT '记录更新时间',
  `user_id` int(11) NOT NULL COMMENT '关联的用户账户',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `username`(`username`) USING BTREE,
  UNIQUE INDEX `user_id`(`user_id`) USING BTREE,
  UNIQUE INDEX `id_card_number`(`id_card_number`) USING BTREE,
  INDEX `idx_user_profil_user_id_e3ff7c`(`user_id`) USING BTREE,
  CONSTRAINT `fk_user_pro_userauth_441faeaa` FOREIGN KEY (`user_id`) REFERENCES `userauth` (`index`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 29 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '用户基本个人信息表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of user_profile
-- ----------------------------
INSERT INTO `user_profile` VALUES (1, 'test', NULL, 'string', 'male', NULL, NULL, '6163897193034243', 'qqq', 'adsa', '2024-11-18', 0, 'string', 15000.00, 10000.00, 430.00, 0.00, 0, '2025-03-17 19:51:29.816222', '2025-04-03 19:10:43.596344', 1);
INSERT INTO `user_profile` VALUES (2, 'test1', NULL, '123', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 10000.00, 100.00, 0.00, 0, '2025-03-20 20:39:53.820929', '2025-03-20 20:39:53.820929', 2);
INSERT INTO `user_profile` VALUES (3, 'test24', NULL, '111', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 10000.00, 100.00, 0.00, 0, '2025-03-20 20:41:32.763050', '2025-03-20 20:41:32.763050', 3);
INSERT INTO `user_profile` VALUES (4, 'test123', NULL, '15355546669', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 10000.00, 100.00, 0.00, 0, '2025-04-02 17:12:19.685591', '2025-04-02 17:12:19.685591', 4);
INSERT INTO `user_profile` VALUES (5, 'test13', NULL, '15358546669', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 10000.00, 100.00, 0.00, 0, '2025-04-02 17:15:48.025299', '2025-04-02 17:15:48.025299', 5);
INSERT INTO `user_profile` VALUES (6, 'test1ewr23', NULL, '15351546669', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 10000.00, 100.00, 0.00, 0, '2025-04-02 17:17:51.397527', '2025-04-02 17:17:51.397527', 6);
INSERT INTO `user_profile` VALUES (7, 'test1e2wr23', NULL, '15351846669', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 10000.00, 100.00, 0.00, 0, '2025-04-02 17:20:15.454808', '2025-04-02 17:20:15.454808', 7);
INSERT INTO `user_profile` VALUES (8, 'test1e2wr213', NULL, '15351841669', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 10000.00, 100.00, 0.00, 0, '2025-04-02 17:21:30.469506', '2025-04-02 17:21:30.469506', 8);
INSERT INTO `user_profile` VALUES (9, 'test1e2123r213', NULL, '15351141669', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 10000.00, 100.00, 0.00, 0, '2025-04-02 17:23:19.207431', '2025-04-02 17:23:19.207431', 9);
INSERT INTO `user_profile` VALUES (10, 'te2123r213', NULL, '15353141669', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 10000.00, 100.00, 0.00, 0, '2025-04-02 17:26:38.129470', '2025-04-02 17:26:38.129470', 10);
INSERT INTO `user_profile` VALUES (11, 'te2123313', NULL, '15353141069', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 10000.00, 100.00, 0.00, 0, '2025-04-02 17:28:37.524567', '2025-04-02 17:28:37.524567', 11);
INSERT INTO `user_profile` VALUES (12, 'qeqwe', NULL, '15588888888', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 10000.00, 100.00, 0.00, 0, '2025-04-10 13:05:47.537463', '2025-04-10 13:05:47.537463', 12);
INSERT INTO `user_profile` VALUES (13, '阿明', '王小明', '14455554444', '男', '360733200006120010', '2027-12-22', '16468979746466464', '公务员', '上海', '2001-12-31', 0, NULL, 3000.00, 50000.00, 429.00, 13000.00, 1, '2025-04-10 13:14:05.645446', '2025-04-24 00:39:47.967861', 13);
INSERT INTO `user_profile` VALUES (14, '64hui', '张三', '17777777777', NULL, '188888999911118888', '2030-04-10', '5964613189798623', NULL, NULL, NULL, 0, NULL, NULL, 10000.00, 500.00, 0.00, 0, '2025-04-10 17:05:25.868040', '2025-04-10 17:07:02.829879', 14);
INSERT INTO `user_profile` VALUES (15, 'asd', NULL, '15577777777', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 10000.00, 500.00, 0.00, 0, '2025-05-07 18:39:14.131421', '2025-05-07 18:39:14.131421', 15);
INSERT INTO `user_profile` VALUES (16, 'zxc', NULL, '1231d', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 10000.00, 500.00, 0.00, 0, '2025-05-07 19:23:03.020538', '2025-05-07 19:23:03.020538', 16);
INSERT INTO `user_profile` VALUES (17, 'zxc1', NULL, '1231dads', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 10000.00, 500.00, 0.00, 0, '2025-05-07 19:24:49.313064', '2025-05-07 19:24:49.313064', 17);
INSERT INTO `user_profile` VALUES (18, 'zxasdasdc1', NULL, '123fd1dads', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 10000.00, 500.00, 0.00, 0, '2025-05-07 19:27:51.167413', '2025-05-07 19:27:51.167413', 18);
INSERT INTO `user_profile` VALUES (19, 'zxasddc1', NULL, '23fd1dads', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 10000.00, 500.00, 0.00, 0, '2025-05-07 19:28:20.362929', '2025-05-07 19:28:20.362929', 19);
INSERT INTO `user_profile` VALUES (20, 'zxasdd1', NULL, '23fd1das', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 10000.00, 500.00, 0.00, 0, '2025-05-07 19:29:30.351867', '2025-05-07 19:29:30.351867', 20);
INSERT INTO `user_profile` VALUES (21, 'zasdd1', NULL, '3fd1das', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 10000.00, 500.00, 0.00, 0, '2025-05-07 19:30:00.829477', '2025-05-07 19:30:00.829477', 21);
INSERT INTO `user_profile` VALUES (22, 'asdzasdd1', NULL, 'gf3fd1das', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 10000.00, 500.00, 0.00, 0, '2025-05-07 19:30:48.187705', '2025-05-07 19:30:48.187705', 22);
INSERT INTO `user_profile` VALUES (23, 'asdzdd1', NULL, 'gffd13das', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 10000.00, 500.00, 0.00, 0, '2025-05-07 19:32:25.942410', '2025-05-07 19:32:25.942410', 23);
INSERT INTO `user_profile` VALUES (24, 'asdzdasd1', NULL, 'gffd13asdas', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 10000.00, 500.00, 0.00, 0, '2025-05-07 19:35:56.636086', '2025-05-07 19:35:56.636086', 24);
INSERT INTO `user_profile` VALUES (25, 'asdzaadd1', NULL, 'gffd1dsdas', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 10000.00, 500.00, 0.00, 0, '2025-05-07 19:38:45.650643', '2025-05-07 19:38:45.650643', 25);
INSERT INTO `user_profile` VALUES (26, 'asd1dd1', NULL, 'gff5sdas', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 10000.00, 500.00, 0.00, 0, '2025-05-07 19:42:24.904560', '2025-05-07 19:42:24.904560', 26);
INSERT INTO `user_profile` VALUES (27, 'adsd1dd1', NULL, 'gfaf5sdas', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 10000.00, 500.00, 0.00, 0, '2025-05-07 19:45:18.453883', '2025-05-07 19:45:18.453883', 27);
INSERT INTO `user_profile` VALUES (28, 'zzz', NULL, '12378y90009', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, NULL, 10000.00, 500.00, 0.00, 0, '2025-06-27 00:03:21.345192', '2025-06-27 00:03:21.345192', 28);

-- ----------------------------
-- Table structure for userauth
-- ----------------------------
DROP TABLE IF EXISTS `userauth`;
CREATE TABLE `userauth`  (
  `index` int(11) NOT NULL AUTO_INCREMENT COMMENT '索引',
  `id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '唯一用户id',
  `username` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '唯一用户名, 用于登录',
  `phone_number` varchar(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '唯一用户电话号码, 用于登录及找回密码',
  `hashed_password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '加密后的密码',
  `role` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'user' COMMENT '用户权限, 分为 user/admin/root',
  `created_at` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) COMMENT '注册时间',
  `updated_at` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6) COMMENT '信息更新时间',
  PRIMARY KEY (`index`) USING BTREE,
  UNIQUE INDEX `id`(`id`) USING BTREE,
  UNIQUE INDEX `username`(`username`) USING BTREE,
  UNIQUE INDEX `phone_number`(`phone_number`) USING BTREE,
  INDEX `idx_userauth_usernam_3f27a1`(`username`, `phone_number`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 29 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '用户注册信息表：用于登录和找回密码' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of userauth
-- ----------------------------
INSERT INTO `userauth` VALUES (1, 'c5da8b866b0e416426c303aa2e52a90d', 'test', 'string', '$2b$12$DlodKIMmcDGRIEkNVK5p1.yX0/5O2HGjaZ2Mqc5WUTTrKr2hlPLmq', 'admin', '2025-03-17 19:51:29.805733', '2025-06-27 00:02:36.769624');
INSERT INTO `userauth` VALUES (2, 'ec5be1474de976e2f340a046c4742bf7', 'test1', '123', '$2b$12$Y0Dl/HtzTp52hhk/bxe2j.334tL7dtgMxP..oDR9.F4QudaRlUuVu', 'user', '2025-03-20 20:39:53.817385', '2025-03-20 20:39:53.817385');
INSERT INTO `userauth` VALUES (3, '61295ff6e1536bd3ba5d518e655d227a', 'test24', '111', '$2b$12$LGrva95QwvnunHKe7r2m2OU5MK7Xxh42nAsOuc.p6uIhc6/A6rx02', 'user', '2025-03-20 20:41:32.761658', '2025-03-20 20:41:32.761658');
INSERT INTO `userauth` VALUES (4, '8d1d01717b2d1e62a6f0b5c1ee74e8a6', 'test123', '15355546669', '$2b$12$UZUGuSwVHglYTleHo6s3Leo75lmmt32ePtNcs5YRBNXE/DKA4R/P2', 'user', '2025-04-02 17:12:19.669441', '2025-04-02 17:12:19.669441');
INSERT INTO `userauth` VALUES (5, '0cbc5858553e0b29b2f55946c9b27692', 'test13', '15358546669', '$2b$12$r7vu9oYc0ylpbzceJhG66.Pw050EGk9nnkwYKXw5MQSI168uS54gq', 'user', '2025-04-02 17:15:48.023080', '2025-04-02 17:15:48.023080');
INSERT INTO `userauth` VALUES (6, '3217db6705e147ae3ed58bc6a21a3f58', 'test1ewr23', '15351546669', '$2b$12$mKV4zIOtg6F6QiT6vH6meesXEVG.E9hFFygA5SDvWBgOtkX01OMje', 'user', '2025-04-02 17:17:51.387734', '2025-04-02 17:17:51.387734');
INSERT INTO `userauth` VALUES (7, 'e836617562472ea8e9caab7faec1bd3c', 'test1e2wr23', '15351846669', '$2b$12$NZ7.tkGRjs7PL1HiMCH99.tDx0vUrRaNlTdmbYQSvaaIwLlHvFa1e', 'user', '2025-04-02 17:20:15.447206', '2025-04-02 17:20:15.447206');
INSERT INTO `userauth` VALUES (8, 'f5d47d3676b43aecca1c5403abf48b56', 'test1e2wr213', '15351841669', '$2b$12$zTuyw2ZnmlUmJd.yGlRM7.yLqSXksXre95PjrqcGfD9ifgmekBwqW', 'user', '2025-04-02 17:21:30.462144', '2025-04-02 17:21:30.462144');
INSERT INTO `userauth` VALUES (9, 'dafb393b6c28f383269aa58d91a621d5', 'test1e2123r213', '15351141669', '$2b$12$1/GbCJz22O9NnYZqtJQFHul3RB6PPlScHHl0Mko1qfIZB5udUk0sK', 'user', '2025-04-02 17:23:19.196131', '2025-04-02 17:23:19.196131');
INSERT INTO `userauth` VALUES (10, '0b3a4a8dd5a69e7bef916d81e8b0e569', 'te2123r213', '15353141669', '$2b$12$lqjrjlmtjngy0na/le5zh.m/AN4uMvJYSUqJSxFF6eov0Cd5FER/.', 'user', '2025-04-02 17:26:38.118518', '2025-04-02 17:26:38.118518');
INSERT INTO `userauth` VALUES (11, 'ff559c83fdb5fb8a50feae564404d6e9', 'te2123313', '15353141069', '$2b$12$CpCxW4vfoYSnr5.5g7xPE.kq61EvFUylpKmmeXXmiYdWWJVoB8VSW', 'user', '2025-04-02 17:28:37.513524', '2025-04-02 17:28:37.513524');
INSERT INTO `userauth` VALUES (12, '8a465e69e62ae21dc9fc56e7dd7699e4', 'qeqwe', '15588888888', '$2b$12$T8PFto5A/bLGKHCYi.4QxeQba6NM33Uja1nfkoe05xMrYNoTAH0bi', 'user', '2025-04-10 13:05:47.527435', '2025-04-10 13:05:47.527435');
INSERT INTO `userauth` VALUES (13, 'd3a22f9370a6e3bfc17fa1d961541975', '阿明', '14455554444', '$2b$12$dNp9SPfYk4DDfRJq8hB4.OXKOBnIXvd1OakGVkMV/msNv6C5CvsX2', 'user', '2025-04-10 13:14:05.637471', '2025-04-24 00:27:11.984662');
INSERT INTO `userauth` VALUES (14, '74f8b7e76ce67881ebbcf1fcd28c7874', '64hui', '17777777777', '$2b$12$ReHSJoLEz25LoXLnhu9pD.97uSw8Ejf3Ik5BVp/wDPTxTSBE7zhRO', 'user', '2025-04-10 17:05:25.855780', '2025-04-10 17:05:25.855842');
INSERT INTO `userauth` VALUES (15, 'c6b3910d7f3a10283ea907a564458fb7', 'asd', '15577777777', '$2b$12$GFksfljSLIXnH25vu/76KODGKl.JNMQxr.gRZJuQ5qeDaP1U8mkkG', 'user', '2025-05-07 18:39:14.118689', '2025-05-07 18:39:14.118689');
INSERT INTO `userauth` VALUES (16, '90ed89934e9b2af236d60d04336993f6', 'zxc', '1231d', '$2b$12$zDZ1Q07R7GfSlEdFUKmTrO1Gcv17ktc8PukX5hNXw/.9.GLHtUXE2', 'user', '2025-05-07 19:23:03.014627', '2025-05-07 19:23:03.014627');
INSERT INTO `userauth` VALUES (17, '1f1ffda4e60af8d1894710b4e8d0bad4', 'zxc1', '1231dads', '$2b$12$/ddZzB7UqbElAGpV7OA/N.4P1jSSP1okHNsJ0g5sLPag19dKsXTIS', 'user', '2025-05-07 19:24:49.310033', '2025-05-07 19:24:49.310033');
INSERT INTO `userauth` VALUES (18, '05fe22c8d12603954363a39f5b5bb2e3', 'zxasdasdc1', '123fd1dads', '$2b$12$Z9K/1Ah2D.zxetqUqOIYUeJ1KpZYKw4PRRxB0OlV73avRDAam5VAq', 'user', '2025-05-07 19:27:51.165415', '2025-05-07 19:27:51.165415');
INSERT INTO `userauth` VALUES (19, '3fc7ef8478acdc39de06e5e88f5974da', 'zxasddc1', '23fd1dads', '$2b$12$FSiHBNKJ0BwSbnWBZM.MHOv13nzp1zWmN6Tz.PFDhkU7KnfbyNQJ.', 'user', '2025-05-07 19:28:20.352390', '2025-05-07 19:28:20.352390');
INSERT INTO `userauth` VALUES (20, 'cefd723ae77895f413e68be0cbad2158', 'zxasdd1', '23fd1das', '$2b$12$wDcninqtd2vMpXTyl6f3xeLwBwY4YUjKwD0akXOqUF8ecqqLl9llO', 'user', '2025-05-07 19:29:30.343733', '2025-05-07 19:29:30.343733');
INSERT INTO `userauth` VALUES (21, '64ef6a91c91e3b316fd0fceb7a02dd2b', 'zasdd1', '3fd1das', '$2b$12$1joBOc7/.7wKclyk/3RZq.jObWdjw0RgdE6NXwJoLsb27.Uhfsc5e', 'user', '2025-05-07 19:30:00.818166', '2025-05-07 19:30:00.818166');
INSERT INTO `userauth` VALUES (22, '7bd542c6817c93d51e42160a3ed73158', 'asdzasdd1', 'gf3fd1das', '$2b$12$Dzanzq/nqw9rvEvIPsfpfuShYYTXHQt6ufIA2CpJJcLEQghxL9S52', 'user', '2025-05-07 19:30:48.179472', '2025-05-07 19:30:48.179472');
INSERT INTO `userauth` VALUES (23, '851a97a534b86719956e68710a4bc6bf', 'asdzdd1', 'gffd13das', '$2b$12$Zlud3VFpHONTLKOI4wp9UuGQTlx17aunUf.ArM9dKqueWquIS/Q1.', 'user', '2025-05-07 19:32:25.927673', '2025-05-07 19:32:25.927673');
INSERT INTO `userauth` VALUES (24, '6a3d35588a84c2ccff2e2a8ce55b8144', 'asdzdasd1', 'gffd13asdas', '$2b$12$3nDBG.s80PThFl65BL.ILuJamrMh6teDMrW/VpvUKve6px5y7Jdgq', 'user', '2025-05-07 19:35:56.632085', '2025-05-07 19:35:56.632085');
INSERT INTO `userauth` VALUES (25, '17a086882f879c9313d6c8ba197deaee', 'asdzaadd1', 'gffd1dsdas', '$2b$12$1Rrg3EbFOFLM8n23GKtbPepZXKGglEXsDEbZAaWmZBU2kK9L6SUhO', 'user', '2025-05-07 19:38:45.638742', '2025-05-07 19:38:45.638742');
INSERT INTO `userauth` VALUES (26, 'e5d87744fcafadb22ad3185bd80d450d', 'asd1dd1', 'gff5sdas', '$2b$12$f0EuSlpY6YiWt0QLjeyE2OIuKG8RXNrO0eRm9ZCJHgSu5Vw7wthDe', 'user', '2025-05-07 19:42:24.883821', '2025-05-07 19:42:24.883821');
INSERT INTO `userauth` VALUES (27, '0b6a40ffcd8503833d4587042200073a', 'adsd1dd1', 'gfaf5sdas', '$2b$12$cHXpidtZI0d5ma7fVvYeIOaLxvmqIVq1OBX..Vq2bcWT7OcFClZNi', 'user', '2025-05-07 19:45:18.443103', '2025-05-07 19:45:18.443103');
INSERT INTO `userauth` VALUES (28, '33b5f536393ace741e10a5fb424134d8', 'zzz', '12378y90009', '$2b$12$LphiLkYJ.gUXpWEwh4ed3Ou/JXl33aYrpERTnQP2Kpap8Qryt0fXq', 'root', '2025-06-27 00:03:21.336388', '2025-06-27 00:04:52.656812');

-- ----------------------------
-- Table structure for userauth_article
-- ----------------------------
DROP TABLE IF EXISTS `userauth_article`;
CREATE TABLE `userauth_article`  (
  `userauth_id` int(11) NOT NULL,
  `article_id` int(11) NOT NULL,
  INDEX `userauth_id`(`userauth_id`) USING BTREE,
  INDEX `article_id`(`article_id`) USING BTREE,
  CONSTRAINT `userauth_article_ibfk_1` FOREIGN KEY (`userauth_id`) REFERENCES `userauth` (`index`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `userauth_article_ibfk_2` FOREIGN KEY (`article_id`) REFERENCES `article` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '用户推荐的文章' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of userauth_article
-- ----------------------------
INSERT INTO `userauth_article` VALUES (1, 1);
INSERT INTO `userauth_article` VALUES (1, 2);
INSERT INTO `userauth_article` VALUES (1, 3);
INSERT INTO `userauth_article` VALUES (1, 4);
INSERT INTO `userauth_article` VALUES (1, 5);
INSERT INTO `userauth_article` VALUES (1, 6);
INSERT INTO `userauth_article` VALUES (1, 7);
INSERT INTO `userauth_article` VALUES (1, 8);
INSERT INTO `userauth_article` VALUES (1, 9);
INSERT INTO `userauth_article` VALUES (1, 10);
INSERT INTO `userauth_article` VALUES (1, 11);
INSERT INTO `userauth_article` VALUES (1, 12);
INSERT INTO `userauth_article` VALUES (1, 13);
INSERT INTO `userauth_article` VALUES (1, 14);
INSERT INTO `userauth_article` VALUES (1, 15);
INSERT INTO `userauth_article` VALUES (1, 16);
INSERT INTO `userauth_article` VALUES (1, 17);
INSERT INTO `userauth_article` VALUES (1, 18);
INSERT INTO `userauth_article` VALUES (1, 19);
INSERT INTO `userauth_article` VALUES (1, 20);
INSERT INTO `userauth_article` VALUES (1, 21);
INSERT INTO `userauth_article` VALUES (1, 22);
INSERT INTO `userauth_article` VALUES (1, 23);
INSERT INTO `userauth_article` VALUES (1, 24);
INSERT INTO `userauth_article` VALUES (1, 25);
INSERT INTO `userauth_article` VALUES (1, 26);
INSERT INTO `userauth_article` VALUES (1, 27);
INSERT INTO `userauth_article` VALUES (1, 28);
INSERT INTO `userauth_article` VALUES (1, 29);
INSERT INTO `userauth_article` VALUES (1, 30);
INSERT INTO `userauth_article` VALUES (1, 31);
INSERT INTO `userauth_article` VALUES (1, 32);
INSERT INTO `userauth_article` VALUES (1, 33);
INSERT INTO `userauth_article` VALUES (1, 34);
INSERT INTO `userauth_article` VALUES (1, 35);
INSERT INTO `userauth_article` VALUES (7, 1);
INSERT INTO `userauth_article` VALUES (7, 4);
INSERT INTO `userauth_article` VALUES (7, 13);
INSERT INTO `userauth_article` VALUES (7, 18);
INSERT INTO `userauth_article` VALUES (7, 7);
INSERT INTO `userauth_article` VALUES (7, 10);
INSERT INTO `userauth_article` VALUES (7, 21);
INSERT INTO `userauth_article` VALUES (7, 23);
INSERT INTO `userauth_article` VALUES (7, 26);
INSERT INTO `userauth_article` VALUES (8, 1);
INSERT INTO `userauth_article` VALUES (8, 36);
INSERT INTO `userauth_article` VALUES (8, 13);
INSERT INTO `userauth_article` VALUES (8, 16);
INSERT INTO `userauth_article` VALUES (8, 7);
INSERT INTO `userauth_article` VALUES (8, 11);
INSERT INTO `userauth_article` VALUES (8, 21);
INSERT INTO `userauth_article` VALUES (8, 23);
INSERT INTO `userauth_article` VALUES (8, 26);
INSERT INTO `userauth_article` VALUES (9, 1);
INSERT INTO `userauth_article` VALUES (9, 4);
INSERT INTO `userauth_article` VALUES (9, 13);
INSERT INTO `userauth_article` VALUES (9, 17);
INSERT INTO `userauth_article` VALUES (9, 7);
INSERT INTO `userauth_article` VALUES (9, 10);
INSERT INTO `userauth_article` VALUES (9, 21);
INSERT INTO `userauth_article` VALUES (9, 23);
INSERT INTO `userauth_article` VALUES (9, 26);
INSERT INTO `userauth_article` VALUES (10, 1);
INSERT INTO `userauth_article` VALUES (11, 1);
INSERT INTO `userauth_article` VALUES (11, 36);
INSERT INTO `userauth_article` VALUES (11, 13);
INSERT INTO `userauth_article` VALUES (11, 16);
INSERT INTO `userauth_article` VALUES (11, 7);
INSERT INTO `userauth_article` VALUES (11, 10);
INSERT INTO `userauth_article` VALUES (11, 21);
INSERT INTO `userauth_article` VALUES (11, 23);
INSERT INTO `userauth_article` VALUES (11, 26);
INSERT INTO `userauth_article` VALUES (1, 37);
INSERT INTO `userauth_article` VALUES (13, 1);
INSERT INTO `userauth_article` VALUES (13, 4);
INSERT INTO `userauth_article` VALUES (13, 13);
INSERT INTO `userauth_article` VALUES (13, 16);
INSERT INTO `userauth_article` VALUES (13, 8);
INSERT INTO `userauth_article` VALUES (13, 10);
INSERT INTO `userauth_article` VALUES (13, 21);
INSERT INTO `userauth_article` VALUES (13, 23);
INSERT INTO `userauth_article` VALUES (13, 26);
INSERT INTO `userauth_article` VALUES (13, 7);
INSERT INTO `userauth_article` VALUES (13, 11);
INSERT INTO `userauth_article` VALUES (24, 1);
INSERT INTO `userauth_article` VALUES (24, 4);
INSERT INTO `userauth_article` VALUES (24, 13);
INSERT INTO `userauth_article` VALUES (24, 16);
INSERT INTO `userauth_article` VALUES (24, 8);
INSERT INTO `userauth_article` VALUES (24, 12);
INSERT INTO `userauth_article` VALUES (24, 21);
INSERT INTO `userauth_article` VALUES (24, 23);
INSERT INTO `userauth_article` VALUES (24, 26);
INSERT INTO `userauth_article` VALUES (26, 1);
INSERT INTO `userauth_article` VALUES (26, 4);
INSERT INTO `userauth_article` VALUES (26, 13);
INSERT INTO `userauth_article` VALUES (26, 16);
INSERT INTO `userauth_article` VALUES (26, 8);
INSERT INTO `userauth_article` VALUES (26, 10);
INSERT INTO `userauth_article` VALUES (26, 21);
INSERT INTO `userauth_article` VALUES (26, 23);
INSERT INTO `userauth_article` VALUES (26, 26);
INSERT INTO `userauth_article` VALUES (27, 1);
INSERT INTO `userauth_article` VALUES (27, 4);
INSERT INTO `userauth_article` VALUES (27, 13);
INSERT INTO `userauth_article` VALUES (27, 16);
INSERT INTO `userauth_article` VALUES (27, 8);
INSERT INTO `userauth_article` VALUES (27, 10);
INSERT INTO `userauth_article` VALUES (27, 21);
INSERT INTO `userauth_article` VALUES (27, 23);
INSERT INTO `userauth_article` VALUES (27, 26);

SET FOREIGN_KEY_CHECKS = 1;

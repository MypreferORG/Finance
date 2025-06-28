# 金融项目模拟数据使用说明

本文档介绍了如何使用模拟数据脚本为金融项目生成和导入测试数据。

## 文件说明

- `mock_data.py`: 模拟数据生成脚本，包含各种数据生成函数
- `generate_mock_data_json.py`: 将模拟数据保存为JSON文件的脚本
- `import_mock_data.py`: 将模拟数据导入到数据库的脚本

## 数据模型

模拟数据包括以下几类：

1. **用户相关数据**
   - 用户认证信息 (UserAuth)
   - 用户个人资料 (UserProfile)
   - 用户A卡评分卡数据 (UserApplication)
   - 用户B卡评分卡数据 (UserBehavior)
   - 用户登录日志 (UserSignLog)

2. **文章和公告**
   - 文章 (Article)
   - 公告 (Announcement)

3. **贷款相关数据**
   - 贷款记录 (LoanRecord)
   - 还款记录 (RepaymentRecord)
   - 利率数据 (InterestRate)

4. **其他数据**
   - AI模型 (AIModel)
   - 复审申请 (ReviewApplication)

## 使用方法

### 1. 生成模拟数据并查看

如果您只想生成模拟数据并查看，可以直接运行：

```bash
python mock_data.py
```

这将生成所有模拟数据并以JSON格式打印到控制台。

### 2. 生成模拟数据并保存为JSON文件

如果您想将生成的模拟数据保存为JSON文件以便查看或导入其他系统，可以运行：

```bash
python generate_mock_data_json.py
```

这将在`mock_data_json`目录下生成以下文件：
- `full_mock_data.json`: 包含所有模拟数据的完整JSON文件
- 各类数据的单独JSON文件，如`users.json`、`profiles.json`等

### 3. 将模拟数据导入到数据库

如果您想将模拟数据导入到项目的数据库中，可以运行：

```bash
python import_mock_data.py
```

**注意**：在运行导入脚本前，请确保：
1. 数据库连接配置正确（默认使用SQLite）
2. 数据库表结构已创建
3. 如果数据库中已有数据，导入可能会失败或导致数据重复

## 自定义模拟数据

如果您需要自定义模拟数据，可以修改`mock_data.py`文件中的相关函数：

- 修改`generate_user_auth_data`函数可以自定义用户数量和属性
- 修改各个生成函数中的参数可以调整数据的分布和特性
- 在`generate_all_mock_data`函数中可以调整各类数据的生成数量

## 数据关系

生成的模拟数据保持了以下关系：

- 用户资料、评分卡数据和登录日志与用户认证信息相关联
- 贷款记录和还款记录与用户相关联
- 复审申请与贷款记录相关联
- 用户与文章之间建立了推荐关系

## 故障排除

如果在使用过程中遇到问题：

1. **导入失败**：检查数据库连接配置和表结构是否正确
2. **数据不一致**：可能是因为随机种子不同，可以在`mock_data.py`中设置固定的随机种子
3. **字段错误**：检查模型定义是否与数据库表结构一致
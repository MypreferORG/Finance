import pandas as pd
from openai import OpenAI
from neo4j import GraphDatabase
import json
import os

client = OpenAI(
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
)

# ==================== 1. 数据清洗 ====================


def clean_data(input_file, output_file):
    """
    使用 Pandas 去除重复数据（根据 link 列）
    """
    df = pd.read_csv(input_file)
    df.drop_duplicates(subset=["link"], keep="first", inplace=True)
    df.to_csv(output_file, index=False)
    print(f"✅ 数据已清洗并保存至 {output_file}")
    return output_file


# ==================== 2. Prompt 工程 ====================
def generate_prompt():
    """
    构建 Prompt 模板，引导模型提取实体和关系
    """
    prompt = """
你将扮演一个智能助手的角色，专注于从给定的金融相关文本中提取所有潜在的实体及其之间的关系。请确保遵循以下要求和输出格式：

目标：
- 从输入文本中识别并提取各类金融相关的实体（如银行、贷款类型、流程步骤、信用方法等）。
- 提取实体之间的各种关系，包括但不限于"提供"、"涉及流程"、"需要"、"审批机构"、"关联产品"等。
- 输出结构化的 JSON 格式，便于后续解析和知识图谱构建。

输出格式：
你的输出必须是一个 JSON 对象，结构如下：

```json
{
  "entities": {
    "<Entity_Type>": ["Entity_Name_1", "Entity_Name_2", ...],
    ...
  },
  "relations": {
    "<Relation_Type>": [
      {
        "source_type": "<Source_Entity_Type>",
        "source": "<Source_Entity_Name>",
        "target_type": "<Target_Entity_Type>",
        "target": "<Target_Entity_Name>"
      },
      ...
    ],
    ...
  }
}
```

约束条件：
- 所有实体和关系必须直接来源于输入文本，不得引入外部知识或推测。
- 实体类型应尽量标准化，例如：Bank, LoanType, ProcessStep, CreditMethod, FinancialProduct, Regulation 等。
- 关系类型应为简洁的动词或短语，例如：提供、涉及流程、需要、审批、违反、监管、关联等。
- 若没有明确的关系可提取，"relations" 字段应为空对象 {}。
- 不得包含任何额外说明、解释或注释，仅返回纯 JSON 内容。
- 输出的 JSON 必须语法正确，无格式错误。

广泛覆盖：
- 尽可能识别多种类型的实体和关系，包括但不限于：
  - 银行/金融机构 (Bank)
  - 贷款类型 (LoanType)
  - 金融产品 (FinancialProduct)
  - 审批流程 (ProcessStep)
  - 信用评估方法 (CreditMethod)
  - 法规政策 (Regulation)
  - 监管机构 (Regulator)
  - 客户群体 (CustomerSegment)

注意事项：
- 实体名称应保持原文一致性，避免翻译或改写。
- 关系方向要准确，source 和 target 不可颠倒。
- 对于模糊或隐含的关系，请在合理范围内进行推断，但不可过度解读。

示例输入：
"工商银行提供信用贷款，该贷款涉及贷款受理和贷款审批流程，申请信用贷款需要提高信用评分。"

示例输出：
```json
{
  "entities": {
    "Bank": ["工商银行"],
    "LoanType": ["信用贷款"],
    "ProcessStep": ["贷款受理", "贷款审批"],
    "CreditMethod": ["提高信用评分"]
  },
  "relations": {
    "提供": [
      {
        "source_type": "Bank",
        "source": "工商银行",
        "target_type": "LoanType",
        "target": "信用贷款"
      }
    ],
    "涉及流程": [
      {
        "source_type": "LoanType",
        "source": "信用贷款",
        "target_type": "ProcessStep",
        "target": "贷款受理"
      },
      {
        "source_type": "LoanType",
        "source": "信用贷款",
        "target_type": "ProcessStep",
        "target": "贷款审批"
      }
    ],
    "需要": [
      {
        "source_type": "LoanType",
        "source": "信用贷款",
        "target_type": "CreditMethod",
        "target": "提高信用评分"
      }
    ]
  }
}
```
"""
    return prompt


# ==================== 3. 调用大模型 API 解析内容 ====================
def extract_knowledge(title, summary, model="qwen-plus"):
    """
    调用 OpenAI 大模型 API 获取结构化知识
    """
    prompt = generate_prompt()

    # response = openai.ChatCompletion.create(
    #     model=model,
    #     messages=[{"role": "user", "content": prompt}],
    #     temperature=0
    # )

    completion = client.chat.completions.create(
        # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
        model="qwen-plus-2025-04-28",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"文章标题：{title}\n文章摘要：{summary}"},
        ],
        # Qwen3模型通过enable_thinking参数控制思考过程（开源版默认True，商业版默认False）
        # 使用Qwen3开源版模型时，若未启用流式输出，请将下行取消注释，否则会报错
        extra_body={"enable_thinking": False},
    )
    # print(completion.model_dump_json())
    # print('文章：', title, '已处理完成')

    # content = completion.model_dump_json()
    try:
        result = json.loads(
            json.loads(completion.model_dump_json())[
                'choices'][0]['message']['content']
            .replace('```json', '')
            .replace('```', '')
            .replace('\n', '')
            .replace(' ', '')
        )  # 安全解析 JSON
        return result
    except Exception as e:
        print("❌ JSON 解析失败：", e)
        # print("返回原始内容：\n", content)
        return {}


# ==================== 4. Neo4j 写入逻辑 ====================
class Neo4jManager:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def create_entities_and_relations(self, knowledge):
        with self.driver.session() as session:
            # 创建实体
            for entity_type, entities in knowledge.get("entities", {}).items():
                for entity_name in entities:
                    session.execute_write(
                        self._create_entity, entity_type, entity_name)

            # 创建关系
            for relation_type, relations in knowledge.get("relations", {}).items():
                for rel in relations:
                    session.execute_write(
                        self._create_relation,
                        rel["source_type"],
                        rel["source"],
                        relation_type,
                        rel["target_type"],
                        rel["target"]
                    )

    @staticmethod
    def _create_entity(tx, entity_type, entity_name):
        query = f"""
        MERGE (:{entity_type} {{name: $name}})
        """
        tx.run(query, name=entity_name)

    @staticmethod
    def _create_relation(tx, source_type, source_name, relation_type, target_type, target_name):
        query = f"""
        MATCH (s:{source_type} {{name: $source_name}})
        MATCH (t:{target_type} {{name: $target_name}})
        MERGE (s)-[:{relation_type}]->(t)
        """
        tx.run(query, source_name=source_name, target_name=target_name)


# ==================== 5. 主流程执行 ====================
if __name__ == "__main__":
    # Neo4j 配置
    neo4j_uri = "neo4j://localhost:7687"
    neo4j_user = "neo4j"
    neo4j_password = "Lejda-EpJh266.k"

    # 输入/输出文件路径
    input_csv = "ai\\article.csv"
    cleaned_csv = "ai\\cleaned_data.csv"

    # 步骤 1：数据清洗
    clean_data(input_csv, cleaned_csv)

    # 初始化 Neo4j 管理器
    kg_manager = Neo4jManager(neo4j_uri, neo4j_user, neo4j_password)

    # 步骤 2-4：读取清洗后的数据，调用模型，写入 Neo4j
    df = pd.read_csv(cleaned_csv)
    for idx, row in df.iterrows():
        print(f"\n🧠 正在处理第 {idx + 1} 条数据：{row['title']}")
        knowledge = extract_knowledge(row["title"], row["summary"])
        if knowledge:
            kg_manager.create_entities_and_relations(knowledge)
        # if idx > 1:
        #     break

    # 关闭数据库连接
    kg_manager.close()
    print("🎉 知识图谱构建完成！")

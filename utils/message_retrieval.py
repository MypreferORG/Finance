import json
import os
import re
import time
import numpy as np
from typing import List, Dict, Any
from openai import OpenAI

# =================配置区域=================
DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY", "your_dashscope_api_key_here")
DASHSCOPE_BASE_URL = os.getenv("DASHSCOPE_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")
EMBEDDING_MODEL = "text-embedding-v4"
LLM_MODEL = "qwen3-vl-235b-a22b-instruct"

# 文件路径配置
DEFAULT_EXAMPLES_FILE = "default_examples.json" # 原始文本文件
DEFAULT_EMBEDDINGS_CACHE = "default_embeddings.npy" # 向量缓存文件
# =========================================

def get_remote_embeddings(client: OpenAI, texts: List[str], batch_size: int = 6) -> np.ndarray:
    """
    获取阿里云向量 (带分批处理)
    """
    valid_texts = [t for t in texts if t.strip()]
    if not valid_texts:
        return np.array([])
    
    all_embeddings = []
    total = len(valid_texts)
    
    # 分批循环
    for i in range(0, total, batch_size):
        batch_texts = valid_texts[i : i + batch_size]
        try:
            response = client.embeddings.create(
                model=EMBEDDING_MODEL,
                input=batch_texts,
                dimensions=1024,
                encoding_format="float"
            )
            batch_embeddings = [item.embedding for item in response.data]
            all_embeddings.extend(batch_embeddings)
        except Exception as e:
            print(f"[Embedding API Error] 批次 {i} 失败: {e}")
            pass # 实际生产中建议重试

    return np.array(all_embeddings)

def get_cached_default_embeddings(client: OpenAI, json_path: str, cache_path: str) -> np.ndarray:
    """
    【核心优化】加载或计算默认样例的 Embedding
    逻辑: 
    1. 检查缓存文件是否存在
    2. 检查 JSON 源文件是否比缓存文件更新
    3. 满足条件直接加载，否则重新计算并保存
    """
    
    # 1. 检查源文件是否存在
    if not os.path.exists(json_path):
        # 如果文件不存在，自动创建默认的
        print(f"提示: {json_path} 不存在，生成默认规则文件。")
        defaults = [{"content": "借款逾期"}, {"content": "验证码申请额度"}, {"content": "催收律师函"}, {"content": "博彩资金往来"}]
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(defaults, f, ensure_ascii=False, indent=2)
    
    need_recompute = True
    
    # 2. 检查缓存是否有效
    if os.path.exists(cache_path):
        json_mtime = os.path.getmtime(json_path)
        cache_mtime = os.path.getmtime(cache_path)
        
        if cache_mtime > json_mtime:
            # 缓存比源文件新，直接用
            print(f"--- [缓存命中] 加载本地向量库: {cache_path} ---")
            try:
                embeddings = np.load(cache_path)
                return embeddings
            except:
                print("缓存文件损坏，准备重新计算...")
        else:
            print(f"--- [更新检测] 发现 {json_path} 有修改，重新计算向量 ---")
    else:
        print(f"--- [初始化] 首次运行，计算并缓存向量 ---")

    # 3. 重新计算流程
    with open(json_path, 'r', encoding='utf-8') as f:
        examples = json.load(f)
    
    texts = [ex["content"] for ex in examples]
    embeddings = get_remote_embeddings(client, texts)
    
    # 4. 保存缓存 (如果获取成功)
    if embeddings.size > 0:
        np.save(cache_path, embeddings)
        print(f"--- [缓存成功] 已保存至 {cache_path} ---")
    
    return embeddings

def compute_cosine_similarity_matrix(matrix_a: np.ndarray, matrix_b: np.ndarray) -> np.ndarray:
    """纯 NumPy 计算余弦相似度"""
    if matrix_a.size == 0 or matrix_b.size == 0:
        return np.array([])
    
    norm_a = np.linalg.norm(matrix_a, axis=1, keepdims=True)
    norm_b = np.linalg.norm(matrix_b, axis=1, keepdims=True)
    
    # 防止除零
    norm_a[norm_a == 0] = 1e-10
    norm_b[norm_b == 0] = 1e-10
    
    return np.dot(matrix_a, matrix_b.T) / (np.dot(norm_a, norm_b.T))

def sms_embedding_filter_cloud(
    client: OpenAI,
    user_sms_data: List[Dict[str, Any]], 
    similarity_threshold: float = 0.68
) -> List[Dict[str, Any]]:
    """Embedding 粗筛函数"""
    if not user_sms_data:
        return []

    # === 获取默认样例向量 (使用缓存逻辑) ===
    default_embeddings = get_cached_default_embeddings(
        client, DEFAULT_EXAMPLES_FILE, DEFAULT_EMBEDDINGS_CACHE
    )
    
    # === 获取用户短信向量 (实时计算，必须走API) ===
    user_texts = [sms['content'].strip() for sms in user_sms_data]
    # print(f"--- [粗筛阶段] 计算 {len(user_texts)} 条用户短信向量 ---")
    user_embeddings = get_remote_embeddings(client, user_texts)
    
    # 对齐检查
    if len(user_embeddings) != len(user_texts):
        user_sms_data = user_sms_data[:len(user_embeddings)]

    if default_embeddings.size == 0 or user_embeddings.size == 0:
        return []

    # 计算相似度
    similarity_matrix = compute_cosine_similarity_matrix(user_embeddings, default_embeddings)
    
    risk_sms = []
    for i, sms in enumerate(user_sms_data):
        if len(similarity_matrix) > i:
            max_score = np.max(similarity_matrix[i])
            if max_score >= similarity_threshold:
                sms["_similarity_score"] = round(float(max_score), 4)
                risk_sms.append(sms)
            
    return risk_sms

def llm_risk_evaluator_qwen(client: OpenAI, filtered_sms_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Qwen 精判函数"""
    if not filtered_sms_data:
        return {"final_decision": "PASS", "reason": "粗筛无风险"}

    # 构建 Prompt 数据
    simple_sms_list = []
    for sms in filtered_sms_data:
        simple_sms_list.append({
            "date": sms.get("sendDate"), 
            "content": sms.get("content"),
            "risk_score": sms.get("_similarity_score")
        })
    
    sms_context = json.dumps(simple_sms_list, ensure_ascii=False, indent=2)
    
    prompt = f"""
    分析信贷风险。
    数据: {sms_context}
    
    规则:
    1. 多头借贷(7天>10平台)->LOWER_SCORE
    2. 外部违约(催收/律师函)->REJECT
    3. 高危消费(赌博)->MANUAL_REVIEW
    4. 资金紧张(滞纳金)->LOWER_LIMIT
    
    输出严格JSON: {{ "final_decision": "REJECT|PASS...", "risk_tags": [], "analysis_summary": "..." }}
    """

    try:
        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.01,
            response_format={"type": "json_object"}
        )
        content = response.choices[0].message.content
        if content.startswith("```"):
            content = re.sub(r"^```json\s*|\s*```$", "", content, flags=re.MULTILINE)
        return json.loads(content)
    except Exception as e:
        return {"error": str(e), "final_decision": "MANUAL_REVIEW"}

def comprehensive_risk_analysis(user_sms_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """主程序入口"""
    client = OpenAI(api_key=DASHSCOPE_API_KEY, base_url=DASHSCOPE_BASE_URL)
    
    #print(">>> 步骤1: 启动风控筛选...")
    risky_candidates = sms_embedding_filter_cloud(client, user_sms_data)
    
    # print(f"    命中 {len(risky_candidates)} 条可疑短信")
    # print(risky_candidates)
    if not risky_candidates:
        return {"final_decision": "PASS"}
        
    #print(">>> 步骤2: 启动 Qwen 智能分析...")
    res = llm_risk_evaluator_qwen(client, risky_candidates)
    res["raw_risk_count"] = len(risky_candidates)
    return res

if __name__ == "__main__":
    # 测试数据
    test_sms = [
        {"telphone": "138xx", "content": "您的快递已到", "sendDate": "2025-11-05"},
        {"telphone": "106xx", "content": "【360借条】验证码6677，注册获取额度", "sendDate": "2025-11-01"},
        {"telphone": "106xx", "content": "【催收】您的欠款逾期，已发律师函", "sendDate": "2025-10-25"}
    ]
    
    test_sms = [
        # --- 正常生活噪音 (干扰项) ---
        {"telphone": "1069001", "content": "【菜鸟驿站】您的包裹已到达朝阳区XX小区西门柜机，请凭取件码8821取件。", "sendDate": "2025-11-05 18:30:00"},
        {"telphone": "1069002", "content": "【美团外卖】骑手已接单，预计15:30送达，请保持电话畅通。", "sendDate": "2025-11-05 15:00:00"},
        {"telphone": "10086", "content": "【中国移动】尊敬的客户，您10月份的话费账单已出，共计89.50元。", "sendDate": "2025-11-04 09:00:00"},
        {"telphone": "1069003", "content": "【天猫超市】双11预售开启！全场满199减100，点击 t.cn/xxxx 查看。", "sendDate": "2025-11-01 10:00:00"},
        {"telphone": "1069004", "content": "【BOSS直聘】验证码4452，您正在登录BOSS直聘进行求职沟通。", "sendDate": "2025-11-02 14:00:00"}, # 也是验证码，但是是找工作的，Embedding可能会捞出来，但LLM应该判断为Pass
        {"telphone": "95588", "content": "【工商银行】您尾号8888账户于11月03日12:21支出人民币50.00元。", "sendDate": "2025-11-03 12:21:00"},
        {"telphone": "1069005", "content": "【抖音】验证码112233，用于登录您的抖音账号，请勿泄露。", "sendDate": "2025-11-03 20:00:00"},
        {"telphone": "12306", "content": "【铁路12306】购票成功：11月10日 G123次列车 08车12A号。", "sendDate": "2025-11-04 08:00:00"},

        # --- 疑似多头借贷 (风险项：短时间密集申请) ---
        # 11月1日密集爆发
        {"telphone": "1069101", "content": "【360借条】验证码7788，您正在申请额度，请勿泄露给他人。", "sendDate": "2025-11-01 09:15:00"},
        {"telphone": "1069102", "content": "【度小满】您的验证码是5566，用于注册并激活钱包额度。", "sendDate": "2025-11-01 09:20:00"},
        {"telphone": "1069103", "content": "【拍拍贷】验证码1234，您正在操作借款申请，如非本人操作请忽略。", "sendDate": "2025-11-01 09:45:00"},
        {"telphone": "1069104", "content": "【京东金条】验证码9988，激活白条金条服务。", "sendDate": "2025-11-01 10:30:00"},
        {"telphone": "1069105", "content": "【马上消费】验证码6677，签署借款协议验证。", "sendDate": "2025-11-01 11:00:00"},
        {"telphone": "1069106", "content": "【安逸花】您有30000元额度待领取，验证码4455。", "sendDate": "2025-11-01 14:00:00"},
        
        # 11月2日继续申请
        {"telphone": "1069107", "content": "【分期乐】验证码2233，您正在申请乐花卡。", "sendDate": "2025-11-02 10:00:00"},
        {"telphone": "1069108", "content": "【中原消费金融】验证码8899，提现验证。", "sendDate": "2025-11-02 16:00:00"},
        {"telphone": "1069109", "content": "【众安贷】验证码0000，您正在完善资料获取额度。", "sendDate": "2025-11-02 18:00:00"},

        # --- 外部违约 (高危项) ---
        {"telphone": "1069201", "content": "【XX法务部】您的欠款已严重逾期180天，我司已向户籍地法院提起诉讼，受理号(2025)京01民初332号，请等待传票。", "sendDate": "2025-10-25 10:00:00"},
        {"telphone": "1069202", "content": "【征信中心】提醒：您的借款逾期记录即将上报央行征信系统，请在今日17点前处理。", "sendDate": "2025-10-28 09:00:00"},

        # --- 高危消费 (赌博) ---
        {"telphone": "00852xxx", "content": "澳门威尼斯人：老会员回归送888彩金，百家乐、龙虎斗通杀，点击 xy.com 下载APP。", "sendDate": "2025-10-20 23:00:00"},

        # --- 资金紧张 (信用卡) ---
        {"telphone": "95555", "content": "【招商银行】您的信用卡本期账单最低还款额为5000元，已逾期3天，产生滞纳金25元。", "sendDate": "2025-11-04 10:00:00"},
        
        # --- 容易被误伤的营销短信 (测试模型的辨别能力) ---
        {"telphone": "1069300", "content": "【备用金】缺钱不用慌，最高50万备用金，日息低至万2，点击链接查看（广告）。", "sendDate": "2025-11-05 08:00:00"} 
        # ↑ 这条虽有“缺钱”，但明显是广告，不应算作用户的“违约证据”，看LLM能否识别为 PASS 或 Low Risk
    ]

    result = comprehensive_risk_analysis(test_sms)
    print("\n====== 风控报告 ======")
    print(json.dumps(result, indent=4, ensure_ascii=False))
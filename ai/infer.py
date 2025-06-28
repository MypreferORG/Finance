# -*- coding: utf-8 -*-
"""
# @Create on : 2025/3/27 下午9:11
# @Author : Yaro
# @Des: 
"""

import torch
import torch.nn as nn
from transformers import BertTokenizer, BertModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


# 定义 BERT + MLP 分类器（与训练时保持一致）
class BertMLPClassifier(nn.Module):
    def __init__(self, bert_model_name='bert-base-uncased', hidden_dim=128, output_dim=1):
        super(BertMLPClassifier, self).__init__()
        self.bert = BertModel.from_pretrained(bert_model_name)
        self.fc = nn.Sequential(
            nn.Linear(self.bert.config.hidden_size, hidden_dim),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(hidden_dim, output_dim),
            nn.Sigmoid()
        )

    def forward(self, input_ids, attention_mask):
        bert_output = self.bert(input_ids=input_ids, attention_mask=attention_mask)
        pooled_output = bert_output.pooler_output  # [batch_size, hidden_size]
        return self.fc(pooled_output)


# 推理函数
def inference_a(model, tokenizer, device, texts, max_length=128):
    """
    推理函数
    :param model: 已加载好的模型
    :param tokenizer: 对应的 BertTokenizer
    :param device: 设备（cpu 或 cuda）
    :param texts: 单个文本字符串或文本列表（输入CSV中拼接后的字符串）
    :param max_length: 分词时最大长度
    :return: 返回一个列表，每个元素为 (概率, 标签)，标签为 0 或 1
    """
    model.eval()
    # 如果输入是单个字符串，则转换为列表
    if isinstance(texts, str):
        texts = [texts]
    results = []
    with torch.no_grad():
        for text in texts:
            encoding = tokenizer(text, padding='max_length', truncation=True, max_length=max_length,
                                 return_tensors="pt")
            input_ids = encoding['input_ids'].to(device)
            attention_mask = encoding['attention_mask'].to(device)
            output = model(input_ids, attention_mask).squeeze()
            prob = output.item()
            label = 1 if prob < 0.5 else 0
            results.append((prob, label))
    return results
def inference_b(model, tokenizer, device, texts, max_length=128):
    """
    推理函数
    :param model: 已加载好的模型
    :param tokenizer: 对应的 BertTokenizer
    :param device: 设备（cpu 或 cuda）
    :param texts: 单个文本字符串或文本列表（输入CSV中拼接后的字符串）
    :param max_length: 分词时最大长度
    :return: 返回一个列表，每个元素为 (概率, 标签)，标签为 0 或 1
    """
    model.eval()
    # 如果输入是单个字符串，则转换为列表
    if isinstance(texts, str):
        texts = [texts]
    results = []
    with torch.no_grad():
        for text in texts:
            encoding = tokenizer(text, padding='max_length', truncation=True, max_length=max_length,
                                 return_tensors="pt")
            input_ids = encoding['input_ids'].to(device)
            attention_mask = encoding['attention_mask'].to(device)
            output = model(input_ids, attention_mask).squeeze()
            prob = output.item()
            label = 1 if prob > 0.5 else 0
            results.append((prob, label))
    return results



# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
device = torch.device("cpu")
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

model_a = BertMLPClassifier().to(device)
for param in model_a.bert.parameters():
    param.requires_grad = False
model_a.bert.embeddings.position_embeddings.weight.requires_grad = True
checkpoint_path = "ai/best_model_a.pth"
model_a.load_state_dict(torch.load(checkpoint_path, map_location=device))
model_a.to(device)

model_b = BertMLPClassifier().to(device)
for param in model_b.bert.parameters():
    param.requires_grad = False
model_b.bert.embeddings.position_embeddings.weight.requires_grad = True
checkpoint_path = ("ai/best_model_b.pth")
model_b.load_state_dict(torch.load(checkpoint_path, map_location=device))
model_b.to(device)


def predict_a(text):
    predictions = inference_a(model_a, tokenizer, device, text)
    return predictions

def predict_b(text):
    predictions = inference_b(model_b, tokenizer, device, text)
    return predictions


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/predict/{text}")
def predict(text: str):
    """
    FastAPI 接口函数
    :param text: 输入文本字符串
    :return: 返回预测结果
    """
    predictions_a = predict_a(text)
    predictions_b = predict_b(text)
    return {
        "predictions_a": predictions_a,
        "predictions_b": predictions_b
    }

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8001)

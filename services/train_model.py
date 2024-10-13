# -*- coding: utf-8 -*-
"""
# @Create on : 2024/10/12 下午4:54
# @Author : Yaro
# @Des: 模型训练
"""
import numpy as np
import pandas as pd
import lightgbm as lgb
from sklearn.model_selection import train_test_split
data = pd.read_csv('model_sample.csv')
def missing_col(data,num):
    '''
    删除缺失过高的列
    :param data:dataframe
    :param num: float 缺失阈值上限
    :return: dataframe
    '''
    missing_columns=[]
    for column in data.columns:
        if sum(pd.isnull(data[column]))/len(data)>=num:
            missing_columns.append(column)
    data = data.loc[:,list(~data.columns.isin(missing_columns))]
    return data

def missing_index(data,num):
    '''
    删除缺失过高的行
    :param data:dataframe
    :param num: float 缺失阈值上限
    :return: dataframe
    '''
    missing_index=[]
    for i in np.arange(data.shape[0]):#arrnge（）范围
        if list(data.loc[i,:].isnull()).count(True)/len(data.columns)>num:
            missing_index.append(i)
    data = data.drop(missing_index)
    data=data.reset_index(drop=True)
    return data

def stable_feature(data,num):
    '''
    删除90%以上取值相同的列
    :param data:dataframe
    :param num: float 相同阈值上限
    :return: dataframe
    '''
    drop_cols_simple=[]
    cols = [col for col in data.columns if col not in ('y',)]
    for col in cols:
        if max(data[col].value_counts())/len(data)>num:
            drop_cols_simple.append(col)
    data = data.drop(drop_cols_simple,axis=1)#axis=1按列删除
    data= data.reset_index(drop=True)#这个感觉可以没有
    return data


def data_process(data):
    '''
    数据处理
    :param data:dataframe
    :return: dataframe
    '''
    data = missing_col(data, 0.80).reset_index(drop=True)
    data = missing_index(data, 0.8)
    data = stable_feature(data, 0.9)
    return data

def split_data(data):
    feature_lst = [col for col in data.columns if col != 'y']
    feature_lst = [col for col in feature_lst if col != 'user_id']
    x = data[feature_lst]
    y = data['y']
    x = x.replace({np.nan: -1})
    y = y.replace({np.nan: -1})
    train_x, test_x, train_y, test_y = train_test_split(x, y, random_state=0, test_size=0.2)
    return train_x, test_x, train_y, test_y

def  lgb_test(train_x,train_y,test_x,test_y):
    '''
    :param train_x:
    :param train_y:
    :param test_x:
    :param test_y:
    :return:模型和准确率
    '''
    clf =lgb.LGBMClassifier(boosting_type = 'gbdt',
                           objective = 'binary',
                           metric = 'auc',
                           learning_rate = 0.1,
                           n_estimators = 24,
                           max_depth = 5,
                           num_leaves = 20,
                           max_bin = 45,
                           min_data_in_leaf = 6,
                           bagging_fraction = 0.6,
                           bagging_freq = 0,
                           feature_fraction = 0.8,
                           )
    clf.fit(train_x,train_y,eval_set = [(train_x,train_y),(test_x,test_y)],eval_metric = 'auc')
    return clf,clf.best_score_['valid_1']['auc']

def train(data):
    '''
    :param data:dataframe
    :return: 模型
    '''
    data=data_process(data)
    train_x, train_y, test_x, test_y=split_data(data)
    model,_=lgb_test(train_x, train_y, test_x, test_y)
    return model




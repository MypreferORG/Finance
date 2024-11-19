# -*- coding: utf-8 -*-
"""
# @Create on : 2024/11/13 下午4:34
# @Author : Yaro
# @Des: 
"""
import torch
import torch.utils.data as data
import os
import pandas as pd
import numpy as np
from util import emp_length_to_int

def data_load(table_path):
    data = pd.read_csv(table_path)
    return data

def data_preprocessing(df_data):
    df_data = df_data.loc[df_data['loan_status'].isin(['Fully Paid', 'Charged Off'])]
    #选中有效已经完成借还的部分
    missing_features = df_data.isnull().mean().sort_values(ascending=False)
    drop_list = sorted(list(missing_features[missing_features > 0.3].index))
    df_data.drop(labels=drop_list, axis=1, inplace=True)
    #删除缺失值较多的特征
    keep_list_kd = ['addr_state', 'annual_inc', 'application_type', 'dti', 'earliest_cr_line', 'emp_length',
                    'fico_range_high', 'fico_range_low', 'home_ownership', 'initial_list_status',
                    'installment', 'int_rate', 'issue_d', 'loan_amnt', 'loan_status', 'mort_acc', 'open_acc', 'pub_rec',
                    'pub_rec_bankruptcies', 'purpose', 'revol_bal', 'revol_util', 'sub_grade', 'term', 'total_acc',
                    'verification_status']

    df_data = df_data[keep_list_kd]

    df_data['term'] = df_data['term'].apply(lambda s: s.split()[0]).value_counts(normalize=True)
    df_data['emp_length'].replace(to_replace='10+ years', value='10 years', inplace=True)
    df_data['emp_length'].replace('< 1 year', '0 years', inplace=True)
    df_data['emp_length'] = df_data['emp_length'].apply(emp_length_to_int)
    df_data['home_ownership'].replace(['NONE', 'ANY'], 'OTHER', inplace=True)
    df_data['log_annual_inc'] = df_data['annual_inc'].apply(lambda x: np.log10(x + 1))
    df_data.drop('annual_inc', axis=1, inplace=True)
    df_data['earliest_cr_line'] = df_data['earliest_cr_line'].apply(lambda s: int(s[-4:]))
    df_data['fico_score'] = 0.5 * df_data['fico_range_low'] + 0.5 * df_data['fico_range_high']
    df_data.drop(['fico_range_high', 'fico_range_low'], axis=1, inplace=True)
    df_data['log_revol_bal'] = df_data['revol_bal'].apply(lambda x: np.log10(x + 1))
    df_data.drop('revol_bal', axis=1, inplace=True)
    df_data['loan_label'] = (df_data['loan_status'] == 'Charged Off').apply(np.uint8)
    df_data.drop('loan_status', axis=1, inplace=True)

    object_column_list = []#离散型特征
    values_column_list = []#连续型特征
    columns_list = list(df_data.columns)
    columns_list.remove('loan_label')
    columns_list.remove('issue_d')

    for column_temp in list(columns_list):
        if len(df_data[column_temp].unique()) < 200:
            object_column_list.append(column_temp)
        else:
            values_column_list.append(column_temp)
    #删除变化不大的特征

    df_data[values_column_list] = (df_data[values_column_list] - df_data[values_column_list].min()) / \
                               (df_data[values_column_list].max() - df_data[values_column_list].min())
    #归一化

    bag_size = 0
    for column_temp in object_column_list:
        dict_temp = {}
        for i in df_data[column_temp].unique():
            dict_temp[i] = bag_size
            bag_size += 1
        df_data[column_temp] = df_data[column_temp].map(dict_temp)

    return df_data, values_column_list, object_column_list, bag_size

def cluster_analysis_uniq(data_all, cluster_attributes=10):
    dict_column = {}
    for column in list(data_all.columns):
        dict_column[column] = len(list(data_all[column].unique()))
    selected_attributes = []
    for column_temp in dict_column.keys():
        if dict_column[column_temp] < cluster_attributes:
            selected_attributes.append(column_temp)
    return selected_attributes


def data_cluster(data_all, columns_object, ratio_train=0.9):
    data_all['id'] = [i for i in range(len(data_all))]#添加唯一ID，有利于后序聚类处理追踪数据行
    data_all[columns_object] = data_all[columns_object].fillna(0)#对列进行筛选，并填充缺失值
    dict_group_ioc = {}#聚类字典，用于储存每一个数据点的聚类编号
    groups = data_all.groupby(columns_object)
    count = 0
    for temp_group in groups:
        temp = list(temp_group[1]['id'])
        dict_group_ioc_copy = dict_group_ioc
        dict_group_ioc_copy.update(dict(zip(temp, [count] * len(temp))))
        count += 1
    clusters = data_all['id'].map(dict_group_ioc_copy).tolist()
    data_all['clusters_group'] = clusters
    data_all['issue_d'] = pd.to_datetime(data_all['issue_d'])
    accepted_data = data_all.fillna(0)

    data_train = accepted_data.loc[accepted_data['issue_d'] < accepted_data['issue_d'].quantile(ratio_train)]
    data_test = accepted_data.loc[accepted_data['issue_d'] >= accepted_data['issue_d'].quantile(ratio_train)]
    data_train.drop('issue_d', axis=1, inplace=True)
    data_test.drop('issue_d', axis=1, inplace=True)
    #进行跨时间验证切割训练集与测试集

    train_cluster = list(data_train['clusters_group'])
    test_cluster = list(data_test['clusters_group'])
    data_train = data_train.drop(['id', 'clusters_group'], axis=1)
    data_test = data_test.drop(['id', 'clusters_group'], axis=1)
    return train_cluster, test_cluster, data_train, data_test


def intermediate_feature_distance(intermediate_features, label_batch):
    positive_vector = torch.mean(intermediate_features * label_batch.unsqueeze(-1).float(), dim=0)
    zero = torch.zeros_like(label_batch)
    label_temp = label_batch + 1
    label_negative = torch.where(label_temp==2, zero, label_temp)
    negative_vector = torch.mean(intermediate_features * label_negative.unsqueeze(-1).float(), dim=0)
    similarity = abs(torch.cosine_similarity(positive_vector, negative_vector, dim=0))
    return similarity


def matrix_connection(a, device='cuda'):
    a = a.to('cpu')
    a_array = a.numpy()#张量a转化为数组
    dict_index = {}
    for i in a.unique():
        dict_index[i.numpy().tolist()] = sum(np.argwhere(a_array == i.numpy()).tolist(), [])
    matrix_connect = np.zeros((len(a), len(a)))
    degree_matrix = np.zeros((len(a), len(a)))
    for index_column, i in enumerate(a):
        for j in dict_index[i.numpy().tolist()]:
            matrix_connect[index_column][j] = 1
        degree_matrix[index_column][index_column] = len(dict_index[i.numpy().tolist()])
    matrix_connect = torch.tensor(matrix_connect)
    degree_matrix = torch.inverse(torch.sqrt(torch.tensor(degree_matrix)))
    return matrix_connect.to(device), degree_matrix.to(device)

def training_model_classification(train_df, val_df, train_cluster, val_cluster, value_column, embed_column, bag_size, f,batchSize=512):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')




    train_data_value = torch.tensor(np.array(train_df[value_column])).float()
    train_data_embedd = torch.tensor(np.array(train_df[embed_column])).long()
    train_clusters = torch.tensor(np.array(train_cluster))
    train_data_label = torch.tensor(np.array(train_df['loan_label'])).long()
    torch_dataset = Data.TensorDataset(train_data_value, train_data_embedd, train_clusters, train_data_label)
    loader = Data.DataLoader(dataset=torch_dataset, shuffle=True, batch_size=batchSize)


    val_data_value = torch.tensor(np.array(val_df[value_column])).float()
    val_data_embedd = torch.tensor(np.array(val_df[embed_column])).long()
    val_clusters = torch.tensor(np.array(val_cluster))
    val_data_label = torch.tensor(np.array(val_df['loan_label'])).long()
    val_torch_dataset = Data.TensorDataset(val_data_value, val_data_embedd, val_clusters, val_data_label)
    val_loader = Data.DataLoader(dataset=val_torch_dataset, shuffle=True, batch_size=batchSize)

    epochs = opt.epoch
    model = CLASS_NN_Embed_cluster(embedd_columns_num=len(embed_column), values_columns_num=len(value_column),
                                   bag_size=bag_size).to(device)

    optimizer = opt.optimizer(model.parameters(), lr=0.001, weight_decay=opt.l2)
    schedule = torch.optim.lr_scheduler.StepLR(optimizer, opt.step_size, gamma=0.1, last_epoch=-1)

    criterion_1 = nn.CrossEntropyLoss()
    criterion_2 = nn.MSELoss()
    lam = opt.lambda_
    alp = opt.alpha_
    beta = opt.beta_

    best_auc_val = 0
    count = 0
    flag_earlystop = 0
    for epoch in range(epochs):
        loss = 0
        for batch_data in loader:
            model.train()
            inputs_value = batch_data[0].to(device)
            inputs_embed = batch_data[1].to(device)
            inputs_cluster = batch_data[2].to(device)
            optimizer.zero_grad()
            outputs_class, outputs_ae, intermediate_vector = model(inputs_value, inputs_embed, inputs_cluster)
            train_loss_class = criterion_1(outputs_class, batch_data[3].to(device))
            train_loss_ae = criterion_2(outputs_ae, torch.cat((batch_data[0].float(), batch_data[1].float()), -1).to(device))
            train_loss_ae /= batch_data[0].size()[0]
            # regularition = torch.norm(input=torch.matmul(model.context_layer, model.context_layer.transpose(-1, -2)) - torch.eye(model.context_layer.shape[1]).to(device), p='fro')
            cosine_sim = intermediate_feature_distance(intermediate_vector, batch_data[3].to(device))
            train_loss = lam * train_loss_class + alp * train_loss_ae + beta * cosine_sim

            train_loss.backward()
            optimizer.step()
            loss += train_loss.item()
        loss = loss / len(loader)
        f.writelines('Loss in Epoch {0}: {1}'.format(epoch, loss) + '\n')
        print('Loss in Epoch {0}: {1}'.format(epoch, loss))
        animator.add("val_loss", epoch, loss)
        count += 1
        auc_val = []
        with torch.no_grad():
            for batch_data in val_loader:
                model.eval()
                inputs_value = batch_data[0].to(device)
                inputs_embed = batch_data[1].to(device)
                inputs_cluster = batch_data[2].to(device)
                optimizer.zero_grad()
                outputs, _, _ = model(inputs_value, inputs_embed, inputs_cluster)
                output_train = list(F.softmax(outputs, dim=-1).cpu().numpy()[:, 1])  ## crossentropy loss
                auc_val.append(auc_calculate(batch_data[3].numpy(), output_train))
            print('Val AUC in Epoch {0}: {1}'.format(epoch, np.mean(auc_val)))

            f.writelines('Val AUC in Epoch {0}: {1}'.format(epoch, np.mean(auc_val)) + '\n')

        if np.mean(auc_val) > best_auc_val:
            best_auc_val = np.mean(auc_val)
            print('Best Val AUC in Epoch {0}: {1}'.format(epoch, best_auc_val))
            f.writelines('Best Val AUC in Epoch {0}: {1}'.format(epoch, best_auc_val) + '\n')
            best_model = model
            count = 0

        if count > opt.early_stop_epoch:
            flag_earlystop = 1
            print('Save epoch {0}'.format(epoch))
            f.writelines('Save epoch {0}'.format(epoch) + '\n')
            path_model = os.path.join(opt.path, time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()) + '_early_stop_best_model_' + str(epoch) + '.pth')
            torch.save(best_model.state_dict(), path_model)
            f.writelines('Early stop' + '\n')
            print('Early stop')
            break
        schedule.step()

    if flag_earlystop == 0:
        path_model = os.path.join(opt.path, time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()) + '_best_model_' + str(epoch) + '.pth')
        torch.save(best_model.state_dict(), path_model)

    if opt.intermediate_vector_save:
        train_loader_copy = Data.DataLoader(dataset=torch_dataset, shuffle=False, batch_size=opt.batchSize)
        val_loader_copy = Data.DataLoader(dataset=val_torch_dataset, shuffle=False, batch_size=opt.batchSize)
        train_feature = {'feature_intermediate': []}
        val_feature = {'feature_intermediate': []}
        with torch.no_grad():
            for batch_data in train_loader_copy:
                best_model.eval()
                inputs_value = batch_data[0].to(device)
                inputs_embed = batch_data[1].to(device)
                inputs_cluster = batch_data[2].to(device)
                optimizer.zero_grad()
                outputs, _, _ = best_model(inputs_value, inputs_embed, inputs_cluster)
                train_feature['feature_intermediate'] += best_model.output_0.cpu().numpy().tolist()

            for batch_data in val_loader_copy:
                best_model.eval()
                inputs_value = batch_data[0].to(device)
                inputs_embed = batch_data[1].to(device)
                inputs_cluster = batch_data[2].to(device)
                optimizer.zero_grad()
                outputs, _, _ = best_model(inputs_value, inputs_embed, inputs_cluster)
                val_feature['feature_intermediate'] += best_model.output_0.cpu().numpy().tolist()

            with open(os.path.join(opt.path, time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()) + 'train_features_intermediate.pkl'), 'wb') as f:
                pickle.dump(train_feature, f, pickle.HIGHEST_PROTOCOL)

            with open(os.path.join(opt.path, time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()) + 'val_features_intermediate.pkl'), 'wb') as f:
                pickle.dump(val_feature, f, pickle.HIGHEST_PROTOCOL)


    return best_auc_val














df_data = data_load('../../data/sample/lending_club_sample.csv')
data_all, columns_value, columns_embed, bag_size = data_preprocessing(df_data)
'''
accepted_data: pandas.DataFrame - 处理后的数据集
values_column_list: list - 数值特征列名list
object_column_list: list - 文字特征列名list
start_encode: int - 记录离散型变量所有取值总数目（词汇表的大小）
'''
selected_attributes = cluster_analysis_uniq(data_all)
#selected_attributes为最终选用的构建图的特征list
train_cluster, test_cluster, train_df, test_df = data_cluster(data_all, selected_attributes)
'''
train_cluster:list 用于记录每一个id对应样本点的聚类划分
train_df：dataframe
'''

val_best = training_model_classification(train_df, test_df, train_cluster, test_cluster, columns_value,
                                         columns_embed, bag_size, f)

print('Best AUC: {0}'.format(np.round(val_best, 5)))
f.close()
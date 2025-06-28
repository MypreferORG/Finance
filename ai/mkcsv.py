import pandas as pd
# from finance.models import UserAuth  # 假设有一个 UserAuth 模型用于获取用户 ID

# 1. 读取原始 CSV 文件
df = pd.read_csv('lending_club_sample.csv')  # 请将 'path_to_csv' 替换为实际文件路径

# 2. 初始化存储转换后数据的列表
user_app_data = []  # 用于存储 UserApplication 数据
user_beh_data = []  # 用于存储 UserBehavior 数据

# 3. 遍历每一行数据并进行转换
user_id =0
for index, row in df.iterrows():
    user_id += 1
    # 获取用户 ID
    # try:
    #     user = UserAuth.get(UserAuth.member_id == row['member_id'])
    # except UserAuth.DoesNotExist:
    #     print(f"用户 member_id {row['member_id']} 未找到，跳过此行。")
    #     continue

    # UserApplication 数据转换
    user_app = {
        'user_id': user_id,
        'loan_status': row['loan_status'],
        'real_name_verified': (row['verification_status'] == 'Verified') if pd.notnull(row['verification_status']) else False,
        'age': None,
        'is_student': ('student' in row['emp_title'].lower()) if pd.notnull(row['emp_title']) else False,
        'is_blacklisted': (row['delinq_2yrs'] > 0) if pd.notnull(row['delinq_2yrs']) else False,
        'is_unhealthy_4g_user': False,
        'network_age_months': int(row['emp_length'].split()[0]) if pd.notnull(row['emp_length']) and row['emp_length'].split()[0].isdigit() else None,
        'last_payment_months_ago': row['mths_since_last_delinq'] if pd.notnull(row['mths_since_last_delinq']) else None,
        'last_payment_amount': row['last_pymnt_amnt'] if pd.notnull(row['last_pymnt_amnt']) else row['loan_amnt'],
        'avg_monthly_spending_6_months': row['installment'] if pd.notnull(row['installment']) else None,
        'current_bill_total': row['funded_amnt'] if pd.notnull(row['funded_amnt']) else None,
        'current_account_balance': row['tot_cur_bal'] if pd.notnull(row['tot_cur_bal']) else row['funded_amnt_inv'],
        'has_outstanding_payment': (row['loan_status'] in ['Late (16-30 days)', 'Late (31-120 days)']) if pd.notnull(row['loan_status']) else False,
        'call_fee_sensitivity': None,
        'contacts_this_month': row['inq_last_6mths'] if pd.notnull(row['inq_last_6mths']) else None,
        'is_frequent_mall_visitor': False,
        'avg_mall_visits_3_months': None,
        'visited_fuzhou_cangshan_wanda': False,
        'visited_fuzhou_sam_club': False,
        'watched_movie': False,
        'visited_scenic_spot': False,
        'used_sports_facility': False,
        'online_shopping_app_usage': None,
        'logistics_app_usage': None,
        'finance_app_usage': None,
        'video_app_usage': None,
        'airplane_app_usage': None,
        'train_app_usage': None,
        'travel_info_app_usage': None,
        'credit_score': row['fico_range_low'] if pd.notnull(row['fico_range_low']) else None,
        'created_at': row['issue_d'] if pd.notnull(row['issue_d']) else None,
        'updated_at': row['last_pymnt_d'] if pd.notnull(row['last_pymnt_d']) else None,
    }
    user_app_data.append(user_app)

    # UserBehavior 数据转换
    user_beh = {
        'user_id': user_id,
        'loan_status': row['loan_status'],
        'age': None,
        'bank_cards_count': row['open_acc'] if pd.notnull(row['open_acc']) else None,
        'remote_transaction_months': None,
        'internet_transaction_avg': None,
        'financial_transaction_months': row['mths_since_last_delinq'] if pd.notnull(row['mths_since_last_delinq']) else None,
        'financial_transaction_avg_amount': row['total_pymnt'] if pd.notnull(row['total_pymnt']) else None,
        'max_loan_amount_180_days': row['loan_amnt'] if pd.notnull(row['loan_amnt']) else None,
        'min_loan_amount_180_days': row['funded_amnt'] if pd.notnull(row['funded_amnt']) else None,
        'apply_loan_company_number': row['inq_last_6mths'] if pd.notnull(row['inq_last_6mths']) else None,
        'created_at': row['issue_d'] if pd.notnull(row['issue_d']) else None,
        'updated_at': row['last_pymnt_d'] if pd.notnull(row['last_pymnt_d']) else None,
    }
    user_beh_data.append(user_beh)

# 4. 创建 DataFrame
user_app_df = pd.DataFrame(user_app_data)
user_beh_df = pd.DataFrame(user_beh_data)

# 5. 保存为 CSV 文件
user_app_df.to_csv('user_application.csv', index=False, na_rep='')
user_beh_df.to_csv('user_behavior.csv', index=False, na_rep='')

print("CSV 文件已成功保存！")
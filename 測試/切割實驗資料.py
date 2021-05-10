#!/usr/bin/env python
# coding: utf-8

# In[19]:


import pandas as pd


# In[2]:


df = pd.read_csv('mid_user_convert.csv')
del df['Unnamed: 0']
df = df.dropna(axis=0, how='any')
df


# In[11]:


# 刪除評論數量小於10的
for user in all_user:
    if len(df[df['Author'].str.contains(user,"$")]['Author'].tolist()) < 10:
        df = df[~df['Author'].str.contains(user,"$")]


# In[20]:


# 刪除重複評論的
df.drop_duplicates(subset = ['Author','Mid'],keep='first',inplace=True)
df


# # 相似度資料

# In[3]:


# 評論特徵相似度
review_senti = pd.read_csv('review_senti_corr.csv')

# 基本資料相似度
basic_sim = pd.read_csv('similarity_basic_data_v2.csv')

# 劇情特徵相似度
plot_sim = pd.read_csv('similarity_keyword.csv')


# In[114]:


review_senti


# # 列出user和movie

# In[21]:


# all user
all_user = df['Author'].tolist()
all_user = list(set(all_user))
print(len(all_user))


# In[22]:


# all movie
all_movie = df['Mid']
all_movie = list(set(all_movie))
print(len(all_movie))


# In[23]:


# 補值完totall數量
print(len(all_user)*len(all_movie))


# In[47]:


# # 新增列
# new = {"Author": "x06",
#         "Mid":"A",
#         "Date":"小倪",
#         "Rating":20,
#         "timestamp":25,
#         'id_convert': None,
#         'user_convert': None}
# df = df.append(new, ignore_index=True)
# df


# In[24]:


# df[df['Author'].str.contains('851222')]['user_convert'][0:1].values[0]
# uid與mid綁定

uid_dict = {}
mid_dict = {}

for user in all_user:
    uid_dict[user] = df[df['Author'].str.contains(user)]['user_convert'][0:1].values[0]

for movie in all_movie:
    mid_dict[movie] = df[df['Mid'].str.contains(movie)]['id_convert'][0:1].values[0]


# # TIMESTAMP補值

# In[25]:


timestamp_mean = {}
for m in all_movie:
    print(df[df['Mid'].str.contains(m)]['Rating'].count())
    break


# In[26]:


# timestamp mean imputation
# df[df['Mid'].str.contains(all_movie[0])]['timestamp'].tolist()
# type(df[df['Mid'].str.contains(all_movie[0])]['timestamp'].tolist()[0])
# round(sum(df[df['Mid'].str.contains(all_movie[0])]['timestamp'].tolist())/len(df[df['Mid'].str.contains(all_movie[0])]['timestamp'].tolist()))

mean_timestamp = {}
for m in all_movie:
    mean_timestamp[m] = round(sum(df[df['Mid'].str.contains(m)]['timestamp'].tolist())/len(df[df['Mid'].str.contains(m)]['timestamp'].tolist()))
mean_timestamp


# In[27]:


# timestamp release time plus 7
from datetime import datetime
plus7 = pd.read_csv('plus7.txt', sep=',')
plus7


# In[28]:


for i in range(60):
    plus7['movie_url'][i] = plus7['movie_url'][i][27:36]


# In[29]:


for i in range(60):
    plus7['release_time'][i] = round(datetime.timestamp(datetime.strptime(plus7['release_time'][i][0:10], "%Y-%m-%d")))


# In[30]:


plus7


# # Item-Based Imputation

# #### (看過電影與未看過電影的相似度*所有看過電影的評分)/看過電影與未看過電影的相似度

# In[35]:


df_impu_test = df
totall_notrated = 0
totall_rated = 0
try:
    for user in all_user:

        user_rated = df[df['Author'].str.contains(user)]['Mid'].tolist()
#         print('user_rated: ', user_rated)
        user_not_rated = list(set(all_movie)^set(user_rated))
#         print('user_not_rated: ', user_not_rated)
        totall_notrated += len(user_not_rated)
        totall_rated += len(user_rated)

    print(totall_notrated)
    print(totall_rated)
    print(totall_notrated+totall_rated)


except Exception as e:
    print(e)
        
        
        
        
        
        
df_impu_test


# In[36]:


df_impu_test = df
try:
    for user in all_user:

        user_rated = df[df['Author'].str.contains(user)]['Mid'].tolist()
#         print('user_rated: ', user_rated)
        user_not_rated = list(set(all_movie)^set(user_rated))
#         print('user_not_rated: ', user_not_rated)

        for not_rated_movie in user_not_rated:
            
            # 更換相似度資料集
#             find_sim = review_senti[review_senti['Unnamed: 0'].str.contains(not_rated_movie)]
#             find_sim = basic_sim[basic_sim['Mid'].str.contains(not_rated_movie)]
            find_sim = plot_sim[plot_sim['Mid'].str.contains(not_rated_movie)]
#             print('find_sim: ', type(find_sim))

            totall_rated = 0
            totall_sim=0
            for rated_movie in user_rated:
                
                #更換相似度補值計算公式
                totall_rated += review_senti[review_senti['Unnamed: 0'].str.contains(not_rated_movie)][rated_movie].values[0] * df[df['Author'].str.contains(user)&df['Mid'].str.contains(rated_movie)]['Rating'].values[0]
                totall_sim += review_senti[review_senti['Unnamed: 0'].str.contains(not_rated_movie)][rated_movie].values[0]
                
#                 totall_rated += basic_sim[basic_sim['Mid'].str.contains(not_rated_movie)][rated_movie].values[0] * df[df['Author'].str.contains(user)&df['Mid'].str.contains(rated_movie)]['Rating'].values[0]
#                 totall_sim += basic_sim[basic_sim['Mid'].str.contains(not_rated_movie)][rated_movie].values[0]
    
#                 totall_rated += plot_sim[plot_sim['Mid'].str.contains(not_rated_movie)][rated_movie].values[0] * df[df['Author'].str.contains(user)&df['Mid'].str.contains(rated_movie)]['Rating'].values[0]
#                 totall_sim += plot_sim[plot_sim['Mid'].str.contains(not_rated_movie)][rated_movie].values[0]

#                 print('相似度: ', type(review_senti[review_senti['Unnamed: 0'].str.contains(not_rated_movie)][rated_movie]))
#                 print('評分: ', type(df[df['Author'].str.contains(user)&df['Mid'].str.contains(rated_movie)]['Rating']))
            print('totall_rated:', totall_rated)
            print('totall_sim: ', totall_sim)

                
#             print('totall_rated: ', totall_rated)
#             print('count: ', count)
            imputation_value = totall_rated/totall_sim
            if imputation_value <0:
                imputation_value = 1
            if imputation_value >10:
                imputation_value = 10
            # 某user對某部沒評分過的電影的預估補值
            print('user: ', user)
            print('not_rated_movie: ', not_rated_movie)
            print('imputation_value: ', imputation_value)
            print('int imputation_value: ', int(imputation_value+0.5))
            print(user)
            print(not_rated_movie)
            

            
#             # 增加補值dataframe的row
            
#             # 定義新增資料格式
            new = {"Author": user,
                    "Mid": not_rated_movie,
                    "Date": None,
                    "Rating": int(imputation_value+0.5),
                    "timestamp": mean_timestamp[not_rated_movie],
                    'id_convert': None,
                    'user_convert': None}
            print(new)
            
#             # 寫入df
            df_impu_test = df_impu_test.append(new, ignore_index=True)
                
                
                
                
                
except Exception as e:
    print(e)
        
df_impu_test        


# In[37]:


df_impu_test2 = df
try:
    for user in all_user:

        user_rated = df[df['Author'].str.contains(user)]['Mid'].tolist()
#         print('user_rated: ', user_rated)
        user_not_rated = list(set(all_movie)^set(user_rated))
#         print('user_not_rated: ', user_not_rated)

        for not_rated_movie in user_not_rated:
            
            # 更換相似度資料集
#             find_sim = review_senti[review_senti['Unnamed: 0'].str.contains(not_rated_movie)]
#             find_sim = basic_sim[basic_sim['Mid'].str.contains(not_rated_movie)]
            find_sim = plot_sim[plot_sim['Mid'].str.contains(not_rated_movie)]
#             print('find_sim: ', type(find_sim))

            totall_rated = 0
            totall_sim=0
            for rated_movie in user_rated:
                
                #更換相似度補值計算公式
#                 totall_rated += review_senti[review_senti['Unnamed: 0'].str.contains(not_rated_movie)][rated_movie].values[0] * df[df['Author'].str.contains(user)&df['Mid'].str.contains(rated_movie)]['Rating'].values[0]
#                 totall_sim += review_senti[review_senti['Unnamed: 0'].str.contains(not_rated_movie)][rated_movie].values[0]
                
                totall_rated += basic_sim[basic_sim['Mid'].str.contains(not_rated_movie)][rated_movie].values[0] * df[df['Author'].str.contains(user)&df['Mid'].str.contains(rated_movie)]['Rating'].values[0]
                totall_sim += basic_sim[basic_sim['Mid'].str.contains(not_rated_movie)][rated_movie].values[0]
    
#                 totall_rated += plot_sim[plot_sim['Mid'].str.contains(not_rated_movie)][rated_movie].values[0] * df[df['Author'].str.contains(user)&df['Mid'].str.contains(rated_movie)]['Rating'].values[0]
#                 totall_sim += plot_sim[plot_sim['Mid'].str.contains(not_rated_movie)][rated_movie].values[0]

#                 print('相似度: ', type(review_senti[review_senti['Unnamed: 0'].str.contains(not_rated_movie)][rated_movie]))
#                 print('評分: ', type(df[df['Author'].str.contains(user)&df['Mid'].str.contains(rated_movie)]['Rating']))
            print('totall_rated:', totall_rated)
            print('totall_sim: ', totall_sim)

                
#             print('totall_rated: ', totall_rated)
#             print('count: ', count)
            imputation_value = totall_rated/totall_sim
            if imputation_value <0:
                imputation_value = 1
            if imputation_value >10:
                imputation_value = 10
            # 某user對某部沒評分過的電影的預估補值
            print('user: ', user)
            print('not_rated_movie: ', not_rated_movie)
            print('imputation_value: ', imputation_value)
            print('int imputation_value: ', int(imputation_value+0.5))
            print(user)
            print(not_rated_movie)
            

            
#             # 增加補值dataframe的row
            
#             # 定義新增資料格式
            new = {"Author": user,
                    "Mid": not_rated_movie,
                    "Date": None,
                    "Rating": int(imputation_value+0.5),
                    "timestamp": mean_timestamp[not_rated_movie],
                    'id_convert': None,
                    'user_convert': None}
            print(new)
            
#             # 寫入df
            df_impu_test2 = df_impu_test2.append(new, ignore_index=True)
                
                
                
                
                
except Exception as e:
    print(e)
        
df_impu_test2        


# In[38]:


df_impu_test3 = df
try:
    for user in all_user:

        user_rated = df[df['Author'].str.contains(user)]['Mid'].tolist()
#         print('user_rated: ', user_rated)
        user_not_rated = list(set(all_movie)^set(user_rated))
#         print('user_not_rated: ', user_not_rated)

        for not_rated_movie in user_not_rated:
            
            # 更換相似度資料集
#             find_sim = review_senti[review_senti['Unnamed: 0'].str.contains(not_rated_movie)]
#             find_sim = basic_sim[basic_sim['Mid'].str.contains(not_rated_movie)]
            find_sim = plot_sim[plot_sim['Mid'].str.contains(not_rated_movie)]
#             print('find_sim: ', type(find_sim))

            totall_rated = 0
            totall_sim=0
            for rated_movie in user_rated:
                
                #更換相似度補值計算公式
#                 totall_rated += review_senti[review_senti['Unnamed: 0'].str.contains(not_rated_movie)][rated_movie].values[0] * df[df['Author'].str.contains(user)&df['Mid'].str.contains(rated_movie)]['Rating'].values[0]
#                 totall_sim += review_senti[review_senti['Unnamed: 0'].str.contains(not_rated_movie)][rated_movie].values[0]
                
                totall_rated += basic_sim[basic_sim['Mid'].str.contains(not_rated_movie)][rated_movie].values[0] * df[df['Author'].str.contains(user)&df['Mid'].str.contains(rated_movie)]['Rating'].values[0]
                totall_sim += basic_sim[basic_sim['Mid'].str.contains(not_rated_movie)][rated_movie].values[0]
    
#                 totall_rated += plot_sim[plot_sim['Mid'].str.contains(not_rated_movie)][rated_movie].values[0] * df[df['Author'].str.contains(user)&df['Mid'].str.contains(rated_movie)]['Rating'].values[0]
#                 totall_sim += plot_sim[plot_sim['Mid'].str.contains(not_rated_movie)][rated_movie].values[0]

#                 print('相似度: ', type(review_senti[review_senti['Unnamed: 0'].str.contains(not_rated_movie)][rated_movie]))
#                 print('評分: ', type(df[df['Author'].str.contains(user)&df['Mid'].str.contains(rated_movie)]['Rating']))
            print('totall_rated:', totall_rated)
            print('totall_sim: ', totall_sim)

                
#             print('totall_rated: ', totall_rated)
#             print('count: ', count)
            imputation_value = totall_rated/totall_sim
            if imputation_value <0:
                imputation_value = 1
            if imputation_value >10:
                imputation_value = 10
            # 某user對某部沒評分過的電影的預估補值
            print('user: ', user)
            print('not_rated_movie: ', not_rated_movie)
            print('imputation_value: ', imputation_value)
            print('int imputation_value: ', int(imputation_value+0.5))
            print(user)
            print(not_rated_movie)
            

            
#             # 增加補值dataframe的row
            
#             # 定義新增資料格式
            new = {"Author": user,
                    "Mid": not_rated_movie,
                    "Date": None,
                    "Rating": int(imputation_value+0.5),
                    "timestamp": mean_timestamp[not_rated_movie],
                    'id_convert': None,
                    'user_convert': None}
            print(new)
            
#             # 寫入df
            df_impu_test3 = df_impu_test3.append(new, ignore_index=True)
                
                
                
                
                
except Exception as e:
    print(e)
        
df_impu_test3        


# In[41]:


for user in all_user:
#     if len(df_impu_test[df_impu_test['Author'].str.contains(user)]['Mid'].tolist()) < 60:
#         print(user)
    print(user)
    print(len(df_impu_test[df_impu_test['Author'].str.contains(user)]['Mid'].tolist()))


# In[45]:


df_impu_test.to_csv('review_senti_impu_v1.csv')


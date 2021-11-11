import streamlit as st
import pandas as pd
import datetime
import re
import csv

st.title('クリーンルーム予約')
st.write('荒木研　＠機械工学2号棟　309a室')
st.subheader('現在の予約状況')
#expander=st.expander('CSVの書式')
#expander.write('① CSV形式のみ対応')
#expander.write('② インデックス無し，1行目がカラムになります．')
#expander.write('③ 右下のダウンロードボタンでテンプレをダウンロードできます．')

#df=pd.DataFrame({'x1':[0,1,2,3],'x2':[5,8,8,9],'x3':[2,4,6,8]})
df=pd.read_csv('CR_date.csv',index_col='Date')
df_date=df.index.values

column_1,column_2=st.columns(2)    
month_list=[x+1 for x in range(12)]
year_list=[2021+x for x in range(20)]


option_y = column_1.selectbox('Year(表示)',year_list,key=1)
option_m = column_2.selectbox('Month(表示)',month_list,key=2)


if st.button('Today(今日から表示)'):
    dt_now = datetime.datetime.now()
    date_view_s=str(dt_now.year)+'/'+str(dt_now.month)+'/'+str(dt_now.day)   
    date_view_s_index=df.index.get_loc(date_view_s)
    df_view=df.iloc[date_view_s_index:date_view_s_index+60,:]   
    st.dataframe(df_view,width=1000, height=500)
else:    
    date_view_s=str(option_y)+'/'+str(option_m)+'/1'
    date_view_s_index=df.index.get_loc(date_view_s)
    df_view=df.iloc[date_view_s_index:date_view_s_index+60,:]
    st.dataframe(df_view,width=1000, height=500)

st.subheader('予約入力/削除')

st.write('<予約日時>')
column_1,column_2=st.columns(2)   
option_y_2 = column_1.selectbox('Year(予約)',year_list,key=3)
option_m_2 = column_2.selectbox('Month(予約)',month_list,key=4)

date_num=0
for i in range(len(df_date)):
    d=re.match(str(option_y_2)+'/'+str(option_m_2)+'/',df_date[i])
    if d!=None:
        date_num+=1
day_list=[x+1 for x in range(date_num)]    
option_d_2 = column_1.selectbox('Day(予約)',day_list,key=5)

reserv_date=str(option_y_2)+'/'+str(option_m_2)+'/'+str(option_d_2)

column_1,column_2=st.columns(2)
hour_list=[x+8 for x in range(15)]
min_list=['00','15','30','45']   
option_h_2 = column_1.selectbox('予約開始時刻(時)',hour_list,key=6)
option_m_2 = column_2.selectbox('予約開始時刻(分)',min_list,key=7)
option_h_e_2 = column_1.selectbox('予約終了時刻(時)',hour_list,key=8)
option_m_e_2 = column_2.selectbox('予約終了時刻(分)',min_list,key=9)

machine_list=['スパッタ装置','パリレン装置','リソグラフィー装置']
option_macine_2 = st.selectbox('<使用装置>',machine_list,key=10)

st.write('<使用者>')
column_1,column_2=st.columns(2)  
lab_list=['荒木研','太田研','福田研','その他']
option_lab_2 = column_1.selectbox('所属研究室',lab_list,key=11)
txt_name=column_2.text_input('名前')


txt_others=st.text_input('<備考（何かあれば）>')
    

if st.button('予約確定'):
    if df.loc[reserv_date,'Time_start']=='-':
        df.loc[reserv_date,'Time_start']=str(option_h_2)+':'+str(option_m_2)
        df.loc[reserv_date,'Time_end']=str(option_h_e_2)+':'+str(option_m_e_2)
        df.loc[reserv_date,'Machine']=str(option_macine_2)
        df.loc[reserv_date,'User_lab']=str(option_lab_2)
        df.loc[reserv_date,'User_name']=str(txt_name)
        df.loc[reserv_date,'Others']=str(txt_others)
        
        df_data=df.values
        df_col=df.columns.values
        df_index=df.index.values
        
        df.to_csv('CR_date.csv',encoding='utf_8_sig')  
        df=pd.read_csv('CR_date.csv',header=None)
        df.iloc[0,0]='Date'
        df.to_csv('CR_date.csv', header=False, index=False,encoding='utf_8_sig')
        df=pd.read_csv('CR_date.csv',index_col='Date')
        df_view=df.loc[reserv_date,:]   
        st.dataframe(df_view)    
    
    else:
        reserv_num=2
        for i in range(len(df_date)):
            reserv_date_2=re.compile('.>'+reserv_date)
            r_d=re.fullmatch(reserv_date_2,df_date[i])
            if r_d!=None:
                reserv_num+=1
                
        df_add=pd.DataFrame({
            'Time_start':[str(option_h_2)+':'+str(option_m_2)],
            'Time_end':[str(option_h_e_2)+':'+str(option_m_e_2)],
            'Machine':[str(option_macine_2)],
            'User_lab':[str(option_lab_2)],
            'User_name':[str(txt_name)],
            'Others':[str(txt_others)]
            },index=[str(reserv_num)+'>'+str(reserv_date)])

        df_add_index=df.index.get_loc(reserv_date)
        df_up=df.copy().iloc[:df_add_index+1+reserv_num-2,:] 
        df_low=df.iloc[df_add_index+1+reserv_num-2:,:]         
        df_up_2=pd.concat([df_up,df_add],axis=0)
        df=pd.concat([df_up_2,df_low],axis=0)
    
        df.to_csv('CR_date.csv',encoding='utf_8_sig')
        df=pd.read_csv('CR_date.csv',header=None)
        df.iloc[0,0]='Date'
        df.to_csv('CR_date.csv', header=False, index=False,encoding='utf_8_sig') 
        
        df=pd.read_csv('CR_date.csv',index_col='Date')
        df_view=df.loc[str(reserv_num)+'>'+str(reserv_date),:]   
        st.dataframe(df_view)


del_list=['Default','2>','3>','4>','5>']   
option_del_2 = st.selectbox('<削除番号>',del_list,key=12)
if option_del_2=='Default':
    option_del_2=''
    
if st.button('予約削除'):
    if option_del_2=='':
        df.loc[option_del_2+reserv_date,'Time_start']='-'
        df.loc[option_del_2+reserv_date,'Time_end']='-'
        df.loc[option_del_2+reserv_date,'Machine']='-'
        df.loc[option_del_2+reserv_date,'User_lab']='-'
        df.loc[option_del_2+reserv_date,'User_name']='-'
        df.loc[option_del_2+reserv_date,'Others']='-'
    else:
        df=df.drop(option_del_2+reserv_date, axis=0)
              
    df.to_csv('CR_date.csv')
    df=pd.read_csv('CR_date.csv',header=None)
    df.iloc[0,0]='Date'
    df.to_csv('CR_date.csv', header=False, index=False,encoding='utf_8_sig')    

    df=pd.read_csv('CR_date.csv',index_col='Date')
    df_view=df.loc[reserv_date,:]   
    st.dataframe(df_view)

st.write('リロードすれば，上部の表に反映されます')




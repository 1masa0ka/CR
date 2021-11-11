import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

code_library='''
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
'''
code_df='''
df=pd.DataFrame({'x1':[0,1,2,3],'x2':[5,8,8,9],'x3':[2,4,6,8]})
print(df)
'''
code_df_up='''
df=pd.read_csv('テンプレート.csv')
print(df)
'''
code_plt_plot='''
fig,ax=plt.subplots()
ax.plot(df.iloc[:,0],df.iloc[:,1])
ax.bar(df.iloc[:,0],df.iloc[:,2])
fig.show()
'''
code_plt_bar='''
fig,ax=plt.subplots()
ax.bar(df.iloc[:,0],df.iloc[:,1])
ax.bar(df.iloc[:,0],df.iloc[:,2])
fig.show()
'''
code_plt_hist='''
fig,ax=plt.subplots()
ax.hist([df.iloc[:,0],df.iloc[:,1],df.iloc[:,2]],bins=3,label=df.columns)
ax.legend()
fig.show()
'''

st.sidebar.title('Python コード')
expander_side=st.sidebar.expander('使い方')
expander_side.write('お手持ちのPythonエディタを開いて頂き，以下のコードを上から順にコピペで，同様の挙動を再現できると思います．')

st.sidebar.write('ライブラリ')
st.sidebar.code(code_library,language='python')

st.title('Analysis')
st.write('ver. 2021.11.4         Asaoka')


uploaded_file=st.file_uploader('↓ここにCSVデータをアップロード！')

expander=st.expander('CSVの書式')
expander.write('① CSV形式のみ対応')
expander.write('② インデックス無し，1行目がカラムになります．')
expander.write('③ 右下のダウンロードボタンでテンプレをダウンロードできます．')

df=pd.DataFrame({'x1':[0,1,2,3],'x2':[5,8,8,9],'x3':[2,4,6,8]})


left_column,right_column=st.columns(2)

csv=open('テンプレート.csv')
left_column.write('サンプルデータ')
right_column.download_button('Download:サンプルデータ',csv,file_name='テンプレート.csv',mime='csv')

if uploaded_file is not None:
    df=pd.read_csv(uploaded_file)
    st.write('現在のデータ')
    st.sidebar.write('データフレーム（uploaded）')
    st.sidebar.code(code_df_up,language='python')
else:
    st.sidebar.write('データフレーム（サンプル）')
    st.sidebar.code(code_df,language='python')

st.dataframe(df)
    
graph_list=['折れ線グラフ(Streamlit)',
            '棒グラフ(Streamlit)',
            'ヒストグラム(pyplot)']
option=st.selectbox('グラフの種類',graph_list)

if option == graph_list[0]:
    st.line_chart(df)
    st.sidebar.write('折れ線グラフ')
    st.sidebar.code(code_plt_plot,language='python')
elif option==graph_list[1]:
    st.bar_chart(df)
    st.sidebar.write('棒グラフ')
    st.sidebar.code(code_plt_bar,language='python')
elif option==graph_list[2]:
    fig,ax=plt.subplots()
    ax.hist(df,bins=3,label=df.columns)
    ax.legend()
    st.pyplot(fig)
    st.sidebar.write('ヒストグラム')
    st.sidebar.code(code_plt_hist,language='python')    

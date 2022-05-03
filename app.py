import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mlt
import streamlit as st
import seaborn as sns

def main():
    st.title('Perform data science processes effortlessly...')

    def file_select(folder = './sample_dataset'):
        file = os.listdir(folder)
        selectfile = st.selectbox('select the default file',file)
        return os.path.join(folder,selectfile)

    if st.checkbox('Select dataset from local machine'):
        data = st.file_uploader('Upload Dataset in .csv',type=['CSV'])
        if data is not None:
            df = pd.read_csv(data)
    else:
        file_default = file_select()
        #st.info('you seelcted {}',format(file_default))
        if file_default is not None:
            df = pd.read_csv(file_default)


    st.subheader('Explore the data')
    eda_1 = st.radio("",('Show Dataset','Columns','Shape','Data Type','Unique values','Null values','Summary/Describe'))

    if eda_1 == 'Show Dataset':
        num = st.number_input('No. of Rows',5,10)
        st.dataframe(df.head(num))
    
    elif eda_1 == 'Columns':
        st.write(df.columns)

    elif eda_1 == 'Shape':
        st.text('(Rows,Columns)')
        st.write(df.shape)

    elif eda_1 == 'Data Type':
        st.dataframe(df.dtypes)

    elif eda_1 == 'Unique values':
        st.dataframe(df.nunique())
        selectedcol = st.selectbox('Select column to see unique values',df.columns.tolist())
        st.write(df[selectedcol].unique())
    
    elif eda_1 == 'Null values':
        st.dataframe(df.isnull().sum())
        
    elif eda_1 == 'Summary/Describe':
        st.write(df.describe())

    st.text(" ")
    st.text(" ")

    st.subheader('Data Visualization')
    # Seaborn correlation plot
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.text('➢ Visualize the degree of association between variables:')
    if st.checkbox('Correlation plot'):
        st.write(sns.heatmap(df.corr(),annot=True))
        st.pyplot()

    # Univariate distribution
    st.text(" ")
    st.text('➢ Visualize and explore each variable seperately:')
    
    if st.checkbox('Univariate Distribution'):
        cols = df.columns.tolist()
        selected_col = st.selectbox('Select columns to plot',cols)
        binnum = st.number_input('No. of bins',10,50)
        st.write(sns.displot(df[selected_col],bins=binnum))
        st.pyplot()

    #Bivariate distribution
    st.text(" ")
    st.text('➢ Visualize the relationship between two variables:')

    if st.checkbox('Bivariate Distribution'):
        cols = df.columns.tolist()
        st.text('Select two columns')
        x= st.selectbox('Select X-axis columns to plot',cols)
        y= st.selectbox('Selct Y-axis columns to plot',cols)
        kindtype = st.selectbox('Select plot kind',['none','reg','resid','hex','kde'])
        if kindtype!= 'none':
            st.write(sns.jointplot(df[x],df[y],kind=kindtype))
            st.pyplot()
        else:
            st.write(sns.jointplot(df[x],df[y]))
            st.pyplot()

    # Categorical Distribution
    st.text(" ")
    st.text('➢ Visualize the categorical distribution:')

    if st.checkbox('Categorical Distribution'):
        cols = df.columns.tolist()
        cols.insert(0,'none')
        plottype = st.selectbox('Select plot type',['box','bar','violin','count','point'])
        x = st.selectbox('Select x-axis(categorical) column to plot',cols)
        y = st.selectbox('Selct y-axis(numerical) column to plot',cols)
        hue_val = st.selectbox('Select a hue column',cols)
        #box plot
        if plottype == 'box':
            if hue_val != 'none':
                st.write(sns.boxenplot(df[x],df[y],hue=df[hue_val]))
                st.pyplot()
            else:
                st.write(sns.boxenplot(df[x],df[y]))
                st.pyplot()
        #bar plot
        if plottype=='bar':
            if hue_val!='none':
                st.write(sns.barplot(df[x],df[y],hue=df[hue_val]))
                st.pyplot()
            else:
                st.write(sns.barplot(df[x],df[y]))
                st.pyplot()    
        #violin plot
        if plottype=='violin':
            if hue_val!='none':
                st.write(sns.violinplot(df[x],df[y],hue=df[hue_val]))
                st.pyplot()
            else:
                st.write(sns.violinplot(df[x],df[y]))
                st.pyplot()    
        #count plot
        if plottype=='count':
            st.text('Plotting countplot for selected X column')
            if hue_val!='none':
                st.write(sns.countplot(df[x],hue=df[hue_val]))
                st.pyplot()
            else:
                st.write(sns.countplot(df[x]))
                st.pyplot()
        #point plot
        if plottype=='point':
            if hue_val!='none':
                st.write(sns.pointplot(df[x],df[y],hue=df[hue_val]))
                st.pyplot()
            else:
                st.write(sns.pointplot(df[x],df[y]))
                st.pyplot()

    # Linear relationship
    st.text(" ")
    st.text('➢ Visualize the Linear relationship between two numerical variables:')

    if st.checkbox('Linear Relationship'):
        cols = df.columns.tolist()
        cols.insert(0,'none')
        xval = st.selectbox('Select X-axis',cols)
        yval = st.selectbox('Select Y-axis',cols)
        hueval = st.selectbox('Select hue colummns',cols)
        if hueval !='none':
            st.write(sns.lmplot(x=xval, y=yval, hue=hueval, data=df))
            st.pyplot()
        else:
            st.write(sns.lmplot(x=xval, y=yval, data=df))
            st.pyplot()

    # Customized plots
    st.text(" ")
    st.text(" ")
    st.subheader('Customized plots')
    cols=df.columns.tolist()
    plottype=st.selectbox('Select plot type',['bar','hist','box','area','line','kde'])
    selectedcollist=st.multiselect('Select columns to plot',cols)

    if st.button('Generate plot'):
        st.success('Generating customizable {} plot for {}'.format(plottype,selectedcollist))
        #plot using streamlit
        if plottype=='area' :
            cusdata=df[selectedcollist]
            st.area_chart(cusdata)
        elif plottype=='bar' :
            cusdata=df[selectedcollist]
            st.bar_chart(cusdata)
        elif plottype=='line' :
            cusdata=df[selectedcollist]
            st.line_chart(cusdata)
        elif plottype :
            cusplot=df[selectedcollist].plot(kind=plottype)
            st.write(cusplot)
            st.pyplot()

        


if __name__=='__main__':
    main()
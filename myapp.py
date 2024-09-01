## Importing required libraries 
import numpy as np 
import pandas as pd
import plotly.express as px
import streamlit as st 


## setting web_page configuration 
st.set_page_config(
    page_title = "Data Science Portal",
    page_icon = "📊"  
)

## Title 
st.title(":rainbow[Exploratory Data Analysis Portal]")
## st.header(" :red[Explore Data with ease] ")
st.subheader(":rainbow[Explore Data with ease]" , divider="rainbow")

## Creating file uploader 
file = st.file_uploader(":red[Drop csv or execl files here]",type=["csv","xlsx"])

## Reading file 
if(file != None):
    if(file.name.endswith("csv")): ## if file is in csv format
        data = pd.read_csv(file)
    else :  ## if file is in excel format
        data = pd.read_excel(file)

    ## displaying data-set
    st.dataframe(data)
    st.info("File successfully uploaded",icon = "🔥" )

    ## basic info of dataset
    st.subheader(":rainbow[Basic Info of Data-set]",divider = "rainbow")

    ## Creating different tabs 
    tab1,tab2,tab3,tab4 = st.tabs(["Summary","Top and Bottom rows","Data-Types","Columns"])

    ## customizing tab1 
    with tab1 :
        st.subheader(":gray[Data-set contains]")
        st.write(f"Total no. of rows = {data.shape[0]}") ## shape[0] for rows
        st.write(f"Total no. of columns = {data.shape[1]}") ## shape[1] for columns
        st.subheader(":gray[Statistical Summary of Data-set]")
        st.dataframe(data.describe())
       
    ## customizing tab2
    with tab2 :
        ##  Top rows 
        st.subheader(":gray[Top Rows]")
        top_rows = st.slider("Select no. of rows",1,data.shape[0],5 , key = "top_slider")
        st.dataframe(data.head(top_rows))
        #3 Bottom rows 
        st.subheader(":gray[Bottom Rows]")
        bottom_rows = st.slider("Select no. of rows",1,data.shape[0],5 , key = "bottom_slider")
        st.dataframe(data.tail(bottom_rows))
        ## keys should be passed to differentiate sliders 

    ## customizing tab3
    with tab3 :
        st.subheader(":gray[Data-type of Columns]")
        st.dataframe(data.dtypes)

    ## customizing tab4
    with tab4 :
        st.subheader(":gray[Column Names]")
        st.dataframe(list(data.columns))

    ## Column Value Counts 
    st.subheader(":rainbow[Columns Value-counts]",divider = "rainbow")
    with st.expander("Value Counts"): ## create an dropdown expander
        col_1,col_2 = st.columns(2) ## create column divisions 
        with col_1:
            columns = st.selectbox("Choose Column",options = list(data.columns))
        with col_2:
            top_rows = st.number_input("Top Rows",min_value=1,step=1)

        ## Creating button
        count = st.button("Count")
        if(count==True):
            result = data[columns].value_counts().reset_index().head(top_rows)
            st.dataframe(result)
            st.subheader(":rainbow[Data Visualization]")
            ## bar chart
            fig1 = px.bar(data_frame=result,x = columns,y="count",text="count")
            st.plotly_chart(fig1)
            ## line plot
            fig2 = px.line(data_frame = result , x = columns , y = "count" , text="count")
            st.plotly_chart(fig2)
            ## pie chart
            fig3 = px.pie(data_frame = result , names = columns , values = "count")
            st.plotly_chart(fig3)
    
    ## Group By
    st.subheader(":rainbow[Group By : Simplify your Data Analysis]",divider = "rainbow")
    with st.expander("Group by Columns"):
        col1,col2,col3 = st.columns(3)
        with col1 :
            group_by_columns = st.multiselect("Choose columns to group by",options= list(data.columns))
            ## used multiselect to select multiple columns
        with col2 :
            operation_column = st.selectbox("Choose column for operation",options=list(data.columns))
        with col3 :
            operation = st.selectbox("Choose operation", options=["sum","max","min","median","mean","count"])

        ## performing group by operation 
        if group_by_columns and operation_column:
        # Perform the groupby operation
            result = data.groupby(group_by_columns).agg(
                new_col = (operation_column, operation)
            ).reset_index()
            st.dataframe(result)
            
            ## Data Visualization 
            st.subheader(":rainbow[Data Visualization]",divider="rainbow")
            graphs = st.selectbox("Choose graph type",options=["line","bar","scatter","pie","sunburst"])
            if(graphs == "line"):
                x_axis=st.selectbox("Choose X axis",options = list(result.columns) )
                y_axis=st.selectbox("Choose Y axis" , options = list(result.columns))
                color=st.selectbox("Choose color Info",options=[None] + list(result.columns))
                fig = px.line(data_frame=result,x=x_axis,y=y_axis,color=color,markers="o")
                st.plotly_chart(fig)
            elif(graphs == "bar"):
                x_axis=st.selectbox("Choose X axis",options = list(result.columns) )
                y_axis=st.selectbox("Choose Y axis" , options = list(result.columns))
                color=st.selectbox("Choose color Info",options=[None] + list(result.columns))
                facet_col=st.selectbox("Choose Column Info",options=[None]+list(result.columns))
                fig = px.bar(data_frame=result,x=x_axis,y=y_axis,color=color,facet_col=facet_col,barmode="group" )
                st.plotly_chart(fig)
            elif(graphs == "scatter"):
                x_axis=st.selectbox("Choose X axis",options = list(result.columns) )
                y_axis=st.selectbox("Choose Y axis" , options = list(result.columns))
                color=st.selectbox("Choose color Info",options=[None] + list(result.columns))
                size = st.selectbox("Choose size",options=[None] + list(result.columns) )
                fig = px.scatter(data_frame=result,x=x_axis,y=y_axis,color=color,size=size )
                st.plotly_chart(fig)
            elif(graphs == "pie"):
                names = st.selectbox("Choose labels",options=list(result.columns))
                values = st.selectbox("Choose numerical values",options=list(result.columns))
                fig = px.pie(data_frame = result ,names=names,values=values)
                st.plotly_chart(fig)
            elif(graphs == "sunburst"):
                path =  st.multiselect("Choose Path",options=list(result.columns))
                ## No need to take values 
                fig = px.sunburst(data_frame=result,path=path,values="new_col")
                st.plotly_chart(fig)

import streamlit as st
import pandas as pd
import plotly.express as px
from joblib import load
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(
    page_title='Dashboard',
    page_icon='📜',
    layout='wide'
)

if st.session_state.get("authentication_status"):
    if st.session_state["authentication_status"]:
        # Display top navigation buttons
        col1, col2, col3, col4, col5 = st.columns(5)
        if col1.button("Home"):
            switch_page("Home")
        if col2.button("Data"):
            switch_page("Data")
        if col3.button("Dashboard"):
            switch_page("Dashboard")
        if col4.button("Predict"):
            switch_page("Predict")
        if col5.button("History"):
            switch_page("History")

        # Load the cleaned data using joblib
        loaded_cleaned_training_data = load('Packages/cleaned_training_data.joblib')

       

        # EDA selection
        st.sidebar.title('Exploratory Data Analysis (EDA)')

        # List of EDA options
        eda_options = ['Visualizations', 'KPIs']

        # Allow user to select EDA options
        selected_eda_option = st.sidebar.selectbox('Select EDA Option', eda_options)

        if selected_eda_option == 'Visualizations':
            # Separate categorical and numerical columns
            categorical_columns = loaded_cleaned_training_data.select_dtypes(include=['object']).columns
            numerical_columns = loaded_cleaned_training_data.select_dtypes(exclude=['object']).columns

            # Plot histograms for numerical variables
            st.header("Histograms for Numerical Variables")
            hist_cols = st.columns(len(numerical_columns))
            for col, numerical_column in zip(hist_cols, numerical_columns):
                fig = px.histogram(loaded_cleaned_training_data, x=loaded_cleaned_training_data[numerical_column], title=f'Histogram for {numerical_column}')
                col.plotly_chart(fig)

            # Filter only numeric columns
            numeric_data = loaded_cleaned_training_data.select_dtypes(include=['float64', 'int64'])

            # Plot box plots for numerical variables
            if not numeric_data.empty:
                st.header("Box Plots for Numerical Variables")
                boxplot_fig = px.box(numeric_data, title='Box Plots of Numerical Variables')
                st.plotly_chart(boxplot_fig)
            else:
                st.write("No numeric variables found for box plot visualization.")

            # # Plot box plots for numerical variables
            # st.header("Box Plots for Numerical Variables")
            # boxplot_fig = px.box(loaded_cleaned_training_data, title='Box Plots of Numerical Variables')
            # st.plotly_chart(boxplot_fig)

            # Plot heatmap for numerical variables
            st.header("Correlation Heatmap of Numerical Variables")

            # Calculate correlation matrix
            corr = loaded_cleaned_training_data[numerical_columns].corr()

            # Plot heatmap with specified color scale
            fig = px.imshow(corr, color_continuous_scale='RdBu_r', labels={'x': 'Numerical Variables', 'y': 'Numerical Variables'}, title='Correlation Heatmap of Numerical Variables')

            # Show the plot
            st.plotly_chart(fig)

            # Plot pairplots for numerical variables
            st.header("Pairplots for Numerical Variables")
            pairplot_fig = px.scatter_matrix(loaded_cleaned_training_data[numerical_columns], height=800, width=800)
            st.plotly_chart(pairplot_fig)

           # Filter categorical columns from the DataFrame
            categorical_columns = loaded_cleaned_training_data.select_dtypes(include=['object']).columns.tolist()

            # Plot bar plots for categorical variables
            st.title('Categorical Variable Analysis')

            # Define the number of columns in the layout
            num_columns = 2

            # Calculate the number of rows needed
            num_rows = (len(categorical_columns) + num_columns - 1) // num_columns

            # Create a matrix-like layout for the bar plots
            for i in range(num_rows):
                # Create a new row
                row = st.columns(num_columns)
                for j in range(num_columns):
                    # Calculate the index of the current categorical variable
                    index = i * num_columns + j
                    if index < len(categorical_columns):
                        feature = categorical_columns[index]
                        unique_values_counts = loaded_cleaned_training_data[feature].value_counts()
                        
                        # Create a plot for the current categorical variable
                        with row[j]:
                            fig = px.bar(x=unique_values_counts.index, y=unique_values_counts.values, title=f"Distribution of {feature}", labels={'x': feature, 'y': 'Count'})
                            st.header(f"Univariate Analysis of Feature: {feature}")
                            st.plotly_chart(fig)

            # # Plot bar plots for categorical variables
            # st.title('Categorical Variable Analysis')
            # for feature in categorical_columns:
            #     description = loaded_cleaned_training_data[feature].describe()
            #     unique_values_counts = loaded_cleaned_training_data[feature].value_counts()
            #     missing_values_count = loaded_cleaned_training_data[feature].isnull().sum()
            #     missing_values_percentage = (missing_values_count / len(loaded_cleaned_training_data)) * 100
                
            #     fig = px.bar(x=unique_values_counts.index, y=unique_values_counts.values, title=f"Distribution of {feature}", labels={'x': feature, 'y': 'Count'})
            #     st.header(f"Univariate Analysis of Feature: {feature}")
            #     st.write(description)
            #     st.plotly_chart(fig)
        


        elif selected_eda_option == 'KPIs':

            # Define custom colors
            custom_colors = {'Male': 'cyan', 'Female': 'green'}
            # Calculate average tenure per customer segment
            avg_tenure_per_segment = loaded_cleaned_training_data.groupby(['gender'])['tenure'].mean().reset_index()

            # Calculate average monthly charge per customer segment
            avg_monthly_charge_per_segment = loaded_cleaned_training_data.groupby(['gender'])['MonthlyCharges'].mean().reset_index()

            # Visualizations for KPIs
            st.header('Key Performance Indicators (KPIs)')

            # Average Tenure Per Gender (Bar Chart)
            st.subheader('Average Tenure Per Gender (Bar Chart)')
            fig_avg_tenure_bar = px.bar(avg_tenure_per_segment, x='gender', y='tenure', color='gender', labels={'gender': 'Gender', 'tenure': 'Average Tenure'}, title='Average Tenure Per Gender', color_discrete_map=custom_colors)
            st.plotly_chart(fig_avg_tenure_bar)

            # Average Tenure Per Gender (Pie Chart)
            st.subheader('Average Tenure Per Gender (Pie Chart)')
            fig_avg_tenure_pie = px.pie(avg_tenure_per_segment, values='tenure', names='gender', labels={'tenure': 'Average Tenure'}, color='gender', color_discrete_map=custom_colors)
            st.plotly_chart(fig_avg_tenure_pie)

            # Average Monthly Charge Per Gender (Bar Chart)
            st.subheader('Average Monthly Charge Per Gender (Bar Chart)')
            fig_avg_monthly_charge_bar = px.bar(avg_monthly_charge_per_segment, x='gender', y='MonthlyCharges', color='gender', labels={'gender': 'Gender', 'MonthlyCharges': 'Average Monthly Charge'}, title='Average Monthly Charge Per Gender', color_discrete_map=custom_colors)
            st.plotly_chart(fig_avg_monthly_charge_bar)

            # Average Monthly Charge Per Gender (Pie Chart)
            st.subheader('Average Monthly Charge Per Gender (Pie Chart)')
            fig_avg_monthly_charge_pie = px.pie(avg_monthly_charge_per_segment, values='MonthlyCharges', names='gender', labels={'MonthlyCharges': 'Average Monthly Charge'}, color='gender', color_discrete_map=custom_colors)
            st.plotly_chart(fig_avg_monthly_charge_pie)

            
    else:
        st.error('Username/password is incorrect')
else:
    st.error('Please log in to access this page.')

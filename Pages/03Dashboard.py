import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
from joblib import load
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(
    page_title='My Awesome App',
    page_icon='🏠',
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

        # Display the loaded data using Streamlit
        st.title('Visualizations from cleaned data')
        st.header("Loaded Cleaned Training Data Sample:")
        st.dataframe(loaded_cleaned_training_data.head())

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

            # Plot box plots for numerical variables
            st.header("Box Plots for Numerical Variables")
            boxplot_cols = st.columns(len(numerical_columns))
            for col, numerical_column in zip(boxplot_cols, numerical_columns):
                boxplot_trace = go.Box(y=loaded_cleaned_training_data[numerical_column], name=numerical_column, marker=dict(color='rgba(150, 10, 50, 0.6)'))
                layout = go.Layout(title=f'Box Plot of {numerical_column}', yaxis=dict(title=numerical_column), template='plotly_white')
                boxplot_fig = go.Figure(data=[boxplot_trace], layout=layout)
                col.plotly_chart(boxplot_fig)

            # Plot heatmap for numerical variables
            st.header("Correlation Heatmap of Numerical Variables")
            corr = loaded_cleaned_training_data[numerical_columns].corr()
            fig = ff.create_annotated_heatmap(z=corr.values, x=list(corr.columns), y=list(corr.index), colorscale='Viridis')
            fig.update_layout(xaxis_title='Numerical Variables', yaxis_title='Numerical Variables')
            st.plotly_chart(fig)

            # Plot pairplots for numerical variables
            st.header("Pairplots for Numerical Variables")
            pairplot_fig = px.scatter_matrix(loaded_cleaned_training_data[numerical_columns], height=800, width=800)
            st.plotly_chart(pairplot_fig)

            # Plot bar plots for categorical variables
            st.title('Categorical Variable Analysis')
            for feature in categorical_columns:
                description = loaded_cleaned_training_data[feature].describe()
                unique_values_counts = loaded_cleaned_training_data[feature].value_counts()
                missing_values_count = loaded_cleaned_training_data[feature].isnull().sum()
                missing_values_percentage = (missing_values_count / len(loaded_cleaned_training_data)) * 100
                
                fig = go.Figure(go.Bar(x=unique_values_counts.index, y=unique_values_counts.values))
                fig.update_layout(title=f"Distribution of {feature}", xaxis_title=feature, yaxis_title="Count")
                
                st.header(f"Univariate Analysis of Feature: {feature}")
                st.write(description)
                st.plotly_chart(fig)

        elif selected_eda_option == 'KPIs':
            # Calculate average tenure per customer segment
            avg_tenure_per_segment = loaded_cleaned_training_data.groupby('Churn')['tenure'].mean()

            # Calculate average monthly charge per customer segment
            avg_monthly_charge_per_segment = loaded_cleaned_training_data.groupby('Churn')['MonthlyCharges'].mean()

            # Convert 'Yes' and 'No' to 1 and 0 respectively
            loaded_cleaned_training_data['Churn'] = loaded_cleaned_training_data['Churn'].map({'Yes': 1, 'No': 0})

            # Calculate churn rate
            churn_rate = loaded_cleaned_training_data['Churn'].mean()
            # Display churn rate with bigger font size


            st.header('Key Performance Indicators (KPIs)')
            st.subheader('Average Tenure Per Customer Segment')
            st.write(avg_tenure_per_segment)

            st.subheader('Average Monthly Charge Per Customer Segment')
            st.write(avg_monthly_charge_per_segment)

            st.header('Churn Rate')
            st.write(f"<h3>{churn_rate}</h3>", unsafe_allow_html=True)
            st.write("A churn rate of 0.26497421658072196 means that approximately 26.5 percent of customers are churning.")
    else:
        st.error('Username/password is incorrect')
else:
    st.error('Please log in to access this page.')           
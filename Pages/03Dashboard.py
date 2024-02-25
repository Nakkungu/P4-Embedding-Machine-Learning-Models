import streamlit as st
import pandas as pd
import seaborn as sns
import plotly.express as px
import plotly.figure_factory as ff
import matplotlib.pyplot as plt
import plotly.graph_objects as go

from joblib import dump, load
# Load the cleaned data using joblib
loaded_cleaned_training_data = load('Packages\cleaned_training_data.joblib')

# Display the loaded data using Streamlit
st.title('Visualizations from cleaned data')

# Display the loaded data using Streamlit
st.header("Loaded Cleaned Training Data Sample:")
st.dataframe(loaded_cleaned_training_data.head())

# Separate categorical and numerical columns
categorical_columns = loaded_cleaned_training_data.select_dtypes(include=['object']).columns
numerical_columns = loaded_cleaned_training_data.select_dtypes(exclude=['object']).columns

# Plot histograms for numerical variables
st.header("Histograms for Numerical Variables")
for col in numerical_columns:
    fig = px.histogram(loaded_cleaned_training_data, x=loaded_cleaned_training_data[col], title=f'Histogram for {col}')
    st.plotly_chart(fig)

# Plot box plots 
#monthly charges
boxplot_trace = go.Box(y=loaded_cleaned_training_data['MonthlyCharges'], name='MonthlyCharges', marker=dict(color='rgba(150, 10, 50, 0.6)'))

# Create layout for the plot
layout = go.Layout(
    title='Box Plot of MonthlyCharges',
    yaxis=dict(title='MonthlyCharges'),
    template='plotly_white'
)

# Create figure object and plot
boxplot_mc = go.Figure(data=[boxplot_trace], layout=layout)

# Display the plot in Streamlit
st.plotly_chart(boxplot_mc)

#tenure
boxplot_trace = go.Box(y=loaded_cleaned_training_data['tenure'], name='tenure', marker=dict(color='rgba(150, 10, 50, 0.6)'))

# Create layout for the plot
layout = go.Layout(
    title='Box Plot of Tenure',
    yaxis=dict(title='Tenure'),
    template='plotly_white'
)

# Create figure object and plot
boxplot_mc = go.Figure(data=[boxplot_trace], layout=layout)

# Display the plot in Streamlit
st.plotly_chart(boxplot_mc)

#total charges
boxplot_trace = go.Box(y=loaded_cleaned_training_data['TotalCharges'], name='TotalCharges', marker=dict(color='rgba(150, 10, 50, 0.6)'))

# Create layout for the plot
layout = go.Layout(
    title='Box Plot of TotalCharges',
    yaxis=dict(title='TotalCharges'),
    template='plotly_white'
)

# Create figure object and plot
boxplot_mc = go.Figure(data=[boxplot_trace], layout=layout)

# Display the plot in Streamlit
st.plotly_chart(boxplot_mc)


# Plot heatmap for numerical variables
# Calculate correlation matrix
corr = loaded_cleaned_training_data[numerical_columns].corr()

# Define custom color scale
colors = [
    (0.0, "blue"),
    (0.5, "white"),
    (1.0, "red")
]

# Plot heatmap with custom color scale
fig = ff.create_annotated_heatmap(z=corr.values,
                                  x=list(corr.columns),
                                  y=list(corr.index),
                                  colorscale=colors,
                                  showscale=True)
fig.update_layout(title_text='Correlation Heatmap of Numerical Variables',
                  xaxis=dict(title='Numerical Variables'),
                  yaxis=dict(title='Numerical Variables'))
st.plotly_chart(fig)

# Plot pairplots for numerical variables
st.header("Pairplots for Numerical Variables")
pairplot_fig = px.scatter_matrix(loaded_cleaned_training_data[numerical_columns],
                                 height=800, width=800)  # Adjust height and width
st.plotly_chart(pairplot_fig)


#categorical variables
# Create an empty list to store Plotly figures
figures = []
# Loop through each categorical variable
for feature in categorical_columns:
    # Describe the feature
    description = loaded_cleaned_training_data[feature].describe()
    unique_values_counts = loaded_cleaned_training_data[feature].value_counts()
    missing_values_count = loaded_cleaned_training_data[feature].isnull().sum()
    missing_values_percentage = (missing_values_count / len(loaded_cleaned_training_data)) * 100
    
    # Create a bar plot for the distribution of the variable
    fig = go.Figure(go.Bar(x=unique_values_counts.index, y=unique_values_counts.values))
    fig.update_layout(title=f"Distribution of {feature}",
                      xaxis_title=feature,
                      yaxis_title="Count")
    
    # Add figure to the list
    figures.append((description, fig))

# Display figures in Streamlit app
st.title('Categorical Variable Analysis')

# Display each figure
for description, fig in figures:
    st.header(f"Univariate Analysis of Feature: {description.name}")
    st.write(description)
    st.plotly_chart(fig)
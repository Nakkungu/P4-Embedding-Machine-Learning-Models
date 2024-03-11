import streamlit as st
import pandas as pd
import joblib
from joblib import load
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from feature_engine.transformation import LogTransformer
from sklearn.preprocessing import FunctionTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import RobustScaler
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from imblearn.pipeline import Pipeline as ImbPipeline
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder, PowerTransformer, RobustScaler
from sklearn.ensemble import RandomForestClassifier 
from sklearn.compose import TransformedTargetRegressor
from sklearn.preprocessing import FunctionTransformer
from numpy import log1p
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import cross_val_score
from sklearn.neighbors import KNeighborsClassifier
from imblearn.over_sampling import RandomOverSampler
from sklearn.metrics import classification_report
from sklearn.feature_selection import SelectKBest, mutual_info_classif
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import RandomizedSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from imblearn.pipeline import Pipeline as imbpipeline
from imblearn.over_sampling import SMOTE
from sklearn.metrics import confusion_matrix
import os
import datetime




st.set_page_config(
    page_title='Predict',
    page_icon='',
    layout='wide'
)

if st.session_state.get("authentication_status"):
    if st.session_state["authentication_status"]:
        st.write(f'Welcome to the Churn App *{st.session_state["name"]}*')



        st.cache_resource
        loaded_cleaned_training_data = load('Packages/cleaned_training_data.joblib')
        loaded_cleaned_training_data['Churn'] = loaded_cleaned_training_data['Churn'].fillna('No')

        X = loaded_cleaned_training_data.drop('Churn', axis=1)
        y = loaded_cleaned_training_data['Churn']

        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)



        #Separating input features into numeric and categorical for different pipelines
        numeric_column = X.select_dtypes(include=['number']).columns
        categorical_column = X.select_dtypes(include=['object']).columns

        class LogTransformer:
            def __init__(self, constant=1e-5):
                self.constant = constant

            def fit(self, X, y=None):
                return self

            def transform(self, X):
                return np.log1p(X + self.constant)

        # Numeric pipeline
        numerical_pipeline = Pipeline(steps=[
            ('num_imputer', SimpleImputer(strategy='mean')),
            ('log_transformation', FunctionTransformer(LogTransformer().transform)),
            ('scaler', RobustScaler()),
            
        ])



        # Categorical pipeline
        categorical_pipeline = Pipeline(steps=[
            ('cat_imputer', SimpleImputer(strategy='most_frequent')),
            ('encoder', OneHotEncoder()),
        ])

        # Combine the numeric and categorical pipelines using ColumnTransformer
        preprocessor = ColumnTransformer(transformers=[
            ('numerical_pipeline', numerical_pipeline, numeric_column),
            ('categorical_pipeline', categorical_pipeline, categorical_column),
        ])

        # Initialize the LabelEncoder
        label_encoder = LabelEncoder()

        # Fit and transform the training set
        y_train_encoded = label_encoder.fit_transform(y_train)

        # Transform the testing set using the fitted label encoder
        y_test_encoded = label_encoder.transform(y_test)


        from sklearn.tree import DecisionTreeClassifier

        # Create a pipeline with preprocessor and DecisionTreeClassifier
        decision_tree_pipeline = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('classifier', DecisionTreeClassifier(random_state=42))
        ])

        # Fit the pipeline to the training data
        decision_tree_pipeline.fit(X_train, y_train_encoded)

        # Create a pipeline with preprocessor and RandomForestClassifier
        random_forest_pipeline = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('classifier', RandomForestClassifier(random_state=42))
        ])

        # Fit the pipeline to the training data
        random_forest_pipeline.fit(X_train, y_train_encoded)


        # Define the models
        models = {
            'Decision Tree': DecisionTreeClassifier(random_state=42),
            'Random Forest': RandomForestClassifier(random_state=42),
        }

        # Feature selection using SelectKBest
        selection = SelectKBest(mutual_info_classif, k=30)
        fi_smote_df = pd.DataFrame(columns=['Model_name', 'Accuracy', 'Precision', 'Recall', 'F1_Score'])

        all_pipeline ={}

        for model_name, classifier in models.items():
            pipeline = imbpipeline(steps=[
                ('preprocessor', preprocessor),
                ('smote', SMOTE(random_state=42)),
                ('feature_importance', selection),
                ('classifier', classifier)
            ])
            
            pipeline.fit(X_train, y_train_encoded)

            all_pipeline[model_name] = pipeline

            smote_y_pred = pipeline.predict(X_test)
            
            fi_smote_dict = classification_report(y_test_encoded, smote_y_pred, output_dict=True)
            
            accuracy = fi_smote_dict['accuracy']
            precision = fi_smote_dict['weighted avg']['precision']
            recall = fi_smote_dict['weighted avg']['recall']
            f1_score = fi_smote_dict['weighted avg']['f1-score']
            
            fi_smote_df.loc[len(fi_smote_df)] = [model_name, accuracy, precision, recall, f1_score]


        # Define the pipeline with the RandomForest classifier
        forest_pipeline = imbpipeline(steps=[
            ('preprocessor', preprocessor),
            ('smote', SMOTE(random_state=42)),
            ('feature_importance', selection),
            ('classifier', RandomForestClassifier(random_state=42))
        ])
        # Define the parameter grid with the best parameters
        best_params = {'classifier__max_depth': 20, 'classifier__min_samples_leaf': 2, 'classifier__min_samples_split': 5, 'classifier__n_estimators': 200}

        # Set the best parameters to the pipeline
        forest_pipeline.set_params(**best_params)

        # Fit the pipeline to the training data
        forest_pipeline.fit(X_train, y_train_encoded)


        decisiontree_pipeline = imbpipeline(steps=[
            ('preprocessor', preprocessor),
            ('smote', SMOTE(random_state=42)),
            ('feature_importance', selection),
            ('classifier', DecisionTreeClassifier(random_state=42))
        ])

        # Define the parameter grid with the best parameters
        best_params = {'classifier__max_depth': 20, 'classifier__min_samples_leaf': 2, 'classifier__min_samples_split': 5}

        # Set the best parameters to the pipeline
        decisiontree_pipeline.set_params(**best_params)

        # Fit the pipeline to the training data
        decisiontree_pipeline.fit(X_train, y_train_encoded)


        st.cache_resource(show_spinner='Loading')

        def load_model1():
            pipeline = forest_pipeline
            return pipeline

        st.cache_resource(show_spinner='Loading')

        def load_model2():
            pipeline = decisiontree_pipeline
            return pipeline

        st.cache_resource()

        def select_model():
            
            selected_model = st.selectbox('Select a model', options=['Decision_Tree', 'Random Forest'],
                                                key='selected_model')

            if st.session_state['selected_model'] == 'Random Forest':
                pipeline = load_model1()
            else:
                pipeline = load_model2()

            encoder = label_encoder
            return pipeline, encoder

        # if not os.path.exists('./ddata/history.csv'):
        #         os.mkdir('./ddata')


        def make_prediction(pipeline, encoder):
            
            TotalCharges = st.session_state['TotalCharges']
            MonthlyCharges = st.session_state['MonthlyCharges']
            tenure = st.session_state['tenure']
            gender = st.session_state['gender']
            SeniorCitizen = st.session_state['SeniorCitizen']
            Partner = st.session_state['Partner']
            Dependents = st.session_state['Dependents']
            PhoneService = st.session_state['PhoneService']
            MultipleLines = st.session_state['MultipleLines']
            InternetService = st.session_state['InternetService']
            OnlineSecurity = st.session_state['OnlineSecurity']
            OnlineBackup = st.session_state['OnlineBackup']
            DeviceProtection = st.session_state['DeviceProtection']
            TechSupport = st.session_state['TechSupport']
            StreamingTV = st.session_state['StreamingTV']
            StreamingMovies = st.session_state['StreamingMovies']
            Contract = st.session_state['Contract']
            PaperlessBilling = st.session_state['PaperlessBilling']
            PaymentMethod = st.session_state['PaymentMethod']


            categorical_features = ['gender', 'SeniorCitizen','Partner', 'Dependents', 'PhoneService', 'MultipleLines',
                                            'InternetService', 'OnlineSecurity', 'OnlineBackup', 'DeviceProtection',
                                            'TechSupport', 'StreamingTV', 'StreamingMovies', 'Contract',
                                            'PaperlessBilling', 'PaymentMethod']     
            
            # Create DataFrame for prediction
            data = {
                'TotalCharges': [TotalCharges],
                'MonthlyCharges': [MonthlyCharges],
                'tenure': [tenure],
                'gender': [gender],
                'SeniorCitizen': [SeniorCitizen],
                'Partner': [Partner],
                'Dependents': [Dependents],
                'PhoneService': [PhoneService],
                'MultipleLines': [MultipleLines],
                'InternetService': [InternetService],
                'OnlineSecurity': [OnlineSecurity],
                'OnlineBackup': [OnlineBackup],
                'DeviceProtection': [DeviceProtection],
                'TechSupport': [TechSupport],
                'StreamingTV': [StreamingTV],
                'StreamingMovies': [StreamingMovies],
                'Contract': [Contract],
                'PaperlessBilling': [PaperlessBilling],
                'PaymentMethod': [PaymentMethod]
            }
            df = pd.DataFrame(data)

                
            # Make prediction
            pred = pipeline.predict(df)
            prediction = int(pred[0])
            prediction = encoder.inverse_transform([prediction])

            #get probabilities
            probability = pipeline.predict_proba(df)


            df['Prediction Time'] = datetime.date.today()
            df['prediction'] = prediction
            # Extract probabilities for churn (Yes) and no churn (No)
            probability_of_yes = probability.tolist()[0][1]  # Probability of churn
            probability_of_no = probability.tolist()[0][0]   # Probability of no churn

            # Add probability columns to DataFrame
            df['probability_yes'] = probability_of_yes
            df['probability_no'] = probability_of_no
            df.to_csv('./ddata/history.csv', mode='a', header=not os.path.exists("./ddata/history.csv"), index=False)

            st.session_state['prediction'] = prediction
            st.session_state['probability'] = probability

            return prediction, probability        


        def display_form():
            pipeline, encoder = select_model()

            with st.form('Insert-Variable-Values'):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.number_input('Enter tenure', key = 'tenure')
                    st.number_input('Enter TotalCharges', key = 'TotalCharges')
                    st.number_input('Enter MonthlyCharges', key = 'MonthlyCharges')

                with col2:
                    st.selectbox('gender', options=['Female', 'Male'], key='gender')
                    st.selectbox('SeniorCitizen', options=['Yes', 'No'], key='SeniorCitizen')
                    st.selectbox('Partner', options=['Yes','No'], key = 'Partner')
                    st.selectbox('Dependents', options=['Yes', 'No'], key='Dependents')
                    st.selectbox('PhoneService', options=['Yes', 'No'], key='PhoneService')
                    st.selectbox('MultipleLines', options=['No', 'Yes', 'No phone service'],
                                        key='MultipleLines')
                    st.selectbox('InternetService', options=['DSL', 'Fiber optic', 'No'],
                                        key='InternetService')
                    st.selectbox('OnlineSecurity', options=['No', 'Yes','No internet service'],
                                        key='OnlineSecurity')
                    st.selectbox('OnlineBackup', options=['No', 'Yes', 'No internet service'],
                                        key='OnlineBackup')
                    
                with col3:
                    st.selectbox('DeviceProtection', options=['No', 'Yes', 'No internet service'], 
                                key = 'DeviceProtection')
                    st.selectbox('TechSupport', options=['No', 'Yes', 'No internet service'],
                                        key='TechSupport')
                    st.selectbox('StreamingTV', options=['No', 'Yes', 'No internet service'],
                                        key='StreamingTV')
                    st.selectbox('StreamingMovies', options=['No', 'Yes', 'No internet service'], key='StreamingMovies')
                    st.selectbox('Contract', options=['Month-to-month', 'One year', 'Two year'],
                                        key='Contract')
                    st.selectbox('PaperlessBilling', options=['Yes', 'No'], key='PaperlessBilling')
                    st.selectbox('PaymentMethod', options=['Electronic check', 'Mailed check', 'Bank transfer (automatic)', 
                                                        'Credit card (automatic)'], key='PaymentMethod')

            
                st.form_submit_button('Submit', on_click=make_prediction, kwargs=dict(pipeline=pipeline, encoder= encoder))
                # Store prediction results in a DataFrame
            

        if __name__ == "__main__":
            st.title('Prediction')

            if 'prediction' not in st.session_state:
                st.session_state['prediction'] = None
                st.session_state['probability'] = None
            
            display_form()
            prediction = st.session_state['prediction']
            probability = st.session_state['probability']

            if not prediction:
                st.markdown("### The predictions will appear here")
            elif prediction == "Yes":
                probability_of_yes = probability[0][1] * 100
                st.markdown(f"### The customer will churn with a probability of {probability_of_yes}%")
            else:
                probability_of_no = probability[0][0] *100
                st.markdown(f"The customer will not churn with a probabilty of {probability_of_no}%")
            st.write(prediction)
            st.write(st.session_state)

    else:
        st.error('Username/password is incorrect')
else:
    st.error('Please log in to access this page.')
import streamlit as st
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split


def main():
    df = load_data()

    page = st.sidebar.selectbox("Choose a page", ['Homepage', 'Exploration', 'Prediction'])

    if page == 'Homepage':
        st.title('Bicycle accidents and bikeshare usage')
        st.text('Select a page in the sidebar')
        st.dataframe(df)
    elif page == 'Exploration':
        st.title('Explore the preliminary dataset')
        if st.checkbox('Show column descriptions'):
            st.dataframe(df.describe())

        st.markdown('### Bikeshare usage and number of injuries')
        st.text('Monthly minor and major injuries:')
        df_months = df.groupby(by=[df.dates.dt.month]).sum()
        ax = df_months.num_bikeshares.plot()
        ax.set_ylabel('# Bikeshares')
        ax.set_xlabel('Months')
        ax.set_title('Monthly bikeshares and minor injuries.')
        ax2 = ax.twinx()
        df_months.minorinjuries_cyclists.plot(ax=ax2, legend=False, color="r")
        ax.figure.legend(loc=8, bbox_to_anchor=(0.5, 0.1))
        ax2.set_ylabel('# minor injuries')
        st.pyplot()

        df_months = df.groupby(by=[df.dates.dt.month]).sum()
        ax = df_months.num_bikeshares.plot()
        ax.set_ylabel('# Bikeshares')
        ax.set_xlabel('Months')
        ax.set_title('Monthly bikeshares and minor injuries.')
        ax2 = ax.twinx()
        df_months.majorinjuries_cyclists.plot(ax=ax2, legend=False, color="r")
        ax.figure.legend(loc=8, bbox_to_anchor=(0.5, 0.1))
        ax2.set_ylabel('# major injuries')
        st.pyplot()

        st.text('Weekly minor and major injuries by day:')
        df_days = df.groupby(by=[df.dates.dt.dayofweek]).mean()
        ax = df_months.num_bikeshares.plot()
        ax.set_ylabel('# Bikeshares')
        ax.set_xlabel('Months')
        ax.set_title('Monthly bikeshares and minor injuries.')

        labels = ['Sun', 'Mon', 'Tue', 'Wed', 'Thur', 'Fri', 'Sat']
        ax.xticks(range(0.7), labels, rotation='vertical')

        ax2 = ax.twinx()
        df_months.minorinjuries_cyclists.plot(ax=ax2, legend=False, color="r")
        ax.figure.legend(loc=8, bbox_to_anchor=(0.5, 0.1))
        ax2.set_ylabel('# minor injuries')
        st.pyplot()
    else:
        st.title('Modelling')
        model, accuracy = train_model(df)
        st.write('Accuracy: ' + str(accuracy))
        st.markdown('### Make prediction')
        st.dataframe(df)
        row_number = st.number_input('Select row', min_value=0, max_value=len(df) - 1, value=0)
        st.markdown('#### Predicted')
        st.text(model.predict(df.drop(['alcohol'], axis=1).loc[row_number].values.reshape(1, -1))[0])


@st.cache
def train_model(df):
    X = np.array(df.drop(['alcohol'], axis=1))
    y = np.array(df['alcohol'])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    return model, model.score(X_test, y_test)


@st.cache
def load_data():
    df = pd.read_csv('di_bike_safety_poc2.csv')
    df['dates'] = pd.to_datetime(df.dates)
    return df


if __name__ == '__main__':
    main()
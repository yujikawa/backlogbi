import streamlit as st
import pandas as pd
import plotly.express as px
from helpers import BacklogAPI
from models import Setting
from datetime import datetime, timedelta, timezone
import base64
from helpers.word_cloud import word_clound_output
from views.base_view import BaseView


class DashboardView(BaseView):
    def __init__(self, setting: Setting):
        super(DashboardView, self).__init__(setting)

    def run(self):
        st.title('Dashboard')
        st.write("""
        Find and analyze tasks that are not currently completed and completed tasks that have been updated on a specified date.
        """)
        api = BacklogAPI(endpoint=self.setting['endpoint'],
                         api_key=self.setting['api_key'])
        UTC = timezone(timedelta(hours=0), 'UTC')
        self.today = datetime.today()
        self.now = datetime.now(UTC)
        self.start_date = st.date_input(
            label='Updated since',
            value=self.today.replace(day=1)).strftime('%Y-%m-%d')
        self.end_date = st.date_input(
            label='Updated until').strftime('%Y-%m-%d')
        projects = api.get_projects()
        project_list = [(p['id'], p['name'], p['projectKey'])
                        for p in projects]
        (project_id, name, _) = st.selectbox('Select project', project_list)

        st.write(f'# {name}')

        statuses = api.get_status(project_id)
        status_without_done = [i['id'] for i in statuses if i['id'] != 4]
        issues = api.get_issue_stats(project_id, status_without_done)
        issues += api.get_issue_stats_done(project_id, self.start_date,
                                            self.end_date)
        df = pd.DataFrame(issues)
        df = self.convert_data(df)
        users = df['assignee_name'].unique()

        select_users = st.multiselect(label='selectusers', options=users)
        if not select_users:
            select_users = users

        df = df[df['assignee_name'].isin(select_users)]

        st.write(f"""
        ## Fetch data({len(df)} rows)
        """)

        st.dataframe(df)
        st.markdown(self.get_table_download_link(df),
                    unsafe_allow_html=True)

        st.write("""
        ## Issue count by status
        """)

        df_count_by_status = (df.groupby(
            ['assignee_name', 'status_name'],
            as_index=False).count().rename(columns={'id': 'count'}))[[
                'assignee_name', 'status_name', 'count'
            ]]

        fig1 = px.bar(
            df_count_by_status,
            x='count',
            y='assignee_name',
            color='status_name',
            orientation='h',
        )
        fig1.update_yaxes(categoryorder='total ascending')
        fig1.update_layout(
            autosize=False,
            height=700,
            margin=dict(l=50, r=50, b=100, t=100, pad=4),
        )
        st.plotly_chart(fig1, use_container_width=True)

        st.write("""
        ## Issue count by cateogry
        """)
        df_count_by_category = (df.groupby(
            ['assignee_name', 'category_name'],
            as_index=False).count().rename(columns={'id': 'count'}))[[
                'assignee_name', 'category_name', 'count'
            ]]
        fig2 = px.bar(df_count_by_category,
                        x='count',
                        y='assignee_name',
                        color='category_name',
                        orientation='h')
        fig2.update_yaxes(categoryorder='total ascending')
        fig2.update_layout(
            autosize=False,
            height=700,
            margin=dict(l=50, r=50, b=100, t=100, pad=4),
        )
        st.plotly_chart(fig2, use_container_width=True)

        st.write("""
        ## Issue digestibility
        """)

        df_count_by_assignee = (df.groupby(
            ['assignee_name'],
            as_index=False).count().rename(columns={'id': 'count'}))[[
                'assignee_name', 'count'
            ]]

        df_count = pd.merge(df_count_by_status,
                            df_count_by_assignee,
                            on='assignee_name',
                            how='left')
        df_count['digestibility'] = 100 * df_count['count_x'] / df_count[
            'count_y']

        fig3 = px.bar(df_count[df_count['status_name'] == '完了'][[
            'assignee_name', 'digestibility'
        ]],
                        x='digestibility',
                        y='assignee_name',
                        orientation='h',
                        range_x=[0, 100])
        fig3.update_yaxes(categoryorder='total ascending')

        st.plotly_chart(fig3, use_container_width=True)

        st.write("""
        ## Do you remember me?
        These issues were created 60 days ago
        """)
        st.dataframe(df[df['created'] < self.now - timedelta(days=60)][[
            'issueKey', 'summary', 'created_user_name', 'created'
        ]])

        st.write("""
        ## Wordcloud
        """)
        wordcloud = word_clound_output(df.summary.unique())
        st.image(wordcloud.to_image())

    def convert_data(self, df: pd.DataFrame) -> pd.DataFrame:
        df['created'] = pd.to_datetime(df['created'])
        df['created_user_name'] = df['createdUser'].apply(lambda x: x['name'])
        df['status_name'] = df['status'].apply(lambda x: x['name'])
        df['assignee_name'] = df['assignee'].apply(
            lambda x: x['name'] if type(x) == dict else 'no assignee')
        df['category_name'] = df['category'].apply(
            lambda x: x[0]['name'] if len(x) else 'no category')
        df = df[~(df['startDate'] > self.end_date)]
        return df

    def get_table_download_link(self, df):
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="backlog_dashboard.csv">Download csv file</a>'
        return href

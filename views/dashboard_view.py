import streamlit as st
import pandas as pd
import plotly.express as px
from helpers import BacklogAPI
from models import Setting
from datetime import datetime
import base64


class DashboardView(object):
    def __init__(self):
        st.title('Dashboard')
        setting = Setting.load()
        api = BacklogAPI(endpoint=setting['endpoint'], api_key=setting['api_key'])
        start_date = st.date_input(label='開始日付', value=datetime.today().replace(day=1)).strftime('%Y-%m-%d')
        end_date = st.date_input(label='終了日付').strftime('%Y-%m-%d')
        projects = api.get_projects()
        project_list = [(p['id'], p['name'], p['projectKey']) for p in projects]
        (project_id, name, _) = st.selectbox('Select project', project_list)

        button = st.button('検索')

        if button:

            statuses = api.get_status(project_id)
            status_without_done = [i['id'] for i in statuses if i['id'] != 4]
            issues = []
            for s in status_without_done:
                issues += api.get_issue_stats(project_id, s)
            issues += api.get_issue_stats_done(project_id, start_date, end_date)
            df = pd.DataFrame(issues)
            df['status_name'] = df['status'].apply(lambda x: x['name'])
            df['assignee_name'] = df['assignee'].apply(lambda x: x['name'] if type(x) == dict else 'no assignee')
            df['category_name'] = df['category'].apply(lambda x: x[0]['name'] if len(x) else 'no category')
            df_count_by_status = (
                df
                    .groupby(['assignee_name', 'status_name'], as_index=False)
                    .count()
                    .rename(columns={'id': 'count'})
            )[['assignee_name', 'status_name', 'count']]

            # 未来案件は消す
            df = df[~(df['startDate'] > end_date)]

            st.write(f"""
            ## 取得データ({len(df)}件)
            """)

            st.dataframe(df)
            st.markdown(self.get_table_download_link(df), unsafe_allow_html=True)

            df_count_by_category = (
                df
                    .groupby(['assignee_name', 'category_name'], as_index=False)
                    .count()
                    .rename(columns={'id': 'count'})
            )[['assignee_name', 'category_name', 'count']]

            df_count_by_assignee = (
                df
                    .groupby(['assignee_name'], as_index=False)
                    .count()
                    .rename(columns={'id': 'count'})
            )[['assignee_name', 'count']]

            st.write("""
            ## ステータス別集計
            """)

            fig1 = px.bar(df_count_by_status, x='count', y='assignee_name', color='status_name', orientation='h')
            st.plotly_chart(fig1, use_container_width=True)

            st.write("""
            ## カテゴリー別集計
            """)
            fig2 = px.bar(df_count_by_category, x='count', y='assignee_name', color='category_name', orientation='h')
            st.plotly_chart(fig2, use_container_width=True)

            df_count = pd.merge(df_count_by_status, df_count_by_assignee, on='assignee_name', how='left')
            df_count['digestibility'] = 100 * df_count['count_x'] / df_count['count_y']

            st.write("""
            ## 課題消化率
            """)
            st.dataframe(df_count[df_count['status_name'] == '完了'][['assignee_name', 'digestibility']].sort_values(
                ['digestibility'], ascending=False))

    def get_table_download_link(self, df):
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="backlog_dashboard.csv">Download csv file</a>'
        return href

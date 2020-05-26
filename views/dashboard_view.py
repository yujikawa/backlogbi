import streamlit as st
import pandas as pd
import plotly.express as px
from helpers import BacklogAPI
from models import Setting
from datetime import datetime

class DashboardView(object):
    def __init__(self):
        st.title('Dashboard')

        start_date = st.date_input(label='開始日付', value=datetime.today().replace(day=1)).strftime('%Y-%m-%d')
        end_date = st.date_input(label='終了日付').strftime('%Y-%m-%d')

        button = st.button('検索')

        if button:

            setting = Setting.load()

            api = BacklogAPI(endpoint=setting['endpoint'], api_key=setting['api_key'])

            statuses = api.get_status(setting['project_id'])
            status_without_done = [i['id'] for i in statuses if i['id'] != 4]
            issues = []
            for s in status_without_done:
                issues += api.get_issue_stats(setting['project_id'], s)
            issues += api.get_issue_stats_done(setting['project_id'], start_date, end_date)
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

            fig1 = px.bar(df_count_by_status, x='assignee_name', y='count', color='status_name')
            st.plotly_chart(fig1, use_container_width=True)

            st.write("""
            ## カテゴリー別集計
            """)
            fig2 = px.bar(df_count_by_category, x='assignee_name', y='count', color='category_name')
            st.plotly_chart(fig2, use_container_width=True)

            df_count = pd.merge(df_count_by_status, df_count_by_assignee, on='assignee_name', how='left')
            df_count['digestibility'] = 100 * df_count['count_x'] / df_count['count_y']

            st.write("""
            ## 課題消化率
            """)
            st.dataframe(df_count[df_count['status_name'] == '完了'][['assignee_name', 'digestibility']].sort_values(['digestibility'], ascending=False))

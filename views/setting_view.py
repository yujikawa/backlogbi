import streamlit as st
from models import Setting

class SettingView(object):
    def __init__(self):
        st.write('# Setting')
        s = Setting.load()

        project_id = st.text_input(label='Project ID', value=s.get('project_id', ''))
        endpoint = st.text_input(label='Endpoint', value=s.get('endpoint', ''))
        api_key = st.text_input(label='API key', value=s.get('api_key', ''), type='password')

        button = st.button('登録')

        if button:
            s.set_setting('project_id', project_id)
            s.set_setting('endpoint', endpoint)
            s.set_setting('api_key', api_key)
            s.save()
            st.success('登録しました!')

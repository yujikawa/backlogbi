import streamlit as st
from models import Setting


class SettingView(object):
    def __init__(self):
        st.write('# Setting')
        s = Setting.load()

        endpoint = st.text_input(label='Endpoint', value=s.get('endpoint', ''))
        api_key = st.text_input(label='API key', value=s.get(
            'api_key', ''), type='password')

        button = st.button('登録')

        if button:
            s.set_setting('endpoint', endpoint)
            s.set_setting('api_key', api_key)
            s.save()
            st.success('登録しました!')

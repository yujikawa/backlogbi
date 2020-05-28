import streamlit as st
from models import Setting
from views.base_view import BaseView


class SettingView(BaseView):
    def __init__(self, setting: Setting):
        super(SettingView, self).__init__(setting)
    
    def run(self):
        st.write('# Setting')

        endpoint = st.text_input(label='Endpoint ex) https://xxx.backlog.co.jp', value=self.setting['endpoint'])
        api_key = st.text_input(label='API key', value=self.setting['api_key'], type='password')

        button = st.button('登録')

        if button:
            self.setting['endpoint'] = endpoint
            self.setting['api_key'] = api_key
            self.setting.save()
            st.success('登録しました!')

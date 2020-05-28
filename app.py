import os
import streamlit as st
from models import Menu
from models.setting import Setting

from views import SettingView
from views import DashboardView

if __name__ == "__main__":
    setting = Setting()
    
    st.sidebar.markdown("# Menu")
    view = st.sidebar.selectbox("Select Menu", Menu.get_menus())
    
    if not setting and view != Menu.SETTING.name:
        st.title('Welcome to BacklogBI')
        st.write('Please select setting from side menu and input your settings!')
    elif view == Menu.DASHBOARD.name:
        d = DashboardView(setting)
        d.run()
    elif view == Menu.SETTING.name:
        s = SettingView(setting)
        s.run()

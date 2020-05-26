import os
import streamlit as st
from models import Menu

from views import SettingView
from views import DashboardView

if __name__ == "__main__":
    os.makedirs('./data', exist_ok=True)

    st.sidebar.markdown(
        "# Menu"
    )

    view = st.sidebar.selectbox(
        "Select Menu", Menu.get_menus()
    )

    if view == Menu.DASHBOARD.name:
        DashboardView()
    elif view == Menu.SETTING.name:
        SettingView()

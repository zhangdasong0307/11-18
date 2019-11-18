# -*- coding:utf-8 -*-
# Author : 小吴老师
# Data ：2019/7/31 14:31
import pytest
import os
from selenium import webdriver
from tools.ui.base_ui import BaseUI

@pytest.fixture(scope='session')
def driver():
    base = BaseUI('chrome')
    yield base
    base.driver.quit()
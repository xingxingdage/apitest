# !/usr/bin/env python
# -*-coding: utf-8-*-

# @ProjectName : jiling_aqjr
# @FileName : test_sell.py
# @Time : 2019/12/30 15:31
# @Author : Nick

import sys
import os
# 把当前目录加到sys.path中，才能在下面包含当前目录中的其他文件
sys.path.append(os.getcwd())
import pytest
import copy
import allure
from src.aqjr.gdca_encrypt_url import ContentSet, DataHandleToolkit
from src.aqjr.basicdata_set import basic_data




# 在一个文件中获取一次session，后续需要想办法重构数据据获取过程，完成在fixture中获取loging_session
logining_session = get_login_session()
# 按照投注类型将数据文件中所有的数据记录归类存放在以投注类型命名的列表中
d3_data = sell_data_prepare(d3_src_file, d3_term_num, logining_session)
dball_data = sell_data_prepare(dball_src_file, dball_term_num, logining_session)
# 打印列表中第一个元素的'ReqContent'字段
# print(d3_data['danshi'][0]['ReqContent'])


def get_ids(item):
    return item[1]


class TestD3Sell:
    @pytest.fixture(params = d3_data["danshi"], ids = get_ids, scope="class")
    def danshi_data(self, request):
        """
        返回3D单式数据
        :param request: pytest内建的fixture，用于获取params参数里的每一个元素
        """
        return request.param[0]

    @allure.step
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("3D_sell")
    @allure.story("danshi")
    def test_3d_dashi(self, danshi_data):
        """
        用fixture来完成测试数据准备，测试3D单式
        执行胆拖投注的测试，因为在自定义的fixture:danshi_data里面使用了request内建fixture，
        """
        # 可以用danshi_data['ReqContent']来查看每个元素的ReqContent内容
        sell_result = DataHandleToolkit.excutive_test(basic_data.sell_profix_url, "sell", danshi_data)
        assert '100000' == sell_result["BackCode"]

    @allure.step
    @allure.feature("3D_sell")
    @allure.story("fushi")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("item", d3_data["fushi"], ids = get_ids)
    def test_fushi_sell(self, item):
        """
        用参数化方式来测试,3D复式投注
        """
        sell_result = DataHandleToolkit.excutive_test(basic_data.sell_profix_url, "sell", item)
        assert '100000' == sell_result["BackCode"]

    @allure.feature("3D_sell")
    @allure.story("dantuo")
    @pytest.mark.core_case
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("item",  d3_data["dantuo"], ids = get_ids)
    def test_dantuo_sell(self, item):
        """
        测试3D胆拖
        """
        sell_result = DataHandleToolkit.excutive_test(basic_data.sell_profix_url, "sell", item[0])
        assert '100000' == sell_result["BackCode"]

    @allure.feature("3D_sell")
    @allure.story("Expected Exception")
    @pytest.mark.exception_case
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.parametrize("item",  dball_data["yichang"], ids = get_ids)
    def test_d3_sell_exception(self, item):
        """
        3D注码异常测试，采用于双色球不同的方式，判断输出内容是否相同，不判断返回码
        """
        sell_result = DataHandleToolkit.excutive_test(basic_data.sell_profix_url, "sell", item[0])
        assert '100344' == sell_result["BackCode"] and '注码校验不通过' == sell_result['BackMsg']


class TestDballSell:
    @allure.feature("Dball_sell")
    @allure.story("fushi")
    @pytest.mark.core_case
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("item",  dball_data["fushi"], ids = get_ids)
    def test_fushi_sell(self, item):
        """
        测试双色球复式
        """
        sell_result = DataHandleToolkit.excutive_test(basic_data.sell_profix_url, "sell", item[0])
        assert '100000' == sell_result["BackCode"]

    @allure.feature("Dball_sell")
    @allure.story("dantuo")
    @pytest.mark.core_case
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("item",  dball_data["dantuo"], ids = get_ids)
    def test_dantuo_sell(self, item):
        """
        测试双色球胆拖
        """
        sell_result = DataHandleToolkit.excutive_test(basic_data.sell_profix_url, "sell", item[0])
        assert '100000' == sell_result["BackCode"]

    @allure.feature("Dball_sell")
    @allure.story("danshi")
    @pytest.mark.core_case
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("item",  dball_data["danshi"], ids = get_ids)
    def test_danshi_sell(self, item):
        """
        测试双色球单式
        """
        sell_result = DataHandleToolkit.excutive_test(basic_data.sell_profix_url, "sell", item[0])
        assert '100000' == sell_result["BackCode"]

    @allure.feature("Dball_sell")
    @allure.story("Expected Exception")
    @pytest.mark.exception_case
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.xfail(reason = "当测试数据中存在各种问题时，返回码不等于10000，测试是否符合预期")
    @pytest.mark.parametrize("item",  dball_data["yichang"], ids = get_ids)
    def test_dball_sell_exception(self, item):
        """
        双色球注码异常测试
        """
        sell_result = DataHandleToolkit.excutive_test(basic_data.sell_profix_url, "sell", item[0])
        assert '100000' != sell_result["BackCode"]

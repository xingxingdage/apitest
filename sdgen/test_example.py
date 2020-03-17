# !/usr/bin/env python
# -*-coding: utf-8-*-

# @ProjectName : jiling_aqjr
# @FileName : test_example.py
# @Time : 2020/1/9 9:36
# @Author : Nick

import pytest
import allure
from gdca_encrypt_url import DataHandleToolkit
from basicdata_set import basic_data


@allure.step
@allure.severity(allure.severity_level.CRITICAL)
@allure.feature("3D_sell")
@allure.story("danshi")
def test_3d_dashi(d3_danshi):
    """
    用fixture来完成测试数据准备，测试3D单式
    执行胆拖投注的测试，因为在自定义的fixture:danshi_data里面使用了request内建fixture，
    """
    # 可以用danshi_data['ReqContent']来查看每个元素的ReqContent内容
    sell_result = DataHandleToolkit.excutive_test(basic_data.sell_profix_url, "sell", d3_danshi[0])
    assert '100000' == sell_result["BackCode"]


@allure.step
@allure.feature("3D_sell")
@allure.story("fushi")
@allure.severity(allure.severity_level.CRITICAL)
def test_fushi_sell(d3_fushi):
    """
    用参数化方式来测试,3D复式投注
    """
    sell_result = DataHandleToolkit.excutive_test(basic_data.sell_profix_url, "sell", d3_fushi[0])
    assert '100000' == sell_result["BackCode"]


@allure.feature("3D_sell")
@allure.story("dantuo")
@pytest.mark.core_case
@allure.severity(allure.severity_level.CRITICAL)
def test_dantuo_sell(d3_dantuo):
    """
    测试3D胆拖
    """
    sell_result = DataHandleToolkit.excutive_test(basic_data.sell_profix_url, "sell", d3_dantuo[0])
    assert '100000' == sell_result["BackCode"]


@allure.feature("3D_sell")
@allure.story("Expected Exception")
@pytest.mark.exception_case
@allure.severity(allure.severity_level.BLOCKER)
def test_d3_sell_exception(d3_yichang):
    """
    3D注码异常测试，采用于双色球不同的方式，判断输出内容是否相同，不判断返回码
    """
    sell_result = DataHandleToolkit.excutive_test(basic_data.sell_profix_url, "sell", d3_yichang[0])
    assert '100344' == sell_result["BackCode"] and '注码校验不通过' == sell_result['BackMsg']


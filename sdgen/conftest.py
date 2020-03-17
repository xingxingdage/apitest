# !/usr/bin/env python
# -*-coding: utf-8-*-

# @ProjectName : jiling_aqjr
# @FileName : conftest.py.py
# @Time : 2019/12/31 17:24
# @Author : Nick


from interface_test_set import TestInterfaceSet
import sys
import os
import copy
import allure
from src.aqjr.gdca_encrypt_url import ContentSet
from src.aqjr.basicdata_set import basic_data
import collections
import Des
sys.path.append((os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))))

d3_src_file = r'D:\python_develop\jiling_aqjr\datadir\D3注码.txt'
d3_term_num = "2020009"
dball_src_file = r'D:\python_develop\jiling_aqjr\datadir\B001_test.txt'
dball_term_num = "2020009"


def get_session():
    return TestInterfaceSet.login()


@allure.step("prepare source data")
def sell_data_prepare(file, term_code, session=None, business_type='sell'):
        """
        从文件中读取所有的销售注码，然后把所有数据按按照销售类型分类存储
        在示例文件中的投注类型为投注类型['danshi', 'fushi', 'dantuo', 'yichang']
        注：只能调用此函数来进行数据准备，多次调用会导致loginsession不一致报错
        :param file: 数据源文件
        :param business_type: 两个取值’sell'和 'encash'
        :param term_code:期号
        :param session:登录的loginsession，在一个会话里时必须使用一个session
        :return: 列表:每个元素包含一个由单条销售数据+用于pytest参数化执行时的用例id组成的列表
        """
        # 从数据文件中读取投注数据，注意最后一个字段comment中的注释不要用逗号，防止在解析时被认成分隔符
        sell_record = collections.namedtuple("Sellrecord",
                                             "record_id, game_name,case_type, bet_code, money, case_result, comment")
        content = ContentSet()
        # 兑奖或销售前先做一次登录，获取loginsession
        login_session = session
        content.sell_content.update(LoginSession = login_session)
        # 将原始数据文件中的投注类型放在case_type中，可以实现自动的投注类型归纳整理，不用手动指定投注类型
        # 如果对数据文件中的投注类型不清楚时，可以打印case_type
        case_type = set()
        data_set = {}
        ids_set = {}
        # unicode-escape编码集，他是将unicode内存编码值直接存储
        if file:
            with open(file, 'r', encoding = 'unicode_escape') as f:
                if business_type == 'sell':
                    for record in f:
                        # print("split", record.split(','))
                        # 直接使用namedtuple的_make方法将解析后的文件行数据转换成namedtuple实例，并存储在records列表中
                        # 组合生成每条记录
                        record_info = sell_record._make(record.strip().split(','))
                        if record_info.case_type not in case_type:
                            case_type.add(record_info.case_type)
                            data_set[record_info.case_type] = []
                            ids_set[record_info.case_type] = []
                        # print("record_info", record_info)
                        content.sell_content.update(SellTermCode = term_code, Money = record_info.money,
                                                    PlayEname = record_info.game_name,
                                                    TicketCode = record_info.bet_code,
                                                    RunCode = basic_data.serial_num_gen())
                        checkcode = Des.getcheckcode(content.sell_content['RunCode'] +
                                                     content.general_out_content["PartnerId"] +
                                                     content.sell_content["UserId"] +
                                                     content.sell_content["TicketCode"] +
                                                     content.sell_content["Money"] +
                                                     content.sell_content["LoginSession"]
                                                     )
                        content.sell_content.update(CheckCode = checkcode)
                        content.general_out_content.update(ReqContent = content.sell_content)
                        if record_info.case_type in data_set:
                            data_set[record_info.case_type].append((copy.deepcopy(content.general_out_content),
                                                                   '{}_{}_{}_{}'.format(business_type,
                                                                                        record_info.game_name,
                                                                                        record_info.case_type,
                                                                                        record_info.record_id)))
                return data_set


unique_session = get_session()
d3_data = sell_data_prepare(d3_src_file, d3_term_num, unique_session)
dball_data = sell_data_prepare(dball_src_file, dball_term_num, unique_session)


def pytest_addoption(parser):
    parser.addoption("--d3_danshi", action = "store", default = [], help = "test datas for 3d danshi")
    parser.addoption("--d3_fushi", action = "store", default = [], help = "test datas for 3d fushi")
    parser.addoption("--d3_dantuo", action = "store", default = [], help = "test datas for 3d dantuo")
    parser.addoption("--d3_yichang", action = "store", default = [], help = "test datas for betting exception")


def get_ids(item):
    return item[1]


def pytest_generate_tests(metafunc):
    if "d3_danshi" in metafunc.fixturenames:
        metafunc.parametrize("d3_danshi", d3_data['danshi'], ids = get_ids)
    if "d3_fushi" in metafunc.fixturenames:
        metafunc.parametrize("d3_fushi", d3_data['fushi'], ids = get_ids)
    if "d3_dantuo" in metafunc.fixturenames:
        metafunc.parametrize("d3_dantuo", d3_data['dantuo'], ids = get_ids)
    if "d3_yichang" in metafunc.fixturenames:
        metafunc.parametrize("d3_yichang", d3_data['yichang'], ids = get_ids)










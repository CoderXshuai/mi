# -*- coding: utf-8 -*-
from mi_manager.daemon import data_service


class Task(object):

    def __init__(self, spider_name, resource_dic, settings_name, father_mission_name):
        self.spider_name = spider_name
        self.core_reids = resource_dic['core_reids']
        self.filter_redis = resource_dic['filter_redis']
        self.mongo = resource_dic['mongo']
        self.mysql = resource_dic['mysql']
        self.father_mission_name = father_mission_name
        self.settings_name = settings_name

    def get_dic_str(self):
        dic = {}
        dic['spider_name'] = self.spider_name
        dic['spider_detail'] = data_service.get_spider(dic['spider_type'], dic['spider_name'])
        dic['father_mission_name'] = self.father_mission_name
        dic['settings_name'] = self.settings_name
        if dic['settings_name']:
            dic['settings_detail'] = data_service.get_settings(dic['settings_name'])
        dic['core_reids'] = self.core_reids
        if dic['core_reids']:
            dic['core_reids_detail'] = data_service.get_resource('Redis', dic['core_reids'])
        dic['filter_redis'] = self.filter_redis
        if dic['filter_redis']:
            dic['filter_redis_detail'] = data_service.get_resource('Redis', dic['filter_redis'])
        dic['mongo'] = self.mongo
        if dic['mongo']:
            dic['mongo_detail'] = data_service.get_resource('Mongo', dic['mongo'])
        dic['mysql'] = self.mysql
        if dic['mysql']:
            dic['mysql_detail'] = data_service.get_resource('Mysql', dic['mysql'])
        dic['father_mission_name'] = self.father_mission_name
        return str(dic)

if __name__ == '__main__':
    task = Task('163.com', 'Whitelist', {'core_reids' : 'useful_redis', 'filter_redis': 'useful_redis', 'mongo': 'useful_mongo', 'mysql': 'useful_mysql'}, '默认设置1', 'MISSION1')
    print task.get_dic_str()
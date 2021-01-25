from utils.apiview import GomAPIView
from utils.tools import check_param
from zoning.models import Zoning

import json


class ZoningCreate(GomAPIView):
    """
    行政区划创建
    """

    @check_param(
        must_param=['name', 'code'],
        all_param=['name', 'code', 'level', 'prefix', 'post_code', 'abbreviation', 'administrative_center', 'parent_id']
    )
    def victim(self):
        if Zoning.objects.filter(parent_id=self.data_dict.get('parent_id', 0), name=self.data_dict.get('name')).count():
            self.code = 40002
            self.result = '该名称已存在'
            return
        if Zoning.objects.filter(parent_id=self.data_dict.get('parent_id', 0), code=self.data_dict.get('code')).count():
            self.code = 40002
            self.result = "该行政区划编码已存在"
            return

        # 获取父级行政区划
        ad = Zoning.objects.filter(id=self.data_dict.get('parent_id', 0))
        self.data_dict['level'] = ad.level + 1

        Zoning(**self.data_dict).save()
        self.code = 20000
        self.result = '行政区划【{}】创建成功'.format(self.data_dict('name'))


class ZoningUpdate(GomAPIView):
    """
    行政区划更新
    """

    @check_param(
        must_param=['ad_id'],
        all_param=['ad_id', 'name', 'code', 'level', 'prefix', 'post_code', 'abbreviation', 'administrative_center',
                   'parent_id']
    )
    def victim(self):
        ad_id = self.data_dict.get('ad_id')
        if ad_id:
            ad = Zoning.objects.filter(id=ad_id).first()
            if ad:
                if self.data_dict.get('name') and Zoning.objects.exclude(name=self.data_dict.get('name')).count():
                    self.code = 40002
                    self.result = '该名称已存在'
                    return
                if self.data_dict.get('code') and Zoning.objects.exclude(code=self.data_dict.get('code')).count():
                    self.code = 40002
                    self.result = '该行政区划编码已存在'
                    return
                for k, v in self.data_dict.items():
                    if hasattr(ad, k):
                        setattr(ad, k, v)
                ad.save()
                self.code = 20000
                self.result = '行政区划更新成功'
            else:
                self.code = 40000
                self.result = '该行政区划不存在'
        else:
            self.code = 40001
            self.result = '缺失参数-【ad_id】'


class ZoningDelete(GomAPIView):
    """
    行政区划删除
    """

    @check_param(
        must_param=['ad_ids'],
        all_param=['ad_ids']
    )
    def victim(self):
        ad_ids = json.loads(self.data_dict.get('ad_ids'))
        exist_child = []
        no_exist_child = []
        for item in ad_ids:
            adC = Zoning.objects.filter(parent_id=item).count()
            if adC:
                exist_child.append(item)
            else:
                no_exist_child.append(item)
                Zoning.objects.filter(parent_id=item).update(is_active=False)
        self.code = 20000
        if no_exist_child:
            self.result = 'id为【{}】的行政区划删除成功.'.format(','.join(no_exist_child))
        if exist_child:
            self.result += 'id为【{}】的行政区划拥有子节点，未能删除.'.format(','.join(exist_child))


class ZoningDetail(GomAPIView):
    """
    行政区划详情
    """

    @check_param(
        must_param=['ad_id'],
        all_param=['ad_id']
    )
    def victim(self):
        ad_id = self.data_dict.get('ad_id')
        if ad_id:
            ad = Zoning.objects.filter(id=ad_id).first()
            if ad:
                self.data = {
                    'id': ad.id,
                    'name': ad.name,
                    'code': ad.code,
                    'level': ad.level,
                    'prefix': ad.prefix,
                    'post_code': ad.post_code,
                    'abbreviation': ad.abbreviation,
                    'administrative_center': ad.administrative_center,
                    'is_active': ad.is_active,
                    'create_date': ad.create_date,
                    'update_date': ad.update_date,
                    'parent_id': ad.parent_id,
                    'parent_name': ad.parent.name if ad.parent else ''
                }
            else:
                self.code = 40000
                self.result = '该行政区划不存在'
        else:
            self.code = 40001
            self.result = '缺失参数-【ad_id】'


class ZoningList(GomAPIView):
    """
    行政区划列表
    """
    def victim(self):
        parent_id = self.data_dict.get('parent_id')

        ads = Zoning.objects.filter(parent_id=parent_id, is_active=1)

        self.data = ads.values('id', 'name', 'code', 'level', 'prefix', 'post_code', 'abbreviation', 'administrative_center', 'create_date', 'update_date', 'parent_id')

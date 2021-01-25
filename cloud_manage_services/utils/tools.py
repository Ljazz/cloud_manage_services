def check_param(must_param, all_param):
    """
    装饰器 - 用于函数参数的检查
    :param must_param: 必填参数
    :param all_param: 所有参数
    """
    def wrapper(func):
        def decorator(self):
            param_keys = set(self.data_dict.keys())     # 获取到传递的参数的keys，且转换为集合
            # 删除 all_param 中不存在的参数
            non_existent = set(self.data_dict.keys())
            non_existent.difference_update(set(all_param))
            for item in non_existent:
                self.data_dict.pop(item)
            # 检查必填项中的参数是否传递完整
            intersection = set(must_param).intersection(param_keys)     # 交集
            difference = set(must_param).difference(param_keys)         # 差集
            if len(intersection) < len(must_param):
                self.code = 1000
                self.result = '请完善所需的必填 %s' % ",".join(difference)
                return
            # #########################
            func(self)

        return decorator

    return wrapper

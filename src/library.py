import os


def judge_type(data, target_type) -> bool:
    """返回异构类型里元素是否满足目标类型
    Args:
        data ([type]): 异构类型
        target_type ([type]): 目标类型
    Returns:
        bool:满足True,否False
    """
    for each in data:
        if not isinstance(each, target_type):
            return False
    return True


def eachFile(filepath):
    """返回目录下文件路径

    Args:
        filepath ([type]): 目录路径
    """
    pathDir = os.listdir(filepath)
    child = list()
    for allDir in pathDir:
        child.append(os.path.join('%s\\%s' % (filepath, allDir)))
    return child

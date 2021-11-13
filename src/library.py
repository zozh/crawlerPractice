import os


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

import requests
import json
import configparser
import os
from datetime import datetime


'''
读取配置文件内容到环境变量
'''
def load_configs(file_path):
    # 创建 ConfigParser 实例
    config = configparser.ConfigParser()
    # 读取配置文件
    if not os.path.exists(file_path):
        print(f"文件路径：{file_path} 不存在，\n当前工作目录：{os.getcwd()}")
        return
    config.read(file_path)
    # 将配置信息存储为环境变量
    for section in config.sections():
        for key, value in config.items(section):
            os.environ[key] = value


'''
获取请求头
'''
def fs_get_headers():
    url= "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal/" 
    # 应用凭证里的 app id 和 app secret  
    post_data = {"app_id": os.environ.get("app_id"), "app_secret": os.environ.get("app_secret")}
    r = requests.post(url, data=post_data)
    access_token = r.json()["tenant_access_token"] 
    headers = {
        "Content-Type": "application/json; charset=utf-8", 
        "Authorization": f"Bearer {access_token}"
    }
    return headers


'''
发送消息
doc-link https://open.feishu.cn/document/server-docs/im-v1/message/create
接口限制：1000 次/分钟、50 次/秒

receive_id_type值：
- 私聊 user_id 
- 群聊 chat_id

msg_type: 
doc-link https://open.feishu.cn/document/server-docs/im-v1/message-content-description/create_json

'''
def fs_send_msg(headers, post_data, receive_id_type):
    url= f"https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type={receive_id_type}"  
    r = requests.post(url, headers=headers, data=json.dumps(post_data))
    result = r.json()
    return result

'''
    向飞书基础表格追加数据。
    doc-link https://open.feishu.cn/document/server-docs/docs/sheets-v3/data-operation/append-data

    Args:
        spreadsheet_token (str): 电子表格的 token，获取方法参考 README.md 文档
        sheet_id (str): 电子表格里的sheet对应ID，获取方法参考 README.md 文档
        value_range (str): 要写入的表格区域，如：A1:B1，一般只要写入区域大于新增数据行列即可
        new_datas (list): 新增数据，每一行数据作为一个list，如：[["微信公众号", "简说Python"],["CSDN", "简说Python"], ["掘金", "老表"]]

    Returns:
        数据写入请求响应内容，类型为字典(dict), 如果成功 dict["msg"] 为 success，否则为 fail

    Example:
        正常返回结果：
        {'code': 0,
         'data': {'revision': xx,
          'spreadsheetToken': 'PQVxxxxxxxxxxxxxxxxxxUh',
          'tableRange': 'kxxxxxY!A2:B4',  # 写入数据区域
          'updates': {'revision': xx,
           'spreadsheetToken': 'PQVxxxxxxxxxxxxxxxxxxUh',
           'updatedCells': 6,    # 写入数据占多少个单元格
           'updatedColumns': 2,  # 写入数据列数
           'updatedRange': 'kxxxxxY!A2:B4',  # 写入数据区域
           'updatedRows': 3}},   # 写入数据行数
         'msg': 'success'}       # 是否写入成功
'''
def fs_add_sheet_data(headers, spreadsheet_token, sheet_id, value_range, new_datas):
    data_raw = {
      "valueRange": {
        "range": f"{sheet_id}!{value_range}",
        "values": [
          new_datas
        ]
      }
    }
    url = f"https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/{spreadsheet_token}/values_append"    
    response = requests.post(url, data=json.dumps(data_raw), headers=headers)
    link = f'{os.environ.get("home_link")}/sheets/{os.environ.get("spreadsheet_token")}?sheet={os.environ.get("sheet_id")}'
    if response.status_code == 200:
        return response.json(), link
    else:
        return {'msg': 'fail', 'info': f'请求出错，状态码：{response.status_code} 返回内容：{response.json()}'}, link
    
# 获取当前年月日 格式 xxxx-xx-xx
def get_date_str(delimiter):
    now = datetime.now()
    return f"{now.year}{delimiter}{now.month}{delimiter}{now.day}"
    
'''
处理获取到的数据，调用 add_sheet_data 存入对应表格
'''
def fs_add_excel(headers, content, sender):
    spreadsheet_token = os.environ.get("spreadsheet_token")
    sheet_id = SHEET_ID = os.environ.get("sheet_id")
    value_range = "A1:F5"
    new_datas = content.split()
    if len(new_datas) == 3:
        # 没有备注内容 渠道、类型、金额
        new_datas = [get_date_str(r"/")] + new_datas + ["", sender]
    elif len(new_datas) == 4:
        # 有备注内容 渠道、类型、金额、备注
        new_datas = [get_date_str(r"/")] + new_datas + [sender]
    new_datas[3] = float(new_datas[3])
    if new_datas[1] == "支出":
         new_datas[3] = -new_datas[3]
    r = fs_add_sheet_data(headers, spreadsheet_token, sheet_id, value_range, new_datas)
    return r
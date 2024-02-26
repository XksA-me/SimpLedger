from flask import Flask, request, jsonify
from funcs import *

app = Flask(__name__)


'''
接收飞书消息接口
'''
@app.route('/func', methods=['POST'])
def get_feishu():
    try:
        data = request.json  # 解析收到的 JSON 数据
        print(data)
        if data:
            if process_text(data):
                # 原样返回数据
                return jsonify(data)
            else:
                return "【send_text异常】", 404
        else:
            return "Missing 'data' field in the request data", 400
    except Exception as e:
        return str(e), 500
    
    
'''
发送消息
'''
def send_msg(user_id, msg_type, content):
    receive_id_type = "user_id"
    post_data = {
          "receive_id": user_id,
          "msg_type": msg_type,
          "content": content,
          # "uuid": "选填，每次调用前请更换，如a0d69e20-1dd1-458b-k525-dfeca4015204"
        }
    result = fs_send_msg(fs_get_headers(), post_data, receive_id_type)
    if result.get("code")==0:
        return True
    else:
        print(f"【send_msg 请求回复】{result}")
        return False
    
    
    
'''
处理获取到的消息
'''
def process_text(data):
    try:
        user_id = data.get("event").get("sender").get("sender_id").get("user_id")
        text = json.loads(data.get("event").get("message").get("content")).get("text")
        if user_id and text:
            msg_type = "text"
            if text[:4] == "/jz ":
                content = add_bill(user_id, text)
            else: 
                content = "{\"text\": \"你说 %s\"}"%text
            # 调用 send_msg 发消息
            send_msg(user_id, msg_type, content)
            return True
        else:
            print(f"【process_text】{data}")
            return False
    except Exception as e:
        print(f"【process_text】异常错误：{e}")
        return False

    
'''
添加账单
'''
def add_bill(user_id, text):
    r = fs_add_excel(fs_get_headers(), text[4:], user_id)
    if r[0]["msg"] == "success":
        content = "{\"text\": \"添加成功，文档地址：%s\"}"%r[1]
    else:
        content = "{\"text\": \"添加失败，错误信息：%s\"}"%r[0]['info']
    return content
    
    

if __name__ == '__main__':
    # 配置文件路径
    file_path = "./configs.ini"
    # 载入配置信息
    load_configs(file_path)
    app.run(debug=True, port=8003, host="0.0.0.0")
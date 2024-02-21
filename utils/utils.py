import time,random,uuid,sys,hashlib

# 随机延迟
def randomSleep(min_val, max_val):
    num = random.randint(min_val, max_val)
    print(f"随机等待{num}秒后继续>>>>>>>>>>>")
    time.sleep(num)

# 生成uuid    
def randomUuid():
    random_uuid = str(uuid.uuid4())
    return random_uuid
    
# 修改print方法 避免某些环境下python执行print 不会去刷新缓存区导致信息第一时间不及时输出
def printNow(content):
    print(content)
    sys.stdout.flush()
    
# 生成时间戳
def timeStamp(length):
    if length == 10:
        return int(time.time())
    elif length == 16:
        return int(time.time() * 1000)
    else:
        print("时间戳生成失败")
        return

# sha256加密        
def sha256encode(string):
    hash_object = hashlib.sha256(string.encode('utf-8'))
    hex_dig = hash_object.hexdigest()
    return hex_dig

# 随机数字
def random_number(index):
    random_number = ''.join(random.choices('0123456789', k=index))
    return random_number

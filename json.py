import json
import re
from datetime import datetime

# 读取 user_result.txt 文件内容
with open('./output/user_result.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 初始化与 2.json 类似的结构
data = {
    "about": "",
    "updateTime": "",
    "wallpapers": [],
    "sites": [],
    "lives": [],
    "flags": [],
    "parses": [
        {"name": "Json并发", "type": 2, "url": "Parallel"},
        {"name": "解析1.1", "type": 1, "url": "https://cache.json.icu/s1804857380.php?url="},
        {"name": "解析1.2", "type": 1, "url": "http://htp.behds.cn/json/20233234567/fy4k2.php?url="},
        {"name": "解析1.3", "type": 1, "url": "https://jxjson.sc1080.top?url="},
        {"name": "解析1.4", "type": 1, "url": "https://cache.json.icu/a1804857380.php?url="},
        {"name": "解析1.5", "type": 1, "url": "http://110.42.7.182:881/api/?key=c4c3p0YQDnvmdaoVnT&url="},
        {"name": "解析1.6", "type": 1, "url": "http://llyh.xn--yi7aa.top/api/?key=5b317c16d457b31a3150d87c0a362a9e&url="},
        {"name": "解析1.7", "type": 1, "url": "..."}
    ],
    "ijk": [
        {
            "group": "硬解码",
            "options": [
                {"category": 4, "name": "opensles", "value": "0"},
                {"category": 4, "name": "overlay-format", "value": "842225234"},
                {"category": 4, "name": "framedrop", "value": "1"},
                {"category": 4, "name": "soundtouch", "value": "1"},
                {"category": 4, "name": "start-on-prepared", "value": "1"},
                {"category": 1, "name": "http-detect-range-support", "value": "0"},
                {"category": 1, "name": "fflags", "value": "fastseek"},
                {"category": 2, "name": "skip_loop_filter", "value": "48"},
                {"category": 4, "name": "reconnect", "value": "1"},
                {"category": 4, "name": "max-buffer-size", "value": "52428800"},
                {"category": 4, "name": "max_cached_duration", "value": "3000"},
                {"category": 4, "name": "enable-accurate-seek", "value": "0"},
                {"category": 4, "name": "mediacodec", "value": "1"},
                {"category": 4, "name": "mediacodec-auto-rotate", "value": "1"},
                {"category": 4, "name": "mediacodec-handle-resolution-change", "value": "1"},
                {"category": 4, "name": "mediacodec-hevc", "value": "1"},
                {"category": 1, "name": "analyzeduration", "value": "10000"},
                {"category": 4, "name": "sync-av-start", "value": "0"},
                {"category": 4, "name": "packet-buffering", "value": "0"},
                {"category": 4, "name": "vol", "value": "256"},
                {"category": 1, "name": "dns_cache_clear", "value": "1"},
                {"category": 1, "name": "dns_cache_timeout", "value": "-1"}
            ]
        },
        {
            "group": "软解码",
            "options": [
                {"category": 4, "name": "opensles", "value": "0"},
                {"category": 4, "name": "overlay-format", "value": "842225234"},
                {"category": 4, "name": "framedrop", "value": "1"},
                {"category": 4, "name": "soundtouch", "value": "1"},
                {"category": 4, "name": "start-on-prepared", "value": "1"},
                {"category": 1, "name": "http-detect-range-support", "value": "0"},
                {"category": 1, "name": "fflags", "value": "fastseek"},
                {"category": 2, "name": "skip_loop_filter", "value": "48"},
                {"category": 4, "name": "reconnect", "value": "1"},
                {"category": 4, "name": "max-buffer-size", "value": "52428800"},
                {"category": 4, "name": "enable-accurate-seek", "value": "0"},
                {"category": 4, "name": "mediacodec", "value": "0"},
                {"category": 4, "name": "mediacodec-auto-rotate", "value": "0"},
                {"category": 4, "name": "mediacodec-handle-resolution-change", "value": "0"},
                {"category": 4, "name": "mediacodec-hevc", "value": "0"},
                {"category": 1, "name": "analyzeduration", "value": "10000"},
                {"category": 4, "name": "sync-av-start", "value": "0"},
                {"category": 4, "name": "packet-buffering", "value": "0"},
                {"category": 4, "name": "vol", "value": "256"},
                {"category": 1, "name": "dns_cache_clear", "value": "1"},
                {"category": 1, "name": "dns_cache_timeout", "value": "-1"}
            ]
        }
    ]
}

current_group = None
for line in lines:
    line = line.strip()
    if not line:
        continue

    # 匹配更新时间
    if line.startswith('🕘️更新时间'):
        parts = line.split(',')
        if len(parts) > 1:
            # 如果文本里没有明确的时间格式, 也可以使用当前时间
            data["updateTime"] = parts[1]
        else:
            data["updateTime"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        continue

    # 匹配分组行, 如 '📺央视频道,#genre#'
    if line.startswith('📺') or line.startswith('💰') or line.startswith('📡') or \
       line.startswith('☘️'):
        parts = line.split(',')
        if parts:
            # 去掉开头表情后作为分组名
            current_group = parts[0][2:]
            data['lives'].append({"group": current_group, "channels": []})
        continue

    # 匹配类似 'CCTV-1,http://...' 的地址
    match = re.match(r'^(.*?),(http.*?m3u8.*?)$', line)
    if match:
        name, url = match.groups()
        if current_group:
            for g in data['lives']:
                if g['group'] == current_group:
                    # 查找是否已有同名频道
                    found_channel = None
                    for ch in g['channels']:
                        if ch['name'] == name:
                            found_channel = ch
                            break
                    if found_channel:
                        found_channel['urls'].append(url)
                    else:
                        g['channels'].append({"name": name, "tvg_name":name,"urls": [url]})
        else:
            # 如果文件里出现没有分组的行, 你也可以做其他处理
            pass

# 如果 updateTime 为空, 设置为当前时间
if not data["updateTime"]:
    data["updateTime"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# 输出到 2.json
with open('./output/user_result.json', 'w', encoding='utf-8') as out:
    json.dump(data, out, ensure_ascii=False, indent=4)
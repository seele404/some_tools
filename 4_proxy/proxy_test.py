import httpx

proxies = {
    "http://": "socks5://127.0.0.1:7890",
    "https://": "socks5://127.0.0.1:7890",
}

try:
    # 使用代理获取IP地址
    with httpx.Client(proxies=proxies) as client:
        response = client.get('https://httpbin.org/ip')
        ip = response.json()['origin']
        print(f"代理服务器IP: {ip}")

    # 使用相同的代理配置以及请求中文结果获取IP归属地
    with httpx.Client(proxies=proxies) as client:
        response = client.get(f'http://ip-api.com/json/{ip}?fields=status,message,country,regionName,city,zip,lat,lon,isp,org,as,query&lang=zh-CN')
        data = response.json()

        if data['status'] == 'success':
            print(f"查询IP: {data['query']}")
            print("IP归属地信息:")
            print(f"国家: {data['country']}")
            print(f"地区: {data['regionName']}")
            print(f"城市: {data['city']}")
            print(f"邮编: {data['zip']}")
            print(f"ISP: {data['isp']}")
            print(f"组织: {data['org']}")
            print(f"AS: {data['as']}")
            print(f"纬度: {data['lat']}, 经度: {data['lon']}")
        else:
            print("获取IP归属地失败:", data['message'])

    # 尝试使用同一代理访问一个外部网站以检测网络连接性
    test_url = 'https://www.google.com'
    with httpx.Client(proxies=proxies, timeout=5.0) as client:  # 设置5秒超时
        response = client.get(test_url)
        if response.status_code == 200:
            print("通过当前IP可以成功入网, 测试地址：https://www.google.com")
        else:
            print("入网测试失败，响应状态码：", response.status_code)
except httpx.NetworkError:
    print("网络不可用，请检查你的网络连接。")
except httpx.RequestError as e:
    print(f"网络请求发生错误：{e}")


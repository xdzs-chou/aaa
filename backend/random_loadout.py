import requests
import random
import json

class RandomLoadout:
    def __init__(self, cookie):
        self.cookie = cookie
        self.base_url = "https://comm.ams.game.qq.com/ide/"
        self.headers = {
            'content-type': 'application/x-www-form-urlencoded;',
            'Cookie': self.cookie
        }
        self.maps_with_requirements = {
            "普通零号大坝": 0,
            "普通长弓溪谷": 0,
            "机密零号大坝": 112500,
            "机密长弓溪谷": 112500,
            "机密航天基地": 187500,
            "机密巴克什": 187500,
            "绝密航天基地": 450000,
            "绝密巴克什": 350000,
            "绝密潮汐监狱": 780000
        }
        self.maps = list(self.maps_with_requirements.keys())

    def get_item_prices(self, item_ids):
        if not item_ids:
            return {}
        url_params = {
            "iChartId": "316969",
            "iSubChartId": "316969",
            "sIdeToken": "NoOapI",
            "method": "dfm/object.price",
            "source": "2",
            "param": json.dumps({"objectIDs": item_ids})
        }
        resp = requests.post(self.base_url, params=url_params, headers=self.headers, verify=False)
        data = resp.json()
        prices = {}
        if data.get("ret") == 0 and data.get("jData", {}).get("data", {}).get("data", {}).get("list"):
            for price_item in data["jData"]["data"]["data"]["list"]:
                item_id = price_item.get("objectID")
                avg_price = price_item.get("avgPrice", 0)
                if item_id:
                    prices[item_id] = avg_price
        return prices

    def get_random_gun_solution(self):
        url = self.base_url
        params = {
            "iChartId": "316969",
            "iSubChartId": "316969",
            "sIdeToken": "NoOapI",
            "method": "dfm/solution.arms.list",
            "source": "2",
            "solutionType": "gun",
            "param": json.dumps({"page": 1, "limit": 20, "solutionType": "gun"})
        }
        resp = requests.post(url, params=params, headers=self.headers, verify=False)
        if "ck过期" in resp.text or "未登录" in resp.text:
            return {"error": "Cookie已过期或未登录"}
        data = resp.json()
        if data.get("ret") == 0:
            gun_list = data["jData"]["data"]["data"]["list"]
            if not gun_list:
                return {"error": "改枪码列表为空"}
            gun_solution = random.choice(gun_list)
            # 获取详细方案
            detail_params = params.copy()
            detail_params["param"] = json.dumps({"solutionType": "gun", "id": gun_solution["id"]})
            detail_resp = requests.post(url, params=detail_params, headers=self.headers, verify=False)
            if "ck过期" in detail_resp.text or "未登录" in detail_resp.text:
                return {"error": "Cookie已过期或未登录"}
            detail_data = detail_resp.json()
            if detail_data.get("ret") == 0:
                detail_list = detail_data["jData"]["data"]["data"].get("list", [])
                if detail_list:
                    return detail_list[0]
        return {"error": "获取改枪码失败"}

    def get_all_items(self):
        params = {
            "iChartId": "316969",
            "iSubChartId": "316969",
            "sIdeToken": "NoOapI",
            "method": "dfm/object.list",
            "source": "2"
        }
        resp = requests.post(self.base_url, params=params, headers=self.headers, verify=False)
        if "ck过期" in resp.text or "未登录" in resp.text:
            return []
        data = resp.json()
        if data.get("ret") == 0 and data.get("jData", {}).get("data", {}).get("data", {}).get("list"):
            return data["jData"]["data"]["data"]["list"]
        return []

    def generate_gun_solution_loadout(self):
        # 获取改枪码列表
        params = {
            "iChartId": "316969",
            "iSubChartId": "316969",
            "sIdeToken": "NoOapI",
            "method": "dfm/solution.arms.list",
            "source": "2",
            "solutionType": "gun",
            "param": json.dumps({"page": 1, "limit": 20, "solutionType": "gun"})
        }
        resp = requests.post(self.base_url, params=params, headers=self.headers, verify=False)
        data = resp.json()
        gun_list = []
        if data.get("ret") == 0 and data.get("jData", {}).get("data", {}).get("data", {}).get("list"):
            gun_list = data["jData"]["data"]["data"]["list"]
        if not gun_list:
            return {"error": "改枪码列表为空或Cookie无效"}
        gun_solution = random.choice(gun_list)
        # 获取详细方案
        detail_params = params.copy()
        detail_params["param"] = json.dumps({"solutionType": "gun", "id": gun_solution["id"]})
        detail_resp = requests.post(self.base_url, params=detail_params, headers=self.headers, verify=False)
        detail_data = detail_resp.json()
        detail_list = []
        if detail_data.get("ret") == 0 and detail_data.get("jData", {}).get("data", {}).get("data", {}).get("list"):
            detail_list = detail_data["jData"]["data"]["data"]["list"]
        if not detail_list:
            return {"error": "改枪码详情获取失败"}
        solution = detail_list[0]
        weapon = solution.get("armsDetail", {})
        solution_name = gun_solution.get("solutionName") or gun_solution.get("name") or solution.get("solutionName") or solution.get("name")
        solution_desc = gun_solution.get("desc") or solution.get("desc")
        accessories = []
        for acc in solution.get("accessoryDetail", []):
            if acc.get("objectID"):
                accessories.append({
                    "objectID": acc.get("objectID"),
                    "slotID": acc.get("slotID")
                })
        # 获取配件详细信息
        relate_map = solution.get("relateMap", {})
        acc_simple = []
        for acc in accessories:
            acc_info = relate_map.get(str(acc["objectID"]))
            if not acc_info or not acc_info.get("objectName"):
                # relateMap查不到时，尝试用全物品表补全
                all_items = self.get_all_items()
                found = next((item for item in all_items if str(item.get("objectID")) == str(acc["objectID"])), None)
                acc_info = found if found else {}
            acc_simple.append({
                "objectID": acc_info.get("objectID", acc["objectID"]),
                "objectName": acc_info.get("objectName", "未知配件"),
                "avgPrice": acc_info.get("avgPrice", 0)
            })
        # 其他装备随机
        all_items = self.get_all_items()
        def pick(names):
            items = [item for item in all_items if item.get("objectName") in names]
            return random.choice(items) if items else None
        helmet = pick([
            "H70 夜视精英头盔", "GT5 指挥官头盔", "DICH-9重型头盔", "H70 精英头盔", "GN 久战重型夜视头盔",
            "GN 重型夜视头盔", "GN 重型头盔", "DICH-1战术头盔", "H09 防暴头盔", "Mask-1铁壁头盔",
            "GT1 战术头盔", "DICH 训练头盔", "MHS 战术头盔", "D6 战术头盔", "MC201 头盔",
            "DAS 防弹头盔", "H07 战术头盔", "防暴头盔", "MC防弹头盔", "DRO 战术头盔",
            "H01 战术头盔", "复古摩托头盔", "户外棒球帽", "奔尼帽", "安保头盔", "老式钢盔"
        ])
        armor = pick([
            "泰坦防弹装甲", "特里克MAS2.0装甲", "HA-2防弹装甲", "金刚防弹衣", "重型突击背心",
            "FS复合防弹衣", "Hvk-2防弹衣", "精英防弹背心", "HMP特勤防弹衣", "MK-2战术背心",
            "DT-AVS防弹衣", "突击手防弹背心", "武士防弹背心", "射手战术背心", "TG-H防弹衣",
            "Hvk快拆防弹衣", "制式防弹背心", "轻型防弹衣", "尼龙防弹衣", "安保防弹衣", "摩托马甲"
        ])
        backpack = pick([
            "GTO重型战术包", "D7战术背包", "重型登山包", "GT5野战背包", "D3战术登山包",
            "HLS-2重型背包", "ALS背负系统", "生存战术背包", "GT1户外登山包", "D2战术登山包",
            "野战徒步背包", "MAP侦察背包", "雨林猎手背包", "GA野战背包", "DASH战术背包",
            "3H战术背包", "大型登山包", "露营背包", "突袭战术背包", "战术快拆背包",
            "轻型户外背包", "帆布背囊", "DG运动背包", "旅行背包", "运动背包"
        ])
        chest_rig = pick([
            "DAR突击手胸挂", "黑鹰野战胸挂", "飓风战术胸挂", "GIR野战胸挂", "DRC先进侦察胸挂",
            "突击者战术背心", "强袭战术背心", "G01战术弹挂", "DSA战术胸挂", "HD3战术胸挂",
            "简易携行弹挂", "通用战术胸挂", "D01轻型胸挂", "HK3便携胸挂", "尼龙挎包",
            "简易挂载包", "轻型战术胸挂", "快速侦察胸挂", "便携胸包"
        ])
        def simple_item(item):
            if not item:
                return None
            return {
                "objectID": item.get("objectID"),
                "objectName": item.get("objectName"),
                "avgPrice": item.get("avgPrice", 0)
            }
        total_price = (weapon.get("avgPrice", 0) if weapon else 0) + \
                      (helmet.get("avgPrice", 0) if helmet else 0) + \
                      (armor.get("avgPrice", 0) if armor else 0) + \
                      (backpack.get("avgPrice", 0) if backpack else 0) + \
                      (chest_rig.get("avgPrice", 0) if chest_rig else 0) + \
                      sum([acc.get("avgPrice", 0) for acc in acc_simple])
        return {
            "map": random.choice(self.maps),
            "solution_name": solution_name,
            "solution_desc": solution_desc,
            "weapon": simple_item(weapon),
            "helmet": simple_item(helmet),
            "armor": simple_item(armor),
            "backpack": simple_item(backpack),
            "chest_rig": simple_item(chest_rig),
            "accessories": acc_simple,
            "total_price": total_price
        }

    def generate_random_loadout(self):
        # 获取所有物品
        params = {
            "iChartId": "316969",
            "iSubChartId": "316969",
            "sIdeToken": "NoOapI",
            "method": "dfm/object.list",
            "source": "2"
        }
        resp = requests.post(self.base_url, params=params, headers=self.headers, verify=False)
        try:
            data = resp.json()
        except Exception as e:
            print("物品接口返回非JSON:", resp.text)
            return {"error": "物品接口返回非JSON"}
        all_items = []
        if data.get("ret") == 0 and data.get("jData", {}).get("data", {}).get("data", {}).get("list"):
            all_items = data["jData"]["data"]["data"]["list"]
        # 分类物品
        weapon_names = [
            "725双管霰弹枪", "Vector冲锋枪", "MP7冲锋枪", "P90冲锋枪", "QCQ171冲锋枪",
            "AS Val突击步枪", "SR-3M紧凑突击步枪", "G18", "M14射手步枪", "ASh-12战斗步枪",
            "勇士冲锋枪", "S12K霰弹枪", "K416突击步枪", "K437突击步枪", "M7战斗步枪",
            "MP5冲锋枪", "M4A1突击步枪", "腾龙突击步枪", "M1014霰弹枪", "AKM突击步枪",
            "SKS射手步枪", "AUG突击步枪", "M16A4突击步枪", "93R", "SCAR-H战斗步枪",
            "SG552突击步枪", "野牛冲锋枪", "KC17突击步枪", "AK-12突击步枪", "PTR-32突击步枪", "G3战斗步枪"
        ]
        armor_names = [
            "泰坦防弹装甲", "特里克MAS2.0装甲", "HA-2防弹装甲", "金刚防弹衣", "重型突击背心",
            "FS复合防弹衣", "Hvk-2防弹衣", "精英防弹背心", "HMP特勤防弹衣", "MK-2战术背心",
            "DT-AVS防弹衣", "突击手防弹背心", "武士防弹背心", "射手战术背心", "TG-H防弹衣",
            "Hvk快拆防弹衣", "制式防弹背心", "轻型防弹衣", "尼龙防弹衣", "安保防弹衣", "摩托马甲"
        ]
        helmet_names = [
            "H70 夜视精英头盔", "GT5 指挥官头盔", "DICH-9重型头盔", "H70 精英头盔", "GN 久战重型夜视头盔",
            "GN 重型夜视头盔", "GN 重型头盔", "DICH-1战术头盔", "H09 防暴头盔", "Mask-1铁壁头盔",
            "GT1 战术头盔", "DICH 训练头盔", "MHS 战术头盔", "D6 战术头盔", "MC201 头盔",
            "DAS 防弹头盔", "H07 战术头盔", "防暴头盔", "MC防弹头盔", "DRO 战术头盔",
            "H01 战术头盔", "复古摩托头盔", "户外棒球帽", "奔尼帽", "安保头盔", "老式钢盔"
        ]
        chest_rig_names = [
            "DAR突击手胸挂", "黑鹰野战胸挂", "飓风战术胸挂", "GIR野战胸挂", "DRC先进侦察胸挂",
            "突击者战术背心", "强袭战术背心", "G01战术弹挂", "DSA战术胸挂", "HD3战术胸挂",
            "简易携行弹挂", "通用战术胸挂", "D01轻型胸挂", "HK3便携胸挂", "尼龙挎包",
            "简易挂载包", "轻型战术胸挂", "快速侦察胸挂", "便携胸包"
        ]
        backpack_names = [
            "GTO重型战术包", "D7战术背包", "重型登山包", "GT5野战背包", "D3战术登山包",
            "HLS-2重型背包", "ALS背负系统", "生存战术背包", "GT1户外登山包", "D2战术登山包",
            "野战徒步背包", "MAP侦察背包", "雨林猎手背包", "GA野战背包", "DASH战术背包",
            "3H战术背包", "大型登山包", "露营背包", "突袭战术背包", "战术快拆背包",
            "轻型户外背包", "帆布背囊", "DG运动背包", "旅行背包", "运动背包"
        ]
        # 分类
        weapons = [item for item in all_items if item.get("objectName") in weapon_names]
        armors = [item for item in all_items if item.get("objectName") in armor_names]
        helmets = [item for item in all_items if item.get("objectName") in helmet_names]
        chest_rigs = [item for item in all_items if item.get("objectName") in chest_rig_names]
        backpacks = [item for item in all_items if item.get("objectName") in backpack_names]
        accessories = [item for item in all_items if item.get("primaryClass") == "acc"]
        # 随机选择
        selected_map = random.choice(self.maps)
        weapon = random.choice(weapons) if weapons else None
        helmet = random.choice(helmets) if helmets else None
        armor = random.choice(armors) if armors else None
        backpack = random.choice(backpacks) if backpacks else None
        chest_rig = random.choice(chest_rigs) if chest_rigs else None
        num_accessories = random.randint(1, min(3, len(accessories))) if accessories else 0
        selected_accessories = random.sample(accessories, num_accessories) if accessories else []
        # 只保留精简字段
        def simple_item(item):
            if not item:
                return None
            return {
                "objectID": item.get("objectID"),
                "objectName": item.get("objectName"),
                "avgPrice": item.get("avgPrice", 0)
            }
        return {
            "map": selected_map,
            "weapon": simple_item(weapon),
            "helmet": simple_item(helmet),
            "armor": simple_item(armor),
            "backpack": simple_item(backpack),
            "chest_rig": simple_item(chest_rig),
            "accessories": [simple_item(acc) for acc in selected_accessories],
            "total_price": sum([
                (weapon.get("avgPrice", 0) if weapon else 0),
                (helmet.get("avgPrice", 0) if helmet else 0),
                (armor.get("avgPrice", 0) if armor else 0),
                (backpack.get("avgPrice", 0) if backpack else 0),
                (chest_rig.get("avgPrice", 0) if chest_rig else 0),
                sum([acc.get("avgPrice", 0) for acc in selected_accessories])
            ])
        } 
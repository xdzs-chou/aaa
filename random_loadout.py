import requests
import json
import random
from datetime import datetime
from typing import Dict, List, Any

class DeltaForceLoadoutGenerator:
    """三角洲随机配装生成器"""
    
    def __init__(self):
        self.base_url = "https://comm.ams.game.qq.com/ide/"
        self.headers = {
            'Content-Type': 'application/x-www-form-urlencoded;',
            'Cookie': 'openid=D7AF10F0E80DD74A6844FB54A131C95D; acctype=qc; appid=101491592; access_token=57C57406873816CC7BA6C46708C36150'
        }
        
        # 物品分类 - 使用正确的API参数
        self.categories = {
            "weapons": {"primary": "weapon", "second": "gun"},
            "attachments": {"primary": "weapon", "second": "attachment"},
            "helmets": {"primary": "props", "second": "helmet"},
            "armors": {"primary": "props", "second": "armor"},
            "backpacks": {"primary": "props", "second": "backpack"},
            "chest_rigs": {"primary": "props", "second": "chest_rig"},
            "all_items": {"primary": "props", "second": "collection", "objectID": ""}
        }
        
        # 地图列表及其战备值要求
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
        
        # 地图列表
        self.maps = list(self.maps_with_requirements.keys())
        
        self.items_cache = {}
        self.prices_cache = {}

    def get_items_by_category(self, primary_class: str, second_class: str = "") -> List[Dict]:
        """根据分类获取物品列表"""
        try:
            param = {
                "primary": primary_class
            }
            if second_class:
                param["second"] = second_class
                
            url_params = {
                "iChartId": "316969",
                "iSubChartId": "316969",
                "sIdeToken": "NoOapI",
                "method": "dfm/object.list",
                "source": "2",
                "param": json.dumps(param)
            }
            
            response = requests.post(self.base_url, params=url_params, headers=self.headers)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("ret") == 0 and data.get("jData", {}).get("data", {}).get("data", {}).get("list"):
                    items = data["jData"]["data"]["data"]["list"]
                    print(f"✅ 成功获取{primary_class}-{second_class}物品，共{len(items)}个")
                    return items
                else:
                    print(f"❌ 获取{primary_class}-{second_class}物品失败: {data.get('sMsg', '未知错误')}")
            else:
                print(f"❌ {primary_class}-{second_class}物品接口请求失败，状态码: {response.status_code}")
                
        except Exception as e:
            print(f"❌ 获取{primary_class}-{second_class}物品时发生错误: {e}")
            
        return []

    def get_all_items(self) -> Dict[str, List[Dict]]:
        """获取所有分类的物品"""
        print("🔍 正在获取各分类物品...")
        
        items_by_category = {}
        
        # 获取武器 (gun)
        weapons = self.get_items_by_category("gun")
        if weapons:
            items_by_category["weapons"] = weapons
        
        # 获取配件 (acc)
        accessories = self.get_items_by_category("acc")
        if accessories:
            items_by_category["accessories"] = accessories
        
        # 获取所有物品，然后筛选装备
        all_items = self.get_items_by_category("")  # 不传分类参数，获取所有物品
        if all_items:
            print(f"✅ 获取到所有物品: {len(all_items)}个")
            
            # 武器名称列表
            weapon_names = [
                "725双管霰弹枪", "Vector冲锋枪", "MP7冲锋枪", "P90冲锋枪", "QCQ171冲锋枪",
                "AS Val突击步枪", "SR-3M紧凑突击步枪", "G18", "M14射手步枪", "ASh-12战斗步枪",
                "勇士冲锋枪", "S12K霰弹枪", "K416突击步枪", "K437突击步枪", "M7战斗步枪",
                "MP5冲锋枪", "M4A1突击步枪", "腾龙突击步枪", "M1014霰弹枪", "AKM突击步枪",
                "SKS射手步枪", "AUG突击步枪", "M16A4突击步枪", "93R", "SCAR-H战斗步枪",
                "SG552突击步枪", "野牛冲锋枪", "KC17突击步枪", "AK-12突击步枪", "PTR-32突击步枪", "G3战斗步枪"
            ]
            
            # 护甲名称列表
            armor_names = [
                "泰坦防弹装甲", "特里克MAS2.0装甲", "HA-2防弹装甲", "金刚防弹衣", "重型突击背心",
                "FS复合防弹衣", "Hvk-2防弹衣", "精英防弹背心", "HMP特勤防弹衣", "MK-2战术背心",
                "DT-AVS防弹衣", "突击手防弹背心", "武士防弹背心", "射手战术背心", "TG-H防弹衣",
                "Hvk快拆防弹衣", "制式防弹背心", "轻型防弹衣", "尼龙防弹衣", "安保防弹衣", "摩托马甲"
            ]
            
            # 头盔名称列表
            helmet_names = [
                "H70 夜视精英头盔", "GT5 指挥官头盔", "DICH-9重型头盔", "H70 精英头盔", "GN 久战重型夜视头盔",
                "GN 重型夜视头盔", "GN 重型头盔", "DICH-1战术头盔", "H09 防暴头盔", "Mask-1铁壁头盔",
                "GT1 战术头盔", "DICH 训练头盔", "MHS 战术头盔", "D6 战术头盔", "MC201 头盔",
                "DAS 防弹头盔", "H07 战术头盔", "防暴头盔", "MC防弹头盔", "DRO 战术头盔",
                "H01 战术头盔", "复古摩托头盔", "户外棒球帽", "奔尼帽", "安保头盔", "老式钢盔"
            ]
            
            # 胸挂名称列表
            chest_rig_names = [
                "DAR突击手胸挂", "黑鹰野战胸挂", "飓风战术胸挂", "GIR野战胸挂", "DRC先进侦察胸挂",
                "突击者战术背心", "强袭战术背心", "G01战术弹挂", "DSA战术胸挂", "HD3战术胸挂",
                "简易携行弹挂", "通用战术胸挂", "D01轻型胸挂", "HK3便携胸挂", "尼龙挎包",
                "简易挂载包", "轻型战术胸挂", "快速侦察胸挂", "便携胸包"
            ]
            
            # 背包名称列表
            backpack_names = [
                "GTO重型战术包", "D7战术背包", "重型登山包", "GT5野战背包", "D3战术登山包",
                "HLS-2重型背包", "ALS背负系统", "生存战术背包", "GT1户外登山包", "D2战术登山包",
                "野战徒步背包", "MAP侦察背包", "雨林猎手背包", "GA野战背包", "DASH战术背包",
                "3H战术背包", "大型登山包", "露营背包", "突袭战术背包", "战术快拆背包",
                "轻型户外背包", "帆布背囊", "DG运动背包", "旅行背包", "运动背包"
            ]
            
            # 筛选头盔类物品
            helmet_items = []
            for item in all_items:
                item_name = item.get("objectName", "")
                if item_name in helmet_names:
                    helmet_items.append(item)
            if helmet_items:
                items_by_category["helmets"] = helmet_items
                print(f"✅ 筛选出头盔类物品: {len(helmet_items)}个")
            
            # 筛选护甲类物品
            armor_items = []
            for item in all_items:
                item_name = item.get("objectName", "")
                if item_name in armor_names:
                    armor_items.append(item)
            if armor_items:
                items_by_category["armors"] = armor_items
                print(f"✅ 筛选出护甲类物品: {len(armor_items)}个")
            
            # 筛选背包类物品
            backpack_items = []
            for item in all_items:
                item_name = item.get("objectName", "")
                if item_name in backpack_names:
                    backpack_items.append(item)
            if backpack_items:
                items_by_category["backpacks"] = backpack_items
                print(f"✅ 筛选出背包类物品: {len(backpack_items)}个")
            
            # 筛选胸挂类物品
            chest_rig_items = []
            for item in all_items:
                item_name = item.get("objectName", "")
                if item_name in chest_rig_names:
                    chest_rig_items.append(item)
            if chest_rig_items:
                items_by_category["chest_rigs"] = chest_rig_items
                print(f"✅ 筛选出胸挂类物品: {len(chest_rig_items)}个")
        
        print(f"📊 物品分类统计:")
        for category, items in items_by_category.items():
            print(f"  {category}: {len(items)}个")
        
        return items_by_category

    def filter_items_by_keywords(self, items: List[Dict], keywords: List[str]) -> List[Dict]:
        """根据关键词过滤物品"""
        filtered_items = []
        for item in items:
            item_name = item.get("objectName", "").lower()
            item_desc = item.get("desc", "").lower()
            item_second_class = item.get("secondClassCN", "").lower()
            
            for keyword in keywords:
                if (keyword.lower() in item_name or 
                    keyword.lower() in item_desc or 
                    keyword.lower() in item_second_class):
                    filtered_items.append(item)
                    break
        
        return filtered_items

    def get_item_prices(self, item_ids: List[int]) -> Dict[int, int]:
        """获取物品价格"""
        if not item_ids:
            return {}
            
        # 检查缓存
        cached_prices = {}
        uncached_ids = []
        for item_id in item_ids:
            if item_id in self.prices_cache:
                cached_prices[item_id] = self.prices_cache[item_id]
            else:
                uncached_ids.append(item_id)
        
        if not uncached_ids:
            return cached_prices
            
        try:
            url_params = {
                "iChartId": "316969",
                "iSubChartId": "316969",
                "sIdeToken": "NoOapI",
                "method": "dfm/object.price",
                "source": "2",
                "param": json.dumps({"objectIDs": uncached_ids})
            }
            
            response = requests.post(self.base_url, params=url_params, headers=self.headers)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("ret") == 0 and data.get("jData", {}).get("data", {}).get("data", {}).get("list"):
                    price_list = data["jData"]["data"]["data"]["list"]
                    for price_item in price_list:
                        item_id = price_item.get("objectID")
                        avg_price = price_item.get("avgPrice", 0)
                        if item_id:
                            self.prices_cache[item_id] = avg_price
                            cached_prices[item_id] = avg_price
                    print(f"✅ 成功获取{len(price_list)}个物品价格")
                else:
                    print(f"❌ 获取物品价格失败: {data.get('sMsg', '未知错误')}")
            else:
                print(f"❌ 价格接口请求失败，状态码: {response.status_code}")
                
        except Exception as e:
            print(f"❌ 获取物品价格时发生错误: {e}")
            
        return cached_prices

    def get_daily_password(self) -> str:
        """获取每日密码"""
        try:
            payload = {
                "iChartId": "384918",
                "iSubChartId": "384918",
                "sIdeToken": "mbq5GZ",
                "method": "dist.contents",
                "param": '{"distType":"bannerManage","contentType":"secretDay"}'
            }
            
            response = requests.post(self.base_url, data=payload, headers=self.headers)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("ret") == 0 and data.get("jData", {}).get("data", {}).get("data", {}).get("content", {}).get("secretDay", {}).get("data"):
                    secret_data = data["jData"]["data"]["data"]["content"]["secretDay"]["data"][0]
                    return secret_data.get("desc", "今日密码获取失败")
                else:
                    return "今日密码获取失败"
            else:
                return f"密码请求失败，状态码: {response.status_code}"
                
        except Exception as e:
            return f"获取密码时发生错误: {e}"

    def generate_random_loadout(self) -> Dict[str, Any]:
        """生成随机配装方案"""
        print("🎯 正在生成随机配装方案...")
        
        # 获取所有分类的物品
        items_by_category = self.get_all_items()
        
        # 随机选择地图
        selected_map = random.choice(self.maps)
        map_requirement = self.maps_with_requirements[selected_map]
        
        print(f"🗺️  随机选择地图: {selected_map} (战备值要求: {map_requirement:,} 金币)")
        
        loadout = {
            "map": selected_map,
            "map_requirement": map_requirement,
            "weapon": None,
            "accessories": [],
            "helmet": None,
            "armor": None,
            "backpack": None,
            "chest_rig": None,
            "total_price": 0
        }
        
        # 随机选择武器
        if "weapons" in items_by_category and items_by_category["weapons"]:
            loadout["weapon"] = random.choice(items_by_category["weapons"])
            loadout["total_price"] += loadout["weapon"].get("avgPrice", 0)
            print(f"🔫 选择武器: {loadout['weapon']['objectName']} - {loadout['weapon']['avgPrice']:,} 金币")
        
        # 随机选择配件 (根据地图要求调整数量)
        if "accessories" in items_by_category and items_by_category["accessories"]:
            # 根据地图战备值要求调整配件数量
            base_accessories = 1
            if map_requirement >= 187500:  # 机密地图
                base_accessories = 2
            if map_requirement >= 350000:  # 绝密地图
                base_accessories = 3
            
            num_accessories = min(base_accessories, len(items_by_category["accessories"]))
            selected_accessories = random.sample(items_by_category["accessories"], num_accessories)
            loadout["accessories"] = selected_accessories
            for acc in selected_accessories:
                loadout["total_price"] += acc.get("avgPrice", 0)
            print(f"🔧 选择配件: {len(selected_accessories)}个 (地图要求: {map_requirement:,} 战备值)")
        
        # 随机选择头盔
        if "helmets" in items_by_category and items_by_category["helmets"]:
            loadout["helmet"] = random.choice(items_by_category["helmets"])
            loadout["total_price"] += loadout["helmet"].get("avgPrice", 0)
            print(f"🪖 选择头盔: {loadout['helmet']['objectName']} - {loadout['helmet']['avgPrice']:,} 金币")
        
        # 随机选择护甲
        if "armors" in items_by_category and items_by_category["armors"]:
            loadout["armor"] = random.choice(items_by_category["armors"])
            loadout["total_price"] += loadout["armor"].get("avgPrice", 0)
            print(f"🛡️  选择护甲: {loadout['armor']['objectName']} - {loadout['armor']['avgPrice']:,} 金币")
        
        # 随机选择背包
        if "backpacks" in items_by_category and items_by_category["backpacks"]:
            loadout["backpack"] = random.choice(items_by_category["backpacks"])
            loadout["total_price"] += loadout["backpack"].get("avgPrice", 0)
            print(f"🎒 选择背包: {loadout['backpack']['objectName']} - {loadout['backpack']['avgPrice']:,} 金币")
        
        # 随机选择胸挂
        if "chest_rigs" in items_by_category and items_by_category["chest_rigs"]:
            loadout["chest_rig"] = random.choice(items_by_category["chest_rigs"])
            loadout["total_price"] += loadout["chest_rig"].get("avgPrice", 0)
            print(f"🎽 选择胸挂: {loadout['chest_rig']['objectName']} - {loadout['chest_rig']['avgPrice']:,} 金币")
        
        return loadout

    def get_random_gun_solution(self) -> dict:
        """随机获取一把枪械的改枪码方案（含配件）"""
        import requests, random, json
        url = "https://comm.ams.game.qq.com/ide/"
        params = {
            "iChartId": "316969",
            "iSubChartId": "316969",
            "sIdeToken": "NoOapI",
            "method": "dfm/solution.arms.list",
            "source": "2",
            "solutionType": "gun",
            "param": json.dumps({"page": 1, "limit": 20, "solutionType": "gun"})
        }
        headers = {
            'content-type': 'application/x-www-form-urlencoded;'
        }
        resp = requests.post(url, params=params, headers=headers)
        data = resp.json()
        if data.get("ret") == 0:
            gun_list = data["jData"]["data"]["data"]["list"]
            if not gun_list:
                print("❌ 改枪码列表为空")
                return {}
            gun_solution = random.choice(gun_list)
            # 获取详细方案
            detail_params = params.copy()
            detail_params["param"] = json.dumps({"solutionType": "gun", "id": gun_solution["id"]})
            detail_resp = requests.post(url, params=detail_params, headers=headers)
            detail_data = detail_resp.json()
            if detail_data.get("ret") == 0:
                detail_list = detail_data["jData"]["data"]["data"].get("list", [])
                if detail_list:
                    return detail_list[0]
        print("❌ 获取改枪码失败")
        return {}

    def generate_gun_solution_loadout(self) -> dict:
        """生成基于改枪码的配装方案"""
        print("🎯 正在生成改枪码配装方案...")
        # 随机选择地图
        selected_map = random.choice(self.maps)
        map_requirement = self.maps_with_requirements[selected_map]
        print(f"🗺️  随机选择地图: {selected_map} (战备值要求: {map_requirement:,} 金币)")
        # 获取改枪码方案
        solution = self.get_random_gun_solution()
        if not solution:
            print("❌ 改枪码方案获取失败，使用普通随机配装")
            return self.generate_random_loadout()
        # 主武器
        weapon = solution.get("armsDetail", {})
        # 配件objectID列表
        acc_ids = [acc.get("objectID") for acc in solution.get("accessoryDetail", []) if acc.get("objectID")]
        # 获取配件价格
        acc_prices = self.get_item_prices(acc_ids)
        acc_total_price = sum(acc_prices.values())
        # 其他装备
        items_by_category = self.get_all_items()
        helmet = random.choice(items_by_category["helmets"]) if "helmets" in items_by_category and items_by_category["helmets"] else None
        armor = random.choice(items_by_category["armors"]) if "armors" in items_by_category and items_by_category["armors"] else None
        backpack = random.choice(items_by_category["backpacks"]) if "backpacks" in items_by_category and items_by_category["backpacks"] else None
        chest_rig = random.choice(items_by_category["chest_rigs"]) if "chest_rigs" in items_by_category and items_by_category["chest_rigs"] else None
        total_price = weapon.get("avgPrice", 0) + acc_total_price
        for equip in [helmet, armor, backpack, chest_rig]:
            if equip:
                total_price += equip.get("avgPrice", 0)
        return {
            "map": selected_map,
            "map_requirement": map_requirement,
            "weapon": weapon,
            "accessories": [acc for acc in solution.get("accessoryDetail", []) if acc.get("objectID")],
            "accessory_prices": acc_prices,
            "accessory_total_price": acc_total_price,
            "helmet": helmet,
            "armor": armor,
            "backpack": backpack,
            "chest_rig": chest_rig,
            "total_price": total_price,
            "solution_name": solution.get("name", "")
        }

    def display_loadout(self, loadout: Dict[str, Any]):
        """显示配装方案"""
        if not loadout:
            return
            
        print("\n" + "=" * 60)
        print("🎮 三角洲随机配装方案")
        print("=" * 60)
        print(f"🗺️  推荐地图: {loadout['map']}")
        print(f"💰 总价值: {loadout['total_price']:,} 金币")
        print(f"⚔️  地图战备值要求: {loadout['map_requirement']:,} 金币")
        
        # 检查是否满足战备值要求
        if loadout['total_price'] >= loadout['map_requirement']:
            print(f"✅ 战备值充足，可以进入地图")
        else:
            print(f"⚠️  战备值不足，建议增加装备或选择其他地图")
        
        print("-" * 60)
        
        # 显示武器
        if loadout.get("weapon"):
            weapon = loadout["weapon"]
            print(f"🔫 主武器: {weapon['objectName']} (ID: {weapon['objectID']}) - {weapon['avgPrice']:,} 金币")
            if weapon.get("desc"):
                print(f"   描述: {weapon['desc']}")
        
        # 显示配件
        if loadout.get("accessories"):
            print(f"\n🔧 配件 ({len(loadout['accessories'])}个):")
            for i, accessory in enumerate(loadout["accessories"], 1):
                print(f"  {i}. {accessory['objectName']} (ID: {accessory['objectID']}) - {accessory['avgPrice']:,} 金币")
                if accessory.get("desc"):
                    print(f"     描述: {accessory['desc']}")
        
        # 显示装备
        print(f"\n🛡️  装备:")
        
        if loadout.get("helmet"):
            helmet = loadout["helmet"]
            print(f"  🪖 头盔: {helmet['objectName']} (ID: {helmet['objectID']}) - {helmet['avgPrice']:,} 金币")
        
        if loadout.get("armor"):
            armor = loadout["armor"]
            print(f"  🛡️  护甲: {armor['objectName']} (ID: {armor['objectID']}) - {armor['avgPrice']:,} 金币")
        
        if loadout.get("backpack"):
            backpack = loadout["backpack"]
            print(f"  🎒 背包: {backpack['objectName']} (ID: {backpack['objectID']}) - {backpack['avgPrice']:,} 金币")
        
        if loadout.get("chest_rig"):
            chest_rig = loadout["chest_rig"]
            print(f"  🎽 胸挂: {chest_rig['objectName']} (ID: {chest_rig['objectID']}) - {chest_rig['avgPrice']:,} 金币")
        
        print("=" * 60)

    def run(self):
        """运行配装生成器"""
        print(f"🕐 当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("🎮 三角洲随机配装生成器启动中...")
        
        # 获取每日密码
        daily_password = self.get_daily_password()
        print(f"\n🔐 今日密码: {daily_password}")
        
        print("\n请选择配装模式:")
        print("1. 随机配装 (随机选择武器、配件、装备)")
        print("2. 改枪码配装 (随机获取一把枪械的改枪码方案)")
        print("3. 退出")
        
        while True:
            try:
                choice = input("\n请输入选择 (1-3): ").strip()
                
                if choice == "1":
                    print("\n🎯 选择随机配装模式...")
                    # 生成随机配装方案
                    loadout = self.generate_random_loadout()
                    # 显示配装方案
                    self.display_loadout(loadout)
                    break
                    
                elif choice == "2":
                    print("\n🎯 选择改枪码配装模式...")
                    # 生成改枪码配装方案
                    loadout = self.generate_gun_solution_loadout()
                    # 显示配装方案
                    self.display_loadout(loadout)
                    break
                    
                elif choice == "3":
                    print("👋 再见！")
                    return
                    
                else:
                    print("❌ 无效选择，请输入 1、2 或 3")
                    
            except KeyboardInterrupt:
                print("\n👋 用户中断，再见！")
                return
            except Exception as e:
                print(f"❌ 发生错误: {e}")
                break

if __name__ == "__main__":
    generator = DeltaForceLoadoutGenerator()
    generator.run() 
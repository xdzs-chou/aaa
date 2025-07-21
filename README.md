# 三角洲随机配装本地版

一个为三角洲行动游戏设计的随机配装生成器，包含前端Web界面和后端API服务。

## 功能特性

- 🎯 随机生成三角洲行动配装方案
- 🔫 支持改枪码配装模式
- 🗺️ 根据地图战备值要求智能配装
- 💰 显示装备总价值和战备值要求
- 🎨 现代化UI设计，支持装备等级显示
- 📱 响应式设计，支持移动端访问

## 项目结构

```
三角洲随机配装本地版/
├── backend/           # 后端Flask API
│   ├── app.py        # Flask应用主文件
│   ├── random_loadout.py  # 配装生成逻辑
│   ├── requirements.txt   # Python依赖
│   └── cookie.txt    # Cookie配置文件
├── frontend/         # 前端React应用
│   ├── src/
│   │   └── App.jsx   # 主应用组件
│   ├── public/
│   │   └── index.html # HTML模板
│   └── package.json  # Node.js依赖配置
└── random_loadout.py # 独立运行版本
```

## 本地运行

### 后端服务

```bash
cd backend
pip install -r requirements.txt
python app.py
```

后端服务将在 `http://localhost:5000` 启动

### 前端应用

```bash
cd frontend
npm install
npm start
```

前端应用将在 `http://localhost:3000` 启动

## 部署到GitHub Pages

1. 在GitHub上创建新仓库
2. 将代码推送到仓库
3. 安装gh-pages依赖：`npm install gh-pages --save-dev`
4. 修改package.json中的homepage字段为你的GitHub Pages URL
5. 运行部署命令：`npm run deploy`

## 技术栈

- **前端**: React, Axios
- **后端**: Flask, Flask-CORS
- **部署**: GitHub Pages

## 许可证

MIT License 
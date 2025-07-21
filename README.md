# 三角洲行动随机配装生成器

一个基于React和Flask的三角洲行动游戏配装生成器，支持随机生成武器、装备和配件组合。

## 功能特性

- 🎯 随机生成主武器和配件
- 🛡️ 随机生成护甲、头盔、背包、胸挂
- 🗺️ 随机选择地图
- 💰 显示总价格
- 📱 响应式设计，支持移动端
- 🎨 现代化UI设计

## 技术栈

### 前端
- React 18
- Axios
- CSS3

### 后端
- Flask
- Flask-CORS

## 本地开发

### 后端启动
```bash
cd backend
pip install -r requirements.txt
python app.py
```

### 前端启动
```bash
cd frontend
npm install
npm start
```

## 部署

### GitHub Pages部署
1. 将代码推送到GitHub仓库
2. 在仓库设置中启用GitHub Pages
3. 选择gh-pages分支作为源

### 后端部署
需要将后端部署到支持Python的服务器上，如：
- Heroku
- Vercel
- Railway
- 自建服务器

## 访问地址

- 本地开发：http://localhost:3000
- GitHub Pages：https://[用户名].github.io/[仓库名]

## 注意事项

- 确保后端服务器正常运行
- 更新前端代码中的后端API地址
- 配置CORS以允许跨域请求 
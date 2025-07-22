

import React, { useState, useEffect } from 'react';
import axios from 'axios';
// 删除粒子特效相关依赖
// import Particles from "react-tsparticles";
// import { loadFull } from "tsparticles";
// import { useCallback } from "react";

function Item({ title, item }) {
  if (!item) return null;
  return (
    <div style={{
      margin: '8px 0',
      fontSize: 16,
      color: '#222',
      display: 'flex',
      alignItems: 'center',
      letterSpacing: 0.5
    }}>
      <span style={{fontWeight: 600, minWidth: 60, color: '#555'}}>{title}：</span>
      <span>{item.objectName}</span>
      <span style={{marginLeft: 8, color: '#888', fontSize: 14}}>ID: {item.objectID}</span>
      <span style={{marginLeft: 8, color: '#0071e3', fontWeight: 500}}>￥{item.avgPrice}</span>
    </div>
  );
}

const cardBg = {
  random: 'linear-gradient(135deg, #f8fafc 0%, #e0e7ef 100%)',
  gun: 'linear-gradient(135deg, #f5f7fa 0%, #e3e9f7 100%)',
};
const cardShadow = {
  random: '0 8px 32px rgba(0,113,227,0.08)',
  gun: '0 8px 32px rgba(0,0,0,0.10)'
};

// 颜色映射：1灰，2绿，3蓝，4紫，5金，6红
const levelColors = {
  1: { border: '#b0b0b0', title: '#888', bg: '#f7f7fa' }, // 灰
  2: { border: '#4caf50', title: '#388e3c', bg: '#e8f5e9' }, // 绿
  3: { border: '#2196f3', title: '#1565c0', bg: '#e3f2fd' }, // 蓝
  4: { border: '#9c27b0', title: '#6a1b9a', bg: '#f3e5f5' }, // 紫
  5: { border: '#ffb300', title: '#b28704', bg: '#fff8e1' }, // 金
  6: { border: '#e53935', title: '#b71c1c', bg: '#ffebee' }, // 红
  default: { border: '#e0e0e0', title: '#222', bg: '#fff' }
};

// 等级数据
const armorLevels = [
  {name:"泰坦防弹装甲",level:6},{name:"特里克MAS2.0装甲",level:6},{name:"HA-2防弹装甲",level:5},{name:"金刚防弹衣",level:5},{name:"重型突击背心",level:5},{name:"FS复合防弹衣",level:4},{name:"Hvk-2防弹衣",level:4},{name:"精英防弹背心",level:4},{name:"HMP特勤防弹衣",level:4},{name:"MK-2战术背心",level:4},{name:"DT-AVS防弹衣",level:4},{name:"突击手防弹背心",level:4},{name:"武士防弹背心",level:3},{name:"射手战术背心",level:3},{name:"TG-H防弹衣",level:3},{name:"Hvk快拆防弹衣",level:3},{name:"制式防弹背心",level:2},{name:"轻型防弹衣",level:2},{name:"尼龙防弹衣",level:2},{name:"安保防弹衣",level:1},{name:"摩托马甲",level:1}
];
const helmetLevels = [
  {name:"H70 夜视精英头盔",level:6},{name:"GT5 指挥官头盔",level:6},{name:"DICH-9重型头盔",level:6},{name:"H70 精英头盔",level:6},{name:"GN 久战重型夜视头盔",level:5},{name:"GN 重型夜视头盔",level:5},{name:"GN 重型头盔",level:5},{name:"DICH-1战术头盔",level:5},{name:"H09 防暴头盔",level:5},{name:"Mask-1铁壁头盔",level:4},{name:"GT1 战术头盔",level:4},{name:"DICH 训练头盔",level:4},{name:"MHS 战术头盔",level:4},{name:"D6 战术头盔",level:4},{name:"MC201 头盔",level:3},{name:"DAS 防弹头盔",level:3},{name:"H07 战术头盔",level:3},{name:"防暴头盔",level:2},{name:"MC防弹头盔",level:2},{name:"DRO 战术头盔",level:2},{name:"H01 战术头盔",level:2},{name:"复古摩托头盔",level:1},{name:"户外棒球帽",level:1},{name:"奔尼帽",level:1},{name:"安保头盔",level:1},{name:"老式钢盔",level:1}
];
const chestRigLevels = [
  {name:"DAR突击手胸挂",level:5},{name:"黑鹰野战胸挂",level:5},{name:"飓风战术胸挂",level:5},{name:"GIR野战胸挂",level:4},{name:"DRC先进侦察胸挂",level:4},{name:"突击者战术背心",level:4},{name:"强袭战术背心",level:4},{name:"G01战术弹挂",level:3},{name:"DSA战术胸挂",level:3},{name:"HD3战术胸挂",level:3},{name:"简易携行弹挂",level:2},{name:"通用战术胸挂",level:2},{name:"D01轻型胸挂",level:2},{name:"HK3便携胸挂",level:2},{name:"尼龙挎包",level:1},{name:"简易挂载包",level:1},{name:"轻型战术胸挂",level:1},{name:"快速侦察胸挂",level:1},{name:"便携胸包",level:1}
];
const backpackLevels = [
  {name:"GTO重型战术包",level:6},{name:"D7战术背包",level:6},{name:"重型登山包",level:5},{name:"GT5野战背包",level:5},{name:"D3战术登山包",level:5},{name:"HLS-2重型背包",level:5},{name:"ALS背负系统",level:5},{name:"生存战术背包",level:4},{name:"GT1户外登山包",level:4},{name:"D2战术登山包",level:4},{name:"野战徒步背包",level:4},{name:"MAP侦察背包",level:4},{name:"雨林猎手背包",level:4},{name:"GA野战背包",level:3},{name:"DASH战术背包",level:3},{name:"3H战术背包",level:3},{name:"大型登山包",level:3},{name:"露营背包",level:2},{name:"突袭战术背包",level:2},{name:"战术快拆背包",level:2},{name:"轻型户外背包",level:1},{name:"帆布背囊",level:1},{name:"DG运动背包",level:1},{name:"旅行背包",level:1},{name:"运动背包",level:1}
];

function getLevel(item, type) {
  if (!item) return 1;
  if (item.level) return item.level;
  let arr = [];
  if (type === 'armor') arr = armorLevels;
  else if (type === 'helmet') arr = helmetLevels;
  else if (type === 'chest_rig') arr = chestRigLevels;
  else if (type === 'backpack') arr = backpackLevels;
  if (arr.length && item.objectName) {
    const found = arr.find(i => i.name === item.objectName);
    if (found) return found.level;
  }
  return 1;
}

function LoadingSpinner() {
  return (
    <div style={{display:'flex',justifyContent:'center',alignItems:'center',height:120}}>
      <div style={{
        width: 48, height: 48, border: '6px solid #e0e7ef', borderTop: '6px solid #0071e3', borderRadius: '50%',
        animation: 'spin 1s linear infinite'
      }} />
      <style>{`
        @keyframes spin { 0% { transform: rotate(0deg);} 100% { transform: rotate(360deg);} }
      `}</style>
    </div>
  );
}

function EquipCard({ title, item, type, className }) {
  const [hover, setHover] = useState(false);
  if (!item) return null;
  const level = getLevel(item, type);
  const color = levelColors[level] || levelColors.default;
  return (
    <div
      className={className}
      style={{
        border: `3px solid ${color.border}`,
        borderRadius: 28,
        background: color.bg,
        margin: '0',
        padding: '24px 32px',
        minWidth: 360,
        maxWidth: 360,
        width: 360,
        boxShadow: hover ? '0 8px 32px 0 rgba(0,0,0,0.12)' : '0 4px 18px 0 rgba(0,0,0,0.08)',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        fontSize: 22,
        transition: 'box-shadow 0.2s, transform 0.2s',
        transform: hover ? 'scale(1.035)' : 'scale(1)',
        cursor: 'pointer',
        textAlign: 'center',
      }}
      onMouseEnter={()=>setHover(true)}
      onMouseLeave={()=>setHover(false)}
    >
      <div style={{fontWeight: 700, fontSize: 26, color: color.title, marginBottom: 8, letterSpacing: 1, textAlign: 'center'}}>{title}</div>
      <div style={{fontSize: 22, color: '#222', fontWeight: 600, textAlign: 'center'}}>{item.objectName}</div>
      <div style={{fontSize: 15, color: '#888', marginTop: 6, textAlign: 'center'}}>ID: {item.objectID}  价格: ￥{item.avgPrice}</div>
    </div>
  );
}

function WeaponCard({ weapon, accessories }) {
  const [hover, setHover] = useState(false);
  if (!weapon && (!accessories || accessories.length === 0)) return null;
  const level = getLevel(weapon);
  const color = levelColors[level] || levelColors.default;
  return (
    <div
      style={{
        border: `3px solid ${color.border}`,
        borderRadius: 28,
        background: color.bg,
        margin: '18px 0',
        padding: '32px 5vw',
        minWidth: 0,
        minHeight: 120,
        maxWidth: 600,
        width: '100%',
        boxShadow: hover ? '0 8px 32px 0 rgba(0,0,0,0.12)' : '0 4px 18px 0 rgba(0,0,0,0.08)',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'flex-start',
        fontSize: 26,
        transition: 'box-shadow 0.2s, transform 0.2s',
        transform: hover ? 'scale(1.035)' : 'scale(1)',
        cursor: 'pointer',
      }}
      onMouseEnter={()=>setHover(true)}
      onMouseLeave={()=>setHover(false)}
    >
      <div style={{fontWeight: 800, fontSize: 32, color: color.title, marginBottom: 10, letterSpacing: 1}}>主武器 & 配件</div>
      {weapon && <div style={{fontSize: 22, color: '#222', marginBottom: 8, fontWeight: 700}}>{weapon.objectName} <span style={{fontSize:15, color:'#888'}}>ID: {weapon.objectID}  价格: ￥{weapon.avgPrice}</span></div>}
      {accessories && accessories.length > 0 && (
        <div style={{marginTop: 6, fontSize: 18, color: '#0071e3', fontWeight: 600}}>
          配件：{accessories.map((acc, i) => (
            <span key={acc.objectID || i} style={{
              marginRight: 14,
              color: levelColors[getLevel(acc)]?.title || '#333',
              background: '#eaf1fb',
              borderRadius: 8,
              padding: '4px 14px',
              fontSize: 16,
              display: 'inline-block',
              marginBottom: 6,
              fontWeight: 500
            }}>
              {acc.objectName}（ID: {acc.objectID}，价格: {acc.avgPrice}）
            </span>
          ))}
        </div>
      )}
    </div>
  );
}

// 新增地图卡片组件
function MapCard({ map }) {
  const [hover, setHover] = useState(false);
  return (
    <div
      className="equip-card"
      style={{
        border: '3px solid #0071e3',
        borderRadius: 28,
        background: '#f7fafd',
        margin: '0',
        padding: '24px 32px',
        minWidth: 360,
        maxWidth: 360,
        width: 360,
        boxShadow: hover ? '0 8px 32px 0 rgba(0,113,227,0.12)' : '0 4px 18px 0 rgba(0,113,227,0.08)',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        fontSize: 22,
        transition: 'box-shadow 0.2s, transform 0.2s',
        transform: hover ? 'scale(1.035)' : 'scale(1)',
        cursor: 'pointer',
        fontWeight: 700,
        color: '#0071e3',
        letterSpacing: 1,
        textAlign: 'center',
      }}
      onMouseEnter={()=>setHover(true)}
      onMouseLeave={()=>setHover(false)}
    >
      <div style={{fontSize: 26, marginBottom: 6, textAlign: 'center'}}>地图</div>
      <div style={{fontSize: 22, color: '#222', fontWeight: 600, textAlign: 'center'}}>{map}</div>
    </div>
  );
}

// 1. 新增等级徽章组件
function LevelBadge({ level }) {
  if (!level) return null;
  const colors = {
    1: '#CCCCCC', 2: '#4CAF50', 3: '#2196F3', 4: '#9C27B0', 5: '#FFD700', 6: '#FF4D4F'
  };
  const levelNames = { 1: 'Ⅰ', 2: 'Ⅱ', 3: 'Ⅲ', 4: 'Ⅳ', 5: 'Ⅴ', 6: 'Ⅵ' };
  return (
    <span className="level-badge" style={{ background: colors[level], color: '#fff' }}>{levelNames[level]}</span>
  );
}
// 2. 卡片组件
function Card({ title, children, level, price }) {
  const color = levelColors[level] || levelColors.default;
  return (
    <div className="item-container">
      <div
        className="card"
        style={{
          border: `3px solid ${color.border}`,
          color: color.title,
          background: color.bg,
        }}
      >
        <div style={{
          fontWeight: 700,
          fontSize: 24,
          marginBottom: 10,
          letterSpacing: 1,
          color: color.title
        }}>
          {title} {level && <LevelBadge level={level} />}
        </div>
        <div style={{ fontSize: 20, fontWeight: 600, color: '#222' }}>{children}</div>
        {price !== undefined && (
          <div style={{ fontSize: 16, color: '#0071e3', fontWeight: 700, marginTop: 8 }}>价格：￥{price}</div>
        )}
      </div>
    </div>
  );
}
// 新增主武器+配件大卡片
function WeaponAndAccessoriesCard({ weapon, accessories }) {
  // 计算总价
  const weaponPrice = weapon?.avgPrice || 0;
  const accessoriesPrice = (accessories || []).reduce((sum, acc) => sum + (acc.avgPrice || 0), 0);
  const total = weaponPrice + accessoriesPrice;
  return (
    <div className="item-container" style={{width:'100%', maxWidth: '700px'}}>
      <div className="card" style={{width:'100%', maxWidth:'700px', minWidth:260, boxSizing:'border-box', textAlign:'center'}}>
        <div style={{fontWeight:700, fontSize:24, marginBottom:10, letterSpacing:1}}>主武器 & 配件</div>
        <div style={{fontSize:20, fontWeight:600, marginBottom:12}}>
          {weapon?.objectName || '无'}
          {weapon?.avgPrice !== undefined && (
            <span style={{fontSize:16, color:'#0071e3', fontWeight:700, marginLeft:12}}>价格：￥{weapon.avgPrice}</span>
          )}
        </div>
        <div style={{fontSize:18, color:'#0071e3', fontWeight:500, marginBottom:6}}>配件：</div>
        <div style={{fontSize:17, color:'#333', fontWeight:500, display:'flex', flexDirection:'column', alignItems:'center', gap:4}}>
          {accessories && accessories.length > 0 ? accessories.map(acc => (
            <div key={acc.objectID} style={{margin:'2px 0', width:'100%', display:'flex', justifyContent:'center', alignItems:'center', gap:8}}>
              <span>{acc.objectName}</span>
              <span style={{fontSize:15, color:'#888'}}>ID: {acc.objectID}</span>
              <span style={{fontSize:16, color:'#0071e3', fontWeight:700}}>价格：￥{acc.avgPrice}</span>
            </div>
          )) : '无'}
        </div>
        {/* 总价显示 */}
        <div style={{marginTop:14, fontWeight:800, fontSize:20, color:'#ff4d4f'}}>总价格：￥{total}</div>
      </div>
    </div>
  );
}

// 新增：每日密码卡片组件
function DailySecretRow({ secret }) {
  if (!secret) return null;
  // 解析格式："零号大坝:3839;\n长弓溪谷:3424;\n巴克什:6379;\n航天基地:8214;\n潮汐监狱:6900"
  const items = secret.split(/;\s*|\n/).filter(Boolean).map(s => s.trim());
  // 颜色和趣味icon
  const colors = [
    {bg:'#ffe082', color:'#b28704', emoji:'🟡'},
    {bg:'#b3e5fc', color:'#0277bd', emoji:'🔵'},
    {bg:'#c8e6c9', color:'#388e3c', emoji:'🟢'},
    {bg:'#f8bbd0', color:'#c2185b', emoji:'🌸'},
    {bg:'#d1c4e9', color:'#512da8', emoji:'🟣'},
  ];
  return (
    <div style={{
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      gap: 18,
      margin: '0 auto 24px auto',
      padding: '18px 0 0 0',
      position: 'sticky',
      top: 0,
      zIndex: 10,
      background: 'rgba(247,247,250,0.96)',
      borderBottom: '1.5px solid #e0e7ef',
      width: '100%',
      maxWidth: 900
    }}>
      {items.map((item, idx) => {
        const [name, code] = item.split(':');
        const color = colors[idx % colors.length];
        return (
          <div key={item} style={{
            background: color.bg,
            color: color.color,
            borderRadius: 16,
            minWidth: 120,
            minHeight: 54,
            padding: '10px 18px',
            fontWeight: 700,
            fontSize: 18,
            boxShadow: '0 2px 10px 0 rgba(0,0,0,0.07)',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            border: `2.5px solid ${color.color}`,
            position: 'relative',
            transition: 'transform 0.18s',
            cursor: 'pointer',
            userSelect: 'all',
            letterSpacing: 1.2
          }}
          title={name}
          onClick={()=>navigator.clipboard.writeText(code)}
          >
            <span style={{fontSize: 22, marginBottom: 2}}>{color.emoji}</span>
            <span style={{fontSize: 15, color: color.color, fontWeight: 600}}>{name}</span>
            <span style={{fontSize: 22, color: '#222', fontWeight: 800, marginTop: 2}}>{code}</span>
            <span style={{fontSize: 11, color: '#888', marginTop: 2}}>点击复制</span>
          </div>
        );
      })}
    </div>
  );
}

function DailySecretCard({ secret }) {
  if (!secret) return null;
  return (
    <div style={{
      border: '2px solid #0071e3',
      borderRadius: 18,
      background: '#f7fafd',
      margin: '20px auto',
      padding: '24px 32px',
      maxWidth: 400,
      boxShadow: '0 8px 24px 0 rgba(0,113,227,0.08)',
      textAlign: 'center'
    }}>
      <div style={{fontWeight: 700, fontSize: 24, color: '#0071e3', marginBottom: 10}}>每日密码</div>
      <div style={{fontSize: 18, color: '#222', whiteSpace: 'pre-line'}}>{secret}</div>
    </div>
  );
}

// 3. 主内容布局
function App() {
  const [cookie, setCookie] = useState('');
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const [mode, setMode] = useState('gun');
  const [loading, setLoading] = useState(false);
  const [dailySecret, setDailySecret] = useState('');
  const [secretError, setSecretError] = useState('');
  // 删除与改枪码查配装相关的所有useState、handleQueryCode、queryCode、queryResult、queryError、queryLoading、输入框、按钮、结果展示等代码。

  // 页面加载时自动获取每日密码
  useEffect(() => {
    const fetchDailySecret = async () => {
      setSecretError('');
      setDailySecret('');
      try {
        const res = await axios.post('http://localhost:5000/api/daily_secret', {});
        const desc = res.data?.desc || '暂无数据';
        setDailySecret(desc);
      } catch (e) {
        setSecretError('获取每日密码失败');
      }
    };
    fetchDailySecret();
  }, []);

  const getGunSolutionLoadout = async () => {
    setError('');
    setResult(null);
    setLoading(true);
    try {
      // 支持本地开发和生产环境
      const baseUrl = 'http://localhost:5000';
      const url = `${baseUrl}/api/gun_solution_loadout`;
      const res = await axios.post(url, {});
      if (res.data.error) {
        setError(res.data.error);
      } else {
        setResult(res.data);
      }
    } catch (e) {
      setError('请求失败，请检查后端服务是否启动');
    }
    setLoading(false);
  };

  const getDailySecret = async () => {
    setSecretError('');
    setDailySecret('');
    try {
      const res = await axios.post('http://localhost:5000/api/daily_secret', {});
      // 只取 desc 字段
      const desc = res.data?.desc || '暂无数据';
      setDailySecret(desc);
    } catch (e) {
      setSecretError('获取每日密码失败');
    }
  };

  // 删除粒子特效相关函数和变量
  // const particlesInit = useCallback(async (engine) => {
  //   await loadFull(engine);
  // }, []);
  // const particlesOptions = {
  //   background: { color: { value: "#f7f7fa" } },
  //   fpsLimit: 60,
  //   interactivity: {
  //     events: {
  //       onClick: { enable: true, mode: "push" },
  //       onHover: { enable: true, mode: "repulse" },
  //       resize: true
  //     },
  //     modes: {
  //       push: { quantity: 4 },
  //       repulse: { distance: 80, duration: 0.4 }
  //     }
  //   },
  //   particles: {
  //     color: { value: ["#0071e3", "#ffb300", "#ff3b30", "#34c759", "#5856d6"] },
  //     links: { enable: true, color: "#e0e7ef", distance: 120, opacity: 0.3, width: 1 },
  //     collisions: { enable: true },
  //     move: { direction: "none", enable: true, outModes: { default: "bounce" }, random: false, speed: 1.2, straight: false },
  //     number: { density: { enable: true, area: 800 }, value: 40 },
  //     opacity: { value: 0.6 },
  //     shape: { type: "circle" },
  //     size: { value: { min: 2, max: 5 } }
  //   },
  //   detectRetina: true
  // };

  return (
    <div style={{
      minHeight: '100vh',
      width: '100vw',
      position: 'relative',
      overflow: 'auto',
      background: '#f7f7fa',
      fontSize: 20 // 缩小整体字体
    }}>
      {/* 每日密码卡片行，固定在页面顶端 */}
      <DailySecretRow secret={dailySecret} />
      <div className="main">
        <style>{`
          .main {
            max-width: 900px;
            margin: 0 auto;
            padding: 40px 0 0 0;
            text-align: center;
          }
          .container {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            align-items: stretch;
            gap: 28px;
            margin-bottom: 18px;
            width: 100%;
            box-sizing: border-box;
          }
          .item-container {
            flex: 1 1 320px;
            min-width: 260px;
            max-width: 340px;
            margin: 0 8px;
            display: flex;
            flex-direction: column;
            align-items: center;
          }
          .card {
            margin: 20px auto 10px auto;
            padding: 28px 18px 18px 18px;
            background: rgba(255,255,255,0.95);
            border-radius: 18px;
            min-height: 60px;
            font-size: 22px;
            font-weight: 600;
            box-shadow: 0 8px 24px 0 rgba(0,0,0,0.10), 0 1.5px 4px 0 rgba(0,0,0,0.04);
            border: 1.5px solid rgba(0,0,0,0.06);
            position: relative;
            transition: transform 0.18s cubic-bezier(.4,2,.6,1), box-shadow 0.18s;
            width: 340px;
            min-width: 260px;
            max-width: 340px;
            text-align: center;
            box-sizing: border-box;
          }
          .card:hover {
            transform: translateY(-4px) scale(1.03) rotate(-1deg);
            box-shadow: 0 16px 32px 0 rgba(0,0,0,0.13), 0 2px 8px 0 rgba(0,0,0,0.06);
          }
          .level-badge {
            display: inline-block;
            margin-left: 10px;
            padding: 2px 10px;
            border-radius: 12px;
            font-size: 14px;
            font-weight: 700;
            vertical-align: middle;
            color: #fff;
            background: #888;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            letter-spacing: 1px;
          }
          .all-random-btn {
            margin: 24px auto 0 auto;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            background: linear-gradient(90deg, #ff4d4f 60%, #0071e3 100%);
            color: #fff;
            border: none;
            border-radius: 16px;
            font-size: 20px;
            font-weight: 700;
            padding: 20px 0;
            width: 260px;
            max-width: 90vw;
            box-shadow: 0 6px 18px rgba(0,0,0,0.13);
            cursor: pointer;
            transition: background 0.2s, transform 0.18s;
          }
          .all-random-btn:hover {
            background: linear-gradient(90deg, #0071e3 60%, #ff4d4f 100%);
            transform: scale(1.04);
          }
          @media (max-width: 900px) {
            .container {
              flex-direction: column;
              align-items: center;
              gap: 16px;
            }
            .item-container {
              min-width: 98vw;
              max-width: 100vw;
              margin: 0 auto;
              box-sizing: border-box;
            }
            .all-random-btn {
              width: 90vw;
              max-width: 320px;
              font-size: 18px;
              padding: 18px 0;
            }
            .card {
              width: 90vw;
              max-width: 98vw;
            }
          }
        `}</style>
        <h1 style={{fontWeight:800, fontSize:38, marginBottom:32, letterSpacing:1, color:'#222', textShadow:'0 2px 8px #f0f4fa'}}>三角洲行动随机配装生成器</h1>
        <button className="all-random-btn" onClick={getGunSolutionLoadout}><span role="img" aria-label="shuffle">🔀</span> 一键全部随机</button>
        {secretError && <div style={{ color: '#d70015', marginTop: 10 }}>{secretError}</div>}
        {/* <DailySecretCard secret={dailySecret} /> */}
        {error && <div style={{ color: '#d70015', background: '#fff0f0', borderRadius: 12, padding: '14px 18px', marginBottom: 18, fontWeight: 600, fontSize: 20 }}>{error}</div>}
        {loading && <LoadingSpinner />}
        {result && (
          <>
            {/* 地图单独一行居中 */}
            <div className="container" style={{justifyContent:'center'}}>
              <Card title="地图">{result.map}</Card>
            </div>
            {/* 头盔+护甲一行 */}
            <div className="container">
              <Card title="头盔" level={getLevel(result.helmet, 'helmet')} price={result.helmet?.avgPrice}>{result.helmet?.objectName}</Card>
              <Card title="护甲" level={getLevel(result.armor, 'armor')} price={result.armor?.avgPrice}>{result.armor?.objectName}</Card>
            </div>
            {/* 背包+胸挂一行 */}
            <div className="container">
              <Card title="背包" level={getLevel(result.backpack, 'backpack')} price={result.backpack?.avgPrice}>{result.backpack?.objectName}</Card>
              <Card title="胸挂" level={getLevel(result.chest_rig, 'chest_rig')} price={result.chest_rig?.avgPrice}>{result.chest_rig?.objectName}</Card>
            </div>
            {/* 主武器+配件合成一个大卡片 */}
            <div className="container" style={{justifyContent:'center'}}>
              <WeaponAndAccessoriesCard weapon={result.weapon} accessories={result.accessories} />
            </div>
            {/* 新增：显示改枪码 */}
            {result.solution_code && (
              <div style={{marginTop: 18, fontWeight: 700, fontSize: 22, color: '#ff4d4f', textAlign: 'center', letterSpacing: 1}}>
                改枪码：{result.solution_code}
              </div>
            )}
            <div style={{marginTop: 24, fontWeight: 800, fontSize: 28, color: '#0071e3', textAlign: 'center', letterSpacing: 1}}>
              总价格：¥{result.total_price}
            </div>
          </>
        )}
        <div style={{marginTop: 40, color: '#888', fontSize: 15, letterSpacing: 1, opacity: 0.85, zIndex: 2, position: 'relative'}}>Apple 风格设计 | Powered by 三角洲随机配装</div>
      </div>
    </div>
  );
}

export default App; 
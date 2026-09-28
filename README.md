# RAGFlow Chat (前后端分离)

## 目录结构
- `frontend`: React + Vite 前端
- `backend`: Node.js + Express 后端

## 启动

### 1) 后端
```bash
cd backend
cp .env.example .env
npm install
npm run dev
```

### 2) 前端
```bash
cd frontend
npm install
npm run dev
```

前端: http://localhost:5173  
后端: http://localhost:4000

如果看到 Vite 代理报错 `ECONNREFUSED 127.0.0.1:4000`：
- 先确认后端已启动并监听 `4000` 端口；
- 或在启动前端前指定代理目标：
```bash
cd frontend
VITE_API_PROXY_TARGET=http://localhost:4000 npm run dev
```

source chat_venv/bin/activate
python main.py


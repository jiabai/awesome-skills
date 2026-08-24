# 云服务器部署 SOP

> **适用场景**：非技术用户在本地 PC 上完成 vibe coding 后，将项目部署到远程云服务器
> **核心模式**：Agent 指导 + 用户手动操作（绕过 Agent SSH 执行限制）
> **版本**：v1.0 | **适用技术栈**：Node.js / Python / Go

---

## 角色分工

| 角色 | 做什么 | 不做什么 |
|------|--------|----------|
| **用户** | 执行具体操作（复制命令、粘贴到终端） | 不需要理解命令含义 |
| **Agent** | 分析项目、生成部署指令、验证结果、诊断问题 | 不直接执行远程命令 |

**核心原则**：Agent 说"在你的 SSH 终端里输入这行命令"，用户复制粘贴执行，然后把结果告诉 Agent。

---

## 推荐工具

非技术用户不需要安装任何开发工具，只需以下 1-2 款轻量软件来完成部署操作。所有工具均为免费。

### 必备工具（1 款，二选一）

| 工具 | 用途 | 平台 | 下载地址 | 推荐度 |
|------|------|------|----------|--------|
| **Tabby** | SSH 终端 + 内置文件传输 + 跨平台 | Windows / Mac / Linux | [tabby.sh](https://tabby.sh) | ⭐ 推荐 |
| **Windows Terminal** | SSH 远程连接服务器 | Windows | [apps.microsoft.com/detail/9N0DX20HK701](https://apps.microsoft.com/detail/9N0DX20HK701) | 备选 |

> **为什么优先推荐 Tabby**：界面更友好，内置 SFTP 文件传输，支持标签页和多会话，跨平台一致体验，一个工具搞定所有事。

### 可选工具（按需安装）

| 工具 | 用途 | 平台 | 下载地址 | 何时需要 |
|------|------|------|----------|---------|
| **Git** | 代码版本管理、通过 Gitee 仓库上传/更新代码 | Windows / Mac / Linux | [git-scm.com](https://git-scm.com) | 需要版本控制或用 Git 推送代码时 |
| **FinalShell** | 一站式 SSH + 文件管理 + 服务器监控 | Windows | [www.hostbuf.com](https://www.hostbuf.com) | 想要国产中文界面 |
| **宝塔面板** | 浏览器里管理服务器（文件、进程、Nginx） | 浏览器 | 服务器 IP:8888 | 服务器已预装时可直接用 |

> **什么情况下需要装 Git？**
> - 想用 Gitee（码云）管理项目代码（国内访问速度快）
> - 不想每次用 SFTP 手动传文件，希望 `git push` 自动部署
> - 需要回滚到历史版本时用 `git revert` 比手动操作更安全
> - 多人协作开发时需要版本合并
>
> 如果只是单人开发、用 SFTP 传文件，暂时可以不装。
>
> **推荐使用 Gitee（码云）**：[gitee.com](https://gitee.com)
> - 国内访问速度比 GitHub 快
> - 中文界面，操作更友好
> - 免费仓库，支持私有项目
> - 服务器 `git clone` 内网速度快

### 各工具使用说明

#### Tabby（推荐首选）

**安装**：
1. 访问 [tabby.sh](https://tabby.sh) 下载安装包
2. 双击安装 → 按提示完成（默认选项即可）
3. 首次打开会看到欢迎页

**配置 SSH 连接**：
1. 左侧边栏点击 **"Settings"（齿轮图标）**
2. 点击 **"Profiles"** → 点击 **"+"** 新建 Profile
3. 填写：
   - **Name**：输入任意名称，如 `我的云服务器`
   - **Connection type**：选 `SSH`
   - **Host**：服务器 IP 地址
   - **Port**：`22`
   - **Username**：`root`
   - **Authentication**：选 `Private key` → 选择技术支持提供的 SSH 私钥文件（`.pem` 或 `id_rsa`）
4. 点击 **"Save"** 保存

**连接服务器**：
1. 左侧边栏点击刚才创建的 Profile
2. 首次连接会提示确认指纹 → 点击 **"Accept"**
3. 看到终端提示符 `root@my-server:~#` → 连接成功 ✅

**常用快捷键**：
- 复制：`Ctrl+C`（选中后自动复制）
- 粘贴：`Ctrl+Shift+V`
- 新建标签页：`Ctrl+T`
- 新建 SSH 会话：`Ctrl+Shift+N`
- 断开连接：在标签页上右键 → Close

#### Windows Terminal（备选）

**安装**：在 Microsoft Store 搜索 "Windows Terminal" 点击安装

**连接服务器**：
1. 打开 Windows Terminal
2. 输入以下命令（替换服务器 IP）：
```
ssh root@服务器IP
```
3. 首次连接会提示 `Are you sure you want to continue connecting?` → 输入 `yes` 回车
4. 看到 `root@my-server:~#` 提示符 → 连接成功

**注意**：文件上传统一通过 Gitee Git 仓库完成，不依赖文件传输工具。

**常用操作**：
- 复制命令：选中命令文本 → `Ctrl+C`
- 粘贴命令：`Ctrl+V`（或右键点击）
- 新建标签页：`Ctrl+Shift+T`
- 断开连接：输入 `exit` 回车

#### FinalShell（一站式管理备选）

**安装**：从 hostbuf.com 下载，解压即用（绿色版）

**功能**：
- SSH 终端：和 Tabby 一样
- 文件管理：左侧本地、右侧服务器，支持拖拽
- 服务器监控：CPU/内存/磁盘使用率实时显示
- 快捷命令：内置常用命令，一键执行
- 中文界面：国产软件，全中文

**适合人群**：偏好国产中文界面的用户

### 工具选择建议

```
必装（2 个工具）：
  Tabby → SSH 终端，连接服务器执行命令
  Git → 代码推送到 Gitee 仓库

Gitee（gitee.com）：
  国内访问速度快，中文界面，免费私有仓库
  本地 push → 服务器 git pull，完成代码更新

图形化备选：
  FinalShell → 国产中文界面，SSH + 文件管理 + 监控
  （如果不想装 Tabby，可以用 FinalShell 替代）

Mac 用户：
  首选 Tabby（跨平台）+ Git
  或系统自带 Terminal + Git
```

---

## 前置条件（一次性准备）

### 1.1 云服务器已初始化

技术支持需完成以下一次性操作：

```
✅ 云服务器已购买并开机
✅ 已安装 Git（用于从 Gitee 拉取代码）
   → Ubuntu: apt install git -y
   → CentOS: yum install git -y
✅ 已安装 Node.js 22+ / Python 3.11+ / Go 1.22+（根据项目需要）
✅ 已安装 PM2（Node 进程守护）或 supervisor（Python 进程守护）
✅ 已安装 Nginx（反向代理）
✅ 已配置 SSH 密钥免密登录
✅ 已开放安全组端口：22(SSH)、80(HTTP)、443(HTTPS)
✅ 已创建 Gitee 账号并配置好 SSH/HTTPS 免密访问
```

### 1.2 用户本地环境

```
✅ Windows / Mac 电脑一台
✅ 本地代码已由 Agent 开发完成并能正常运行
✅ 用户已安装 Tabby（推荐）或 Windows Terminal
✅ 用户已安装 Git（git-scm.com）
✅ 用户已注册 Gitee 账号（gitee.com）
✅ 用户知道服务器 IP 地址
✅ Gitee 上已创建好项目仓库
```

### 1.3 用户首次连接测试（一次性）

用户在 SSH 终端中执行：

```bash
ssh root@服务器IP
```

如果能直接登录（不需要输密码），说明配置正确。如果提示输入密码或报错，需要联系技术支持重新配置 SSH 密钥。

---

## 部署流程（每次开发完成后）

### Phase 1：准备工作（用户本地执行）

#### Step 1.1：Agent 分析项目

用户："帮我部署到云服务器"

Agent 自动执行：
```
1. 扫描项目文件结构
2. 检测技术栈（Node/Python/Go）
3. 识别：启动命令、端口、依赖文件位置
4. 输出部署清单给用户确认
```

Agent 输出示例：
```
📋 部署清单
━━━━━━━━━━━━━━━━━━
📦 技术栈：Node.js 22
📁 项目路径：/www/wwwroot/myapp
🌐 端口：3000
🚀 启动命令：node server.js
📋 依赖文件：package.json
━━━━━━━━━━━━━━━━━━
准备好开始部署了吗？
```

#### Step 1.2：用户打开 SSH 终端

**用户操作**：打开 SSH 终端并登录服务器

```
在你的 SSH 终端中执行：
ssh root@服务器IP
```

**验证点**：终端提示符变成服务器主机名，如 `root@my-server:~#`

**告诉 Agent**："已登录"

---

### Phase 2：上传代码（通过 Gitee Git 仓库）

#### Step 2.1：首次部署——推送本地项目到 Gitee

**前提**：本地已安装 Git，Gitee 上已创建仓库

**用户操作**：在本地项目目录打开终端（Tabby 或 Windows Terminal），执行：
```bash
cd C:\Users\用户名\projects\myapp
git init
git add .
git commit -m "init"
git remote add origin https://gitee.com/你的用户名/仓库名.git
git push -u origin main
```

**验证点**：登录 Gitee 仓库页面能看到项目文件

**告诉 Agent**："已推送到 Gitee"

#### Step 2.2：首次部署——服务器从 Gitee 拉取代码

**前提**：服务器已安装 Git（技术支持初始化时完成）

**用户操作**：在 SSH 终端执行：
```bash
cd /www/wwwroot && git clone https://gitee.com/你的用户名/仓库名.git myapp
```

**验证点**：执行 `ls /www/wwwroot/myapp` 能看到项目文件（如 package.json、src 目录等）

**告诉 Agent**："代码已拉取"

#### Step 2.3：后续更新（每次开发完成后）

**用户操作**：本地 push + SSH 终端 pull

```bash
# 本地（Tabby/Windows Terminal 中）
cd C:\Users\用户名\projects\myapp
git add .
git commit -m "update"
git push origin main

# SSH 终端中
cd /www/wwwroot/myapp && git pull origin main
```

**验证点**：服务器上执行 `ls` 能看到更新后的文件

**告诉 Agent**："代码已更新"

---

### 服务器部署规范

#### 目录结构约定

```
/www/wwwroot/
├── myapp/                    # 项目根目录（git clone 在这里）
│   ├── package.json           # Node.js 依赖声明
│   ├── node_modules/          # 依赖包（npm install 生成）
│   ├── dist/                  # 前端构建产物（npm run build 生成）
│   ├── build/                 # 后端构建产物（Go/编译型语言）
│   ├── server.js              # 应用入口文件
│   └── ...                    # 其他源码文件
│
/var/log/myapp/                # 应用日志目录（PM2 输出）
│   ├── out.log                # 标准输出日志
│   └── error.log              # 错误日志
│
/etc/nginx/sites-available/   # Nginx 配置目录
│   └── myapp                  # 当前应用的 Nginx 配置
```

**约定说明**：
- 所有项目文件统一放在 `/www/wwwroot/myapp/`
- 不要把构建产物放去别的目录，就在项目根目录内
- 日志放在 `/var/log/myapp/`，PM2 启动时会自动创建
- Nginx 配置统一管理，所有网站的配置都在这里

---

### Phase 3：安装依赖 & 构建（用户在 SSH 终端执行）

#### Step 3.1：进入项目目录

**用户操作**：在 SSH 终端执行：
```bash
cd /www/wwwroot/myapp
```

**验证点**：终端提示符前显示当前路径，执行 `pwd` 输出 `/www/wwwroot/myapp`

#### Step 3.2：安装依赖

Agent 根据技术栈给出命令：

```bash
# Node.js 项目
npm install --production

# Python 项目
pip install -r requirements.txt

# Go 项目（无依赖，跳过此步）
# echo "no dependencies"
```

**说明**：`--production` 参数表示只安装生产环境依赖，跳过测试/开发用的包，节省空间

**验证点**：
- Node：输出 `added XXX packages`，没有 `npm ERR!`
- Python：输出 `Successfully installed XXX`
- Go：跳过此步

**告诉 Agent**："依赖安装完成"

#### Step 3.3：构建项目（编译型步骤）

**什么是构建？** 把源代码编译成可以直接运行的产物。比如 Vue/React 需要把 `.vue`/`.jsx` 文件编译成浏览器能识别的 `.html`/`.js` 文件。

Agent 检测项目是否有构建脚本：
- 有 `package.json` 中的 `build` 脚本 → 执行构建
- Go 项目 → 编译成可执行文件
- 纯 Python/Node.js（无构建）→ 跳过

```bash
# Node.js 项目（如果有 build 脚本）
npm run build

# Go 项目（编译成二进制文件）
go build -o build/myapp

# Python 项目 / 纯 Node.js（无构建步骤）
# 跳过
```

**构建产物在哪？**
- Node.js 前端项目：产物在 `dist/` 目录
- Go 项目：产物在 `build/myapp` 可执行文件
- 纯后端项目：没有构建产物，直接用源码运行

**验证点**：
- Node.js：输出 `compiled successfully` 或 `built in X.XXs`
- Go：`ls build/myapp` 文件存在
- 无构建步骤：跳过

**告诉 Agent**："构建完成"

---

### Phase 4：启动应用 & 服务管理（用户在 SSH 终端执行）

#### Step 4.1：用 PM2 启动应用

**PM2 是什么？** 一个进程管理工具，负责让你的应用持续运行——即使崩溃了也会自动重启，服务器重启后也能自动拉起。

**首次启动**（新建服务）：
```bash
cd /www/wwwroot/myapp && pm2 start server.js --name myapp && pm2 save
```

**说明**：
- `server.js` → 替换为你的入口文件（如 `app.js`、`index.js`）
- `--name myapp` → 给服务起一个名字，方便后续管理
- `pm2 save` → 保存当前服务列表，配合开机自启使用

**验证点**：输出类似：
```
[PM2] Spawning PM2 daemon with pm2_home=.pm2
[PM2] PM2 successfully stopped
[PM2] [myapp] (0)✓
[PM2] Saving current process list...
```

#### Step 4.2：配置开机自启

让服务器重启后应用自动启动（只需配置一次）：

```bash
pm2 startup systemd
pm2 save
```

**说明**：
- `pm2 startup systemd` → 生成 systemd 配置，会输出一条命令让你再执行一次
- 按提示复制那条命令执行即可
- `pm2 save` → 保存当前运行的服务列表，开机时自动恢复

**验证点**：执行 `pm2 list` 能看到 `myapp` 状态为 `online`

#### Step 4.3：日常管理命令

这些命令是日常运维用的，需要时在 SSH 终端执行：

```bash
# 查看服务状态
pm2 list
# 输出示例：
# ┌────┬────────────┬─────────┬──────┬────────┬─────────┐
# │ id │ name       │ status  │ cpu  │ memory │ uptime  │
# ├────┼────────────┼─────────┼──────┼────────┼─────────┤
# │ 0  │ myapp      │ online  │ 0%   │ 128mb  │ 2m      │
# └────┴────────────┴─────────┴──────┴────────┴─────────┘

# 查看实时日志（调试问题用）
pm2 logs myapp

# 重启服务（更新代码后用）
pm2 restart myapp

# 停止服务
pm2 stop myapp

# 删除服务（停止并移除）
pm2 delete myapp

# 查看详细信息
pm2 show myapp
```

#### Step 4.4：验证应用运行

**用户操作**：在 SSH 终端执行：
```bash
curl -s http://localhost:3000/health
```

**验证点**：
- ✅ 返回 `OK` 或 `{"status":"healthy"}` → 部署成功，进入 Phase 5
- ❌ 返回错误或超时 → 执行 `pm2 logs myapp --lines 30`，把日志发给 Agent

**告诉 Agent**：健康检查结果

---

### Phase 5：配置 Nginx（用户在 SSH 终端执行）

#### Step 5.1：生成 Nginx 配置

**Agent 自动生成** Nginx 配置内容：

```
在 SSH 终端中执行（注意替换端口和域名）：
```bash
cat > /etc/nginx/sites-available/myapp << 'NGINXEOF'
server {
    listen 80;
    server_name _;
    
    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
NGINXEOF
```

**用户操作**：复制整个代码块 → 粘贴 → 回车

**验证点**：没有报错，直接返回命令提示符

#### Step 5.2：启用并重载 Nginx

```bash
ln -sf /etc/nginx/sites-available/myapp /etc/nginx/sites-enabled/myapp
nginx -t && systemctl reload nginx
```

**验证点**：
- `nginx -t` 输出 `syntax is ok` 和 `test is successful`
- `systemctl reload nginx` 没有报错

**告诉 Agent**："Nginx 配置完成"

---

### Phase 6：最终验证（用户在本地浏览器）

#### Step 6.1：浏览器访问

**用户操作**：在本地浏览器打开 `http://服务器IP`

**验证点**：
- ✅ 看到应用页面 → 部署成功！
- ❌ 看到 Nginx 默认页 → 检查 Nginx 配置，告诉 Agent
- ❌ 页面无法访问 → 检查安全组端口，告诉 Agent

#### Step 6.2：输出部署报告

**Agent 输出**：
```
🎉 部署成功！
━━━━━━━━━━━━━━━━━━
📁 项目路径：/www/wwwroot/myapp
🌐 访问地址：http://服务器IP
📊 进程状态：运行中
🕐 部署耗时：约 X 分钟
━━━━━━━━━━━━━━━━━━
下次部署只需再次执行相同流程。
```

---

## 常见问题排查

### Q1：npm install 报错 `EACCES` 权限问题

**Agent 诊断**：
```
在 SSH 终端中执行：
```bash
chown -R root:root /www/wwwroot/myapp
```
然后重新执行 `npm install`。

### Q2：PM2 启动后立即退出

**Agent 诊断**：
```
在 SSH 终端中执行：
```bash
pm2 logs myapp --lines 30
```
把日志内容发给 Agent，Agent 根据错误信息给出修复方案。

### Q3：浏览器访问显示 502 Bad Gateway

**Agent 诊断**：
```
在 SSH 终端中依次执行：
```bash
curl http://localhost:3000
pm2 status
cat /etc/nginx/sites-enabled/myapp
```
把三条命令的输出都发给 Agent。

### Q4：忘记服务器 IP 或密码

联系技术支持获取。**不要**让 Agent 在对话中索要或存储密码。

### Q5：想回滚到上一版本

```
在 SSH 终端中执行：
```bash
cd /www/wwwroot/myapp && git log --oneline -5
git reset --hard HEAD~1
pm2 restart myapp
```

---

## 安全规范

| 规则 | 原因 |
|------|------|
| Agent **永不**索要密码 | 密码在对话历史中可能泄露 |
| 敏感操作（rm、chown）必须用户手动执行 | 防止误删/误改 |
| 每一步操作结果必须用户确认后再继续 | 防止错误连锁发生 |
| 不在 SOP 中包含明文密钥/密码 | 安全考虑 |
| 环境变量由用户在服务器上手动填入 | 避免密钥出现在对话中 |

---

## 快速部署命令汇总

### 首次部署（完整流程）

**Step 1：本地 PC 推送到 Gitee**
```bash
cd C:\path\to\project
git init
git add .
git commit -m "init"
git remote add origin https://gitee.com/你的用户名/仓库名.git
git push -u origin main
```

**Step 2：SSH 终端——服务器拉取代码**
```bash
cd /www/wwwroot && git clone https://gitee.com/你的用户名/仓库名.git myapp
cd /www/wwwroot/myapp
```

**Step 3：SSH 终端——安装依赖 + 构建**
```bash
cd /www/wwwroot/myapp && npm install --production
# 如果有构建步骤：
cd /www/wwwroot/myapp && npm run build
```

**Step 4：SSH 终端——启动应用（PM2）**
```bash
cd /www/wwwroot/myapp && pm2 start server.js --name myapp && pm2 save
pm2 startup systemd   # 开机自启（按提示再执行一次生成的命令）
```

**Step 5：SSH 终端——验证**
```bash
curl -s http://localhost:3000/health && echo "✅ OK" || echo "❌ FAIL"
```

### 日常更新（每次开发完成后）

**本地 PC 终端执行**：
```bash
cd C:\path\to\project && git add . && git commit -m "update" && git push origin main
```

**SSH 终端执行**：
```bash
cd /www/wwwroot/myapp && git pull origin main
cd /www/wwwroot/myapp && npm install --production   # 有新依赖时需要
cd /www/wwwroot/myapp && npm run build               # 有构建步骤时需要
pm2 restart myapp
curl -s http://localhost:3000/health && echo "✅ OK" || echo "❌ FAIL"
```

### 常用管理命令速查

```bash
# 查看服务状态
pm2 list

# 查看日志（调试用）
pm2 logs myapp

# 重启服务（更新后）
pm2 restart myapp

# 停止服务
pm2 stop myapp

# 查看服务器上的项目文件
ls /www/wwwroot/myapp/

# 查看应用日志
tail -f /var/log/myapp/out.log
tail -f /var/log/myapp/error.log
```

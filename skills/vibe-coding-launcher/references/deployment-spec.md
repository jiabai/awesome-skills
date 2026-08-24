# 部署规范生成与引导（docs/DEPLOYMENT.md）

本文件定义：什么项目生成 `docs/DEPLOYMENT.md`、模板长什么样、开发完成后 agent 如何按该文档引导用户部署。完整方法论见仓库 `Conventions/DEPLOY-SOP.md`；本文件是面向 launcher 的执行版。

## 生成条件

| 条件 | 判定 |
|------|------|
| 项目类型 | Web 应用 / API 服务 / 需要长期运行的服务端程序（Node.js / Python / Go） |
| 用户需求 | 阶段 1 了解用户时确认有云服务器部署意图 |

**不生成时**：

- CLI 本地工具、无服务器的纯静态页面、用户明确表示本地运行即可 → 不生成。
- 项目后续需要部署时（含恢复模式），按本模板补生成，并同步 AGENTS.md 快速入口。

**写入位置**：`docs/DEPLOYMENT.md`（扩展集，阶段 4 生成）。

**AGENTS.md 联动**：生成后在根级 AGENTS.md 快速入口追加一行 `- 部署：见 docs/DEPLOYMENT.md`。未生成时不列出，避免死链。

## 模板

生成时将 `{占位符}` 替换为项目实际信息（阶段 2-4 已确认技术栈、端口、启动命令）。用户项目的 `docs/DEPLOYMENT.md` 必须自包含：任何 agent 之后只读它就能引导部署，不依赖本 skill。

```markdown
# 部署规范

> 适用场景：本地开发完成后，将项目部署到云服务器
> 核心模式：Agent 指导 + 用户手动操作

## 项目部署信息

| 项 | 值 |
|----|-----|
| 技术栈 | {Node.js 22 / Python 3.11 / Go 1.22} |
| 运行端口 | {3000} |
| 启动命令 | {node server.js} |
| 依赖文件 | {package.json / requirements.txt / 无} |
| 构建命令 | {npm run build / go build -o build/myapp / 无} |
| 服务器项目路径 | /www/wwwroot/{项目名} |
| 访问地址 | http://{服务器IP} |

## 角色分工

| 角色 | 做什么 | 不做什么 |
|------|--------|----------|
| 用户 | 在 SSH 终端执行 agent 给出的命令，回报结果 | 不需要理解命令含义 |
| Agent | 分析项目、生成部署指令、验证结果、诊断问题 | 不直接执行远程命令，不索要密码 |

核心模式：Agent 说"在你的 SSH 终端里输入这行命令"，用户复制粘贴执行，把结果告诉 Agent。

## 推荐工具

| 工具 | 用途 | 何时需要 |
|------|------|---------|
| Tabby（tabby.sh） | SSH 终端 + 内置 SFTP 文件传输 | 必备，推荐首选 |
| Git（git-scm.com） | 代码推送到 Gitee 仓库，服务器拉取更新 | 需要版本控制或频繁更新时 |

## 前置条件（一次性）

- 云服务器已初始化（未初始化时先执行 Phase 0）：Git / 运行时（Node/Python/Go）/ PM2 / Nginx 已安装，SSH 免密已配置，安全组已开放 22、80、443 端口
- 本地已装 Tabby，知道服务器 IP
- Gitee 上已创建项目仓库（如使用 Git 传输）

## 部署流程（首次）

### Phase 0：初始化服务器（仅首次，已装过可跳过）

```bash
apt update && apt install -y git nginx
# 运行时（按项目技术栈三选一）
curl -fsSL https://deb.nodesource.com/setup_22.x | bash - && apt install -y nodejs   # Node.js 项目
apt install -y python3 python3-pip                                                   # Python 项目
apt install -y golang                                                                # Go 项目
# PM2（仅 Node.js 项目需要）
npm install -g pm2
```

验证点：`git --version && nginx -v` 有版本输出；`node -v` / `python3 --version` / `go version` 与项目要求的运行时版本一致。

> 端口开放（22/80/443）需在云厂商控制台的安全组中设置，只能用户自己操作；完成后告知 agent 再继续。

### Phase 1：连接服务器

用户打开 Tabby，登录服务器。验证点：终端提示符为 `root@{主机名}:~#`。

### Phase 2：上传代码

```bash
# 本地（首次）
cd {本地项目路径}
git init && git add . && git commit -m "init"
git remote add origin https://gitee.com/{用户名}/{仓库名}.git
git push -u origin main

# 服务器（首次）
cd /www/wwwroot && git clone https://gitee.com/{用户名}/{仓库名}.git {项目名}
```

验证点：`ls /www/wwwroot/{项目名}` 能看到项目文件。

### Phase 3：安装依赖 & 构建

```bash
cd /www/wwwroot/{项目名}
{npm install --production / pip install -r requirements.txt / # Go 无需安装}
{npm run build / go build -o build/{项目名} / # 无构建步骤则跳过}
```

验证点：安装输出无 `ERR!`；构建产物存在（`dist/` 或 `build/`）。

### Phase 4：启动应用（PM2）

```bash
cd /www/wwwroot/{项目名} && pm2 start {入口文件} --name {项目名} && pm2 save
pm2 startup systemd   # 开机自启，按提示再执行一次生成的命令
```

验证点：`pm2 list` 中 {项目名} 状态为 `online`；`curl -s http://localhost:{端口}/health` 返回正常。

### Phase 5：配置 Nginx

```bash
cat > /etc/nginx/sites-available/{项目名} << 'NGINXEOF'
server {
    listen 80;
    server_name _;
    location / {
        proxy_pass http://localhost:{端口};
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
NGINXEOF
ln -sf /etc/nginx/sites-available/{项目名} /etc/nginx/sites-enabled/{项目名}
nginx -t && systemctl reload nginx
```

验证点：`nginx -t` 输出 `syntax is ok`。

### Phase 6：最终验证

浏览器打开 `http://{服务器IP}`，看到应用页面即部署成功。

## 日常更新流程

```bash
# 本地
cd {本地项目路径} && git add . && git commit -m "update" && git push origin main

# 服务器
cd /www/wwwroot/{项目名} && git pull origin main
{npm install --production}   # 有新依赖时
{npm run build}              # 有构建步骤时
pm2 restart {项目名}
curl -s http://localhost:{端口}/health
```

## 常见问题排查

| 症状 | 排查命令 |
|------|---------|
| npm install 报 EACCES | `chown -R root:root /www/wwwroot/{项目名}` 后重试 |
| PM2 启动后立即退出 | `pm2 logs {项目名} --lines 30`，日志发给 agent |
| 浏览器 502 Bad Gateway | 依次执行 `curl http://localhost:{端口}`、`pm2 status`、`cat /etc/nginx/sites-enabled/{项目名}`，输出发给 agent |
| 想回滚版本 | `git log --oneline -5` → `git reset --hard HEAD~1` → `pm2 restart {项目名}` |

## 安全规范

- Agent 永不索要服务器密码或 SSH 私钥内容
- 对话中不出现明文密钥/密码；环境变量由用户在服务器上手动填入
- 敏感操作（rm、chown）必须用户手动执行
- 每步验证点通过后再推进下一步
```

## Agent 引导规则（开发完成后）

1. **触发时机**：阶段 8 完成门禁通过后的交付说明中，或用户说"帮我部署 / 部署到服务器"。
2. **入口检查**：读 `docs/DEPLOYMENT.md`。存在则严格按其中流程引导；不存在但项目可部署时，先按上方模板生成（填好项目实际信息）再引导。
3. **引导节奏**：一次只给一步 → 用户在自己的 SSH 终端执行 → 用户回报"成功"或报错原文 → 验证通过再给下一步。
4. **职责边界**：agent 不直接执行远程命令；命令由用户复制粘贴执行。
5. **失败处理**：按「常见问题排查」诊断；要求用户粘贴报错原文，不接受转述。
6. **收尾**：部署完成后输出部署报告（项目路径、访问地址、进程状态）。

## 安全红线

- 永不索要服务器密码、SSH 私钥内容或云平台账号凭证。
- 对话与生成的文档中不包含明文密钥/密码。
- 每一步验证点通过后才推进，防止错误连锁。

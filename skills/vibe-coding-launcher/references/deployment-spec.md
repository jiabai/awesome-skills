# Deployment Specification and Guidance (`docs/DEPLOYMENT.md`)

This document defines which projects generate `docs/DEPLOYMENT.md`, the template it uses, and how an agent guides deployment after development.

## Generation Criteria

| Condition | Requirement |
|-----------|-------------|
| Project type | Web app / API service / long-running server program (Node.js / Python / Go) |
| User intent | Phase 1 confirms an intent to deploy to a cloud server |

**When not to generate:**

- Omit for local CLI tools, serverless static pages, or users who explicitly want local-only execution.
- If deployment becomes necessary later, including during recovery, generate it from this template and update AGENTS.md Quick Entry.

**Location:** `docs/DEPLOYMENT.md`, generated in Phase 4 as part of the extended set.

**AGENTS.md integration:** add `- Deployment: see docs/DEPLOYMENT.md` to root Quick Entry only when the document exists.

## Template

Replace every `{placeholder}` with confirmed project information from Phases 2–4, including the stack, port, and startup command. The generated `docs/DEPLOYMENT.md` must be self-contained so a future agent can guide deployment by reading it alone.

````markdown
# Deployment Specification

> Use case: deploy the finished local project to a cloud server
> Core model: agent guidance + manual user execution

## Project Deployment Information

| Item | Value |
|------|-------|
| Tech stack | {Node.js 22 / Python 3.11 / Go 1.22} |
| Runtime port | {3000} |
| Start command | {node server.js} |
| Dependency file | {package.json / requirements.txt / none} |
| Build command | {npm run build / go build -o build/myapp / none} |
| Server project path | `/www/wwwroot/{project-name}` |
| URL | `http://{server-IP}` |

## Responsibilities

| Role | Does | Does Not Do |
|------|------|-------------|
| User | Runs commands supplied by the agent in an SSH terminal and reports the result | Need to understand every command |
| Agent | Analyzes the project, supplies deployment commands, validates results, and diagnoses problems | Execute remote commands directly or request passwords |

Core model: the agent says, "Enter this command in your SSH terminal." The user copies it, runs it, and sends the result back.

## Recommended Tools

| Tool | Purpose | When Needed |
|------|---------|-------------|
| Tabby (`tabby.sh`) | SSH terminal with built-in SFTP transfer | Required; preferred option |
| Git (`git-scm.com`) | Push code to a Gitee repository and pull updates on the server | Version control or frequent updates |

## One-Time Prerequisites

- The cloud server is initialized. If not, run Phase 0 first. Git, the runtime (Node/Python/Go), PM2, and Nginx are installed; passwordless SSH is configured; security-group ports 22, 80, and 443 are open.
- Tabby is installed locally and the server IP is known.
- A project repository exists on Gitee when Git transfer is used.

## First Deployment

### Phase 0: Initialize the Server (First Time Only)

```bash
apt update && apt install -y git nginx
# Choose one runtime for the project
curl -fsSL https://deb.nodesource.com/setup_22.x | bash - && apt install -y nodejs   # Node.js
apt install -y python3 python3-pip                                                   # Python
apt install -y golang                                                                # Go
# PM2 is required only for Node.js
npm install -g pm2
```

Validation: `git --version && nginx -v` prints versions, and `node -v`, `python3 --version`, or `go version` matches project requirements.

> Ports 22/80/443 must be opened by the user in the cloud provider's security-group console. Continue only after the user confirms this.

### Phase 1: Connect to the Server

The user opens Tabby and logs in. Validation: the terminal prompt resembles `root@{hostname}:~#`.

### Phase 2: Upload Code

```bash
# Local machine, first time
cd {local-project-path}
git init
git status --short
git add -- {explicit-project-paths}
git diff --cached
git commit -m "init"
git remote add origin https://gitee.com/{username}/{repository}.git
git push -u origin main

# Server, first time
cd /www/wwwroot && git clone https://gitee.com/{username}/{repository}.git {project-name}
```

Validation: `ls /www/wwwroot/{project-name}` shows the project files.

### Phase 3: Install Dependencies and Build

```bash
cd /www/wwwroot/{project-name}
{npm install --production / pip install -r requirements.txt / # Go needs no install step}
{npm run build / go build -o build/{project-name} / # skip when no build is needed}
```

Validation: installation output contains no `ERR!`, and the expected artifact such as `dist/` or `build/` exists.

### Phase 4: Start the Application with PM2

```bash
cd /www/wwwroot/{project-name} && pm2 start {entry-file} --name {project-name} && pm2 save
pm2 startup systemd   # Then run the generated command as instructed
```

Validation: `{project-name}` is `online` in `pm2 list`, and `curl -s http://localhost:{port}/health` succeeds.

### Phase 5: Configure Nginx

```bash
cat > /etc/nginx/sites-available/{project-name} << 'NGINXEOF'
server {
    listen 80;
    server_name _;
    location / {
        proxy_pass http://localhost:{port};
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
NGINXEOF
ln -sf /etc/nginx/sites-available/{project-name} /etc/nginx/sites-enabled/{project-name}
nginx -t && systemctl reload nginx
```

Validation: `nginx -t` reports `syntax is ok`.

### Phase 6: Final Validation

Open `http://{server-IP}` in a browser. The deployment succeeds when the application appears.

## Routine Updates

```bash
# Local machine
cd {local-project-path}
git status --short
git add -- {explicit-changed-paths}
git diff --cached
git commit -m "update"
git push origin main

# Server
cd /www/wwwroot/{project-name} && git pull origin main
{npm install --production}   # when dependencies changed
{npm run build}              # when a build step exists
pm2 restart {project-name}
curl -s http://localhost:{port}/health
```

## Troubleshooting

| Symptom | Diagnostic Command |
|---------|--------------------|
| `npm install` reports EACCES | Run `chown -R root:root /www/wwwroot/{project-name}`, then retry |
| PM2 exits immediately | Run `pm2 logs {project-name} --lines 30` and send the log to the agent |
| Browser shows 502 Bad Gateway | Run `curl http://localhost:{port}`, `pm2 status`, and `cat /etc/nginx/sites-enabled/{project-name}` in order; send outputs to the agent |
| Need to roll back | `git log --oneline -5` → `git revert <bad-commit>` → rebuild when needed → `pm2 restart {project-name}` |

## Security Rules

- The agent never requests a server password or SSH private-key contents.
- Never place plaintext secrets or passwords in the conversation. The user enters environment variables directly on the server.
- Stage explicit project paths and keep `.env`, credentials, private keys, and unrelated files out of commits.
- The user must manually execute sensitive operations such as `rm` and `chown`.
- Advance only after each phase's validation passes.
````

## Agent Guidance Rules

1. **Trigger:** the Phase 8 completion gates pass, or the user asks for deployment or server deployment.
2. **Entry check:** read `docs/DEPLOYMENT.md`. If present, follow it exactly. If absent but the project is deployable, generate it from the template with real project information before guiding deployment.
3. **Pacing:** provide one step at a time → user runs it in their SSH terminal → user reports success or pastes the exact error → validate before continuing.
4. **Boundary:** the agent does not execute remote commands directly; the user copies and runs them.
5. **Failure handling:** use Troubleshooting and require the exact error text rather than a paraphrase.
6. **Closeout:** after deployment, report the project path, URL, and process status.

## Security Red Lines

- Never request server passwords, SSH private-key contents, or cloud-account credentials.
- Never include plaintext secrets or passwords in the conversation or generated documents.
- Advance only after each step validates successfully, preventing cascading errors.

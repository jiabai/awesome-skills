---
name: canvas-sequence
description: AI驱动的交互序列图生成引擎。分析项目代码的动态交互流程，生成 Obsidian Canvas 格式的时序图。触发词：序列图、时序图、交互流程、调用链、数据流、sequence diagram、interaction diagram、请求生命周期、API调用链。当用户想要可视化一个业务流程的执行路径、查看模块间的调用顺序、理解请求从入口到数据库的完整流程时使用此skill。
---

# Canvas Sequence - 交互序列图生成引擎

你是 AI 交互分析总师，专注分析代码的**动态执行流程**，生成富有洞察力的 Obsidian Canvas 序列图。

## 与 canvas-architect 的区别

| Skill | 关注点 | 输出 |
|-------|--------|------|
| canvas-architect | **静态架构**（模块、依赖） | 架构图 |
| canvas-sequence | **动态流程**（调用链、时序） | 序列图 |

---

## 核心概念

### 序列图元素

| 元素 | Canvas 表示 | 说明 |
|------|-------------|------|
| **生命线** | 顶部文本节点 | 参与交互的角色/模块 |
| **激活条** | 细长矩形节点 | 表示执行周期 |
| **消息** | 边 + 文本标签节点 | 调用/返回/数据传递 |
| **组合片段** | 大背景节点 | 循环/条件/并行区域 |

### 消息类型

| 类型 | 边样式 | 含义 |
|------|--------|------|
| 同步调用 | 实线 → | 阻塞等待返回 |
| 异步调用 | 实线 →（无返回） | 不等待返回 |
| 返回消息 | 虚线 ← | 返回结果 |
| 自调用 | 边指向自身 | 内部方法调用 |

---

## 执行流程

### 第一阶段：场景识别

**目标**：找出一个值得可视化的核心业务场景

**启发式识别**：
1. 分析入口点（API路由、main函数、事件处理器）
2. 查找命名线索（`OrderController`、`processPayment`、`handleRequest`）
3. 结合 README/文档判断核心业务
4. 选择**最重要或最复杂**的一个场景

**输出**：确定分析场景（如"用户下单流程"、"API请求生命周期"）

---

### 第二阶段：生命线决策

**动态选择生命线的抽象层次**：

| 级别 | 适用场景 | 生命线代表 |
|------|----------|-----------|
| 系统级 | 微服务/分布式 | 各服务、数据库、外部API |
| 模块级 | 单体应用 | Controller、Service、Repository |
| 类级 | 复杂业务逻辑 | 关键业务类实例 |

**决策因素**：
- 调用链深度和广度
- 跨技术边界数量（API网关、消息队列、数据库）
- 避免过度细化导致图表爆炸

---

### 第三阶段：调用链追踪

**追踪方法**：
1. 从场景入口点开始
2. 递归跟踪函数调用
3. 记录每次调用：
   - 调用者 → 被调用者
   - 参数类型（关键数据载荷）
   - 同步/异步判断
4. 识别循环、条件分支、并行执行

---

### 第四阶段：Canvas 布局

**水平布局**：生命线从左到右按调用发起顺序排列
```
Client → Gateway → Service → Database
```

**垂直布局**：消息严格按时间顺序从上到下排列

**视觉编码**：
- 生命线：顶部节点 + 垂直虚线（用边模拟）
- 激活条：细长矩形节点，覆盖在生命线上
- 消息标签：独立文本节点，放在消息边旁边

---

## Canvas JSON 结构

### 节点类型

```json
{
  "nodes": [
    // 生命线节点
    {
      "id": "lifeline_client",
      "type": "text",
      "text": "**Client**\n`前端/调用者`",
      "x": 0,
      "y": 0,
      "width": 150,
      "height": 60,
      "color": "1"
    },
    // 激活条节点
    {
      "id": "activation_client_1",
      "type": "text",
      "text": "",  // 空文本，仅作视觉元素
      "x": 30,     // 与生命线中心对齐
      "y": 100,
      "width": 20,
      "height": 150,  // 由消息时序决定
      "color": "1"
    },
    // 消息标签节点
    {
      "id": "msg_1_label",
      "type": "text",
      "text": "1. login(credentials)\n`// 验证用户身份`",
      "x": 180,    // 在消息箭头上方/下方
      "y": 120,
      "width": 200,
      "height": 40,
      "color": "6"
    },
    // 组合片段节点（可选）
    {
      "id": "loop_1",
      "type": "text",
      "text": "**[Loop]**\n`循环直到成功`",
      "x": -50,
      "y": 200,
      "width": 400,
      "height": 200,
      "color": "5"  // 半透明背景色
    }
  ],
  "edges": [
    // 同步消息
    {
      "id": "msg_1",
      "fromNode": "activation_client_1",
      "fromSide": "right",
      "toNode": "activation_service_1",
      "toSide": "left",
      "color": "1"  // 实线表示同步
    },
    // 返回消息
    {
      "id": "return_1",
      "fromNode": "activation_service_1",
      "fromSide": "left",
      "toNode": "activation_client_1",
      "toSide": "right",
      "color": "4"  // 虚线表示返回
    }
  ]
}
```

---

## 消息标签模板

每个消息生成语义化摘要：

```markdown
{序号}. {方法名}({关键参数})
`// {AI生成的功能摘要}`
```

**示例**：
```
1. authenticate(token)
`// 验证JWT令牌并提取用户ID`

2. fetchUserProfile(userId)
`// 从数据库查询用户完整信息`

3. return ProfileDTO
`// 返回用户资料对象`
```

---

## 必须输出项

### 1. 场景识别节点（必须）

```markdown
**交互场景识别**
`动态流程分析`

**分析场景**: {场景名称，如"用户登录流程"}

**场景特征**:
- 调用起点: {入口点}
- 调用终点: {终点}
- 调用深度: {层数} 层

**置信度**: {百分比}
```

节点要求：`id: node_scene_pattern`，`color: 6`

### 2. 关键发现节点（必须）

```markdown
**交互洞察**
`调用链分析`

**关键发现**:

1. {发现1，如"API调用链存在3次数据库查询"}

2. {发现2，如"认证与业务逻辑串行执行，存在优化空间"}

3. {发现3，如"外部API调用为异步，不影响主流程"}

**潜在瓶颈**: {如"数据库查询集中在一个服务"}
```

节点要求：`id: node_interaction_insight`，`color: 6`

### 3. 执行摘要（必须）

```
✓ AI交互序列图已生成：{文件路径}
  ├─ 分析场景：{场景名}
  ├─ 交互深度：{层数} 层
  ├─ 生命线数：{数量} 个
  ├─ 消息数量：{数量} 条
  └─ 关键发现：{数量} 条
```

---

## 颜色编码

| color | 含义 | 使用 |
|-------|------|------|
| 1 | 外部调用者 | Client、Gateway |
| 2 | 业务服务 | Service、Controller |
| 3 | 数据层 | Database、Cache |
| 4 | 外部系统 | 第三方API |
| 5 | 组合片段 | Loop/Alt/Par |
| 6 | 分析/标注 | 场景识别、洞察节点 |

---

## 完整示例

**输入**："分析这个项目的用户登录流程"

**输出**：`login_flow.canvas`，包含：

```
生命线: Client → AuthAPI → UserService → Database → Cache

消息序列:
1. Client → AuthAPI: login(email, password)
2. AuthAPI → UserService: authenticate(credentials)
3. UserService → Database: findUser(email)
4. Database → UserService: return User
5. UserService → Cache: storeSession(userId)
6. UserService → AuthAPI: return JWT
7. AuthAPI → Client: return token

关键发现:
- 认证流程为同步阻塞
- 数据库查询与缓存写入串行
- 可优化：并行查询缓存与数据库
```

---

## 使用示例

**触发方式**：
- "分析用户下单的完整流程"
- "帮我理解 API 请求的调用链"
- "生成 login_sequence.canvas"
- "可视化这个请求从入口到数据库的路径"

**输出位置**：默认 `{场景名}_sequence.canvas` 到项目根目录
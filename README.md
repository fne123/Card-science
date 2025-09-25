# Card Science Insight

一个基于 FastAPI 的纸牌科学 SaaS 原型，支持在 Railway 上直接部署。系统通过用户生日生成纸牌科学的本命蓝图，并提供免费与付费订阅两种体验：

- **免费订阅**：查看生命牌、守护牌、灵魂资源牌、灵魂挑战牌（特殊家族生日仅包含生命牌与守护牌）。
- **付费订阅**：解锁全量功能，包括 52 天流年周期分析、今日牌分析、两人合盘洞察、以及新周期和每日提醒的邮件推送能力。

> ⚠️ 邮件推送需在 Railway 上配置 SMTP 凭据（`MAIL_USERNAME`、`MAIL_PASSWORD` 等），若未配置将以日志形式记录。

## 主要特性

- FastAPI + async SQLAlchemy 构建的 RESTful API。
- JWT 鉴权、OAuth2 Password Flow。
- 基于纸牌科学的本命与流年算法封装在 `app/services/card_science.py`。
- 简洁现代的前端落地页 & 仪表板（Jinja2 + Tailwind 灵感 CSS）。
- 可配置的邮件推送服务，支持异步投递。
- Railway 兼容的部署脚本与配置。

## 快速开始

### 本地运行

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

首次运行会自动创建 SQLite 数据库 `card_science.db`。访问：

- 网站主页：<http://127.0.0.1:8000>
- 交互式 API 文档：<http://127.0.0.1:8000/docs>

### Railway 部署

1. 在 Railway 创建新项目并关联此仓库。
2. 在环境变量中配置至少以下项目：
   - `SECRET_KEY`：JWT 签名密钥。
   - `DATABASE_URL`：建议使用 Railway 的 PostgreSQL 插件生成的连接串（需为 async driver，例如 `postgresql+asyncpg://...`）。
   - SMTP 相关变量（可选）：`MAIL_USERNAME`、`MAIL_PASSWORD`、`MAIL_SMTP_HOST`、`MAIL_SMTP_PORT`、`MAIL_USE_TLS`。
3. Railway 会自动检测 `Procfile` 并运行 `uvicorn app.main:app --host 0.0.0.0 --port $PORT`。

## 核心 API 概览

| Endpoint | 描述 | 权限 |
| --- | --- | --- |
| `POST /api/auth/register` | 注册并创建生日档案 | 公共 |
| `POST /api/auth/login` | 账号密码登录（OAuth2） | 公共 |
| `GET /api/users/me` | 获取当前用户信息 | 登录 |
| `GET /api/insights/personal` | 获取本命蓝图（免费可用） | 登录 |
| `GET /api/insights/forecast` | 获取流年周期与今日牌 | 付费 |
| `POST /api/insights/compatibility` | 两人合盘分析 | 付费 |

更多端点请查阅 `/docs`。

## 开发说明

- 所有业务逻辑均采用异步实现，可轻松扩展至 Celery/Airflow 等任务系统。
- `app/services/card_science.py` 中存放 52 张纸牌的关键字与建议，可根据实际需求调整。
- 付费订阅的切换目前以 API 调用模拟，生产环境可接入 Stripe、Paddle 等支付回调。

## 许可证

MIT

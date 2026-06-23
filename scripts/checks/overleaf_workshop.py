"""Check whether Overleaf Workshop is installed and cookie login is configured."""

from __future__ import annotations

from dataclasses import dataclass

from scripts.lib.cursor_extensions import is_overleaf_workshop_installed
from scripts.lib.overleaf_workshop import any_server_logged_in, read_server_login_status

COOKIE_LOGIN_GUIDE_URL = (
    "https://github.com/overleaf-workshop/overleaf-workshop#how-to-login-with-cookies"
)


@dataclass(frozen=True)
class CheckResult:
    name: str
    ok: bool
    message: str
    details: list[str]


def run_check() -> CheckResult:
    extension = is_overleaf_workshop_installed()
    if extension is None:
        return CheckResult(
            name="overleaf-workshop",
            ok=True,
            message="未检测到 Overleaf Workshop 插件，无需配置 Cookie 登录。",
            details=[],
        )

    version = extension.version or "未知版本"
    details = [
        f"插件 ID: {extension.extension_id}",
        f"版本: {version}",
        f"检测方式: {extension.source}",
    ]
    if extension.install_path:
        details.append(f"安装路径: {extension.install_path}")

    login_statuses = read_server_login_status()
    if login_statuses:
        for status in login_statuses:
            state = "已登录" if status.logged_in else "未登录"
            user = f" ({status.username})" if status.username else ""
            details.append(f"服务器 {status.name}: {state}{user}")
    elif any_server_logged_in():
        details.append("检测到已登录状态。")
    else:
        details.append("尚未配置任何 Overleaf 服务器登录。")

    if any_server_logged_in():
        return CheckResult(
            name="overleaf-workshop",
            ok=True,
            message=(
                "已安装 Overleaf Workshop，且至少有一个服务器已完成登录。"
                "若使用 www.overleaf.com，请确保通过 Cookie 方式登录。"
            ),
            details=details,
        )

    return CheckResult(
        name="overleaf-workshop",
        ok=False,
        message=(
            "检测到本机 Cursor 已安装 Overleaf Workshop 插件，但尚未完成登录。"
            "对于 www.overleaf.com 等启用 SSO / 验证码的服务器，必须使用 Cookie 登录。"
        ),
        details=details
        + [
            "",
            "Cookie 登录步骤：",
            "1. 在已登录 Overleaf 的浏览器中打开开发者工具 (F12)，切换到 Network 面板。",
            "2. 访问 Overleaf 主页 (如 https://www.overleaf.com)。",
            "3. 在请求列表中筛选 /project，选中对应请求。",
            "4. 复制 Request Headers 中的 Cookie 值 (形如 overleaf_session2=...)。",
            "5. 在 Cursor 侧边栏打开 Overleaf Workshop，选择服务器后点击 Login with Cookies 并粘贴。",
            f"详细说明: {COOKIE_LOGIN_GUIDE_URL}",
        ],
    )

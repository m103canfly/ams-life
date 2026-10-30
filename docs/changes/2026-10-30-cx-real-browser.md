# 真浏览器读网页

起因：主人原话“同意装 playwright”；既有评估推荐使用电脑已有的 Edge，以无头、临时配置读取需要脚本的网页。这里没有核实安装或浏览器版本。

- 新开关 `browser_enabled` 默认关闭；读网页同时要求 `browse_enabled`，真截图同时要求 `screenshot_enabled`。
- DeepSeek 返回空正文、短正文或启用脚本提示时才尝试浏览器；失败保留原结果。正文长度门槛是 `BROWSER_MIN_CHARS`，提示语在 `BROWSER_SCRIPT_PROMPTS`；现有资料包装与截断继续使用 `PAGE_CHARS`。
- 安全：Edge 无头启动并启用沙箱；临时上下文和浏览器无论成功、失败或超时都关闭。
- 安全：上下文禁止下载和服务工作线程，不授予权限，保留证书及内容安全策略检查，也不传入登录状态。
- 安全：每个请求检查地址和解析结果，只允许读取方法；关闭 WebSocket 和浏览器加密 DNS。检查与浏览器实际连接之间仍有 DNS 解析竞态，不能视为彻底消除。
- 安全：每个响应和最终地址均检查，任何不合格的响应或最终地址使本页作废。
- 安全：关闭新页面并拒绝弹窗。
- 安全：仅读取标题和可见正文，截图只截可见区域；不点击、输入或注入修改页面的脚本。
- 安全：读取结果交给原有资料包装，仍按不可信内容处理。
- 安全：读取和截图共用同一把锁，同一时间仅一页；打开、取字和截图有独立时限，整体也有上限。
- 安全：不更改浏览器标识、不登录、不处理验证；正文短于 `CHALLENGE_MAX_CHARS` 且命中验证提示才按验证页面处理，识别并不保证穷尽。
- 安全：只记录失败原因，不记录地址、网页内容或截图内容。

离线测试：`test_launch_and_context_are_temporary_and_sandboxed`、`test_request_method_and_public_addresses`、`test_response_redirect_to_local_is_rejected`、`test_final_redirect_to_local_is_rejected`、`test_popup_and_dialog_are_closed`、`test_websocket_is_closed`、`test_timeout_closes_context_and_browser`、`test_verification_page_is_not_read`、`test_missing_playwright_returns_none`、`test_one_page_at_a_time`、`test_source_has_no_persistent_or_debug_access`、`test_default_switch_is_off`、`test_short_empty_and_script_prompts`、`test_read_fallback_switch_and_material_wrapper`、`test_material_is_limited`。

第二轮加入真截图：窗口使用 `SHOT_VIEWPORT`，图片质量使用 `SHOT_QUALITY`，截图超时使用 `SHOT_SECONDS`。生成文件仅保留 `SHOT_RETENTION` 指定数量，清理只匹配自身生成的文件名。截图先由看图通道描述，描述和标题、网址、配文经发送检查后才发图；截取或描述失败、描述未通过检查时回退文字。看图账目单列 `screenshot`，浏览器账本与面板增加读取、截图、失败和请求拦截计数；拦截计数通过回调传递，即使浏览器操作失败也记录。

新增离线测试：`test_short_challenge_and_long_cloudflare_article`、`test_screenshot_uses_common_safety_and_viewport`、`test_screenshot_redirect_refused_and_partial_file_removed`、`test_blocked_request_count_survives_failure`、`test_browser_ledger_and_panel`、`test_retention_only_removes_own_old_jpegs`、`test_capture_counts_and_uses_screenshot_vision_source`、`test_vision_gate_counts_screenshot_separately`、`test_media_sends_image_only_after_description_and_checks`。主人反馈此前全套测试通过，两道安全抽查均有效；未修改金样，没有增加本轮范围之外的功能。

主人本机使用真 Edge 实测发现：指向本机的跳转虽然未建立本机连接，仍可能被误判为读到页面；需要脚本的页面在初始加载完成后正文可能仍为空。现检查重定向回应的目标，补全相对地址后复用严格地址检查；主回应缺失、状态非成功或最终协议不合格时判失败。初始加载后最多等待 `SETTLE_SECONDS` 指定时长让脚本请求完成，等待超时继续取字；正文去掉空白后为空则失败。读取与截图共用这些判断。

新增离线测试：`test_redirect_location_to_local_is_rejected_without_followup_request`、`test_relative_redirect_location_is_resolved_and_allowed`、`test_missing_or_error_main_response_is_rejected`、`test_browser_error_url_is_rejected`、`test_networkidle_timeout_still_reads_page`、`test_networkidle_waits_for_script_content_and_screenshot`、`test_empty_body_is_not_read_or_screenshot`。本次修复以后全套 869 项通过。

## 验证

- 全套 869 项通过，金样没变。
- 两道抽查：撤掉“只放行 GET/HEAD”（3 项失败）、撤掉“跳转后再查网址”（3 项失败）。
- 本机用真 Edge（`channel="msedge"`，Edge 156 + playwright 1.64.1，无头、临时配置）实测 7 条，单独脚本，不碰正在跑的插件：
  1. 要跑脚本才有内容的公开页：普通读取只有几十个字，浏览器读到 1715 个字；页面自己发的 4 个 POST 被挡。
  2. 公开网址 302/301 跳到 127.0.0.1：当没读到（navigation failed）；本机临时监听 0 次连接。
  3. 页面自动提交 POST 表单：被挡（为了这一条，测试脚本只让最顶层的 `data:` 测试页过检查，页面发出的请求照常检查）。
  4. 页面弹 alert/confirm、开新窗口：7 秒结束，没卡在对话框上；跑完没有留下 Edge 进程。
  5. 截图：390×844 的 jpg，约 43KB。
  6. 跑完：没有 Edge 进程留下；没有新的临时配置目录留下；主人的 Edge 配置文件修改时间没变（主人的 Edge 当时没开）。
  7. `channel="msedge"` 可以直接用，不用另下浏览器。
- 第一次实测发现两处，已修：跳转到本机时被当成读到了一个空白页；要跑脚本的页取字太早，正文是空的。
- 第一次实测用的另一个公开页要从谷歌拉字体，这台电脑连不上，页面一直不加载完；跟插件无关，换了一个国内能打开的要跑脚本的页。
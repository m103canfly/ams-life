# 2026-10-30 群消息与私聊准入

## 起因

第 68 条主人原话：“她加的任何群都可以看”。第 71–73 条主人均选“照推荐”：其他群只看不说、照出处规矩保存，其他人的私聊不看不存不回。

## 改了什么

- 群消息照常保存，随后按开口名单停止名单外群的事件；自行决定回话也经过同一限制。
- 私聊在任何保存之前检查主人和额外许可；未填主人时全部拒收。翻群的选择和表情包发送检查开口名单；黑话仍照原规则学习。
- 保存失败的日志只记录异常类型，拒收私聊的日志不含身份或内容。

## 开关

- `reply_groups`：可以开口的群，默认空；名单外只看不说。
- `reply_private`：除主人外可以接收私聊的人，默认空；仍须先填写 `owner_qq`。
- `reply_other_groups_when_called`：允许名单外群被叫时回话，默认关闭。被叫沿用现有唤醒判定；主动翻群及发送表情包仍受开口名单限制。

## 装机顺序

先装插件并填测试群，白名单先不动，核对测试群和主人私聊正常。再由主人关白名单，然后只看数量核对其他群进手机、被叫不回、别人的私聊未存未回，以及测试群和主人私聊正常。如有不对，请主人恢复白名单后排查。

## 测试

`test_other_group_saved_and_stopped_even_when_called`、`test_other_group_writes_phone_window_before_stop`、`test_allowed_group_continues`、`test_allowed_group_not_called_is_not_stopped`、`test_empty_reply_groups_stops_all_groups`、`test_private_admission_and_empty_owner`、`test_self_decide_cannot_answer_other_group`、`test_other_group_called_switch`、`test_sticker_never_sent_to_other_group`、`test_group_browse_chooses_only_allowed_groups`。外部全套运行中两段金样通过，记录未改。

## 卡以外

无功能范围扩展；旧测试夹具显式设置许可，以继续覆盖原有行为。外部全套运行后，为受新准入规则影响的听消息、夜间回放和发送检查场景补齐了测试配置，待外部复测；两道突变抽查待外部运行。

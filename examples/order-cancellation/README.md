# 可运行的订单取消示例

使用 Python 3.10+ 标准库，无须安装依赖或连接服务。业务约定只维护在 [SPEC.md](SPEC.md)，四个测试对应其中 S1–S4。

在项目根目录运行：

```sh
python -B examples/order-cancellation/demo.py
```

脚本在临时目录用同一套测试分别执行 `before.py` 和 `order.py`，不会覆盖源码。前者是有意保留的不完整起点，后者是完成后的实现。只有先观察到断言失败、再全部通过，且没有环境错误、跳过项或零测试时，整体验证才以退出码 0 结束。

也可分开观察：

```sh
python -B examples/order-cancellation/demo.py --phase red
python -B examples/order-cancellation/demo.py --phase green
python -B -m unittest discover -s examples/order-cancellation -p test_order.py -v
```

`red` 预期退出码 1、四个断言失败；`green` 和最终单元测试预期退出码 0、四项通过。重放已保存的前后实现用于展示检错能力，不等于每次重放都重新执行了开发过程。

本例只验证内存对象上的权限判断、拒绝行为与状态变更，没有实现退款或库存回补，也不证明数据库、事务、并发、真实账号鉴权或移动端交互。技能行为的独立验证另见 [评测说明](../../evals/README.md)。

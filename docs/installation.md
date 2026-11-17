# 安装与第一次使用

## 从 GitHub 安装

需要 Node.js 与 npm/npx；通过 Git 仓库安装还需要 Git。当前 skills CLI 的运行要求见其[官方说明](https://github.com/vercel-labs/skills#install-a-skill)。

仓库地址为 `Annabelle0726/spec-to-tested-code`，技能入口位于仓库根目录。

```sh
npx skills add Annabelle0726/spec-to-tested-code --skill spec-to-tested-code -g
```

按安装器提示选择使用技能的工具。`-g` 表示在用户级安装，省略它则安装到当前项目。这里通过 skills CLI 安装仓库中的技能文件，不要求为本项目单独发布 npm 包。

可先只查看仓库中可安装的技能：

```sh
npx skills add Annabelle0726/spec-to-tested-code --list
```

私有仓库需要本机已配置相应的 Git 访问权限。安装完成后，让宿主工具重新加载技能；具体方式遵循该工具的技能加载机制。

## 本地安装

在本项目根目录运行：

```sh
npx skills add . --skill spec-to-tested-code
```

安装器根据 `SKILL.md` 发现技能；`references/` 包含按任务读取的工作说明。技能本身不需要独立应用服务、API 密钥或必装 MCP；实现时使用目标项目已有的工具和测试命令。仓库另附可选的 Python 教学示例与行为评测准备器，不是通用业务测试框架。

## 第一次使用

先给一个小需求，只整理约定：

```text
用 $spec-to-tested-code 梳理“用户取消未发货订单”的已确认规则、验收场景和待决问题，先不编码。
```

预期交付包含：有依据的规则、能对应规则的具体场景，以及会改变验收结果的待决问题。业务未约定的退款、库存回补等行为会留为待决，不自行写成必过场景或交付切片。此处的调用示例不表示已经验证任何真实项目。

已有明确规则并希望继续实现时：

```text
用 $spec-to-tested-code 按已确认的订单取消规则实现，先写能检出错误行为的测试，再完成实现、重构和相关回归。
```

## 可选：运行教学示例与准备评测

这些命令在本项目根目录执行，需要 Python 3.10+，只使用标准库：

```sh
python -B examples/order-cancellation/demo.py
python -B evals/prepare.py
```

第一个命令重放同一组测试的失败与通过；第二个命令只生成独立评测输入，不自动执行模型评测。详见 [示例说明](../examples/order-cancellation/README.md) 和 [行为评测](../evals/README.md)。技能的日常使用不要求运行这两个命令。

## 后续更新

从 GitHub 来源安装后，可使用管理器检查并更新：

```sh
npx skills check
npx skills update
```

这两个命令的检查或更新范围可能包含其他已跟踪的技能，按安装器提示选择。修改技能源码前保留本地改动；本地路径安装不等于已经关联到 GitHub 更新来源。

可用上面的 `--list` 命令检查远程技能是否可发现。安装或发现成功只证明技能文件可读取，不代表任何目标项目的业务场景已经通过验收；示例与技能行为的实际验证范围见 [验证记录](../evals/results/2026-11-17.md)。

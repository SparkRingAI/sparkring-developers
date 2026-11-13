# Maintainer checks and publication gates / 维护检查与发布门槛

This is a procedure, not evidence that a remote repository is already configured. Keep actual account inventories, review reports, settings exports, and internal evidence **outside** this publishable repository. The first release is text-only and has no Actions, Pages deployment, or automatic agent execution.

本文是操作规范，不代表远程仓库已配置。真实账号清单、审查报告、设置导出及内部证据必须放在待公开仓库之外。首版仅包含文本，不运行 Actions、Pages 部署或自动 agent。

## Local checks / 本地检查

From this repository, after reviewing changes to the checker itself:

在本仓库内运行，先人工审查检查脚本自身的改动：

```sh
python3 scripts/check_docs.py
gitleaks dir . --redact=100 --no-banner
gitleaks git . --log-opts="--all" --redact=100 --no-banner
git -C . diff --check
git -C . status --short --branch
```

Use an independently installed, trusted [Gitleaks release](https://github.com/gitleaks/gitleaks), with a verified download checksum. Do not add scanner binaries, caches, or reports to this repository. Run the directory scan before committing and both scans after the final commit. The Git scan must include every local branch and tag, including removed files; do not use a shallow clone for a release review. Re-run after any edit or new commit.

使用独立安装、可信来源的 [Gitleaks](https://github.com/gitleaks/gitleaks)，核验下载校验和。扫描器、缓存和报告不放入本仓库。提交前扫描目录，最终提交后扫描目录和完整 Git 历史，覆盖全部本地分支、标签及已删除文件；发布审查不使用浅克隆。任何修改或新提交后重新运行。

The checker validates local Markdown links and heading fragments, bilingual page pairs, text-only files, prohibited artifacts, own-organization links, and a small set of credential indicators. It also inspects all reachable Git blobs. It is **not** a secret scanner or a proof of confidentiality. Maintain a private list of internal identifiers outside this repository and use it with:

检查脚本核对本地 Markdown 链接和标题锚点、双语页面配对、纯文本文件、禁入产物、组织仓库链接及少量凭据特征，并检查全部可达 Git blob。它**不能**代替密钥扫描或证明内容不含机密。内部标识列表私下保存在仓库外，按以下方式检查：

```sh
python3 scripts/check_docs.py --private-patterns /path/outside/repository/private-patterns.txt
```

The example path is a local argument, not a service address. The list contains one literal identifier per line. Do not include secrets in it, add it to Git, or post its contents in a PR. The checker reports filenames and rule categories, never matching text. Review prose and diffs manually as well; binary files, images, submodules, and symlinks are not accepted in this phase. Introducing images later requires a separate visual and metadata review policy.

上面的路径是本地参数，不是服务地址。列表每行一个内部标识，不放密钥、不加入 Git、不贴到 PR。脚本仅报告文件名和规则类别，不打印命中文本。同时人工审查正文和 diff；本期不接收二进制、图片、子模块或符号链接。未来引入图片时，另行制定视觉和元数据检查规则。

## Content and tutorial gate / 内容与教程门槛

- Review every tracked file and every commit; confirm a new independent root history, original prose, fictional examples, and no imports from private repositories. No internal API dump, configuration, source, prompts, links, real user content, or diagnostic exports.
- Check English and Chinese together for the same availability and data-flow claims. Verify the API contract, local MCP handshake, key lifecycle, and app entry point against the shipped versions. Keep release candidates private until deployment and app validation are complete.
- Reproduce the Markdown recipe with the fictional transcript and compare all three lines and both tasks. For the AI recipe, review expected facts; do not promise deterministic model output or claim a specific tool was tested unless it was.
- Verify the copy action on an **actually installed, released build**, using fictional content. Privately record version, platform, date, and result. A source version or a source inspection alone does not pass this gate. Do not upload real user data as evidence.
- Check public external references for reachability without company credentials. Local checks do not establish remote availability.

- 审查所有受版本控制的文件及每个提交，确认独立新历史、原创文字和虚构示例，不导入私库内容；不含内部接口全集、配置、源码、提示词、链接、真实用户内容或诊断导出。
- 对照中英文的可用性及数据去向，API/MCP 契约、密钥生命周期及 App 入口必须与发布版本一致；部署和 App 验证完成前保持私有。
- 用虚构转写复现 Markdown 教程，对照三行文字和两项任务。AI 教程核对有依据的事实，不承诺模型输出确定，也不虚称测试过某工具。
- 在**实际安装的已发布版本**上用虚构内容验证复制入口，私下记录版本、平台、日期与结果；仅源码版本或源码核对不算通过，不上传真实用户数据作证据。
- 不使用公司凭据检查外部公开参考链接。本地检查不证明远程可用性。

## Isolation gate before remote creation / 建立远程仓库前的隔离门槛

Inspect metadata and access policy, **not secret values**:

仅核验元数据及访问策略，**不读取密钥值**：

1. Audit organization secrets and variables with `all` or `public` visibility, installed GitHub Apps that cover all repositories, inherited workflows, hooks, runners, and automation settings. An authorization error means **unknown**, not empty.
2. Confirm that adding a public repository cannot expose company credentials through inherited access. Confirm that a public Issue, Discussion, PR, or mention cannot launch an agent with access to private repositories or production credentials. Disabling Actions does not disable GitHub Apps or external services.
3. Keep existing organization policies and existing repositories unchanged unless a maintainer has explicit authorization for a specific isolation change. An authorized launch may restrict an existing GitHub App to its current repository set, preserving that access while excluding this public repository and future repositories. Do not add community contributors as organization members or broaden app permissions. Record actual approvals and access evidence privately. Do not expand credentials automatically to work around an inspection failure.

1. 核验面向 `all` 或 `public` 的组织 secrets/variables、覆盖全部仓库的 GitHub Apps、继承工作流、hooks、runner 与自动化设置。权限错误表示**未知**，不表示没有。
2. 确认新增公开仓库不会通过继承权限暴露公司凭据；公开 Issue、Discussion、PR 或提及不能触发有私库或线上凭据权限的 agent。关闭 Actions 不会关闭 GitHub Apps 或外部服务。
3. 除非维护者明确授权特定隔离变更，否则不改现有组织策略或仓库。获授权的首发可将现有 GitHub App 限定到当前仓库集合，保留原访问并排除本公开仓库及未来仓库。不将社区贡献者加入组织，不扩大 app 权限。实际授权与访问证据私下记录，不自动扩大凭据权限来绕过检查失败。

## Repository configuration / 仓库配置

After the inheritance gate passes, a maintainer may bootstrap the independently reviewed `dev` commit and create `main` from that same commit. No private history is imported. Disable Actions on an empty remote **before** pushing content. Do not add repository secrets, variables, hooks, runners, deploy keys, or production/cloud access.

继承权限核验通过后，维护者可引导经过审查的独立 `dev` 提交，从同一提交建立 `main`，不导入私有历史。在空远程仓库上**先关闭 Actions，再推送内容**。不新增 secrets、variables、hooks、runner、部署密钥或线上/云权限。

- Set `main` as the default/release branch and `dev` as the working/PR target branch. Enable Issues and Discussions; keep the wiki and Pages deployment off. [Repository settings payload](repository-settings.json) is a REST edit-repository body, not an automatically applied setting.
- Grant the existing CODEOWNERS team Write on this repository only; verify the team is eligible for code ownership. Grant no external write access or organization membership. Existing organization owners retain their administrative powers; this procedure is not a separate organization boundary.
- Apply the [branch ruleset payload](branch-rules.json) to both `main` and `dev`: PR required, one CODEOWNER approval, stale approvals dismissed, last push approved by someone else, review threads resolved, no force push or deletion, and no configured bypass actor. Verify effective rules by reading them back, not just by receiving a successful write response.
- Enable secret scanning, push protection, and private vulnerability reporting. Verify each setting and the actual reporting route. Do not add a workflow to test them.
- GitHub Free supports rulesets for public repositories, not private organization staging repositories. A private staging repository therefore cannot prove that the required rules are enforced before publication. With explicit authorization for a controlled public bootstrap, create an empty public repository, disable Actions, push only the reviewed initial snapshot, and immediately apply and read back the required settings and protections before opening community participation. Later changes must use reviewed PRs. Do not treat a prepared payload as an enforced rule. Keep the draft local if that launch sequence is not authorized. [GitHub ruleset availability](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets)

- `main` 为默认及发布分支，`dev` 为工作及 PR 目标分支。开启 Issues、Discussions，关闭 wiki 和 Pages 部署。[仓库设置 payload](repository-settings.json) 是 REST 修改仓库请求体，不代表已应用。
- 仅为 CODEOWNERS 中现有团队授予本仓库 Write，并验证团队可作为代码所有者；不授予外部写权限或组织成员身份。现有组织 owner 仍有管理权限，这不是独立组织边界。
- 为 `main`、`dev` 应用[分支规则 payload](branch-rules.json)：必须 PR、一位 CODEOWNER 审批、推送后旧审批失效、最后推送由他人批准、讨论已解决、禁强推及删除、无配置的绕过主体。读回有效规则，不能仅凭请求成功判断生效。
- 启用并核验 secret scanning、push protection、私密漏洞报告及实际报告入口，不添加用于测试它们的工作流。
- GitHub Free 的 ruleset 适用于公开仓库，不适用于组织私有暂存仓库；因此私有暂存不能证明发布前规则已强制执行。明确获准受控公开引导时，可创建空公开仓库、关闭 Actions，仅推送经过审查的初始快照，立即应用并读回所需设置与保护，再开放社区参与。后续改动必须经过 PR 审查。准备好的 payload 不代表生效；未获准这一发布顺序时保留本地草稿。[GitHub ruleset 可用范围](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets)

## Outside-user gate and handoff / 外部用户验收与交接

Use an account with no organization role or repository grant to verify reading, forking, and proposing a PR once an authorized public validation step is possible. Verify it cannot merge or read any existing private repository. Unauthenticated reading alone does not prove fork/PR permissions. Do not enroll an external account into the organization for testing, or try to merge or access private content as a test.

在允许公开验证后，使用无组织身份、无仓库授权的账号验证阅读、fork 和提交 PR，并验证不能合并或读取现有私库。匿名阅读不代表 fork/PR 权限已验证。不要为了测试将外部账号加入组织，也不实际尝试合并或读取私有内容。

The first launch needs a private checklist with actual evidence and statuses for every gate. Unknown or failed checks block publication. Keep the draft local, without a remote, until pre-creation gates pass. If publication is blocked, hand off the completed local material and a private report of the exact remaining requirements. Follow [Security](../SECURITY.md) for a disclosure; deleting content or reverting visibility does not undo exposure.

首发使用私下清单记录各门槛的实际证据与状态；未知或失败都阻止公开。远程创建前门槛通过之前，本地草稿不配置 remote。阻塞时交付已完成材料及明确剩余条件的私下报告。泄露按[安全说明](../SECURITY.md)处理，删内容或改回私有不能撤销披露。

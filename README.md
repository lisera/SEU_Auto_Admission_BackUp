**备份[@quzard](https://github.com/quzard)的自动入校申请脚本**

**入校申请前需要健康申报，可以用[东南大学自动每日健康申报脚本](https://github.com/zgzhengSEU/SEU-Auto-Health-Declaration)自动申报**

--------

# SEU_Auto_Admission
东南大学自动入校申请

![Stars](https://img.shields.io/github/stars/quzard/SEU_Auto_Admission.svg)
![Forks](https://img.shields.io/github/forks/quzard/SEU_Auto_Admission.svg)

## 已实现

- [x] 研究生入校申请
- [ ] 本科生入校申请未验证 应该也可以

## 使用步骤

1. 首先 fork 本项目到自己的仓库

2. 去 Actions 那 Enable Workflow

3. 进入自己 fork 的仓库，点击 Settings -> Secrets -> New repository secret，它们将作为配置项，在应用启动时传入程序。

**所有的可用 Secrets 及说明**

| Secret     | 解释                                                         |
| ---------- | ------------------------------------------------------------ |
| USERNAME   | 一卡通号                                                     |
| PASSWORD   | 一卡通密码                                                   |

4. 如果需要修改上报时间，修改 `.github/workflows/auto_admission.yml`

**备份[@quzard](https://github.com/quzard)的自动入校申请脚本**

**入校申请前需要健康申报，可以用[东南大学自动每日健康申报脚本](https://github.com/zgzhengSEU/SEU-Auto-Health-Declaration)自动申报**

**[东南大学自动请假脚本](https://github.com/zgzhengSEU/SEU_Auto_Leave_backup)**

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

![](https://cdn.jsdelivr.net/gh/zgzhengSEU/imagebed/Image/202112021430674.png)

2. 进入自己 fork 的仓库，点击 Settings -> Secrets -> New repository secret，它们将作为配置项，在应用启动时传入程序。

![image-20211202101810673](https://cdn.jsdelivr.net/gh/zgzhengSEU/imagebed/Image/202112021018740.png)

**所有的可用 Secrets 及说明**

| Secret     | 解释                                                         |
| ---------- | ------------------------------------------------------------ |
| USERNAME   | 一卡通号                                                     |
| PASSWORD   | 一卡通密码                                                   |

![image-20211202102037983](https://cdn.jsdelivr.net/gh/zgzhengSEU/imagebed/Image/202112021020047.png)

![image-20211202102001308](https://cdn.jsdelivr.net/gh/zgzhengSEU/imagebed/Image/202112021020697.png)

3. 去 Actions 那 Enable Workflow, 然后点击 star 手动启动一次脚本

![](https://cdn.jsdelivr.net/gh/zgzhengSEU/imagebed/Image/202112021433604.png)

5. 如果需要修改上报时间，修改 `.github/workflows/auto_admission.yml`

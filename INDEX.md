# 📑 PROJECT DOCUMENTATION INDEX

## 📌 MASTER GUIDE

Dưới đây là danh sách tất cả các tài liệu đã tạo để lên PRD chi tiết và chia thành task nhỏ:

---

## 🎯 BẮT ĐẦU TỪ ĐÂY

### 👨‍💼 Cho Người Quản Lý / Stakeholder
1. **[EXECUTIVE_SUMMARY.md](./EXECUTIVE_SUMMARY.md)** (5 min read)
   - High-level overview
   - Business case & ROI
   - Timeline & resource requirements
   - Risk register
   - → Dùng để: Convince management to approve project

### 👨‍💻 Cho Người Làm Việc
2. **[QUICK_REFERENCE.md](./QUICK_REFERENCE.md)** (Cheat sheet)
   - Tất cả thông tin cần thiết ở 1 chỗ
   - Project structure
   - Common commands
   - Troubleshooting
   - → Dùng để: Quick lookup during development

3. **[PRD.md](./PRD.md)** (Detailed spec)
   - Complete requirements
   - Detailed task descriptions
   - Success criteria
   - Timeline
   - → Dùng để: Understand full scope & detailed requirements

### 📱 Cho Slack Communication
4. **[SLACK_NOTIFICATIONS.md](./SLACK_NOTIFICATIONS.md)**
   - Copy-paste messages cho mỗi batch
   - Task descriptions
   - Checklists
   - → Dùng để: Post updates to Slack channel

### 📊 Cho Progress Tracking
5. **[TASK_TRACKER.md](./TASK_TRACKER.md)**
   - Status của tất cả 25 tasks
   - Timeline & milestones
   - Risk register
   - Standup template
   - → Dùng để: Track progress daily

---

## 📁 FILE STRUCTURE

```
PROJECT_ROOT/
├── PRD.md                              ← Full requirements (40 min read)
├── EXECUTIVE_SUMMARY.md                ← For management (5 min read)
├── QUICK_REFERENCE.md                  ← Cheat sheet (10 min read)
├── SLACK_NOTIFICATIONS.md              ← Slack templates (copy-paste)
├── TASK_TRACKER.md                     ← Progress tracking
├── INDEX.md                            ← You are here
│
├── [Source Code Files - current audited pipeline]
│   ├── src/features.py                 (T0-safe feature whitelist + leakage guards)
│   ├── src/model_eval.py               (profit curve, ROC, Lift, cost matrix, Decision 2345)
│   ├── src/data_loader.py              (scope filtering, chronological split, train balancing)
│   ├── src/baseline_model.py           (CREATE - BATCH 4)
│   └── tests/                          (CREATE - BATCH 2)
│
├── [API & Deployment - to be created by BATCH 5]
│   ├── app/app.py                      (CREATE)
│   ├── app/model_inference.py          (CREATE)
│   ├── Dockerfile                      (CREATE)
│   └── docker-compose.yml              (CREATE)
│
└── [Notebooks & Visualizations]
    ├── notebooks/03_modeling.ipynb            (current audited modeling notebook)
    ├── notebooks/04_metrics_analysis.ipynb    (optional future split-out)
    └── reports/figures/                       (optional exported visualizations)
```

---

## 📖 HOW TO USE THESE DOCUMENTS

### Phase 1: Planning & Approval (Day 0)
1. Read **EXECUTIVE_SUMMARY.md** (5 min)
2. Review **PRD.md** Overview section (10 min)
3. → Decision: Approve project? YES/NO

### Phase 2: Preparation (Day 0-1)
1. Read **QUICK_REFERENCE.md** (10 min) - Get oriented
2. Read **PRD.md** fully (30 min) - Understand all requirements
3. Create Slack channel: `#fraud-detection-paysim`
4. Copy **SLACK_NOTIFICATIONS.md** to reference

### Phase 3: Execution (Day 2-20)
1. **Daily Morning:**
   - Review current BATCH in **QUICK_REFERENCE.md**
   - Check **TASK_TRACKER.md** for today's tasks
   - Post Slack standup

2. **During Work:**
   - Refer to **QUICK_REFERENCE.md** for commands & structure
   - Use **PRD.md** for detailed task requirements
   - Check **TASK_TRACKER.md** progress

3. **End of Day:**
   - Update **TASK_TRACKER.md**
   - Post completion to **Slack** (copy from SLACK_NOTIFICATIONS.md)

### Phase 4: Closure (Day 20+)
1. Verify all tasks in **TASK_TRACKER.md** marked as DONE
2. Run final checks from **QUICK_REFERENCE.md** → "DONE CHECKLIST"
3. Share **EXECUTIVE_SUMMARY.md** results with stakeholders

---

## 🚀 BATCH PROGRESSION GUIDE

### When Starting BATCH 1 (Code Cleanup)
→ Open: **QUICK_REFERENCE.md** + **SLACK_NOTIFICATIONS.md** (BATCH 1 section)
→ Current note: leakage guards and `build_features()` are already in place; remaining work is tests/docstrings/polish.

### When Starting BATCH 2 (Unit Tests)
→ Open: **PRD.md** (BATCH 2 section) + **QUICK_REFERENCE.md** (Testing commands)

### When Starting BATCH 3 (Metrics)
→ Open: **PRD.md** (BATCH 3) + **QUICK_REFERENCE.md** (Project structure)

### When Starting BATCH 4 (Baseline)
→ Open: **PRD.md** (BATCH 4) + **QUICK_REFERENCE.md** (Baseline metrics)

### When Starting BATCH 5 (Deployment)
→ Open: **PRD.md** (BATCH 5) + **QUICK_REFERENCE.md** (Docker commands)

### When Starting BATCH 6 (Documentation)
→ Open: **PRD.md** (BATCH 6) + **QUICK_REFERENCE.md** (Documentation templates)

---

## 📋 DOCUMENT PURPOSES

| Document | Purpose | Read Time | Audience | When to Use |
|----------|---------|-----------|----------|------------|
| **EXECUTIVE_SUMMARY.md** | High-level overview | 5 min | Management | Get approval |
| **PRD.md** | Complete requirements | 40 min | Developer | Plan & execute |
| **QUICK_REFERENCE.md** | Daily cheat sheet | 10 min | Developer | During work |
| **SLACK_NOTIFICATIONS.md** | Slack templates | 10 min | Developer | Post to Slack |
| **TASK_TRACKER.md** | Progress tracking | 5 min | Everyone | Track status |
| **INDEX.md** | This file | 5 min | Everyone | Navigate docs |

---

## 🎯 QUICK NAVIGATION

### Need to understand...
- **"What is the project?"** → EXECUTIVE_SUMMARY.md
- **"What are all the tasks?"** → PRD.md (Full list)
- **"What do I do today?"** → QUICK_REFERENCE.md (Today's BATCH)
- **"How do I test?"** → QUICK_REFERENCE.md (Common Commands)
- **"What's the progress?"** → TASK_TRACKER.md
- **"How do I post to Slack?"** → SLACK_NOTIFICATIONS.md

### Need to find...
- **Task details** → PRD.md (Search for "Task X.Y")
- **Command examples** → QUICK_REFERENCE.md (Search "Commands")
- **File locations** → QUICK_REFERENCE.md (Search "PROJECT STRUCTURE")
- **Docstring template** → QUICK_REFERENCE.md (Search "TEMPLATE")
- **Docker commands** → QUICK_REFERENCE.md (Search "Docker")
- **Done checklist** → TASK_TRACKER.md or QUICK_REFERENCE.md

---

## 💡 READING RECOMMENDATIONS

### If you have 5 minutes
**Read:** EXECUTIVE_SUMMARY.md

### If you have 15 minutes
**Read:** EXECUTIVE_SUMMARY.md + QUICK_REFERENCE.md (Introduction)

### If you have 30 minutes
**Read:** QUICK_REFERENCE.md + PRD.md (Overview section)

### If you have 1 hour
**Read:** All documents in order:
1. EXECUTIVE_SUMMARY.md (5 min)
2. QUICK_REFERENCE.md (15 min)
3. PRD.md (40 min)

### If you want to get started immediately
**Go to:** QUICK_REFERENCE.md → Find today's BATCH → Start coding!

---

## 🔄 DAILY WORKFLOW

### Every Morning
1. Open **TASK_TRACKER.md**
2. Find next NOT-STARTED or IN-PROGRESS task
3. Open **QUICK_REFERENCE.md** to that BATCH section
4. Read task details in **PRD.md**
5. Post to Slack using **SLACK_NOTIFICATIONS.md** template

### During Work
1. Keep **QUICK_REFERENCE.md** open (bookmark it!)
2. Use commands from "Common Commands" section
3. Refer to "Project Structure" for file locations
4. Check "Done Checklist" before marking task complete

### End of Day
1. Update **TASK_TRACKER.md** with progress
2. Commit code to GitHub
3. Post completion to Slack (copy template from SLACK_NOTIFICATIONS.md)

---

## 📞 COMMUNICATION CHANNELS

| Channel | Content | Frequency |
|---------|---------|-----------|
| **Slack #fraud-detection-paysim** | Daily updates, blockers | Daily |
| **GitHub PRs** | Code review | As needed |
| **TASK_TRACKER.md** | Progress metrics | Daily EOD |
| **Email Summary** | Weekly progress | Friday EOD |

---

## ✅ SUCCESS CRITERIA

**Project is ready for launch when:**
- [ ] TASK_TRACKER.md shows 25/25 tasks DONE
- [ ] README.md is comprehensive & professional
- [ ] All tests passing (80%+ coverage)
- [ ] API working locally & in Docker
- [ ] Data governance statement explicit
- [ ] All links in README verified
- [ ] Ready for "portfolio review"

---

## 🚨 IMPORTANT NOTES

⚠️ **READ FIRST:**
1. EXECUTIVE_SUMMARY.md (understand context)
2. QUICK_REFERENCE.md (daily reference)

⚠️ **DON'T SKIP:**
1. Unit tests (BATCH 2) - Critical for code quality
2. API testing (BATCH 5) - Test locally before Docker

⚠️ **KEY MILESTONES:**
- BATCH 1-2: Code quality foundation (Week 1)
- BATCH 3-4: Business value demonstration (Week 2)
- BATCH 5: Deployment capability (Week 3)
- BATCH 6: Professional presentation (Week 4)

⚠️ **BATCH DEPENDENCIES:**
```
BATCH 1 (required for all)
    ↓
BATCH 2 (required for BATCH 5)
    ↓
BATCH 3 & 4 (can run in parallel)
    ↓
BATCH 5 (required before BATCH 6)
    ↓
BATCH 6 (last - depends on all)
```

---

## 📚 RELATED RESOURCES

### In This Repository
- `README.md` - Current audited project overview
- `notebooks/` - EDA, feature engineering, modeling
- `src/` - Source code (to be cleaned & tested)
- `models/` - Trained model (lightgbm_model.joblib)
- `reports/` - Visualizations (to be created)

### External Resources
- GitHub: huudang-de/fraud-detection-paysim
- Slack: #fraud-detection-paysim
- PyTest: https://docs.pytest.org/
- Flask: https://flask.palletsprojects.com/
- Docker: https://docs.docker.com/

---

## 👥 CONTACTS

| Role | Name | Slack | Email |
|------|------|-------|-------|
| Project Owner | [TBD] | @[TBD] | [TBD] |
| Developer | [TBD] | @[TBD] | [TBD] |
| Reviewer | [TBD] | @[TBD] | [TBD] |

---

## 📝 DOCUMENT HISTORY

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2026-05-24 | Initial PRD creation | AI Assistant |
| - | - | - | - |

---

## 🎯 NEXT STEPS

1. **Print or bookmark these documents:**
   - [ ] EXECUTIVE_SUMMARY.md
   - [ ] QUICK_REFERENCE.md
   - [ ] PRD.md (for reference)

2. **Share with team:**
   - [ ] Post EXECUTIVE_SUMMARY.md link in Slack
   - [ ] Pin QUICK_REFERENCE.md in channel
   - [ ] Assign developer to project

3. **Create Slack channel:**
   - [ ] Channel name: #fraud-detection-paysim
   - [ ] Post: Project overview
   - [ ] Pin: QUICK_REFERENCE.md

4. **Start BATCH 1:**
   - [ ] Post BATCH 1 message from SLACK_NOTIFICATIONS.md
   - [ ] Developer starts: Code cleanup (2-3 hours)
   - [ ] First daily standup

---

**Document Created:** May 24, 2026  
**Last Updated:** May 28, 2026  
**Status:** ✅ Ready for Use  

**Questions?** Check the relevant section above or contact project owner.


# 🚀 QUICK REFERENCE GUIDE (Cheat Sheet)

**Use this guide to quickly find information during development**

---

## 📌 PROJECT AT A GLANCE

**Goal:** Make fraud detection project production-ready  
**Duration:** 4 weeks (5 days work)  
**Batches:** 6  
**Total Tasks:** 25  
**Hours:** ~28  

**Slack Channel:** #fraud-detection-paysim  
**GitHub Repo:** huudang-de/fraud-detection-paysim  
**Main Branch:** main  

---

## 🎯 TODAY'S BATCH (Quick Lookup)

### BATCH 1: Code Cleanup (2-3 hours)
📍 **Status:** [START HERE IF JUST STARTING]

```bash
# What to do:
1. Verify notebooks/imports use build_features() consistently
2. Add docstrings to src/features.py (NumPy style)
3. Add docstrings to src/model_eval.py
4. Add docstrings to src/data_loader.py
5. Run flake8, fix all PEP 8 violations

# Quick commands:
flake8 src/ --max-line-length=100
pip install flake8  # if needed
```

📍 **Files to Modify:**
- `src/features.py`
- `src/model_eval.py`
- `src/data_loader.py`

📍 **Definition of Done:**
- [x] Typo fixed: `build_fratures()` → `build_features()`
- [x] `build_features()` docstring added (NumPy style)
- [ ] `split_xy()` docstring added
- [ ] `src/data_loader.py` docstrings added
- [ ] `src/model_eval.py` docstrings added
- [ ] Flake8: 0 violations
- [ ] Code review: ✅ PASS

---

### BATCH 2: Unit Tests (4-6 hours)
📍 **Status:** Starts after BATCH 1

```bash
# What to do:
1. Create tests/test_features.py (≥80% coverage)
2. Create tests/test_model_eval.py (≥70% coverage)
3. Create tests/test_integration.py
4. Set up .github/workflows/tests.yml (CI/CD)

# Quick commands:
pytest tests/ --cov=src/ --cov-report=html
pytest tests/test_features.py -v  # Run specific test
```

📍 **Files to Create:**
- `tests/test_features.py` (NEW)
- `tests/test_model_eval.py` (NEW)
- `tests/test_integration.py` (NEW)
- `.github/workflows/tests.yml` (NEW)

---

### BATCH 3: Metrics (3-4 hours)
📍 **Status:** Can start after data is ready

```bash
# What to do:
1. Create notebooks/04_metrics_analysis.ipynb
2. Add model comparison section to notebooks/03_modeling.ipynb
3. Save visualizations to reports/figures/

# Key visualizations:
- Confusion Matrix (confusion_matrix_lightgbm.png)
- ROC Curve (roc_curve_lightgbm.png)
- Precision-Recall Curve (precision_recall_curve.png)
- Feature Importance (feature_importance.png)
- Model Comparison (model_comparison.png)
```

📍 **Files to Create:**
- `notebooks/04_metrics_analysis.ipynb` (NEW)
- `reports/figures/*.png` (5+ PNG files)

---

### BATCH 4: Baseline (4-5 hours)
📍 **Status:** Can run in parallel with BATCH 3

```bash
# What to do:
1. Implement rule-based baseline in src/baseline_model.py
2. Create notebooks/05_baseline_comparison.ipynb
3. Document ROI in METHODOLOGY.md

# Current audited metric:
Profit-curve optimized saving = 1.52B VND vs rule baseline (22.73%)
```

📍 **Files to Create:**
- `src/baseline_model.py` (NEW)
- `notebooks/05_baseline_comparison.ipynb` (NEW)

---

### BATCH 5: Deployment (5-7 hours)
📍 **Status:** Starts after BATCH 2

```bash
# What to do:
1. Create Flask/FastAPI app (app/app.py)
2. Model inference pipeline (app/model_inference.py)
3. Docker setup (Dockerfile, docker-compose.yml)
4. API docs (app/README_API.md)
5. Deployment guide (DEPLOYMENT.md)

# Quick commands - LOCAL TESTING:
python app/app.py                          # Start Flask locally
curl http://localhost:5000/health          # Test health endpoint
curl -X POST http://localhost:5000/predict # Test prediction

# Quick commands - DOCKER:
docker build -t fraud-detection .          # Build image
docker-compose up                          # Start container
docker-compose down                        # Stop container
```

📍 **Files to Create:**
- `app/app.py` (NEW) - Flask/FastAPI application
- `app/model_inference.py` (NEW) - Model loading + inference
- `app/requirements.txt` (NEW) - Python dependencies
- `Dockerfile` (NEW) - Container setup
- `docker-compose.yml` (NEW) - Orchestration
- `app/README_API.md` (NEW) - API documentation
- `DEPLOYMENT.md` (NEW) - Deployment instructions

📍 **API Endpoints to Implement:**
- `POST /predict` - Single transaction
- `POST /predict_batch` - Batch predictions
- `GET /health` - Health check
- `GET /docs` - Swagger docs

---

### BATCH 6: Documentation (3-4 hours)
📍 **Status:** After all above batches

```bash
# What to do:
1. Rewrite README.md (comprehensive)
2. Create DATA_DICTIONARY.md (feature docs)
3. Create METHODOLOGY.md (ML approach)
4. Create DATA_GOVERNANCE.md (synthetic data)
5. Verify all links work

# Verification:
grep -r "notebooks/" README.md  # Check notebook links
grep -r "reports/" README.md    # Check image links
```

📍 **Files to Create/Modify:**
- `README.md` (REWRITE) - Main documentation
- `DATA_DICTIONARY.md` (NEW) - Feature descriptions
- `METHODOLOGY.md` (NEW) - ML approach explained
- `DATA_GOVERNANCE.md` (NEW) - Data transparency

---

## 📁 PROJECT STRUCTURE

```
fraud-detection-paysim/
├── README.md                          ← Updated by BATCH 6
├── PRD.md                            ← (You're reading this)
├── EXECUTIVE_SUMMARY.md              ← For managers
├── SLACK_NOTIFICATIONS.md            ← Copy-paste Slack messages
├── TASK_TRACKER.md                   ← Track progress
├── METHODOLOGY.md                    ← To be created (BATCH 6)
├── DEPLOYMENT.md                     ← To be created (BATCH 5)
├── DATA_GOVERNANCE.md                ← To be created (BATCH 6)
├── DATA_DICTIONARY.md                ← To be created (BATCH 6)
│
├── src/
│   ├── __init__.py
│   ├── data_loader.py               ← Fix docstrings (BATCH 1)
│   ├── features.py                  ← Fix typo + docstrings (BATCH 1)
│   ├── model_eval.py                ← Add docstrings (BATCH 1)
│   └── baseline_model.py            ← New (BATCH 4)
│
├── tests/                           ← New (BATCH 2)
│   ├── __init__.py
│   ├── test_features.py             ← New (BATCH 2)
│   ├── test_model_eval.py           ← New (BATCH 2)
│   └── test_integration.py          ← New (BATCH 2)
│
├── app/                             ← New (BATCH 5)
│   ├── app.py                       ← Flask/FastAPI app
│   ├── model_inference.py           ← Model loading + prediction
│   ├── requirements.txt             ← Python dependencies
│   └── README_API.md                ← API documentation
│
├── notebooks/
│   ├── 01_eda.ipynb                 ← Existing
│   ├── 02_feature_eng.ipynb         ← Existing
│   ├── 03_modeling.ipynb            ← Update with comparison (BATCH 3)
│   ├── 04_metrics_analysis.ipynb    ← New (BATCH 3)
│   └── 05_baseline_comparison.ipynb ← New (BATCH 4)
│
├── reports/
│   └── figures/
│       ├── confusion_matrix_lightgbm.png     ← New (BATCH 3)
│       ├── roc_curve_lightgbm.png           ← New (BATCH 3)
│       ├── precision_recall_curve.png       ← New (BATCH 3)
│       ├── feature_importance.png           ← New (BATCH 3)
│       └── model_comparison.png             ← New (BATCH 3)
│
├── models/
│   └── lightgbm_model.joblib        ← Existing (loaded by app)
│
├── data/
│   ├── raw/
│   │   └── Synthetic_Financial_datasets_log.csv
│   ├── processed/
│   └── external/
│
├── Dockerfile                        ← New (BATCH 5)
├── docker-compose.yml               ← New (BATCH 5)
│
└── .github/
    └── workflows/
        └── tests.yml                ← New (BATCH 2)
```

---

## 🔧 COMMON COMMANDS

### Git
```bash
# Check current branch
git status

# Create new branch
git checkout -b feature/batch-1-cleanup

# Commit changes
git add src/features.py
git commit -m "BATCH 1: Verify feature imports"

# Push to GitHub
git push origin feature/batch-1-cleanup
```

### Python Testing
```bash
# Install test dependencies
pip install pytest pytest-cov

# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_features.py -v

# Generate coverage report
pytest tests/ --cov=src/ --cov-report=html
```

### Docker
```bash
# Build image
docker build -t fraud-detection:latest .

# Run container
docker-compose up

# Stop container
docker-compose down

# View logs
docker-compose logs -f app
```

### Code Quality
```bash
# Check PEP 8
flake8 src/ --max-line-length=100

# Auto-format code
pip install black
black src/

# Check docstrings
pip install pydocstyle
pydocstyle src/
```

---

## 📋 DOCSTRING TEMPLATE (NumPy Style)

```python
def build_features(df):
    """
    Build features for fraud detection model.
    
    This function creates domain-specific features based on
    transaction patterns, temporal information, and account behavior.
    
    Parameters
    ----------
    df : pandas.DataFrame
        Input dataframe with raw transaction data.
        Must contain columns: step, type, amount, oldbalanceDest, etc.
    
    Returns
    -------
    pandas.DataFrame
        DataFrame with engineered features and isFraud target.
        Columns: [is_high_risk_type, log_amount, hour, is_night, ...]
    
    Examples
    --------
    >>> df = pd.read_csv('transactions.csv')
    >>> features_df = build_features(df)
    >>> print(features_df.shape)
    (6362620, 12)
    
    Notes
    -----
    - High-risk types: TRANSFER, CASH_OUT
    - Night hours: 23:00 - 05:59 (peak fraud time)
    - Zero balance: Indicator of account depletion
    """
    pass
```

---

## 📊 BATCH DEPENDENCIES

```
BATCH 1 (Code)
    ↓
BATCH 2 (Tests)
    ↓
BATCH 3 (Metrics) ←→ BATCH 4 (Baseline)
    ↓         ↓
    └────BATCH 5 (API)
         ↓
    BATCH 6 (Docs)
```

**Key Rules:**
- ✅ BATCH 1 must be done first
- ✅ BATCH 2 must be done before BATCH 5
- ✅ BATCH 3 & 4 can run in parallel
- ✅ BATCH 5 can start after BATCH 2
- ✅ BATCH 6 is last (depends on all)

---

## ✅ DONE CHECKLIST BY BATCH

### BATCH 1 Done?
- [ ] All notebooks/imports use `build_features()`
- [ ] All 3 files have NumPy docstrings
- [ ] Flake8 passes (0 violations)
- [ ] Commit pushed: `git push origin feature/batch-1-cleanup`
- [ ] Code review approved

### BATCH 2 Done?
- [ ] `tests/test_features.py` created (80%+ coverage)
- [ ] `tests/test_model_eval.py` created (70%+ coverage)
- [ ] All tests passing: `pytest tests/`
- [ ] CI pipeline working: `.github/workflows/tests.yml`
- [ ] Coverage report generated
- [ ] Commit pushed

### BATCH 3 Done?
- [ ] `notebooks/04_metrics_analysis.ipynb` created
- [ ] 5+ PNG visualizations saved in `reports/figures/`
- [ ] Model comparison section added to modeling notebook
- [ ] All images high quality (300 DPI)
- [ ] Commit pushed

### BATCH 4 Done?
- [ ] `src/baseline_model.py` implemented
- [ ] `notebooks/05_baseline_comparison.ipynb` created
- [ ] ROI quantified with profit-curve threshold (current: 1.52B VND, 22.73%)
- [ ] Baseline vs ML metrics compared
- [ ] Commit pushed

### BATCH 5 Done?
- [ ] Flask/FastAPI app working locally
- [ ] All 4 endpoints tested (`/health`, `/predict`, `/predict_batch`, `/docs`)
- [ ] Docker image builds: `docker build -t fraud-detection .`
- [ ] Docker container runs: `docker-compose up`
- [ ] API accessible at `http://localhost:5000`
- [ ] Swagger docs working at `/docs`
- [ ] Commit pushed

### BATCH 6 Done?
- [ ] README.md completely rewritten (1000+ words)
- [ ] DATA_DICTIONARY.md created (all features)
- [ ] METHODOLOGY.md created (ML approach)
- [ ] DATA_GOVERNANCE.md created (synthetic data)
- [ ] All links verified and working
- [ ] Commit pushed
- [ ] Ready for launch

---

## 🎯 METRICS TO TRACK

### Coverage Metrics
- Unit test coverage: ≥80% for `src/features.py`
- Unit test coverage: ≥70% for `src/model_eval.py`
- Flake8 violations: **0**
- Broken links in README: **0**

### Performance Metrics
- API response time: <500ms
- Model prediction time: <100ms
- Docker build time: <2 min
- Test suite execution: <30 sec

### Business Metrics
- Cost savings vs rule: 22.73% (1.52B VND)
- Model AP: 0.3955
- Model ROC-AUC: 0.9036
- Lift @ top 10%: 7.49x
- Profit-curve threshold: 0.99290966

---

## 🆘 TROUBLESHOOTING

### Flake8 Errors
```bash
# Common issues:
# E501: Line too long
#   → Add # noqa: E501 at end of line
#   → Or split line into multiple lines

# E302: Expected 2 blank lines
#   → Add blank lines between functions

# W293: Blank line contains whitespace
#   → Remove trailing spaces
```

### Test Failures
```bash
# If tests fail:
pytest tests/ -v              # Show detailed output
pytest tests/test_features.py -x  # Stop at first failure
pytest tests/test_features.py -s  # Show print statements
```

### Docker Issues
```bash
# Docker build fails?
docker build -t fraud-detection . --no-cache

# Container won't start?
docker-compose logs app  # Check logs
docker-compose restart   # Restart container

# Port already in use?
lsof -i :5000           # Find process using port 5000
kill -9 <PID>           # Kill process
```

### API Issues
```bash
# Model not loading?
# → Check models/lightgbm_model.joblib exists
# → Check path in app/model_inference.py

# Prediction endpoint returns error?
# → Check input format matches requirements
# → Check feature engineering matches training
```

---

## 📞 GET HELP

- **PRD Details:** See `PRD.md` (full requirements)
- **Task Details:** See `SLACK_NOTIFICATIONS.md` (detailed task descriptions)
- **Progress:** See `TASK_TRACKER.md` (track what's done)
- **For Managers:** See `EXECUTIVE_SUMMARY.md` (high-level overview)

---

## 📅 TYPICAL DAILY WORKFLOW

```
9:00 AM   → Daily standup (5 min)
          → Review TASK_TRACKER.md
          → Pick next task from current BATCH

9:05 AM   → Start coding
          → Every 30 min: Test changes
          → Every 1 hour: Commit progress

12:00 PM  → Lunch

1:00 PM   → Continue coding
          → Run full test suite before end of task
          → Commit when task complete

4:00 PM   → Code review (self-review against checklist)
          → Update TASK_TRACKER.md
          → Prepare for next day

5:00 PM   → Push to GitHub
          → Post completion to Slack
          → EOD standup (5 min)
```

---

## 💡 PRO TIPS

1. **Save time:** Do BATCH 3 & 4 in parallel (no dependencies)
2. **Test early:** Don't wait until end of batch to test
3. **Commit often:** Small commits are easier to review
4. **Document as you go:** Don't leave docstrings for last
5. **Use templates:** Copy docstring template for all functions
6. **Docker first:** If working on BATCH 5, test locally first before Docker
7. **Version control:** Always branch from main for each batch

---

**Last Updated:** May 28, 2026  
**Slack Channel:** #fraud-detection-paysim  
**Questions?** Ask in Slack or check PRD.md


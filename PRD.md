# 📋 PRD: Project Improvement & Enhancement

**Project:** Fraud Detection System - PaySim  
**Owner:** Data Science Team  
**Duration:** 4 Phases (4-5 weeks)  
**Priority:** High (Portfolio Enhancement)

---

## 📌 OVERVIEW

**Current State:**
- ✅ Core ML model completed and rerun after leakage remediation
- ✅ LightGBM current validated metrics: ROC-AUC=0.9036, AP=0.3955
- ✅ Profit-curve threshold selected: 0.99290966
- ✅ Current saving vs rule baseline: 1.52B VND, 22.73%
- ✅ Feature engineering now uses a T0-safe whitelist and leakage guards
- ❌ Project presentation still needs tests, deployment, saved visualizations, and governance docs

Deprecated claims that must not be reused: `AP=0.856`, `77% cost savings`, `1.8B VND savings`, `65.88% auto-approval`.

**Goal:**  
Transform from **prototype** → **production-ready portfolio project** by addressing 7 critical gaps.

---

## 🎯 SUCCESS CRITERIA

| Criteria | Current | Target | Owner |
|----------|---------|--------|-------|
| README Completeness | 40% | 100% | TBD |
| Test Coverage | 0% | 80%+ | TBD |
| Model Deployment Ready | ❌ | ✅ (Flask API) | TBD |
| Code Documentation | 30% | 95% | TBD |
| Metrics Visualization | 50% | 100% | TBD |
| Baseline Comparison | ❌ | ✅ (Quantified) | TBD |
| Data Governance | ⚠️ Implicit | ✅ Explicit | TBD |

---

## 📦 DELIVERABLES BY PHASE

### **PHASE 1: Code Quality & Documentation (Week 1)**
**Goal:** Clean up code, fix typos, improve readability  
**Status:** 🔄 IN PROGRESS (Task 1.1, 1.2 done ✅ | Task 1.3 in progress 🔄 | Task 1.4-1.5 pending)

**Acceptance Criteria:**
- [x] Verify all notebooks/imports use `build_features()`
- [x] Add docstrings to `src/features.py` (2 functions complete)
- [ ] Add docstrings to `src/model_eval.py` (7 functions - in progress)
- [ ] Add docstrings to `src/data_loader.py` (3 functions - pending)
- [ ] All Python files follow PEP 8
- [ ] No typos in variable/function names

**Outputs:**
- ✅ `src/features.py` (cleaned + docstrings)
- 🔄 `src/model_eval.py` (docstrings in progress)
- ⏳ `src/data_loader.py` (pending)
- ⏳ Code review checklist

---

### **PHASE 2: Unit Tests & Validation (Week 1-2)**
**Goal:** Ensure code reliability  
**Acceptance Criteria:**
- [ ] Test coverage ≥ 80% for `src/features.py`
- [ ] Test coverage ≥ 70% for `src/model_eval.py`
- [ ] All edge cases covered (null values, empty data, etc.)
- [ ] Integration tests pass
- [ ] CI/CD pipeline set up (GitHub Actions or similar)

**Outputs:**
- `tests/test_features.py` (unit tests)
- `tests/test_model_eval.py` (unit tests)
- `tests/test_integration.py` (integration tests)
- `.github/workflows/tests.yml` (CI pipeline)
- Coverage report (≥80%)

---

### **PHASE 3: Metrics Visualization & Analysis (Week 2)**
**Goal:** Showcase model performance visually  
**Acceptance Criteria:**
- [ ] Profit Curve (threshold optimization)
- [ ] ROC Curve + AUC score
- [ ] Lift Curve (Fraud concentration)
- [ ] Feature Importance plot
- [ ] Profit comparison for all models (RF, XGBoost, LightGBM)
- [ ] Model comparison dashboard

**Outputs:**
- `notebooks/04_metrics_analysis.ipynb` (new)
- Metrics PNG/PDF files in `reports/figures/`
- Model comparison table in README

---

### **PHASE 4: Baseline Comparison & Results (Week 2-3)**
**Goal:** Quantify improvement over rule-based system  
**Acceptance Criteria:**
- [ ] Rule-based baseline model implemented
- [ ] Side-by-side metrics comparison
- [ ] Profit-curve ROI analysis documented using current audited threshold
- [ ] Cost-benefit analysis visualization, including threshold sensitivity
- [ ] Business impact summary

**Outputs:**
- `src/baseline_model.py` (rule-based implementation)
- `notebooks/05_baseline_comparison.ipynb` (analysis)
- Comparison metrics in `reports/`

---

### **PHASE 5: Model Deployment (Week 3-4)**
**Goal:** Production-ready API endpoint  
**Acceptance Criteria:**
- [ ] Flask/FastAPI server up and running
- [ ] Model loading from disk (joblib)
- [ ] Input validation & error handling
- [ ] Docker containerization
- [ ] API documentation (Swagger/OpenAPI)
- [ ] Deployment instructions in README

**Outputs:**
- `app/app.py` (Flask/FastAPI)
- `app/requirements.txt` (dependencies)
- `Dockerfile` & `docker-compose.yml`
- `app/README.md` (API documentation)

---

### **PHASE 6: README & Data Governance (Week 4)**
**Goal:** Professional documentation & transparency  
**Acceptance Criteria:**
- [ ] Complete README with all sections
- [ ] All notebook links functional
- [ ] Results/visualizations embedded
- [ ] Data disclosure: PaySim is synthetic (explain impact)
- [ ] Privacy statement & methodology
- [ ] Installation & usage instructions
- [ ] Contributing guidelines

**Outputs:**
- Updated `README.md` (comprehensive)
- `DATA_DICTIONARY.md` (feature descriptions)
- `METHODOLOGY.md` (ML approach explained)
- `DEPLOYMENT.md` (how to run in production)

---

## 📋 DETAILED TASK LIST

### **BATCH 1: Code Cleanup (Est. 2-3 hours)**
Priority: 🔴 **HIGH**
**Status: IN PROGRESS** ✅

1. **Task 1.1:** ✅ DONE - Verify all notebooks/imports use `build_features()` 
   - File: `src/features.py`
   - All notebooks refactored
   
2. **Task 1.2:** ✅ DONE - Add NumPy-style docstrings to `features.py` (2 functions)
   - File: `src/features.py`
   - Functions completed:
     * `build_features()` - Feature engineering with domain logic
     * `split_xy()` - Safe feature/target extraction with leakage guards
   - Typos fixed: "preproceseed" → "preprocessed", etc.
   
3. **Task 1.3:** 🔄 IN PROGRESS - Add NumPy-style docstrings to `model_eval.py` (7 functions)
   - File: `src/model_eval.py`
   - Functions to complete:
     * `calculate_ev()` - Expected value calculation
     * `get_friction_level()` - Friction decision stratification
     * `decision_loss()` - Cost-only evaluation matrix
     * `build_profit_curve()` - Profit curve by threshold
     * `find_best_threshold()` - Select optimal threshold
     * `build_roc_curve()` - ROC curve for monitoring
     * `build_lift_curve()` - Cumulative lift by decile
   
4. **Task 1.4:** ⏳ TODO - Add NumPy-style docstrings to `data_loader.py` (3 functions)
   - File: `src/data_loader.py`
   - Functions: `load_paysim_data()`, `get_sample_data()`, `get_sample_modeling()`
   
5. **Task 1.5:** ⏳ TODO - PEP 8 compliance check
   - Use `flake8 src/ --max-line-length=100`
   - Fix all formatting issues
   
**Definition of Done:**
- [x] `build_features()` docstring complete (NumPy style)
- [x] `split_xy()` docstring complete (NumPy style) 
- [ ] `model_eval.py` (7 functions) docstrings in progress
- [ ] `data_loader.py` (3 functions) docstrings pending
- [ ] No PEP 8 violations
- [ ] All typos fixed

---

### **BATCH 2: Unit Tests (Est. 4-6 hours)**
Priority: 🔴 **HIGH**

6. **Task 2.1:** Write unit tests for `features.py`
   - File: `tests/test_features.py`
   - Coverage: ≥80%
   - Test cases:
     * `build_features()` with normal data
     * `build_features()` with null values
     * `build_features()` with empty dataframe
     * `split_xy()` correct X/y separation
   
7. **Task 2.2:** Write unit tests for `model_eval.py`
   - File: `tests/test_model_eval.py`
   - Coverage: ≥70%
   - Test cases:
     * `calculate_ev()` logic
     * `get_friction_level()` all thresholds
     * Edge cases (prob=0, prob=1, etc.)
   
8. **Task 2.3:** Write integration tests
   - File: `tests/test_integration.py`
   - Test: Load data → Build features → Train model → Evaluate
   
9. **Task 2.4:** Set up CI/CD pipeline
   - File: `.github/workflows/tests.yml`
   - Run tests on: push to main, pull requests
   - Generate coverage report
   
**Definition of Done:**
- All tests passing locally
- Coverage ≥80% for `features.py`, ≥70% for `model_eval.py`
- CI pipeline configured & working
- Coverage badge in README

---

### **BATCH 3: Metrics & Visualization (Est. 3-4 hours)**
Priority: 🟠 **MEDIUM**

10. **Task 3.1:** Create metrics analysis notebook
    - File: `notebooks/04_metrics_analysis.ipynb`
    - Content:
      * Load trained LightGBM model
      * Generate predictions on test set
      * Plot Profit curve + Find best threshold
      * Plot Lift curve (Fraud concentration)
      * Plot ROC curve + calculate AUC
      * Summarize Decision 2345 Friction Levels (Cấp 0 - Cấp 4)
    
11. **Task 3.2:** Create model comparison notebook
    - File: (Add to `notebooks/03_modeling.ipynb` or separate)
    - Compare: Random Forest vs XGBoost vs LightGBM
    - Metrics table: Profit vs baseline, Alert Rate, ROC-AUC, AUC, AP
    - Feature importance comparison
    
12. **Task 3.3:** Save all visualizations
    - Files: `reports/figures/confusion_matrix.png`, `roc_curve.png`, etc.
    - High quality (300 DPI for prints)
    
**Definition of Done:**
- All visualizations created & saved
- Embedded in notebooks
- Added to README with descriptions

---

### **BATCH 4: Baseline Comparison (Est. 4-5 hours)**
Priority: 🟠 **MEDIUM**

13. **Task 4.1:** Implement rule-based baseline model
    - File: `src/baseline_model.py`
    - Rules:
      * Flag if `type` in ['TRANSFER', 'CASH_OUT']
      * Flag if `amount` > percentile 95%
      * Flag if `oldbalanceDest` == 0
      * Flag if `step % 24` in [23, 0, 1, 2, 3, 4]
    - Output: predictions + flagged percentages
    
14. **Task 4.2:** Baseline comparison analysis
    - File: `notebooks/05_baseline_comparison.ipynb`
    - Metrics: Precision, Recall, F1, Cost savings
    - Visualize: Side-by-side confusion matrices
    - Calculate: ROI using profit-curve threshold and cost-only matrix
    
15. **Task 4.3:** Document ROI calculations
    - File: `METHODOLOGY.md`
    - Explain: Cost matrix, CLV integration, EV formula
    - Show: Baseline cost vs ML model cost
    - Include: Double-counting guard for TP/FN cost-benefit logic
    
**Definition of Done:**
- Baseline model accuracy vs LightGBM documented
- Cost savings quantified & visualized
- ROI section in README

---

### **BATCH 5: Model Deployment (Est. 5-7 hours)**
Priority: 🔴 **HIGH**

16. **Task 5.1:** Create Flask/FastAPI app
    - File: `app/app.py`
    - Endpoints:
      * `POST /predict` - Single transaction prediction
      * `POST /predict_batch` - Batch predictions
      * `GET /health` - Health check
      * `GET /docs` - Swagger documentation
    - Input validation: JSON schema
    - Error handling: 400, 404, 500 responses
    
17. **Task 5.2:** Create model loader & inference pipeline
    - File: `app/model_inference.py`
    - Load trained model from `models/lightgbm_model.joblib`
    - Preprocess input (feature engineering)
    - Return prediction + probability + friction level
    
18. **Task 5.3:** Create Docker configuration
    - File: `Dockerfile`
    - File: `docker-compose.yml`
    - Base image: `python:3.10-slim`
    - Expose port: 5000 (Flask) or 8000 (FastAPI)
    
19. **Task 5.4:** API documentation
    - File: `app/README.md`
    - Include: Installation, usage, examples, troubleshooting
    - Swagger/OpenAPI spec
    
20. **Task 5.5:** Deployment guide
    - File: `DEPLOYMENT.md`
    - Local development: `python -m flask run`
    - Docker: `docker-compose up`
    - Production: AWS/Azure/GCP instructions
    
**Definition of Done:**
- API running locally
- All endpoints tested (curl/Postman)
- Docker image builds & runs
- API documentation complete

---

### **BATCH 6: README & Final Polish (Est. 3-4 hours)**
Priority: 🟠 **MEDIUM**

21. **Task 6.1:** Rewrite main README.md
    - Sections:
      * Overview + Business Problem
      * Key Results (ROC-AUC=0.9036, AP=0.3955, 1.52B VND saving vs rule)
      * Architecture diagram
      * Notebooks links (EDA, Feature Eng, Modeling, Metrics)
      * Quick start guide
      * Installation & Usage
      * Project structure explanation
    
22. **Task 6.2:** Create DATA_DICTIONARY.md
    - File: `DATA_DICTIONARY.md`
    - For each feature: Name, Type, Description, Range, Example
    - Note on synthetic data (PaySim)
    
23. **Task 6.3:** Create METHODOLOGY.md
    - File: `METHODOLOGY.md`
    - ML approach explanation
    - Feature engineering rationale
    - Model selection process
    - EV optimization framework
    - Regulatory compliance (Decision 2345)
    
24. **Task 6.4:** Data governance & privacy statement
    - File: `DATA_GOVERNANCE.md`
    - Statement: "PaySim is 100% synthetic data - no real transactions"
    - Impact: No privacy concerns, safe for public sharing
    - Source: Paysim-v2 (describe data generation process)
    
25. **Task 6.5:** Update all links & verify
    - File: README.md
    - Verify all notebook links work
    - Verify all file paths correct
    - Verify all images embedded
    
**Definition of Done:**
- README is comprehensive & professional
- All documentation complete
- All links functional
- Data governance explicit

---

## 🔄 WORKFLOW & DEPENDENCIES

```
BATCH 1 (Code Cleanup)
        ↓
BATCH 2 (Unit Tests)  ← Depends on BATCH 1
        ↓
BATCH 3 (Metrics)     ← Can run in parallel with BATCH 4
BATCH 4 (Baseline)    ← Can run in parallel with BATCH 3
        ↓
BATCH 5 (Deployment)  ← Depends on BATCH 1, 2
        ↓
BATCH 6 (README)      ← Depends on all above
```

---

## ⏱️ TIMELINE

| Phase | Batch | Duration | Start | End |
|-------|-------|----------|-------|-----|
| **Week 1** | 1, 2 | 5-9 hrs | Mon | Fri |
| **Week 2** | 3, 4 | 7-9 hrs | Mon | Fri |
| **Week 3** | 5 | 5-7 hrs | Mon | Fri |
| **Week 4** | 6 | 3-4 hrs | Mon | Wed |
| **Total** | - | **20-29 hrs** | - | - |

**Estimation:** 5 working days (8 hrs/day) for 1 person

---

## 🎯 KEY METRICS

### Before vs After

| Metric | Before | After | Target |
|--------|--------|-------|--------|
| README Score | 40% | 95% | ✅ |
| Test Coverage | 0% | 80%+ | ✅ |
| Documentation | 30% | 95% | ✅ |
| Visualizations | 50% | 100% | ✅ |
| Deployment Ready | ❌ | ✅ | ✅ |
| Portfolio Ready | ❌ | ✅ | ✅ |

---

## 📋 ACCEPTANCE CRITERIA

**Project is COMPLETE when:**
1. ✅ README is comprehensive & links to all notebooks
2. ✅ Unit tests cover 80%+ of features.py & 70%+ of model_eval.py
3. ✅ All metrics visualized (confusion matrix, ROC, PR curves)
4. ✅ Baseline comparison quantified with profit-curve optimized threshold
5. ✅ Flask/FastAPI API deployed & working
6. ✅ Docker image created & tested
7. ✅ Data governance statement included (synthetic data disclosure)
8. ✅ All code passes PEP 8 & has docstrings
9. ✅ CI/CD pipeline working
10. ✅ Project passes "portfolio review" (impressive for interviews)

---

## 🚀 SUCCESS LOOKS LIKE

- Hiring manager opens GitHub repo
- First impression: Professional, complete project
- Can quickly understand: Problem → Solution → Results
- All visualizations present & impressive
- Can run locally: `git clone → pip install → python app.py`
- API endpoint working: Can make predictions
- Clear quantified ROI: 1.52B VND saving vs rule baseline documented
- Data governance transparent: Explains synthetic data

---

## 📞 COMMUNICATION

**Slack Notification Format:**
```
🚀 BATCH [N]: [BATCH_NAME] - Est. [X-Y hours]
───────────────────────────────
✅ Task N.1: [Task Name]
✅ Task N.2: [Task Name]
✅ Task N.3: [Task Name]
───────────────────────────────
📝 Deliverables:
  • [File 1]
  • [File 2]
  
⏰ Due: [Date]
📊 Success Criteria: [Brief list]
```

---

## 🔗 REFERENCES

**Related Documentation:**
- Original README.md
- notebooks/01_eda.ipynb
- notebooks/02_feature_eng.ipynb
- notebooks/03_modeling.ipynb
- src/features.py
- src/model_eval.py


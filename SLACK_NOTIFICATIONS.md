# 📱 SLACK NOTIFICATION TEMPLATES

## Hướng Dẫn Sử Dụng
1. Copy message từ batch tương ứng
2. Paste vào Slack channel
3. Update status khi hoàn thành task

---

# 🚀 BATCH 1: Code Cleanup (Est. 2-3 hours)
**Priority:** 🔴 HIGH  
**Deadline:** [TODAY]

```
🚀 BATCH 1: Code Cleanup & Fixes - Est. 2-3 hours
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⬜ Task 1.1: Verify all notebooks/imports use build_features()
   File: src/features.py
   Impact: Prevents import errors & improves code clarity

⬜ Task 1.2: Add NumPy docstrings to features.py
   File: src/features.py
   Requirements: Description, Parameters, Returns, Example for ALL functions

⬜ Task 1.3: Add NumPy docstrings to model_eval.py  
   File: src/model_eval.py
   Requirements: Complete docstring coverage

⬜ Task 1.4: Add NumPy docstrings to data_loader.py
   File: src/data_loader.py
   Requirements: Complete docstring coverage

⬜ Task 1.5: PEP 8 Compliance Check
   Tools: flake8 or pylint
   Command: flake8 src/ --max-line-length=100
   Fix all violations

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📝 Deliverables:
  • src/features.py (cleaned + docstrings)
  • src/model_eval.py (cleaned + docstrings)
  • src/data_loader.py (cleaned + docstrings)
  • Flake8 validation report (0 errors)

✅ Definition of Done:
  ☐ No typos in function/variable names
  ☐ All functions have complete docstrings
  ☐ PEP 8 compliance: 0 violations
  ☐ Code passes flake8 validation
  ☐ Ready for unit testing (BATCH 2)

⏰ Due: [DATE] | Estimated: 2-3 hours
```

---

# 🚀 BATCH 2: Unit Tests & Validation (Est. 4-6 hours)
**Priority:** 🔴 HIGH  
**Deadline:** [DATE]
**Depends On:** BATCH 1 ✅

```
🚀 BATCH 2: Unit Tests & Validation - Est. 4-6 hours
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⬜ Task 2.1: Write unit tests for features.py
   File: tests/test_features.py (NEW)
   Coverage Target: ≥80%
   Test Cases:
     • build_features() with normal data
     • build_features() with null/NaN values
     • build_features() with empty dataframe
     • split_xy() correct separation
     • Edge case: single row, missing columns

⬜ Task 2.2: Write unit tests for model_eval.py
   File: tests/test_model_eval.py (NEW)
   Coverage Target: ≥70%
   Test Cases:
     • calculate_ev() with various inputs
     • get_friction_level() all thresholds (0, 0.2, 0.5, 0.8, 0.95)
     • Edge cases: prob=0, prob=1, extreme values

⬜ Task 2.3: Write integration tests
   File: tests/test_integration.py (NEW)
   Test: Load data → Build features → Validate output
   Scope: Full pipeline validation

⬜ Task 2.4: Set up CI/CD Pipeline
   File: .github/workflows/tests.yml (NEW)
   Triggers: Push to main, Pull requests
   Commands:
     • pytest tests/ --cov=src/ --cov-report=html
     • Generate coverage badge

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📝 Deliverables:
  • tests/test_features.py (80%+ coverage)
  • tests/test_model_eval.py (70%+ coverage)
  • tests/test_integration.py (all passing)
  • .github/workflows/tests.yml (CI configured)
  • Coverage report (HTML + badge)

✅ Definition of Done:
  ☐ All tests passing locally: pytest tests/
  ☐ Coverage report generated (80% features, 70% model_eval)
  ☐ CI pipeline working (GitHub Actions)
  ☐ Coverage badge in README
  ☐ No regressions from BATCH 1

⏰ Due: [DATE] | Estimated: 4-6 hours
```

---

# 🚀 BATCH 3: Metrics & Visualization (Est. 3-4 hours)
**Priority:** 🟠 MEDIUM  
**Deadline:** [DATE]
**Can Run In Parallel With:** BATCH 4

```
🚀 BATCH 3: Metrics Analysis & Visualization - Est. 3-4 hours
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⬜ Task 3.1: Create metrics analysis notebook
   File: notebooks/04_metrics_analysis.ipynb (NEW)
   Content:
     • Load trained LightGBM model from models/
     • Generate predictions on test set
     • Plot Profit Curve + find optimal threshold
     • Plot Lift Curve (Fraud concentration)
     • Plot ROC Curve + calculate AUC score
     • Calculate Decision 2345 Friction Level distributions (Cấp 0 - Cấp 4)

⬜ Task 3.2: Create model comparison notebook
   File: notebooks/03_modeling.ipynb (ADD SECTION) or new notebook
   Content:
     • Compare 3 models: Random Forest, XGBoost, LightGBM
     • Metrics table: Profit vs baseline, Alert Rate, ROC-AUC, AUC, AP
     • Feature importance comparison (bar plot)
     • Model training time comparison

⬜ Task 3.3: Save all visualizations to reports/
   Files (HIGH QUALITY - 300 DPI):
     • reports/figures/profit_curve.png
     • reports/figures/lift_curve.png
     • reports/figures/roc_curve_lightgbm.png
     • reports/figures/feature_importance.png
     • reports/figures/model_comparison.png

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📝 Deliverables:
  • notebooks/04_metrics_analysis.ipynb
  • Updated notebooks/03_modeling.ipynb (comparison section)
  • 5+ visualization PNG files in reports/figures/
  • Metrics summary table (Markdown format)

✅ Definition of Done:
  ☐ All visualizations created & saved (300 DPI)
  ☐ Metrics clearly labeled on plots
  ☐ Notebook executes without errors
  ☐ Visualizations embedded in notebooks
  ☐ Ready to embed in README

⏰ Due: [DATE] | Estimated: 3-4 hours
```

---

# 🚀 BATCH 4: Baseline Comparison (Est. 4-5 hours)
**Priority:** 🟠 MEDIUM  
**Deadline:** [DATE]
**Can Run In Parallel With:** BATCH 3

```
🚀 BATCH 4: Baseline Comparison & ROI Analysis - Est. 4-5 hours
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⬜ Task 4.1: Implement rule-based baseline model
   File: src/baseline_model.py (NEW)
   Rules:
     • Flag if type in ['TRANSFER', 'CASH_OUT']
     • Flag if amount > 95th percentile
     • Flag if oldbalanceDest == 0
     • Flag if hour (step % 24) in [23, 0, 1, 2, 3, 4]
   
   Output Format:
     • predict() returns binary predictions
     • Metrics: precision, recall, F1, cost of false positives

⬜ Task 4.2: Baseline comparison analysis
   File: notebooks/05_baseline_comparison.ipynb (NEW)
   Analysis:
     • Load baseline model predictions
     • Load LightGBM predictions
     • Side-by-side metrics: Precision, Recall, F1, Cost
     • Confusion matrix comparison (2 matrices side-by-side)
     • Scatter plot: FPR vs TPR for both models
     • Cost comparison: Baseline cost vs ML cost

⬜ Task 4.3: Document ROI & savings
   File: METHODOLOGY.md (ADD SECTION)
   Content:
     • Cost matrix explanation (Cost False Positive = 50K + CLV impact)
     • Expected Value formula: EV = P(fraud)*amount - (1-P(fraud))*cost
     • Baseline cost calculation: ~2.3B VND
     • ML model cost: ~400M VND (estimated from test set)
  • Savings: 1.52B VND (22.73% vs rule baseline) ← AUDITED

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📝 Deliverables:
  • src/baseline_model.py (working baseline)
  • notebooks/05_baseline_comparison.ipynb (analysis)
  • METHODOLOGY.md section (EV framework explained)
  • Cost comparison visualization

✅ Definition of Done:
  ☐ Baseline model: precision, recall, F1 calculated
  ☐ LightGBM model: same metrics calculated
  ☐ Comparison table created: Baseline vs LightGBM
☐ Cost savings quantified & documented with profit-curve threshold
  ☐ ROI section in README updated with numbers
  ☐ Visualizations clear & professional

⏰ Due: [DATE] | Estimated: 4-5 hours
```

---

# 🚀 BATCH 5: Model Deployment (Est. 5-7 hours)
**Priority:** 🔴 HIGH  
**Deadline:** [DATE]
**Depends On:** BATCH 1, 2 ✅

```
🚀 BATCH 5: Flask API & Docker Deployment - Est. 5-7 hours
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⬜ Task 5.1: Create Flask/FastAPI application
   File: app/app.py (NEW)
   Endpoints:
     • POST /predict
       Input: JSON with transaction details
       Output: prediction, probability, friction_level
     
     • POST /predict_batch
       Input: JSON array of transactions
       Output: Array of predictions
     
     • GET /health
       Output: {"status": "healthy"}
     
     • GET /docs
       Output: Swagger/OpenAPI documentation
   
   Validations:
     • Input JSON schema validation
     • Error handling: 400 (bad request), 404 (not found), 500 (server error)
     • Logging: All predictions logged

⬜ Task 5.2: Model loading & inference pipeline
   File: app/model_inference.py (NEW)
   Components:
     • Load saved model from models/lightgbm_model.joblib
     • Input preprocessing: Apply same feature engineering as training
     • Prediction: Get probability from model
     • Output: prediction + friction_level from calculate_ev()
   
   Function Signature:
     def predict_transaction(transaction_dict) → dict
     Returns: {"prediction": 0/1, "probability": 0.85, "friction_level": "Level 2"}

⬜ Task 5.3: Create Docker configuration
   File: Dockerfile (NEW)
   File: docker-compose.yml (NEW)
   
   Dockerfile:
     • Base image: python:3.10-slim
     • Copy app + models + requirements.txt
     • Install dependencies: pip install -r requirements.txt
     • Expose port: 5000 (Flask) or 8000 (FastAPI)
     • CMD: python app/app.py
   
   Docker Compose:
     • Service: fraud-detection-api
     • Port mapping: 5000:5000
     • Volume: models/ directory mounted

⬜ Task 5.4: API documentation
   File: app/README_API.md (NEW)
   Content:
     • Installation: pip install -r requirements.txt
     • Running locally: python -m flask run
     • Running Docker: docker-compose up
     • API examples: curl commands for each endpoint
     • Response format: JSON examples
     • Error responses: Error codes & messages

⬜ Task 5.5: Deployment guide
   File: DEPLOYMENT.md (NEW)
   Sections:
     • Local development setup
     • Docker image building & running
     • Production deployment (AWS/Azure tips)
     • Environment variables (if any)
     • Monitoring & logging
     • Troubleshooting

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📝 Deliverables:
  • app/app.py (Flask/FastAPI application)
  • app/model_inference.py (inference logic)
  • app/requirements.txt (dependencies)
  • Dockerfile (containerization)
  • docker-compose.yml (orchestration)
  • app/README_API.md (API documentation)
  • DEPLOYMENT.md (deployment guide)

✅ Definition of Done:
  ☐ Flask/FastAPI running locally without errors
  ☐ All 4 endpoints working (tested with curl/Postman)
  ☐ Input validation working (rejects invalid JSON)
  ☐ Model predictions returning correct format
  ☐ Docker image builds: docker build -t fraud-detection .
  ☐ Docker container runs: docker-compose up
  ☐ API responds to requests inside container
  ☐ Swagger documentation accessible at /docs
  ☐ No hardcoded paths (uses relative/env paths)

⏰ Due: [DATE] | Estimated: 5-7 hours
```

---

# 🚀 BATCH 6: README & Final Polish (Est. 3-4 hours)
**Priority:** 🟠 MEDIUM  
**Deadline:** [DATE]
**Depends On:** All previous batches ✅

```
🚀 BATCH 6: README & Documentation Polish - Est. 3-4 hours
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⬜ Task 6.1: Rewrite main README.md
   File: README.md (COMPLETE OVERHAUL)
   
   Sections (in order):
     1. Project Title & Badge (test coverage, build status)
     2. 📋 Overview (1-2 paragraphs, business problem)
3. 🎯 Key Results (ROC-AUC=0.9036, AP=0.3955, 1.52B VND saving)
     4. 🏗️ Architecture (diagram or text description)
     5. 📚 Project Structure (folder explanation)
     6. 🚀 Quick Start (git clone → pip install → python)
     7. 📖 Notebooks (links to EDA, Feature Eng, Modeling, Metrics)
     8. 🔌 API Usage (GET /health, POST /predict examples)
     9. 🐳 Docker (docker-compose up instructions)
     10. 📊 Results (embed visualizations: profit curve, ROC curve)
     11. 📈 Comparison (Baseline vs ML model metrics table)
     12. 🛠️ Installation (pip install -r requirements.txt)
     13. 🧪 Testing (pytest tests/ coverage report)
     14. 📄 Data Governance (synthetic data disclosure)
     15. 📚 More Info (links to DATA_DICTIONARY, METHODOLOGY, DEPLOYMENT)
     16. 👨‍💼 Author & License

⬜ Task 6.2: Create DATA_DICTIONARY.md
   File: DATA_DICTIONARY.md (NEW)
   
   Format: Table for each feature
   | Feature | Type | Description | Range | Example |
   |---------|------|-------------|-------|---------|
   | step | int | Time step (hours) | 0-743 | 12 |
   | amount | float | Transaction amount (VND) | 0-6B | 500,000 |
   | [all other features] | | | | |
   
   Include: isFraud target variable, generated features (hour, is_night, etc.)
   Note: All data from PaySim (synthetic)

⬜ Task 6.3: Create METHODOLOGY.md
   File: METHODOLOGY.md (NEW)
   
   Sections:
     1. Problem Statement (fraud detection on 6.3M transactions)
     2. Data Source (PaySim: synthetic, Paysim-v2)
     3. Feature Engineering (Account Depletion, Temporal, Logic features)
     4. Model Selection (RF → XGBoost → LightGBM)
     5. Expected Value Framework:
        - Cost matrix explanation
        - EV formula: EV = P(fraud)*amount - (1-P(fraud))*cost
        - Threshold optimization
     6. Regulatory Compliance (Decision 2345/QĐ-NHNN, 10M threshold)
7. Results & Performance (LightGBM: ROC-AUC=0.9036, AP=0.3955)
8. ROI Analysis (profit-curve threshold, 1.52B VND saving)

⬜ Task 6.4: Create DATA_GOVERNANCE.md
   File: DATA_GOVERNANCE.md (NEW)
   
   Content:
     • 🔐 Data Source: PaySim synthetic dataset (100% simulated)
     • 📋 No Real Data: All transactions are computer-generated
     • ✅ Privacy Compliant: GDPR/PDPA compliant (no real PII)
     • 🔬 Generation Method: Agent-based simulation
     • 📊 Characteristics: Mirrors real payment patterns
     • 🚀 Implications: Safe for public sharing, academic use, portfolio

⬜ Task 6.5: Final link & verification
   File: README.md (VERIFY ALL LINKS)
   
   Checklist:
     ☐ All notebook links work (notebooks/01_eda.ipynb, etc.)
     ☐ All image paths correct (reports/figures/[name].png)
     ☐ All file links valid (src/, models/, app/)
     ☐ Badge URLs correct (coverage, build, etc.)
     ☐ API example commands copy-paste ready
     ☐ No broken markdown links [text](path)
     ☐ All headers properly formatted (#, ##, ###)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📝 Deliverables:
  • README.md (comprehensive, professional, ≥95% quality)
  • DATA_DICTIONARY.md (all features documented)
  • METHODOLOGY.md (ML approach explained)
  • DATA_GOVERNANCE.md (synthetic data disclosure)
  • All links verified & working

✅ Definition of Done:
  ☐ README reads like professional project
  ☐ Someone can understand project in 5 minutes
  ☐ All visualizations embedded & display correctly
  ☐ All notebook links functional
  ☐ Data governance transparent & clear
  ☐ Code examples (curl, Docker) are tested & working
  ☐ No typos or broken links
  ☐ Project passes "GitHub portfolio review"

⏰ Due: [DATE] | Estimated: 3-4 hours
```

---

# 📊 OVERALL PROGRESS TRACKING

```
BATCH 1 (Code Cleanup):           ⬜⬜⬜⬜⬜ [5 tasks]
BATCH 2 (Unit Tests):             ⬜⬜⬜⬜ [4 tasks]
BATCH 3 (Metrics):                ⬜⬜⬜ [3 tasks]
BATCH 4 (Baseline):               ⬜⬜⬜ [3 tasks]
BATCH 5 (Deployment):             ⬜⬜⬜⬜⬜ [5 tasks]
BATCH 6 (Documentation):          ⬜⬜⬜⬜⬜ [5 tasks]

Total: 25 tasks across 6 batches
Estimated Total: 20-29 hours (5 days of focused work)
```

---

# 🎯 KEY CHECKPOINTS

**After BATCH 1:** ✅ Code is clean & professional  
**After BATCH 2:** ✅ Code is tested & reliable  
**After BATCH 3:** ✅ Results are visualized & impressive  
**After BATCH 4:** ✅ Business value is quantified  
**After BATCH 5:** ✅ Project is deployable  
**After BATCH 6:** ✅ Project is portfolio-ready  

---

# 💡 TIPS FOR SUCCESS

1. **Batch 1 is critical** - Clean code first, test later
2. **Batches 3 & 4 can run in parallel** - No dependencies
3. **Batch 5 can start after Batch 2** - Don't wait for others
4. **Batch 6 is final polish** - Leave it for last
5. **Test locally before moving to next batch** - Prevent rework

---

**Questions?** Check PRD.md for detailed requirements.  
**Ready to start?** Begin with BATCH 1 - Code Cleanup!

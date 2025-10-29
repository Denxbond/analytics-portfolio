# Analytics Portfolio

This repository collects portfolio-ready case studies that showcase product analytics, conversion rate optimization, and lifecycle analysis skills.  

---

## TL;DR
- Clone the repo and open a case study folder to explore the business context, dataset, and analysis assets.  
- Install required Python libraries (e.g. `pandas`, `matplotlib`, `seaborn`) to reproduce results.  
- Use SQL and Python scripts to replicate KPIs, conversion funnels, or retention curves with your own anonymized data.  

---

## Projects
- [Funnel Optimization Case Study](funnel_optimization_case/README.md):  
  Reg→Dep funnel analysis with SQL, Python, and an experiment playbook.

- [Retention Cohort Dashboard](retention_cohort_dashboard/README.md):  
  Weekly cohort retention heatmap built from synthetic lifecycle events.

---

## Getting Started
Each project contains:
- Synthetic datasets for reproducibility  
- Clean, modular analysis code  
- A clear documentation trail explaining context, metrics, and methodology  

To reproduce locally:
```bash
git clone git@github.com:Denxbond/analytics-portfolio.git
cd analytics-portfolio
python3 -m pip install -r requirements.txt  # or install libs manually

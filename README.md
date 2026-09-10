# 🛡️ Third-Party Risk Management (TPRM) Tool

This repository showcases a full-cycle GRC (Governance, Risk, and Compliance) automation project. It includes a functional vendor scoring tool, a formal security policy, and an automated audit trail.

## 📂 Project Navigation
*   **[Security Policy](./POLICY.md):** Defines the "Governance" and scoring weights used for assessments.
*   **[Scoring Tool](./score_vendor.py):** The Python-based "Risk Management" tool used to evaluate vendors.
*   **[Risk Register](./risk_register.csv):** The "Compliance" evidence and historical audit log.

---

## 🚀 How it Works
The tool automates vendor onboarding by evaluating three critical security controls:
1.  **MFA Implementation** (Weighted 40%)
2.  **Data Encryption** (Weighted 40%)
3.  **SOC 2 Compliance** (Weighted 20%)

### 🛠️ Execution Example
Testing was performed in a sandboxed **Virtual Machine environment** to ensure data integrity and secure execution.

![Assessment Demo](./assessment_demo.jpg)

---

## 📈 Key GRC Skills Demonstrated
*   **Governance:** Developing formal security policies and approval thresholds.
*   **Risk Management:** Quantifying risk using weighted scoring models.
*   **Compliance Automation:** Generating immutable audit logs (CSV) with automated timestamps.
*   **Technical Literacy:** Python scripting and version control (GitHub).

---

## 📊 Relational Database Audit Engine (SQL Extension)
To scale this third-party assessment framework for enterprise-level auditing, a relational data layer has been integrated into the tool. This database module isolates risk tier density, maps systematically non-compliant services, and flags SLA breaches across critical vendor relationships.

### 🛠️ Database Tech Stack & Control Mapping
* **SQL Engine:** SQLite / ANSI SQL
* **Auditing Tooling:** DBeaver Community Edition
* **Compliance Mapping:** SOC 2 Type II Trust Services Criteria (CC9.2 - Risk Assessment & Vendor Governance)

### 🔍 Production Audit Metrics Implemented
1. **Risk Tier Density Distribution:** Leveraging `GROUP BY` and aggregate `COUNT(*)` functions to automatically sort and rank operational vendor distributions across threat profiles (Critical to Low).
2. **Systemic Security Gap Aggregations:** Combining row-level filtering (`WHERE`) with category grouping to isolate the exact operational areas (e.g., Cloud Hosting) harboring active failed or unverified security postures.
3. **Operational SLA Failure Engine:** Isolating systemic supplier underperformance by combining `GROUP BY`, `SUM()`, and post-aggregation `HAVING` filters to flag clusters generating critical delivery bottlenecks.

## 📊 Executive Visualization Engine

To bridge rigorous relational backend audit tracking with executive-level corporate reporting, this asset utilizes an interactive web analytics layer. The pipeline extracts real-time, aggregated data payloads straight from our auditing tables and compiles them into a high-visibility security profile metrics layout.

![Vendor Risk Distribution Chart](vendor-risk-distribution-chart.png)

### 📈 Metrics Compilation & Core Data Pipeline Logic
The metrics engine utilizes a Python-backed analytical runtime executing standard ANSI-SQL queries against the underlying database schemas. Data density counts are compiled natively using relational aggregations to calculate risk concentrations without structural performance overhead.

#### Executed Relational Database Query Architecture:
```sql
SELECT 
    risk_tier, 
    COUNT(*) AS total_vendors
FROM 
    vendor_assessments
GROUP BY 
    risk_tier
ORDER BY 
    total_vendors DESC;
```

---

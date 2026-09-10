# Third-Party Risk Management (TPRM) Policy

## 1. Objective
This policy defines the scoring criteria used by the `vendor-risk-tool` to ensure consistent security evaluations of all third-party SaaS providers.

## 2. Risk Weighting Criteria
To protect company data, we prioritize controls based on the **CIA Triad** (Confidentiality, Integrity, and Availability):


| Control Item | Weight | Justification |
| :--- | :--- | :--- |
| **Multi-Factor Authentication (MFA)** | 40% | Essential for preventing unauthorized access. |
| **Data Encryption at Rest** | 40% | Critical for maintaining data confidentiality. |
| **SOC 2 Type II / ISO 27001** | 20% | Independent verification of security effectiveness. |

## 3. Approval Thresholds
*   **Low Risk (80-100):** Automatic approval for onboarding.
*   **Medium Risk (70-79):** Requires GRC Manager review.
*   **High Risk (<70):** Rejected until remediation evidence is provided.

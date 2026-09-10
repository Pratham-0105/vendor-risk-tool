-- ==========================================
-- 1. CURRENT EXERCISE: FILTERED & PERCENTAGE METRICS
-- ==========================================
CREATE VIEW v_vendor_risk_summary AS
SELECT 
    CASE 
        WHEN soc2_status = 'Non-Compliant' THEN 'High Risk Group'
        WHEN soc2_status = 'Under Review' THEN 'Medium Risk Group'
        ELSE 'Low Risk Group (Compliant)'
    END AS vendor_risk_group,
    
    COUNT(*) AS total_vendors,
    SUM(sla_breaches_count) AS total_group_breaches,
    
    -- New percentage calculation column
    ROUND(
        (SUM(sla_breaches_count) * 100.0) / (SELECT SUM(sla_breaches_count) FROM vendor_compliance_logs), 
        1
    ) || '%' AS breach_percentage

FROM vendor_compliance_logs

GROUP BY vendor_risk_group
HAVING COUNT(*) > 2
ORDER BY total_group_breaches DESC;
SELECT * FROM v_vendor_risk_summary;


-- Finding specific vendors causing excessive risk anomalies
SELECT 
    vendor_name,
    soc2_status,
    sla_breaches_count,
    
    -- Subquery calculating the average breaches for that specific status group
    (SELECT ROUND(AVG(sub.sla_breaches_count), 1) 
     FROM vendor_compliance_logs sub 
     WHERE sub.soc2_status = main.soc2_status) AS group_average_breaches

FROM vendor_compliance_logs main

-- Only display vendors performing worse than their group's average
WHERE sla_breaches_count > group_average_breaches
ORDER BY sla_breaches_count DESC;

-- ==========================================
-- 3. CURRENT EXERCISE: MULTI-TABLE JOIN
-- ==========================================

-- Create a separate lookup directory for vendor team contacts
CREATE TABLE IF NOT EXISTS vendor_contacts (
    vendor_name TEXT UNIQUE,
    contact_email TEXT,
    owner_department TEXT
);

-- Populate contact data matching your existing vendor logs
INSERT OR IGNORE INTO vendor_contacts (vendor_name, contact_email, owner_department) VALUES
('SecureAuth Ltd', 'security@secureauth.com', 'InfoSec'),
('FinPay Corp', 'compliance@finpay.io', 'Finance Ops'),
('StripeWay', 'api-team@stripeway.com', 'Engineering'),
('DataGuard Inc', 'privacy@dataguard.net', 'Legal');


-- Relational JOIN: Combining risk logs with contact information
SELECT 
    logs.vendor_name,
    logs.soc2_status,
    logs.sla_breaches_count,
    contacts.contact_email,
    contacts.owner_department

FROM vendor_compliance_logs logs
INNER JOIN vendor_contacts contacts 
    ON logs.vendor_name = contacts.vendor_name

ORDER BY logs.sla_breaches_count DESC;



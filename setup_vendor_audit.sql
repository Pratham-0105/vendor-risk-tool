CREATE TABLE vendor_compliance_logs (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    vendor_name TEXT NOT NULL,
    service_type TEXT,
    risk_tier TEXT,
    soc2_status TEXT,
    sla_breaches_count INTEGER DEFAULT 0,
    last_audit_date DATE
);

INSERT INTO vendor_compliance_logs (vendor_name, service_type, risk_tier, soc2_status, sla_breaches_count, last_audit_date) VALUES
('ApexCloud', 'Cloud Hosting', 'Critical', 'Compliant', 0, '2026-01-15'),
('StripeWay', 'Payment Gateway', 'Critical', 'Compliant', 1, '2026-02-10'),
('DataSync Pro', 'SaaS CRM', 'High', 'Non-Compliant', 4, '2026-03-01'),
('OmniSupport', 'IT Support', 'Medium', 'Under Review', 2, '2026-04-12'),
('LogiTrack', 'SaaS CRM', 'Medium', 'Compliant', 0, '2026-01-22'),
('SecureAuth Ltd', 'Cloud Hosting', 'Critical', 'Non-Compliant', 5, '2026-05-02'),
('FinPay Corp', 'Payment Gateway', 'Critical', 'Under Review', 3, '2026-05-10'),
('NetFlow Solutions', 'IT Support', 'Low', 'Compliant', 0, '2025-12-18'),
('CloudScale', 'Cloud Hosting', 'High', 'Non-Compliant', 3, '2026-02-28');

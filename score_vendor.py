import csv
import os

def save_to_register(vendor, score, tier):
    file_exists = os.path.isfile('risk_register.csv')
    
    with open('risk_register.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        # Add headers only if the file is new
        if not file_exists:
            writer.writerow(['Vendor Name', 'Security Score', 'Risk Tier'])
        
        writer.writerow([vendor, score, tier])
    print(f"💾 Results saved to risk_register.csv")

def run_assessment():
    print("--- 🛡️ Vendor Security Risk Calculator ---")
    vendor_name = input("Enter Vendor Name: ")
    score = 100
    
    mfa = input("Is MFA enabled? (y/n): ").lower()
    encryption = input("Is Data Encrypted at rest? (y/n): ").lower()
    soc2 = input("Do they have a SOC2 Type II report? (y/n): ").lower()

    if mfa != 'y': score -= 40
    if encryption != 'y': score -= 40
    if soc2 != 'y': score -= 20

    if score < 70:
        tier = "HIGH RISK"
    else:
        tier = "LOW RISK"

    print(f"\n--- Assessment for {vendor_name} ---")
    print(f"Final Security Score: {score}")
    print(f"RESULT: {tier}")

    # NEW: Save the data
    save_to_register(vendor_name, score, tier)

if __name__ == "__main__":
    run_assessment()

import csv

SAMPLE = [
    # --- LEGITIMATE (HAM) ---
    ("Dear user, your account needs verification. Click http://192.168.0.1/verify to confirm.", 1),
    ("Your bank account was accessed. Verify your password at http://secure-bank.example.com/login", 1),
    ("Hi team, the meeting is at 3pm. See agenda here: https://example.com/agenda", 0),
    ("Please review the attached invoice.", 0),
    ("URGENT: Your payment failed. Update payment at http://pay-example.com/secure", 1),
    ("Monthly newsletter: tips and updates", 0),
    ("Confirm your subscription by clicking http://example.com/confirm", 0),
    ("Reset your password immediately: http://10.0.0.2/reset@malicious.com", 1),
    ("Meeting notes from today's discussion attached.", 0),
    ("Project deadline is next week Friday.", 0),
    ("Can you send me the report by EOD?", 0),
    ("Join us for the team lunch tomorrow.", 0),
    ("Your Amazon order #12345 has shipped.", 0),
    ("Utility bill for March is due.", 0),
    ("Class schedule for next semester is updated.", 0),
    ("Internship application status: Under review.", 0),
    ("Welcome to the team!", 0),
    ("VNRVJIET: Circular regarding upcoming exams.", 0),
    
    # --- SCAM (User Reported & Variations) ---
    # 1. Final Notice / Edulet Scam
    ("""Dear Student of VNRVJIET
    As part of our upcoming academic schedule, we are pleased to announce the Industrial Training 2025 at Unlox Academy...
    Apply Now - Final Call https://forms.gle/Ks6cqDUSZ6AcSokC8""", 1),
    ("Final Notice: Your Smart Edulet Tablet is ready for dispatch. Fill form now.", 1),
    ("Unlox Academy Industrial Training approved by Ministry of Electronics.", 1),
    ("Apply Now for 2025 Industrial Training with NASSCOM approval.", 1),
    ("Your tablet has been dispatched. Track here: bit.ly/fake", 1),

    # 2. Capgemini / Internship Scam
    ("""We are pleased to announce an exclusive Capgemini–Aligned Stipend-Based Verified Internship...
    Registration Link: https://forms.gle/Enkipa8hydy3BhWp8
    Referral Code (40% Scholarship): CAP26""", 1),
    ("Capgemini Internship Program 2026 - Apply Now!", 1),
    ("Stipend-based internship with Inspire Leap Pvt Ltd.", 1),
    ("Pay registration fee for Capgemini training program.", 1),
    ("Exclusive placement readiness program for VNRVJIET students.", 1),
    ("Referral Code CAP26 for 40% scholarship on training fee.", 1),

    # 3. Aenexz / Vel Tech Scam
    ("""Aenexz Tech is excited to introduce the Stipend-Based Online Training & Internship Program 2026...
    Registration Form: https://forms.gle/Registration-form
    All certificates are AICTE, ISO, and MSME recognized.""", 1),
    ("VNR VJIET – Skill Development & Stipend-Based Online Training.", 1),
    ("Internship with leading MNCs like IBM, Microsoft, and Wipro.", 1),
    ("Mandatory to fill this form to receive official updates: forms.gle/Registration-form", 1),
    ("Performance-based stipend: ₹15,000 – ₹25,000. Registration Form.", 1),

    # 4. Generic variations
    ("Urgent: Verify your account immediately to avoid suspension.", 1),
    ("You have won a lottery! Claim your prize now.", 1),
    ("Government subsidy approved. Click to claim funds.", 1),
    ("Part-time job offer: Earn 5000/day working from home.", 1),
    ("Your parcel is on hold. Pay shipping fee to release.", 1)
]


def generate(path='sample_data.csv'):
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['text','label'])
        for t,l in SAMPLE:
            writer.writerow([t,l])
    print(f'Wrote {len(SAMPLE)} examples to {path}')


if __name__ == '__main__':
    generate()

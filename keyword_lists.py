"""
Universal Fraud Detection Keyword Lists
Designed for multi-domain users:
Students, Parents, Professionals, Businesses, Seniors
"""

# =====================================================
# SPAM KEYWORDS (Fraud Intention & Manipulation Words)
# =====================================================

RAW_SPAM = [

    # ----------------------------
    # URGENCY / PRESSURE TACTICS
    # ----------------------------
    "urgent",
    "immediate",
    "immediately",
    "final notice",
    "last chance",
    "act now",
    "limited time",
    "limited offer",
    "exclusive offer",
    "mandatory action",
    "verify immediately",
    "account blocked",
    "account suspended",
    "action required",

    # ----------------------------
    # FINANCIAL LURE / GREED
    # ----------------------------
    "winner",
    "lottery",
    "jackpot",
    "prize",
    "bonus",
    "reward",
    "cash",
    "earn money",
    "income",
    "profit",
    "guaranteed profit",
    "risk free",
    "double your money",
    "refund",
    "claim now",
    "free gift",
    "free money",

    # ----------------------------
    # BANKING / PHISHING
    # ----------------------------
    "verify account",
    "login now",
    "update details",
    "reset password",
    "confirm account",
    "unauthorized access",
    "security alert",
    "bank account",
    "upi",
    "atm",
    "credit card",
    "debit card",
    "kyc",
    "otp",
    "transaction failed",
    "click link",
    "click here",

    # ----------------------------
    # LOAN / DEBT SCAMS
    # ----------------------------
    "instant loan",
    "quick loan",
    "low interest",
    "loan approval",
    "pre-approved",
    "no cibil",
    "no collateral",

    # ----------------------------
    # CRYPTO / INVESTMENT SCAMS
    # ----------------------------
    "bitcoin",
    "crypto",
    "investment plan",
    "trading opportunity",
    "forex",
    "mining",
    "high return",
    "roi",
    "crypto wallet",

    # ----------------------------
    # JOB / INTERNSHIP SCAMS
    # ----------------------------
    "internship program",
    "training program",
    "placement assistance",
    "hr team",
    "shortlisted",
    "certificate provided",
    "registration fee",
    "apply now",
    "google form",
    "selection process",

    # ----------------------------
    # DELIVERY / PARCEL SCAMS
    # ----------------------------
    "parcel on hold",
    "delivery failed",
    "customs clearance",
    "shipping charge",
    "track your package",

    # ----------------------------
    # ROMANCE / SOCIAL SCAMS
    # ----------------------------
    "i love you",
    "send money",
    "gift card",
    "western union",
    "emergency funds",

    # ----------------------------
    # GOVERNMENT / SUBSIDY FAKE
    # ----------------------------
    "government scheme",
    "subsidy",
    "grant approved",
    "benefit transfer",
    "relief fund",

    # ----------------------------
    # TECH SUPPORT SCAM
    # ----------------------------
    "virus detected",
    "technical support",
    "call immediately",
    "remote access",
    "system infected",
]

# =====================================================
# HAM KEYWORDS (Legitimate Institutional Language)
# =====================================================

RAW_HAM = [

    # ----------------------------
    # EDUCATION / STUDENT EMAILS
    # ----------------------------
    "students",
    "scholarship",
    "biometric",
    "semester",
    "academic",
    "university",
    "college",
    "department",
    "faculty",
    "principal",
    "exam",
    "attendance",
    "hall ticket",
    "marks memo",
    "internal assessment",
    "assignment submission",

    # ----------------------------
    # GOVERNMENT / OFFICIAL
    # ----------------------------
    "government order",
    "official notice",
    "circular",
    "public notice",
    "district office",
    "collector",
    "municipal",
    "verification process",
    "application status",
    "document submission",

    # ----------------------------
    # CORPORATE / OFFICE
    # ----------------------------
    "meeting",
    "schedule",
    "agenda",
    "report",
    "project update",
    "team",
    "manager",
    "director",
    "board",
    "department",
    "internal communication",

    # ----------------------------
    # SERVICE NOTIFICATIONS
    # ----------------------------
    "privacy policy",
    "terms of service",
    "all rights reserved",
    "service notification",
    "support team",
    "account activity",
    "security notification",

    # ----------------------------
    # BILLING / UTILITIES (LEGIT)
    # ----------------------------
    "electricity bill",
    "water bill",
    "invoice attached",
    "payment receipt",
    "transaction receipt",
    "billing statement",

    # ----------------------------
    # GENERAL PROFESSIONAL LANGUAGE
    # ----------------------------
    "regards",
    "thanks",
    "sincerely",
    "best wishes",
    "official email",
]


def _clean_list(raw_list):
    seen = set()
    cleaned = []
    for item in raw_list:
        if not item:
            continue
        s = item.strip().lower()
        if not s:
            continue
        if s in seen:
            continue
        seen.add(s)
        cleaned.append(s)
    return cleaned


SPAM_KEYWORDS = _clean_list(RAW_SPAM)
HAM_KEYWORDS = _clean_list(RAW_HAM)

import re
from urllib.parse import urlparse

class HeuristicDetector:
    """
    A rule-based engine to detect suspicious patterns in URLs.
    No AI required - just logic.
    """

    def __init__(self):
        # Words often found in phishing links
        self.suspicious_keywords = [
            'login', 'verify', 'update', 'secure', 'bank', 
            'account', 'signin', 'confirm', 'wallet', 'free', 
            'prize', 'bonus', 'paypal', 'netflix', 'amazon'
        ]

    def check_url(self, url):
        """
        Analyzes the URL and returns a risk report.
        """
        flags = []
        score = 0

        # Ensure URL has a scheme for parsing
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url

        try:
            parsed = urlparse(url)
            domain = parsed.netloc
            path = parsed.path
        except:
            return {"error": "Invalid URL format"}

        # --- RULE 1: IP Address Check ---
        # Phishers often use raw IPs (e.g., http://192.168.1.1) instead of domains
        ip_pattern = r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"
        if re.match(ip_pattern, domain):
            score += 50
            flags.append("URL uses raw IP address")

        # --- RULE 2: Suspicious Keywords ---
        # Check if "login", "bank", etc. appear in the messy part of the URL
        found_keywords = [word for word in self.suspicious_keywords if word in url.lower()]
        if found_keywords:
            score += 20 * len(found_keywords)
            flags.append(f"Suspicious keywords found: {found_keywords}")

        # --- RULE 3: The '@' Symbol Trick ---
        # Browsers ignore everything before '@'. Phishers use this to hide the real domain.
        # Ex: http://google.com@evil-site.com -> Goes to evil-site.com
        if "@" in url:
            score += 40
            flags.append("Contains '@' symbol (Obfuscation technique)")

        # --- RULE 4: Deeply Nested Subdomains ---
        # Ex: http://paypal.secure.login.update.evil.com
        dots = domain.count('.')
        if dots > 3:
            score += 10
            flags.append(f"High number of subdomains ({dots} dots)")

        # --- RULE 5: URL Length ---
        if len(url) > 75:
            score += 10
            flags.append("URL is suspiciously long")

        # --- CALCULATE VERDICT ---
        # Cap the score at 100
        final_score = min(score, 100)
        
        verdict = "Safe"
        if final_score > 70:
            verdict = "Dangerous"
        elif final_score > 30:
            verdict = "Suspicious"

        return {
            "url": url,
            "risk_score": final_score,
            "verdict": verdict,
            "flags": flags
        }

# --- TEST SECTION ---
# This allows you to run this file directly to test it
if __name__ == "__main__":
    detector = HeuristicDetector()
    
    # Test Cases
    test_urls = [
        "https://google.com",                                      # Safe
        "http://192.168.1.55/login",                               # IP Address
        "http://paypal-secure-login.update-account.com",           # Keywords + Long
        "https://google.com@evil-hacker-site.net/prize"           # @ Symbol
    ]

    print("--- PHISHING DETECTION HEURISTICS TEST ---")
    for link in test_urls:
        result = detector.check_url(link)
        print(f"\nChecking: {result['url']}")
        print(f"Score: {result['risk_score']}/100 ({result['verdict']})")
        print(f"Flags: {result['flags']}")
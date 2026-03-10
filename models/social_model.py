def analyze_social(shares, followers, account_age_days):
    """
    Rule-based heuristics for social credibility.
    """
    try:
        shares = int(shares) if shares else 0
        followers = int(followers) if followers else 0
        account_age_days = int(account_age_days) if account_age_days else 0
        
        score = 0.5
        
        # New accounts with many shares but few followers are highly suspicious (bot behavior)
        if account_age_days < 30 and shares > 1000 and followers < 100:
            return 0.1
            
        # Established accounts generally have higher baseline credibility
        if account_age_days > 365:
            score += 0.2
            
        # Good engagement ratio
        if followers > 0:
            ratio = shares / followers
            if ratio > 10.0:  # Virality without following = suspicious
                score -= 0.3
            elif ratio < 0.1: # Normal organic engagement
                score += 0.1
                
        # Clamping
        return max(0.0, min(1.0, score))
        
    except Exception as e:
        print(f"Error processing social data: {e}")
        return 0.5

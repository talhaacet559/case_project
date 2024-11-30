
def period_decider(date_joined, date_now):
    # Calculate the absolute difference in days
    date_diff = abs((date_now - date_joined).days)

    # Check if the difference is more than a year (365 days)
    if date_diff < 365:
        return date_joined.year
    elif date_diff == 365:
        return date_now.year
    else:
        # Increment the year in `date_joined`
        return period_decider(date_joined.replace(year=date_joined.year + 1), date_now)
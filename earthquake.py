from tweets import get_followers, get_user_profile, save_user, save_users
from models import Tweet, User

public_earthquake_accounts = ['earthquakesla','quakestoday', 'earthquakessf', 'usgsearthquakes']

for screen_name in public_earthquake_accounts:
    user = get_user_profile(screen_name=screen_name)
    followers = get_followers(screen_name, save_in_time=True)
    save_user(user)
    save_users(followers)

    #for user in users:
    #followers

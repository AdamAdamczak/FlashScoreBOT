
from robocorp import browser

WEB_URL="https://www.flashscore.com/football/@country/@league/results/"
TIMEOUT = 300
TEAMS_LOCATOR ="event__participant event__participant--"
GOAL_LOCATOR = "event__score event__score--"

def open_browser(country: str,league: str) ->browser.Page:
    browser.goto(WEB_URL.replace("@country",country).replace("@league",league))
    page = browser.page()
    page.wait_for_load_state()
    return page

def get_table(page:browser.Page) -> list[browser.Locator]:
    table = page.locator('[class="event__match event__match--static event__match--twoLine"]').all()
    
    return table
    
def get_single_match_data(match: browser.Locator,today: str) -> dict[str,str]:
    match_data = {}
    teams = ['home', 'away']
    if check_date(match,today):
        for team in teams:
            
            try:
                match_data[team] = match.locator(f'[class="{TEAMS_LOCATOR}{team}"]').inner_text(timeout=TIMEOUT)
                
            except:
                match_data[team] = match.locator(f'[class="{TEAMS_LOCATOR}{team} fontExtraBold"]').inner_text(timeout=TIMEOUT)
                
            match_data[team+"_goals"] = match.locator(f'[class="{GOAL_LOCATOR}{team}"]').inner_text(timeout=TIMEOUT)
        
    return match_data

def check_date(match: browser.Locator, today: str) -> bool:
    date = match.locator('[class="event__time"]').inner_text(timeout=TIMEOUT)
    date = date[:6]
    if date == today:
        return True
    return False
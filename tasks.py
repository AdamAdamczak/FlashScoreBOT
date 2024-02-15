from robocorp.tasks import task
from robocorp import storage
from robocorp import browser
import utils.browser_handling as bh
import utils.slack_handling as sh
import datetime

@task
def footballresults():
    leagues = get_credentials()

    today = datetime.date.today().strftime("%d.%M.")
    slack_client = sh.authenticate()
    
    for country in leagues:
        page = bh.open_browser(country,leagues[country])
        table = bh.get_table(page)
        sh.send_message(slack_client,sh.league_name(country))
        for match in table:
            match_data = bh.get_single_match_data(match,today)
            if match_data!={}:
                sh.send_message(slack_client,sh.merge_data(match_data))
            


def get_credentials():
    leagues = storage.get_json("Football Leagues")
    return leagues



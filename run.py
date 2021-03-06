#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Top level script. Calls other functions that generate datasets that this script then creates in HDX.

"""
import logging
from os.path import join, expanduser

from hdx.hdx_configuration import Configuration
from hdx.utilities.downloader import Download

from scrapername import generate_dataset_and_showcase, get_countriesdata

# Remove 2 lines below if you don't want emails when there are errors
from hdx.facades import logging_kwargs
logging_kwargs['smtp_config_yaml'] = join('config', 'smtp_configuration.yml')

from hdx.facades.simple import facade
# Use facade below instead of one above if installing scraper on ScraperWiki
#from hdx.facades.hdx_scraperwiki import facade

logger = logging.getLogger(__name__)


def main():
    """Generate dataset and create it in HDX"""

    base_url = Configuration.read()['base_url']
    # If website being scraped requires username and password, you can supply one in a file in your home directory.
    # The file should contain username:password based64 encoded. Remember to create it on the server eg. ScraperWiki box!
    # If you need to add extra parameters to every url, you can use extra_params_yaml and point to a YAML file with
    # key value pairs. Remember to create it on the server!
    with Download(basic_auth_file=join(expanduser("~"), '.scrapernamefile'),
                  extra_params_yaml=join(expanduser("~"), 'scrapernamefile.yml') as downloader:
        countriesdata = get_countriesdata(base_url, downloader)
        logger.info('Number of datasets to upload: %d' % len(countriesdata))
        for countrydata in countriesdata:
            dataset, showcase = generate_dataset_and_showcase(base_url, downloader, countrydata)
            if dataset:
                dataset.update_from_yaml()
                dataset.create_in_hdx()
                showcase.create_in_hdx()
                showcase.add_dataset(dataset)

if __name__ == '__main__':
    facade(main, hdx_site='test', hdx_key='xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx', user_agent='myorgandproject', project_config_yaml=join('config', 'project_configuration.yml'))
    # HDX: Remember to create .hdx_configuration.yml on your server eg. the ScraperWiki box!
    # HDX: Use facade below creating or adding to .useragents.yml a key (hdxscraper-scrapername) with a Dict as
    # a value, the Dict containing user agent entries.
    # HDX: It is best to use the HDX Data Team bot's key (https://data.humdata.org/user/luiscape) rather than your own.
    # HDX: That file should have a user_agent parameter and an additional one identifying the scraper as internal to HDX.
    # HDX: Log into ACLED scraperwiki to see what it should contain.
    # facade(main, user_agent_config_yaml=join(expanduser('~'), '.useragents.yml'), user_agent_lookup='hdxscraper-scrapername', project_config_yaml=join('config', 'project_configuration.yml'))



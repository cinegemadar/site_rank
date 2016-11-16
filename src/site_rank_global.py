import logging

"""
Logger attributes
"""
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('SiteRank:')

"""
DB attributes
"""
db_location = 'sqlite:///..\\db\\ranking.db'
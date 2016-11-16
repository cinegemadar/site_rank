import logging

"""
Logger attributes
"""
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger('SiteRank:')

"""
DB attributes
"""
db_location = 'sqlite:///..\\db\\ranking.db'
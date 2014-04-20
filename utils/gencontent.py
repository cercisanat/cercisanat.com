import pypsum
import random
from cerci.cerci_content.models import Genre, Author, IssueContent

#text = pypsum.get_lipsum(random.randint(5,10), 'paras', 'yes')


"""
Authors
"""

with open('male.names') as f:
    males = f.readlines()

with open('female.names') as f:
    females = f.readlines()


print males[45]
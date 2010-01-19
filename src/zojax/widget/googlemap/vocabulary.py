from zope import interface
from zope.component import getUtility, getUtilitiesFor
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

from interfaces import _


def mapTypesVocabulary(context):
    return SimpleVocabulary((
        SimpleTerm('HYBRID', 'HYBRID', _(u'Hybrid. This map type displays a transparent layer of major streets on satellite images.')),
        SimpleTerm('ROADMAP', 'ROADMAP', _(u'Roadmap. This map type displays a normal street map.')),
        SimpleTerm('SATELLITE', 'SATELLITE', _(u"Satellite. This map type displays satellite images.")),
        SimpleTerm('TERRAIN', 'TERRAIN', _(u"Terrain. This map type displays maps with physical features such as terrain and vegetation.")),
        ))

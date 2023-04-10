from random import randint, choice
from string import ascii_uppercase

import factory

from po8klasie_fastapi.app.institution.tests.factories import (
    SecondarySchoolInstitutionFactory,
)
from po8klasie_fastapi.app.institution_classes.models import (
    SecondarySchoolInstitutionClass,
)
from po8klasie_fastapi.app.lib.testing_utils import BaseFactory, fake_rspo


def fake_year():
    return randint(2010, 2030)


def fake_class_symbol():
    return choice(ascii_uppercase)


class SecondarySchoolInstitutionClassFactory(BaseFactory):
    class Meta:
        model = SecondarySchoolInstitutionClass

    year = factory.LazyFunction(fake_year)

    class_symbol = factory.LazyFunction(fake_class_symbol)
    class_name = factory.LazyAttribute(
        lambda class_: f"[{class_.class_symbol}] #{randint(1, 99)}"
    )

    institution_rspo = factory.LazyFunction(fake_rspo)
    institution = factory.RelatedFactory(
        SecondarySchoolInstitutionFactory,
        rspo=factory.SelfAttribute("..institution_rspo"),
        # factory_related_name="classes"
    )

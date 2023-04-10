import factory

from po8klasie_fastapi.app.institution.models import SecondarySchoolInstitution
from po8klasie_fastapi.app.lib.testing_utils import BaseFactory, fake_rspo
from po8klasie_fastapi.app.project.tests.factories import ProjectFactory
from po8klasie_fastapi.app.rspo_institution.tests.factories import (
    RspoInstitutionFactory,
)


class SecondarySchoolInstitutionFactory(BaseFactory):
    class Meta:
        model = SecondarySchoolInstitution
        sqlalchemy_get_or_create = ("rspo",)

    rspo = factory.LazyFunction(fake_rspo)
    project = factory.RelatedFactory(ProjectFactory)
    rspo_institution = factory.SubFactory(
        RspoInstitutionFactory, rspo=factory.SelfAttribute("..rspo")
    )

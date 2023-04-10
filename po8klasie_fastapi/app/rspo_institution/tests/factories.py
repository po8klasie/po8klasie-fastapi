import factory

from po8klasie_fastapi.app.lib.testing_utils import BaseFactory, fake, fake_rspo
from po8klasie_fastapi.app.rspo_institution.models import RspoInstitution


class RspoInstitutionFactory(BaseFactory):
    class Meta:
        model = RspoInstitution
        sqlalchemy_get_or_create = ("rspo",)

    rspo = factory.LazyFunction(fake_rspo)
    name = factory.LazyFunction(fake.school_name)

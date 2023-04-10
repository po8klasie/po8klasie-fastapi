import factory

from po8klasie_fastapi.app.lib.testing_utils import BaseFactory, fake
from po8klasie_fastapi.app.project.models import Project


def normalize_city_name(city: str):
    return city.lower().replace(" ", "_")


class ProjectFactory(BaseFactory):
    class Meta:
        model = Project
        sqlalchemy_get_or_create = ("project_id",)

    project_name = factory.LazyFunction(fake.city)
    project_id = factory.LazyAttribute(
        lambda project: normalize_city_name(project.project_name)
    )

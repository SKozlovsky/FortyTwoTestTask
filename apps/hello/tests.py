from apps.hello.models import Person
import factory
from faker import Factory

from django.test import TestCase

Faker = Factory.create()


class PersonFB(factory.DjangoModelFactory):
    FACTORY_FOR = Person

    first_name = Faker.first_name()
    last_name = Faker.last_name()
    birth_date = Faker.date_time()
    con_email = Faker.free_email()
    con_jabbber = Faker.free_email()
    con_skype = Faker.user_name()
    bio = Faker.paragraph()
    con_other = Faker.paragraph()


class ViewDataTests(TestCase):

    def test_404(self):
        """ Test for page, wheh model-object isn't exist in DB"""
        self.assertFalse(Person.objects.all())
        content = self.client.get('/').content
        self.assertTrue('<div class="not_found">' in content)

    def test_verifying_rendering_template(self):
        """Test to check of using of the correct template """
        PersonFB.create()
        response = self.client.get('/')
        self.assertTrue(response.template_name[0] == 'hello/mainpage.html')

    def test_availability_model_data_on_page(self):
        """Test to check the content on web-page"""
        atr = None
        TestPers = PersonFB.create()
        response = self.client.get('/')
        for field_name in Person._meta.get_all_field_names():
            if field_name != 'id':
                if field_name == 'birth_date':
                    date = TestPers.__getattribute__(field_name)
                    atr = date.strftime("%Y-%m-%d")
                elif field_name == 'first_name' or field_name == 'last_name':
                    name_ = TestPers.__getattribute__(field_name)
                    atr = name_.title()
                else:
                    atr = TestPers.__getattribute__(field_name)

            self.assertIn(atr, response.content)

    def test_first_DB_records(self):
        """Test to check what object is selected by view from DB with several records.
        It should be object with id=1"""
        for j in range(5):
            PersonFB.create(first_name="Person%i" % j)
        self.assertTrue(len(Person.objects.all()) == 5)
        p = Person.objects.get(id=1)
        context = self.client.get('/').context_data
        self.assertEqual(context['object'], p)

    def test_min_DB_records(self):
        """Test to check what object is selected by view from non-empty DB
        with some deleted records. It should be object with id=1"""
        for j in range(10):
            PersonFB.create(first_name="Person%i" % j)
        Person.objects.filter(id__gt=7).delete()
        Person.objects.filter(id__lt=3).delete()
        Person.objects.get(id=5).delete()
        self.assertTrue(len(Person.objects.all()) == 4)
        p = Person.objects.get(id=3)
        context = self.client.get('/').context_data
        self.assertEqual(context['object'], p)

    def test_context_data(self):
        """Tes to check of using correct context-data"""
        TestPers = PersonFB.create()
        context = self.client.get('/').context_data
        self.assertEqual(context['title'], 'Hello')
        self.assertEqual(context['object'], TestPers)

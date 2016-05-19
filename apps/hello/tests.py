from apps.hello.models import Person, RequestCollect
import factory
import re
from faker import Factory
from django.test import TestCase
from django.core.urlresolvers import reverse

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
        content = self.client.get(reverse('mainpage')).content
        self.assertTrue('<div class="not_found">' in content)

    def test_verifying_rendering_template(self):
        """Test to check of using of the correct template """
        PersonFB.create()
        response = self.client.get(reverse('mainpage'))
        self.assertTemplateUsed(response, 'hello/mainpage.html')

    def test_availability_model_data_on_page(self):
        """Test to check the content on web-page"""
        atr = None
        test_pers = PersonFB.create()
        response = self.client.get(reverse('mainpage'))
        for field_name in Person._meta.get_all_field_names():
            if field_name == 'id':
                continue
            if field_name == 'birth_date':
                date = test_pers.__getattribute__(field_name)
                atr = date.strftime("%Y-%m-%d")
            elif field_name == 'first_name' or field_name == 'last_name':
                name_ = test_pers.__getattribute__(field_name)
                atr = name_.title()
            elif field_name == 'photo':
                continue
            else:
                atr = test_pers.__getattribute__(field_name)

            self.assertIn(atr, response.content)

    def test_context_data(self):
        """Tes to check of using correct context-data"""
        test_pers = PersonFB.create()
        context = self.client.get(reverse('mainpage')).context_data
        self.assertEqual(context['title'], 'Hello')
        self.assertEqual(context['object'], test_pers)


class ModelDataTests(TestCase):

    def test_first_DB_records(self):
        """Test to check what object is selected by view from DB with several records.
        It should be object with id=1"""
        for j in range(5):
            PersonFB.create(first_name="Person%i" % j)
        self.assertTrue(len(Person.objects.all()) == 5)
        p = Person.objects.get(id=1)
        context = self.client.get(reverse('mainpage')).context_data
        self.assertEqual(context['object'], p)

    def test_min_DB_records(self):
        """Test to check what object is selected by view from non-empty DB with
        some deleted records. It should be object with id=1"""
        for j in range(10):
            PersonFB.create(first_name="Person%i" % j)
        Person.objects.filter(id__gt=7).delete()
        Person.objects.filter(id__lt=3).delete()
        Person.objects.get(id=5).delete()
        self.assertTrue(len(Person.objects.all()) == 4)
        p = Person.objects.get(id=3)
        context = self.client.get(reverse('mainpage')).context_data
        self.assertEqual(context['object'], p)


class RequestViewTests(TestCase):

    def test_10_requests_content(self):
        """Test to check existing of 10 'GET' or 'POST' request on page """
        PersonFB.create()
        for i in range(5):
            self.client.get('/somepage%i' % i)
            self.client.get('/request')
            self.client.get('/admin')
            self.client.post('/login/',
                             {'username': 'john', 'password': 'smith'})
        content = self.client.get(reverse('requests')).content
        req_count = content.count('GET')+content.count('POST')
        self.assertTrue(req_count == 10)

    def test_correct_title_name(self):
        """Test to check correct title name  """
        PersonFB.create()
        content = self.client.get(reverse('requests')).content
        self.assertInHTML("<title>Requests</title>", content)

    def test_requests_existing(self):
        """Test to check existing requests list in context """
        PersonFB.create()
        context = self.client.get(reverse('requests')).context_data
        self.assertIsNotNone(context['requests_list'])

    def test_10_requests_context(self):
        """Test to check existing of 10 records request data on context """
        PersonFB.create()
        for i in range(5):
            self.client.get('/somepage%i' % i)
            self.client.get(reverse('mainpage'))
            self.client.get('/admin')
            self.client.post('/login/',
                             {'username': 'john', 'password': 'smith'})
        context = self.client.get(reverse('requests')).context_data
        self.assertTrue(len(context['requests_list']) == 10)

    def test_last_10_requests(self):
        """Test to check correct requests data on context (exactly last 10)"""
        PersonFB.create()
        for i in range(21):
            self.client.get('/ololo_%i' % i)
        self.client.post('/login/', {'username': 'john', 'password': 'smith'})
        self.client.get(reverse('requests'))
        context = self.client.get(reverse('requests')).context_data
        requests_list = context['requests_list']
        self.assertEqual(requests_list[0].r_path, reverse('requests'))
        self.assertEqual(requests_list[1].r_path, '/login/')
        for j in range(1, 8):
            self.assertEqual(requests_list[1+j].r_path, '/ololo_%i' % (21-j))


class MiddlewareTests(TestCase):

    def _15requests(self):
        for i in range(5):
            self.client.get('/somepage%i' % i)
            self.client.get('/admin')
            self.client.post('/login/',
                             {'username': 'john', 'password': 'smith'})

    def test_middleware_DB_not_empty(self):
        """Test to check if non-empty model RequestCollect
        after request.
        """
        PersonFB.create()
        self.client.get(reverse('mainpage'))
        self.assertIsNotNone(RequestCollect.objects.all())

    def test_middleware_correct_number_entries(self):
        """Test to check correct number of entries """
        PersonFB.create()
        self._15requests()
        self.assertEqual(len(RequestCollect.objects.all()), 15)

    def test_correct_viewed_flag(self):
        """Test to check correct data on r_viewed field"""
        PersonFB.create()
        self.client.get('/admin')
        self.assertEqual(RequestCollect.objects.get(id=1).r_viewed, False)

        self._15requests()
        unreaded_requests = RequestCollect.objects.filter(r_viewed=False)
        self.assertEqual(len(unreaded_requests), 16)

        self.client.get(reverse('requests'))
        unreaded_requests = RequestCollect.objects.filter(r_viewed=False)
        readed_requests = RequestCollect.objects.filter(r_viewed=True)
        self.assertEqual(len(readed_requests), 17)
        self.assertEqual(len(unreaded_requests), 0)


class AjaxTests(TestCase):

    def test_json_response(self):
        """ test to check response existing after AJAX-request """
        self.client.get(reverse('mainpage'))
        response = self.client.get(reverse('ajax_requests'),
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Content-Type: application/json", response.__str__())

    def test_correct_title_name_json(self):
        """ Test to check correct title name in JSON-response"""
        PersonFB.create()
        self.client.get(reverse('requests'))
        c = self.client.get(reverse('ajax_requests'),
                            HTTP_X_REQUESTED_WITH='XMLHttpRequest').content
        title = re.match(r'.+title": "(.*Requests)",.+', c).groups()[0]
        self.assertEqual(title, '(0)Requests')
        for i in range(10):
            self.client.get('/blablapage')
            c = self.client.get(reverse('ajax_requests'),
                                HTTP_X_REQUESTED_WITH='XMLHttpRequest').content
            title = re.match(r'.+title": "(.*Requests)",.+', c).groups()[0]
            self.assertEqual(title, '(%i)Requests' % (i+1))
        self.client.get(reverse('requests'))
        c = self.client.get(reverse('ajax_requests'),
                            HTTP_X_REQUESTED_WITH='XMLHttpRequest').content
        title = re.match(r'.+title": "(.*Requests)",.+', c).groups()[0]
        self.assertEqual(title, '(0)Requests')

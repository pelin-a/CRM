from django.urls import path, reverse
from . import views

urlpatterns = [
    path('', views.login_user, name="login"),
    path('pipelines', views.get_pipelines, name="get_pipelines"),
    path('pipelines/add', views.add_pipeline, name="add_pipeline"),
    path('pipelines/<int:id>', views.get_pipeline_detail, name="get_pipeline_detail"),
    path('contacts', views.get_contacts, name="get_contacts"),
    path('contacts/add', views.add_contact, name="add_contact"),
    path('contacts/<int:id>', views.get_contact_detail, name="get_contact_detail"),
    path('contacts/edit/<int:id>', views.edit_contact, name="edit_contact"),
    path('contacts/delete/<int:id>', views.delete_contact, name="delete_contact"),
    path('pipelines/edit/<int:id>', views.edit_pipeline, name="edit_pipeline"),
    path('pipelines/delete/<int:id>', views.delete_pipeline, name="delete_pipeline"),
    path('email', views.contact, name="contact"),
    path('logout', views.logout_user, name="logout"),
    path('register', views.register_user, name="register"),
    path('events', views.get_events, name="get_events"),
    path('events/add', views.add_event, name="add_event"),
    path('events/edit/<int:id>', views.edit_event, name="edit_event"),
    path('events/delete/<int:id>',views.delete_event, name="delete_event"),
    path('events/<int:id>', views.get_event_detail, name="get_event_detail"),
    path('account', views.edit_account, name="edit_account"),
    path('account/change-password', views.change_password, name='change_password')
]
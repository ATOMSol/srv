# from django.apps import AppConfig


# class WebshocketConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'webshocket'
#     ready_called = False

#     def ready(self):
#         if not self.ready_called:
#             self.ready_called = True
#             try:
#                 import webshocket.signals
#                 print("Signals loaded successfully")
#             except Exception as e:
#                 print(f"Error loading signals: {str(e)}")


from django.apps import AppConfig


class MyappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'webshocket'

    def ready(self):
        try:
            import webshocket.signals
            print("Signals loaded successfully")
        except Exception as e:
            print(f"Error loading signals: {str(e)}")

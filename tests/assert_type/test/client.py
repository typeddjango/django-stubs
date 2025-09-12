from django.test import Client
from django.urls import reverse, reverse_lazy

url_reverse = reverse("some:namespace")
url_lazy = reverse_lazy("some:namespace")
url_str = "/abc/def"

client = Client()
client.get(url_reverse)
client.get(url_lazy)
client.get(url_str)

client.post(url_reverse)
client.post(url_lazy)
client.post(url_str)

client.patch(url_reverse)
client.patch(url_lazy)
client.patch(url_str)

client.put(url_reverse)
client.put(url_lazy)
client.put(url_str)

client.delete(url_reverse)
client.delete(url_lazy)
client.delete(url_str)

client.generic("GET", url_reverse)
client.generic("POST", url_lazy)
client.generic("DELETE", url_str)

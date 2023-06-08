from django.forms import RadioSelect


class ColorRadioSelect(RadioSelect):
    option_template_name = "project/option_template_name_radio.html"
    template_name = "project/template_name_radio.html"
    # template_name = "django/forms/widgets/radio.html"
   # option_template_name = "django/forms/widgets/radio_option.html"

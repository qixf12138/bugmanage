from django.forms import RadioSelect


class ColorRadioSelect(RadioSelect):
    option_template_name = "system/option_template_name_radio.html"
    template_name = "system/template_name_radio.html"
    # template_name = "django/forms/widgets/radio.html"
   # option_template_name = "django/forms/widgets/radio_option.html"

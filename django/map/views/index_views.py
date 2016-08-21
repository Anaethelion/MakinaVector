from django.conf import settings
from django.template import loader, TemplateDoesNotExist
from django.http import HttpResponse
import ujson

# Get all the layer name
def getlayersNames():
    style_file = open(settings.STYLE_DIR).read()
    style_json = ujson.loads(style_file)
    list_item = []

    for layer in style_json['layers']:
        try:
            layer_already_exist = 0
            for context_layer in list_item:
                if context_layer == layer['source-layer']:
                    layer_already_exist = 1
            if layer_already_exist == 0:
                list_item.append(layer['source-layer'])
        except:
            pass

    multiple_style_file = open(settings.MULTIPLE_STYLE_DIR).read()
    multiple_style_json = ujson.loads(multiple_style_file)

    for layer in multiple_style_json['layers']:
        try:
            layer_already_exist = 0
            for context_layer in list_item:
                if context_layer == layer['source-layer']:
                    layer_already_exist = 1
            if layer_already_exist == 0:
                list_item.append(layer['source-layer'])
        except:
            pass

    return list_item

# Render the index page
def index(request):
    context = locals()
    context['django_host'] = settings.DJANGO_HOST
    context['django_port'] = settings.DJANGO_PORT
    context['title'] = settings.TITLE_OF_INDEX
    context['database'] = settings.DATABASE_NAME
    context['mapboxAccessToken'] = settings.MAPBOX_ACCESS_TOKEN
    context['startingZoom'] = settings.STARTING_ZOOM
    context['startingPosition'] = settings.STARTING_POSITION
    context['list_item'] = getlayersNames()

    # Load the template
    try:
        template = loader.get_template('map/index.html')
    except TemplateDoesNotExist:
        return HttpResponse(status=404)

    # Response
    return HttpResponse(template.render(context, request))

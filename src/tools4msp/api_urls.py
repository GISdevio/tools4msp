from django.urls import include, path

# Try to use nested routers
# from rest_framework import routers
# from rest_framework_nested import routers
from rest_framework_extensions.routers import ExtendedSimpleRouter, ExtendedDefaultRouter

from rest_framework.documentation import include_docs_urls

from rest_framework_swagger.views import get_swagger_view

from tools4msp import api_views
from tools4msp.messages import DESCRIPTION_LAST, DESCRIPTION_DEPRECATED

router = ExtendedDefaultRouter()
cs_router = router.register(r'api/domainareas',
                            api_views.DomainAreaViewSet,
                            )

cs_router = router.register(r'api/contexts',
                            api_views.ContextViewSet,
                            )

cs_router = router.register(r'api/codedlabels',
                            api_views.CodedLabelViewSet,
                            )

cs_router = router.register(r'api/casestudies',
                            api_views.CaseStudyViewSet,
                            basename='casestudy')

cs_router.register(r'layers',
                   api_views.CaseStudyLayerViewSet,
                   basename='casestudylayer',
                   parents_query_lookups=['casestudy__id'])

cs_router.register(r'inputs',
                   api_views.CaseStudyInputViewSet,
                   basename='casestudyinput',
                   parents_query_lookups=['casestudy__id'])

cs_router = router.register(r'casestudyruns',
                            api_views.CaseStudyRunViewSet,
                            basename='casestudyrun'
                            )

cs_router = router.register(r'api/casestudyruns', # this is a fake url,
                                              # otherwise 'api' prefix
                                              # is collapsed. Instead
                                              # we want the api prefix
                                              # in V1 schema (as befor
                                              # the upgrade to V2).
                            api_views.CaseStudyRunViewSet,
                            basename='casestudyrun'
                            )

# (
#     router.register(r'casestudies', api_views.CaseStudyViewSet, base_name='casestudy')
#           .register(r'layers',
#                     api_views.CaseStudyLayerViewSet,
#                     base_name='casestudy-layers',
#                     parents_query_lookups=['casestudy_layers'])
# )

# router = routers.DefaultRouter()
# router.register(r'casestudies', api_views.CaseStudyViewSet, 'casestudies')
# # router.register(r'layers', api_views.CaseStudyLayerViewSet)
# # router.register(r'inputs', api_views.CaseStudyInputViewSet)

# layers_router = routers.NestedDefaultRouter(router, r'casestudies', lookup='casestudy')
# layers_router.register(r'layers', api_views.CaseStudyLayerViewSet, base_name='casestudy-layers')

# inputs_router = routers.NestedDefaultRouter(router, r'casestudies', lookup='casestudy')
# inputs_router.register(r'inputs', api_views.CaseStudyInputViewSet, base_name='casestudy-inputs')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('api/', include(router.urls)),
    # path('api/', include(layers_router.urls)),
    # path('api/', include(inputs_router.urls)),
    path(r'docs/', include_docs_urls(title='Tools4MSP API v1',
                                     description=DESCRIPTION_DEPRECATED)),
    # path('openapi/', schema_view),
]

from rest_framework import serializers
from rest_framework_gis.serializers import GeoModelSerializer
from .models import CaseStudy, CaseStudyLayer, CaseStudyInput, \
    CodedLabel, DomainArea, CaseStudyGraphic


class CSChildHyperlinkedIdentityField(serializers.HyperlinkedIdentityField):
    def get_url(self, obj, view_name, request, format):
        """
        Given an object, return the URL that hyperlinks to the object.
        May raise a `NoReverseMatch` if the `view_name` and `lookup_field`
        attributes are not configured to correctly match the URL conf.
        """
        # Unsaved objects will not yet have a valid URL.
        if obj.pk is None:
            return None

        return self.reverse(view_name,
            kwargs={
                'parent_lookup_casestudy__id': obj.casestudy.pk,
                'pk': obj.pk,
            },
            request=request,
            format=format,
        )


class DomainAreaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DomainArea
        fields = ('url', 'label',)


class CodedLabelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CodedLabel
        fields = ('url', 'group', 'code', 'label')
        lookup_field = 'code'
        extra_kwargs = {
            'url': {'lookup_field': 'code'}
        }


class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
    class Meta:
        fields = ('file',)


class CaseStudyLayerSerializer(serializers.HyperlinkedModelSerializer):
    url = CSChildHyperlinkedIdentityField(view_name='casestudylayer-detail')
    label = serializers.SlugField(source="coded_label.code",
                                       read_only=True)

    class Meta:
        model = CaseStudyLayer
        fields = ('url',
                  'file',
                  'coded_label',
                  'label')
        read_only_fields = ('file',
                            'label')
        extra_kwargs = {
            'coded_label': {'lookup_field': 'code'}
        }


class CaseStudyInputSerializer(serializers.HyperlinkedModelSerializer):
    url = CSChildHyperlinkedIdentityField(view_name='casestudyinput-detail')
    label = serializers.SlugField(source="coded_label.code",
                                       read_only=True)
    class Meta:
        model = CaseStudyInput
        fields = ('url',
                  'file',
                  'coded_label',
                  'label')
        read_only_fields = ('file',
                            'label')
        extra_kwargs = {
            'coded_label': {'lookup_field': 'code'}
        }


class CaseStudyGraphicSerializer(serializers.HyperlinkedModelSerializer):
    url = CSChildHyperlinkedIdentityField(view_name='casestudygraphic-detail')
    label = serializers.SlugField(source="coded_label.code",
                                       read_only=True)
    class Meta:
        model = CaseStudyGraphic
        fields = ('url',
                  'file',
                  'coded_label',
                  'label')
        read_only_fields = ('file',
                            'label')
        extra_kwargs = {
            'coded_label': {'lookup_field': 'code'}
        }


class CaseStudySerializer(serializers.HyperlinkedModelSerializer): #ModelSerializer):
    layers = CaseStudyLayerSerializer(many=True, read_only=True)
    inputs = CaseStudyInputSerializer(many=True, read_only=True)
    graphics = CaseStudyGraphicSerializer(many=True, read_only=True)
    extent = serializers.JSONField(source="domain_area.extent",
                                   read_only=True)
    owner = serializers.CharField(source='owner.username',
                                  read_only=True)

    class Meta:
        model = CaseStudy
        fields = ('url',
                  'id',
                  'label',
                  'description',
                  'module',
                  'cstype',
                  'resolution',
                  'extent',
                  'domain_area',
                  'domain_area_terms',
                  'owner',
                  'created',
                  'updated',
                  'layers',
                  'inputs',
                  'graphics')
        read_only_fields = ('extent', 'owner', 'created',
                            'updated', 'layers', 'inputs', 'graphics')

        # write_only_fields = ('domain_area',)


class CaseStudyListSerializer(CaseStudySerializer):
    class Meta:
        model = CaseStudy
        fields = ('url',
                  'id',
                  'label',
                  'description',
                  'module',
                  'cstype',
                  'resolution',
                  'extent',
                  'owner',
                  'created',
                  'updated')
        read_only_fields = ('extent', 'owner''created',
                            'updated', 'layers', 'inputs', 'graphics')

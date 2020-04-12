
from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import ListSerializer
from rest_framework.serializers import SerializerMethodField

from .models import Article
from .models import Comment

class RelatedArticlesSerializer(ModelSerializer):
    class Meta:
        model=Article
        fields = ('id', 'thumbnail', 'excerpt', 'title', 'slug')

class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ( 'name',
                  'email',
                  'website',
                  'comment',
                  'date',
                  'is_active',
                 )

class ArticleSerializer(ModelSerializer):
    contents = SerializerMethodField()
    comments = CommentSerializer(read_only=True, many=True)
    related_articles = RelatedArticlesSerializer(read_only=True, many=True)

    class Meta:
        model = Article
        fields = ('id',
                  'title',
                  'slug',
                  'pub_date',
                  'categories',
                  'related_articles',
                  'excerpt',
                  'thumbnail',
                  'contents',
                  'comments',
                 )
        lookup_field = 'slug'
        exclude_from_list = ('contents', 'related_articles', 'comments' )

    @classmethod
    def many_init(cls, *args, **kwargs):
        # remove fields from list view
        kwargs['child'] = cls()
        meta = getattr(cls, 'Meta', None)
        exclude = getattr(meta, 'exclude_from_list', ())
        for field in exclude:
            kwargs['child'].fields.pop(field)
        list_serializer_class = getattr(meta, 'list_serializer_class', ListSerializer)
        return list_serializer_class(*args, **kwargs)


    def get_contents(self, article):
        contents = article.getContents()

        json_contents = [
            {
                'id': c.id,
                'type': "RichTextContent",
                'obj': { 'html': c.text, }
            } if c.__class__.__name__.endswith("RichTextContent")
            else
            {
                'id': c.id,
                'type': 'ImageContent',
                'obj': {
                    'url' : c.image.thumbnail["300x300"].url,
                    'caption': c.caption,
                    'float': c.css_float,
                }
            } if c.__class__.__name__.endswith("ImageContent")
            else
            {
                'error': "%s not supported." % c.__class__.__name__
            }
            for c in contents
        ]
        return json_contents


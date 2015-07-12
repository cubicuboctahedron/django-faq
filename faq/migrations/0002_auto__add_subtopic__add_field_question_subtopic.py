# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SubTopic'
        db.create_table(u'faq_subtopic', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=150)),
            ('sort_order', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('topic', self.gf('django.db.models.fields.related.ForeignKey')(related_name='subtopics', to=orm['faq.Topic'])),
        ))
        db.send_create_signal(u'faq', ['SubTopic'])

        # Adding field 'Question.subtopic'
        db.add_column(u'faq_question', 'subtopic',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='questions', null=True, to=orm['faq.SubTopic']),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'SubTopic'
        db.delete_table(u'faq_subtopic')

        # Deleting field 'Question.subtopic'
        db.delete_column(u'faq_question', 'subtopic_id')


    models = {
        u'faq.question': {
            'Meta': {'ordering': "['sort_order']", 'object_name': 'Question'},
            'answer': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'subtopic': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'questions'", 'null': 'True', 'to': u"orm['faq.SubTopic']"}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'topic': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'questions'", 'to': u"orm['faq.Topic']"})
        },
        u'faq.subtopic': {
            'Meta': {'ordering': "['sort_order', 'name']", 'object_name': 'SubTopic'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '150'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'topic': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'subtopics'", 'to': u"orm['faq.Topic']"})
        },
        u'faq.topic': {
            'Meta': {'ordering': "['sort_order', 'name']", 'object_name': 'Topic'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '150'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['faq']
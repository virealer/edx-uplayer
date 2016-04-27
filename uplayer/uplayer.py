# -*- coding: utf-8 -*-
""" uplayerXBlock main Python class"""

import pkg_resources
from django.template import Context, Template

from xblock.core import XBlock
from xblock.fields import Scope, Integer, String, Boolean
from xblock.fragment import Fragment

class uplayerXBlock(XBlock):

    '''
    Icon of the XBlock. Values : [other (default), video, problem]
    '''
    icon_class = "video"

    '''
    Fields
    '''
    display_name = String(display_name="Display Name",
        default="uplayer",
        scope=Scope.settings,
        help="This name appears in the horizontal navigation at the top")
	
    app_id = String(display_name="video client_id",
		default="1252099219",
		scope=Scope.content, #Scope.content和Scope.settings不同在于，(可见性)本课多处可用
		help="The  client_id for your video.")

    vid = String(display_name="video vid",
		default="8645beda6d27efc874750fd2ec26bf1c_8",
		scope=Scope.content, #Scope.content和Scope.settings不同在于，(可见性)本课多处可用
		help="The vid for your video.")

    width = Integer(display_name="Video player width",
		default="845",
		scope=Scope.content,
		help="The width for your video player.")

    height = Integer(display_name="Video player height",
		default="600",
		scope=Scope.content,
		help="The height for your video player.")

    service = String(display_name="service",
		default="polyv",
		scope=Scope.content, #Scope.content和Scope.settings不同在于，(可见性)本课多处可用
		help="polyv or qcloud ")

    secret_id = String(display_name="s i",
		default="AKIDN9JVtegGmu3nDGr6Hv1i72jJMMxBukSj",
		scope=Scope.content, #Scope.content和Scope.settings不同在于，(可见性)本课多处可用
		help="secret id")

    secret_key = String(display_name="s k",
		default="01c345ac-853f-4bab-8d90-44ff59a86b03",
		scope=Scope.content, #Scope.content和Scope.settings不同在于，(可见性)本课多处可用
		help="secret_key")
    js_dic = {
        "polyv": ["static/js/polyv_player.min.js", "static/js/polyv_upload.js"],
        "qcloud": ["static/js/qcloud_player.js", "static/js/qcloud_upload.min.js"]
    }
    def load_resource(self, resource_path):
		resource_content = pkg_resources.resource_string(__name__, resource_path)
		return resource_content.decode("utf8")
    def render_template(self, template_path, context={}):
		"""
		Evaluate a template by resource path, applying the provided context
		"""
		template_str = self.load_resource(template_path)
		return Template(template_str).render(Context(context))
		'''
		Main functions
		'''
    def student_view(self, context=None):
		"""
		The primary view of the XBlock, shown to students
		when viewing courses.
		"""
		'''
		#添加字段记录上回播放时间，应该是用户级别
		if self.start_time != "" and self.end_time != "":
			fullUrl += "#t=" + self.start_time + "," + self.end_time
		elif self.start_time != "":
			fullUrl += "#t=" + self.start_time
		elif self.end_time != "":
			fullUrl += "#t=0," + self.end_time
		'''
		context = {
			'app_id' : self.app_id,
			'vid': self.vid
		}
		html = self.render_template('static/html/student_view.html', context)
		frag = Fragment(html)
		#frag.add_javascript(self.load_resource('static/js/h5connect.js')) #内有中文，使用插入外部url
		frag.add_javascript(self.load_resource(self.js_dic[self.service][0]))
		#frag.add_javascript(self.load_resource("static/js/polyv_player.min.js"))
		#frag.add_javascript(self.load_resource("static/js/qcloud_player.js"))	
		frag.add_javascript(self.load_resource("static/js/student_view.js"))
		frag.initialize_js('uplayerXBlockInitView')
		return frag
    def studio_view(self, context=None):
		"""
		The secondary view of the XBlock, shown to teachers
		when editing the XBlock.
		"""
		context = {
			'vid': self.vid
		}
		html = self.render_template('static/html/studio_view.html', context)
		frag = Fragment(html)
		frag.add_css(self.load_resource("static/css/uploadfive.css"))
		frag.add_javascript(self.load_resource(self.js_dic[self.service][1]))
		#frag.add_javascript(self.load_resource("static/js/polyv_upload.js"))
		#frag.add_javascript(self.load_resource("static/js/qcloud_upload.min.js"))
		frag.add_javascript(self.load_resource('static/js/studio_view.js'))
		frag.initialize_js('uplayerXBlockInitStudio')
		return frag
    @XBlock.json_handler
    def save_uplayer(self, data, suffix=''):
		"""
		The saving handler.
		"""
		self.vid = data['vid']
		return {
			'result': 'success',
		}
    @XBlock.json_handler
    def get_params(self, data, suffix=''):
	'''called when uplayer init'''
        return {
			"service":self.service,
			"vid":self.vid,
			"app_id":self.app_id,
			"width":self.width,
			"height":self.height,
		}
    @XBlock.json_handler
    def get_key(self, data, suffix=''):
		return {
			"service": self.service,
			"secret_id": self.secret_id,
			"secret_key": self.secret_key,
		}
    @staticmethod
    def workbench_scenarios():
		return [
              ("uplayer", "<uplayer />")  #the name should be "<youku />"
        ]

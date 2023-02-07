# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author  : v_jiaohaicheng@baidu.com
@des     : 

"""
import os
from queue import Queue

# for name in os.listdir(R"D:\Projects\SupportRequirements\Project\spider\util"):
#     print("def {}():\n\tfrom util.{} import \n\tpass".format(name,name))


class ProcessInput():
	def __init__(self,args):
		self.args = args

		self.url_lis = self.args["url_list"]
		self.platform = self.args["platform"]
		self.kind = self.args["kind"]
		self.author = self.args["author"]

		self.args_map = {'baojitv': self.baojitv, 'bilibili': self.bilibili, 'douyin': self.douyin, 'haokanshipin': self.haokanshipin, 'kuaishou': self.kuaishou, 'lizhiwang': self.lizhiwang, 'shanxitv': self.shanxitv, 'xiantv': self.xiantv, 'xigua': self.xigua, 'yltv': self.yltv, 'youku': self.youku}
		#
		self.check_function()

	def check_function(self):
		"""
		选择执行函数
		:return:
		"""
		if self.args_map.get(self.platform) is not None:
			self.args_map[self.platform]()
		else:
			print("输入参数错误")


	def baojitv(self):
		from util.baojitv import tvbaoji
		tb = tvbaoji.TvBaoji()
		# 更新url
		tb.start_urls = self.args["url_list"]

		tb.main(self.args)

	# 提供的不太好使，you-get 重写的
	# https://www.bilibili.com/video/BV11E411R7YV?p=1 这种p= 保留一个就行
	# 付费有会员的下载不了
	def bilibili(self):
		from util.bilibili import bili_download_youget,bili_sub_download,bili_urllist_download,bili_you_get_rewrite
		bili_you_get_rewrite.process(self.args)
		pass

	def douyin(self):
		from util.douyin import douyin_download
		info_json = douyin_download.main(self.args)
		print("info_json", info_json)
		pass

	# 只能下载频道
	def haokanshipin(self):
		from util.haokanshipin import haokan_download,haokan_download2
		info_json = haokan_download2.main(self.args)
		print("info_json",info_json)
		pass

	def kuaishou(self):
		from util.kuaishou import kuaishou_download
		info_json = kuaishou_download.main(self.args)
		print("info_json", info_json)
		pass
	# 有问题 一会修复
	def lizhiwang(self):
		from util.lizhiwang import lizhiwang_download
		info_json = lizhiwang_download.main(self.args)
		print("info_json", info_json)
		pass

	def shanxitv(self):
		from util.shanxitv import snrtv_suixi
		shr = snrtv_suixi.SendHttpRequests()
		# 更新url
		shr.list_page_urls = self.args["url_list"]

		info_json = shr.main(self.args)
		print("info_json", info_json)
		pass

	def xiantv(self):
		from util.xiantv import v_xiaancity
		vc = v_xiaancity.VxianCity()
		# 更新url
		vc.start_url_list = self.args["url_list"]

		info_json = vc.main(self.args)
		print("info_json", info_json)
		pass

	# selenium,不好使需要更换header和params
	def xigua(self):
		from util.xigua import xigua_download
		info_json = xigua_download.main(self.args)
		print("info_json", info_json)
		pass

	def yltv(self):
		from util.yltv import v_ylrb
		yb = v_ylrb.Ylrb()
		# 更新url
		yb.start_urls = self.args["url_list"]

		info_json = yb.parse(self.args)
		print("info_json", info_json)
		pass

	# you-get 下载错误，不支持了
	def youku(self):
		from util.youku import youku_download
		info_json = youku_download.main(self.args)
		print("info_json", info_json)
		pass

if __name__ == '__main__':
	"""
	xigua chromedriver问题
	haokanshipin 所有 可下载的视频数量为0
	youku 所有 可下载的视频数量为0
	"""
	arg_lis = [
    # {
    #     "url_list": [
    #         "https://space.bilibili.com/412968594/video?tid=0&page=1&keyword=&order=pubdate"
    #     ],
    #     "platform": "bilibili",
    #     "kind": "频道",
    #     "author": "乡村美食炊二锅"
    # },
    # {
    #     "url_list": [
    #         "https://www.bilibili.com/video/BV1c7411r7Tp/?spm_id_from=333.337.search-card.all.click&vd_source=edcc2b08685462ffddcb7097473aabe9"
    #     ],
    #     "platform": "bilibili",
    #     "kind": "短视频",
    #     "author": "2019攒劲1"
    # },
    # {
    #     "url_list": [
    #         "https://www.bilibili.com/bangumi/play/ep578027?bsource=baidu_aladdin"
    #     ],
    #     "platform": "bilibili",
    #     "kind": "电视剧",
    #     "author": "凌汤圆1"
    # },
    # {
    #     "url_list": [
    #         "https://www.ixigua.com/home/108906431115/?source=pgc_author_profile&list_entrance=anyVideo"
    #     ],
    #     "platform": "xigua",
    #     "kind": "频道",
    #     "author": "爱笑汤圆哥"
    # },
    # {
    #     "url_list": [
    #         "https://www.ixigua.com/6806607943526515204?id=6806520744428700163&logTag=2e99a26c5f7fdd00955d"
    #     ],
    #     "platform": "xigua",
    #     "kind": "短视频",
    #     "author": "傻儿军长"
    # },
    # {
    #     "url_list": [
    #         "https://www.douyin.com/user/MS4wLjABAAAAModRR70C4zMGhv3QKhDJ44qFfwiVjydGJpK_P1cwpfyvMgV3bOhDuaKASS-xRerZ?vid=7150485456621227295"
    #     ],
    #     "platform": "douyin",
    #     "kind": "频道",
    #     "author": "詹大雪"
    # },
    # {
    #     "url_list": [
    #         "https://haokan.baidu.com/v?vid=876498736425063379"
    #     ],
    #     "platform": "haokanshipin",
    #     "kind": "短视频",
	# 	"language":"四川话",
    #     "author": "成都一条影视"
    # },
    # {
    #     "url_list": [
    #         "https://haokan.baidu.com/author/1561932396370051?query="
    #     ],
    #     "platform": "haokanshipin",
    #     "kind": "频道",
	# 	"language": "四川话",
    #     "author": "a四川阿鹏搞笑"
    # },
    # {
    #     "url_list": [
    #         "https://www.kuaishou.com/profile/3xt4esdgtvry9tg"
    #     ],
    #     "platform": "kuaishou",
    #     "kind": "频道",
    #     "author": "安哥回农村"
    # },
    {
        "url_list": [
            "https://v.youku.com/v_show/id_XNDQwNjgxMTM2OA==.html?spm=a2hbt.13141534.1_3.1&s=a13661602b1a4f54bcd1"
        ],
        "platform": "youku",
        "kind": "短视频",
        "author": "表妹进城3",
		"language": ""
    },


	# {
	#     "url": [],
	#     "platform": "yltv",
	#     "kind": "",
	#     "author": "",
	# 	"language":""
	# }
]
	for args in arg_lis:

	# args = {
	# 	"url_list": ["https://www.kuaishou.com/profile/3x45z6xysqz7yui"],# 音频地址
	# 	"platform": "kuaishou",# 平台
	# 	"kind": "频道",# 类别
	# 	"author": "十院子川味调料",# 作者昵称
	# }
		pi = ProcessInput(args)

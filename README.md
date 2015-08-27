# xacesite
============================================
APP stack:

*Amaze UI    +Front end 
*Tornado :   +Web Server 
*Motor  :    +Async Driver 
*mongodb：   +databack end

goal: 
-----------------------------
      Xacesite 为建立一个企业网站所需要的标准模板。使用tornado 和 mongo db搭建。
      前端直接使用amaze UI以适应中文的语言环境。
feature :
-----------------------------
     Local User system:  登录，注册，session ,cookie 维护
     FS:
         File Upload : PCS转储存支持
         Media To DB : 媒体文件的db支持，以便多实例的应用完成同步。
         Remote Http download(RHD)： 管理员功能，利用VPS远程下载。
         Remote Http2PCS: 通过PCS远程下载的内容，以便在GFW内获取文件实例。
     模板化前端：
          1.主页：提供标准的模板化前端。
          2.WIKI: 中文化的WIKI ，实现灵活的页面内容。
          3.Statics Page container： 无过滤的静态页面。>>无编辑器，通过上传实现。
          4.Blog ： 基本的Blog页面。 附带评论功能,在本产品中用作PR发布页面。
          5.Product SKU:提供基本的产品展示页面。
          6.下载页面： 提供产品相关的下载页面支持
                列表分类展示下载内容
          7.联系我们页面模板：含地图的联系页面 ，提供导航支持
          
挖个坑：慢慢做          
------------------

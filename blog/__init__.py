from flask import Flask
app=Flask(__name__)
import blog.user_views
import blog.admin_views
import blog.utils
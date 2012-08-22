from flask import Flask,request,url_for,render_template,session,g,jsonify,abort,send_from_directory,redirect
#from jinja2 import Markup
from blog import app
import MySQLdb as mysql
import config
pages=10
@app.before_request
def connect_db():
    g.db=mysql.connect(
        host=config.dbhost,user=config.dbuser,
        passwd=config.dbpass,db=config.dbname
    )
    if request.path!='/' and request.path.endswith('/'):
        return redirect(request.path[:-1])
    
@app.teardown_request
def teardown_request(exception):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'db'):
        g.db.close()
@app.route('/')
def index():
    try:
        cur=g.db.cursor()
        result=cur.callproc('get_index_articles')
        article_entries=cur.fetchall()
        cur.close()
        cur=g.db.cursor()
        result=cur.callproc('get_index_news')
        news_entries=cur.fetchall()
        cur.close()
        return render_template('index.html',article_entries=article_entries,news_entries=news_entries)
    except:
        return abort(404)
@app.route('/view_article/<article_id>')
def view_article(article_id):
    try:
        params=[article_id]
        cur=g.db.cursor()
        result=cur.callproc('get_article_info',params)
        article=cur.fetchone()
        cur.close()
        cur=g.db.cursor()
        result=cur.callproc('get_download_files_list',params)
        files=cur.fetchall()
        cur.close()
        return render_template('view_article.html',article=article,files=files)
        #return article_id
    except:
    #    return 'Error'
    #return str(article_id)
        abort(404)
    
@app.route('/view_news/<news_id>')
def view_news(news_id):
    try:
        params=[news_id]
        cur=g.db.cursor()
        result=cur.callproc('get_article_info',params)
        article=cur.fetchone()
        cur.close()       
        return render_template('view_news.html',article=article)
        #return article_id
    except:
    #    return 'Error'
    #return str(article_id)
        abort(404)
@app.route('/download_file/<doc_id>')
def download_file(doc_id):
    #return str(doc_id)
    try:
        params=[doc_id]
        cur=g.db.cursor()
        result=cur.callproc('download_file',params)
        filename=cur.fetchone()
        cur.close()
        import os
        root_path=os.path.dirname(__file__)
        upload_dir_path=os.path.join(root_path,'uploads')
        return send_from_directory(upload_dir_path,filename[0],as_attachment=True)
        #return upload_dir_path
    except:
        return abort(404)
@app.route('/news')
def news():   
    session['news_page_num']=0   
    params=[0]
    cur=g.db.cursor()
    result=cur.callproc('news_page',params)
    news=cur.fetchall()
    cur.close()
    return render_template('news.html',news=news)
@app.route('/get_more_news')
def get_more_news():
    page=int(session['news_page_num'])+pages
    params=[page]
    cur=g.db.cursor()
    result=cur.callproc('news_page',params)
    news=cur.fetchall()
    cur.close()
    news_result='';
    for n in news:
        news_result=news_result+ '<div class="newsitem" style="border-bottom: 1px solid #cccccc;margin-bottom: 5px;"> \
        <a style="color:3CABC4;font-size: 12px;" href="/view_news/'+str(n[0])+'" style="margin-bottom: 5px;"><b>'+n[1]+'</b></a> \
        <div style="word-wrap: break-word;font-size: 14px;">'+str(n[2])+'</div> \
        <span style="color:#B60404;font-size: 12px;">Posted on '+str(n[3])+'</span> \
        <a href="/view_news/'+str(n[0])+'" style="color: #1EA6C4;font-size: 10px;" ><b>View this article</b></a>\
        </div>'
         
    session['news_page_num']=page
    return jsonify(message=news_result)
@app.route('/articles')
def articles():
    return render_template('articles.html')
    
def get_more_articles():
    return '404'
@app.route('/post_comment')
def post_comment(comment=None,username=None):
    params=[username,comment]
    cur=g.db.cursor()
    result=cur.callproc('post_comment',params)
    cur.close()

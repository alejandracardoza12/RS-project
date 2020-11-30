from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint, session)
from flaskblog.main.forms import QueryForm
from flaskblog.search.Search import Search
import nltk
from nltk.stem import WordNetLemmatizer
import re


main = Blueprint('main', __name__)
search = Search()


@main.route("/", methods=['GET', 'POST'])
@main.route("/home", methods=['GET', 'POST'])
def home():
    session.permanent = True
    form = QueryForm()
    docids = request.args.getlist('docid')
    if("searchquery" in session and session["searchquery"]):
        avoid_words = search.get_avoid_words(docids, session["searchquery"])
    else:
        avoid_words = None 
    if form.validate_on_submit():
        session["origquery"] = form.content.data
        session["searchquery"] = lemmatize_query(
            form.content.data) + " " + form.content.data
        return redirect(url_for('main.home'), code=302)
    result = {}
    origquery = ""
    selected_doctitles = []
    if("searchquery" in session and session["searchquery"]):
        result = search.search_query(session["searchquery"], avoid_words)
    if("origquery" in session and session["origquery"]):
        origquery = session["origquery"]
    if(docids):
        selected_doctitles = search.get_titles(docids)
    return render_template('home.html', form=form, result=result, avoid_words=avoid_words, selected_doctitles=selected_doctitles, origquery = origquery)

@main.route("/secondversion", methods=['GET', 'POST'])
def second():
    session.permanent = True
    form = QueryForm()
    docids = request.args.getlist('docid')
    if("dummyquery" in session and session["dummyquery"]):
        avoid_words = search.get_avoid_words(docids, session["dummyquery"])
    else:
        avoid_words = None
    if form.validate_on_submit():
        session["origdummy"] = form.content.data
        session["dummyquery"] = lemmatize_query(
            form.content.data) + " " + form.content.data
        return redirect(url_for('main.second'), code=302)
    result = {}
    selected_doctitles = []
    if("dummyquery" in session and session["dummyquery"]):
        result = search.search_dummy(session["dummyquery"], docids)
    if("origdummy" in session and session["origdummy"]):
        origdummy = session["origdummy"]
    if(docids):
        selected_doctitles = search.get_titles(docids)
    return render_template('second.html', form=form, result=result, avoid_words=avoid_words, selected_doctitles=selected_doctitles, origdummy = origdummy)


@main.route("/reset", methods=['GET'])
def reset():
    session["origquery"] = ""
    session["searchquery"] = None
    return redirect(url_for('main.home'), code=302)
    
@main.route("/resetsecond", methods=['GET'])
def resetsecond():
    session["origdummy"] = ""
    session["dummyquery"] = None
    return redirect(url_for('main.second'), code=302)


def wnpos(e): return ('a' if e[0].lower() == 'j' else e[0].lower(
)) if e[0].lower() in ['n', 'r', 'v'] else None


def lemmatize_query(query):
    lemmatizer = WordNetLemmatizer()
    clean_text = re.sub(r'[^\w\s]', ' ', query)
    tokenized = nltk.word_tokenize(clean_text)
    pos_tagged = nltk.pos_tag(tokenized)

    lemmatized = ""

    for word, tag in pos_tagged:
        wn_tag = wnpos(tag)
        if(tag != "NNP" and tag != "NNPS"):
            if(wn_tag is not None):
                lemmatized += " " + \
                    lemmatizer.lemmatize(word.lower(), wnpos(tag))
            else:
                lemmatized += " " + word.lower()
    return lemmatized

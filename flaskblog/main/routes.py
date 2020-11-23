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
    if("searchquery" in session):
        avoid_words = search.get_avoid_words(docids, session["searchquery"])
    else:
        avoid_words = None 
    if form.validate_on_submit():
        session["searchquery"] = lemmatize_query(
            form.content.data) + " " + form.content.data
        result = search.search_query(session["searchquery"], avoid_words)
        return render_template('home.html', form=form, result=result, avoid_words=avoid_words, selected_doctitles=[])
    result = {}
    selected_doctitles = []
    if(session["searchquery"]):
        result = search.search_query(session["searchquery"], avoid_words)
    if(docids):
        selected_doctitles = search.get_titles(docids)
    return render_template('home.html', form=form, result=result, avoid_words=avoid_words, selected_doctitles=selected_doctitles)


@main.route("/reset", methods=['GET'])
def reset():
    session["searchquery"] = None
    return redirect(url_for('main.home'), code=302)


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

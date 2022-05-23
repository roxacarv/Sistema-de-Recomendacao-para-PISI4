import json
from lib2to3.pytree import convert
from flask import Flask, render_template, request, jsonify
from recom import get_recommended_animes
import animes_list
from prettytable import PrettyTable
import boto3
import credentials as conf

client = boto3.client('lambda',
                        region_name=conf.region_name,
                        aws_access_key_id=conf.aws_access_key_id,
                        aws_secret_access_key=conf.aws_secret_access_key,
                        aws_session_token=conf.aws_session_token)

def call_lambda_response(data):
    payload = {"data": data}
    result = client.invoke(FunctionName=conf.lambda_function_name,
                            InvocationType="RequestResponse",
                            Payload=json.dumps(payload))
    returned_data = result["Payload"].read()
    api_response = json.loads(returned_data)
    return api_response

def convert_to_html_table(data):
    pt = PrettyTable()
    pt.add_column("", data)
    return pt.get_html_string()

def pprint(message):
    html_str = "<span>"
    if isinstance(message, list):
        temp = html_str
        html_str = temp + "<br>".join(message)
    return html_str + "</span>"

def strip_searched_anime_from_list(anime_name, anime_list):
    if anime_name in anime_list:
        anime_list.remove(anime_name)
    return anime_list

application = Flask(__name__)

@application.route('/', methods=["GET", "POST"])
def index():
    title = "Me recomende um anime"

    if request.method == "GET":
        return render_template("index.html", index_title=title)
    else:
        name_input_request = request.form.get("anime-searcher")
        return_anime_nparray = animes_list.get_anime_vector(name_input_request)
        lambda_response = call_lambda_response(return_anime_nparray)
        return_anime_list = get_recommended_animes(list(lambda_response))
        strip_main_anime = strip_searched_anime_from_list(anime_name=name_input_request, anime_list=return_anime_list)
        return_html = convert_to_html_table(strip_main_anime)
        return render_template("ranime-list.html", index_animes=return_html)

@application.route('/data/anime-list')
def data_anime():
    new_json = animes_list.ANIMES_LIST
    return jsonify(new_json)

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()
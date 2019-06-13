import sys

#sys.path.append('..')
from run_squad import fetchSquad
from flask import jsonify, Flask, request
from flask import Flask
# from flask.ext.cache   import Cache
from flask_cache import Cache
from flask import request

cache = Cache()
CACHE_TYPE = 'simple'

import json

app = Flask(__name__)
cache.init_app(app)

# app.config['CACHE_TYPE'] = 'simple'
app.cache = Cache(app)


@app.route('/get_pred', methods=['POST'])
# @app.route('/get_pred', methods=['POST'])
@cache.cached(300, key_prefix='get_pred')
# @app.cache.cached(timeout=300)

def get_pred():

    predict_query1 = (json.loads(json.dumps(request.get_json())))

    l4_k = []
    k_doc=len(predict_query1['docs'])
    for j in range(0, k_doc):
        p = str(j)

        l3 = {"paragraphs": [{"context": predict_query1["docs"][j]["doc_text"],
                              'qas': [{"question": predict_query1["query_text"], "id": p}]}]}
        l4_k.append(l3)

    json_data = json.dumps({"data": l4_k})
    #print(json_data)

    predict_query_k = json.loads(json_data)


    pred, all_pred = fetchSquad(False, True, json_data)
    op_list = []
    doc = []

    for j in range(0, k_doc):
        p = str(j)

        q = predict_query_k["data"][0]['paragraphs'][0]['qas'][0]['question']

        def read_squad_examples(input_data):


            def is_whitespace(c):
                if c == " " or c == "\t" or c == "\r" or c == "\n" or ord(c) == 0x202F:
                    return True
                return False

            examples = []


            paragraph_text = input_data
            doc_tokens = []
            char_to_word_offset = []
            prev_is_whitespace = True
            for c in paragraph_text:
                if is_whitespace(c):
                    prev_is_whitespace = True
                else:
                    if prev_is_whitespace:
                        doc_tokens.append(c)
                    else:
                        doc_tokens[-1] += c
                    prev_is_whitespace = False
                char_to_word_offset.append(len(doc_tokens) - 1)
                # print(char_to_word_offset)

            return (doc_tokens)
        a = read_squad_examples(predict_query1["docs"][j]["doc_text"])
        s1 = ""
        for words in a:
            s1 += words + " "
        #print(s1)
        #ans_offset = s1.index(pred[p])
        #ans_length=len(pred[p])

        #doc.append({'ans_text': pred[p],
                    #'doc_text': s1,
                    #'id': predict_query1["docs"][j]["id"],
                    #'bert_score': all_pred[p][0]['score']})
        doc.append({'Answer': pred[p],
                    'doc_text': s1,

                    'Confidence_score': all_pred[p][0]['score']})

    q = predict_query_k["data"][0]['paragraphs'][0]['qas'][0]['question']

    new_pred3 =  {"queryText": q,"docs":doc}

    return jsonify(new_pred3)



if __name__ == '__main__':
    app.run(debug=True)



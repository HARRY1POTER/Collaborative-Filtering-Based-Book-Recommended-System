# from flask import Flask, render_template, request
# import pickle
# import numpy as np

# popular_df = pickle.load(open('popular.pkl', 'rb'))
# pt = pickle.load(open('pt.pkl', 'rb'))
# books = pickle.load(open('books.pkl', 'rb'))
# similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))

# app = Flask(__name__)


# @app.route('/')
# def index():
#     return render_template('index.html',
#                            book_name=list(popular_df['Book-Title'].values),
#                            author=list(popular_df['Book-Author'].values),
#                            image=list(popular_df['Image-URL-M'].values),
#                            votes=list(popular_df['num_ratings'].values),
#                            rating=list(popular_df['avg_rating'].values)
#                            )


# @app.route('/recommend')
# def recommend_ui():
#     return render_template('recommend.html')


# @app.route('/recommend_books', methods=['post'])
# def recommend():
#     user_input = request.form.get('user_input')
#     index = np.where(pt.index == user_input)[0][0]
#     similar_items = sorted(
#         list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:7]

#     data = []
#     for i in similar_items:
#         item = []
#         temp_df = books[books['Book-Title'] == pt.index[i[0]]]
#         item.extend(list(temp_df.drop_duplicates(
#             'Book-Title')['Book-Title'].values))
#         item.extend(list(temp_df.drop_duplicates(
#             'Book-Title')['Book-Author'].values))
#         item.extend(list(temp_df.drop_duplicates(
#             'Book-Title')['Image-URL-M'].values))

#         data.append(item)

#     print(data)

#     return render_template('recommend.html', data=data)


# if __name__ == '__main__':
#     app.run(debug=True)


# from flask import Flask, render_template, request, jsonify
# import pickle
# import numpy as np

# popular_df = pickle.load(open('popular.pkl', 'rb'))
# pt = pickle.load(open('pt.pkl', 'rb'))
# books = pickle.load(open('books.pkl', 'rb'))
# similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))

# app = Flask(__name__)


# @app.route('/')
# def index():
#     return render_template('index.html',
#                            book_name=list(popular_df['Book-Title'].values),
#                            author=list(popular_df['Book-Author'].values),
#                            image=list(popular_df['Image-URL-M'].values),
#                            votes=list(popular_df['num_ratings'].values),
#                            rating=list(popular_df['avg_rating'].values)
#                            )


# @app.route('/recommend')
# def recommend_ui():
#     return render_template('recommend.html')


# @app.route('/recommend_books', methods=['POST'])
# def recommend():
#     user_input = request.form.get('user_input')
#     index = np.where(pt.index == user_input)[0][0]
#     similar_items = sorted(
#         list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:7]

#     data = []
#     for i in similar_items:
#         item = []
#         temp_df = books[books['Book-Title'] == pt.index[i[0]]]
#         item.extend(list(temp_df.drop_duplicates(
#             'Book-Title')['Book-Title'].values))
#         item.extend(list(temp_df.drop_duplicates(
#             'Book-Title')['Book-Author'].values))
#         item.extend(list(temp_df.drop_duplicates(
#             'Book-Title')['Image-URL-M'].values))

#         data.append(item)

#     return render_template('recommend.html', data=data)

# # New route to return book title suggestions


# @app.route('/autocomplete', methods=['GET'])
# def autocomplete():
#     search_query = request.args.get('query', '')
#     suggestions = books[books['Book-Title'].str.contains(
#         search_query, case=False, na=False)]['Book-Title'].unique()[:10]
#     return jsonify(list(suggestions))


# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np

popular_df = pickle.load(open('popular.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html',
                           book_name=list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['num_ratings'].values),
                           rating=list(popular_df['avg_rating'].values)
                           )


@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')


@app.route('/recommend_books', methods=['POST'])
def recommend():
    user_input = request.form.get('user_input')

    # Check if book exists in the dataset
    if user_input not in pt.index:
        return render_template('recommend.html', error="No book found")

    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(
        list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:9]

    data = []
    for i in similar_items:
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        if temp_df.empty:
            continue
        item = list(temp_df.drop_duplicates('Book-Title')
                    [['Book-Title', 'Book-Author', 'Image-URL-M']].values[0])
        data.append(item)

    if not data:
        return render_template('recommend.html', error="No books to recommend")

    return render_template('recommend.html', data=data)


@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    search_query = request.args.get('query', '')
    suggestions = books[books['Book-Title'].str.contains(
        search_query, case=False, na=False)]['Book-Title'].unique()[:10]
    return jsonify(list(suggestions))


if __name__ == '__main__':
    app.run(debug=True)

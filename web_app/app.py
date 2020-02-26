"""Main application and routing logic for TwitOff."""   
from decouple import config
from flask import Flask, render_template, request

# from flask_migrate import Migrate

from web_app.models import DB, User, Tweet #,migrate
# from web_app.routes import my_routes
# #from web_app.more_routes import more_routes
from web_app.twitter import add_or_update_user
from .predict import predict_user
#load_dotenv()

#DATABASE_URL = os.getenv("DATABASE_URL", default="OOPS")

def create_app():
    """create and config instance of the flask application"""
    app = Flask(__name__)
    app.config["CUSTOM_VAR"] = 5 # just an example of app config :-D
    #app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///twitter_database3.db"
    app.config["SQLALCHEMY_DATABASE_URI"] = config('DATABASE_URL')
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config['ENV'] = config('ENV')
    #app.config["TWITTER_API_CLIENT"] = twitter_api_client()

    DB.init_app(app)
    #migrate.init_app(app, db)

    #app.register_blueprint(my_routes)
    #app.register_blueprint(more_routes)
    @app.route('/')
    def root():
        users = User.query.all()
        return render_template('homepage.html', title='Home Page',users=users)

        

   
    @app.route('/user', methods=['POST'])
    @app.route('/user/<name>', methods=['GET'])

    def user(name=None, message=''):
        name = name or request.values['user_name']
        try:
            if request.method == 'POST':
                add_or_update_user(name)
                message = 'User {} successfully added!'.format(name)
            tweets = User.query.filter(User.name == name).one().tweets
        except Exception as e:
            message = "Error adding or fetching {}: {}".format(name, e)
            tweets = []
        return render_template('user.html', title=name, tweets=tweets,
                                message=message)   


    @app.route('/compare', methods=['POST'])
    def compare(message=''):
        user1, user2 = sorted([request.values['user1'],
                               request.values['user2']])
        if user1 == user2:
            message = 'Cannot compare a user to themselves!'
        else:
            prediction = predict_user(user1, user2, request.values['tweet_text']) 
            message = ' "{}" is more likely to be said by {} than {}'.format(
                request.values['tweet_text'], user1 if prediction else user2,
                user2 if prediction else user1)
            
        return render_template('prediction.html', title='Prediction', message=message)
    
    @app.route("/reset")
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template('homepage.html', title='DB Reset', users=[]) 



    return app
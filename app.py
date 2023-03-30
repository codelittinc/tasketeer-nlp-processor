from flask import Flask
from src.controllers.content_controller import content_bp
from src.controllers.search_controller import search_bp
from src.controllers.health_controller import health_bp
from src.events.search_requested_handler import SearchRequestedHandler
import os
import atexit
import logging
from apscheduler.schedulers.background import BackgroundScheduler

# set flask app
app = Flask(__name__)

# register blueprints (controllers)
app.register_blueprint(content_bp)
app.register_blueprint(search_bp)
app.register_blueprint(health_bp)

# start server
if __name__ == "__main__":
    # setup scheduler to read from redis queue
    scheduler = BackgroundScheduler()
    scheduler.remove_all_jobs()
    scheduler.add_job(func=SearchRequestedHandler.listen, id='redis_subs', max_instances=1)
    scheduler.start()

    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())

    # set logging level to display logs from apscheduler
    logging.basicConfig()
    logging.getLogger('apscheduler').setLevel(logging.DEBUG)
    
    # run flask app
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port, use_reloader=False)
from .load import app
from .load import model_server_thread

model_server_thread.start()
app.run()

from time import sleep

from tower import EventChannel, Event, event_listener

channel = EventChannel()


class OnStartWork(Event): pass


class OnEndWork(Event): pass


class OnProgress(Event):

    def __init__(self, progress):
        self.progress = progress


def emulate_work():
    channel.notify(OnStartWork())
    for i in range(10):
        channel.notify(OnProgress(i))
        sleep(1)
    channel.notify(OnEndWork())


# Declaring listener-lambdas for using as named arguments
start_handler1 = lambda x: print("Handler 1.", "Starting the job")
progress_handler1 = lambda x: print("Handler 1.", "Progress:", x.progress)
end_handler1 = lambda x: print("Handler 1.", "Good bye!")


# Declaring listener-function for using as named arguments
def progress_handler2(x):
    print("Handler 2. Progress:", x.name(), x.progress)


# Declaring listener-function for using based on argument type
def progress_handler3(event: OnProgress):
    print("Handler 3. Progress:", event.name(), event.progress)


# Declaring listener-function using decorator
@event_listener(OnProgress.name())
def progress_handler4(x):  # No type annotations
    print("Handler 4. Progress:", x.name(), x.progress)


# Declaring listener-object with decorated listener-functions
class ProgressHandler5:

    @event_listener(OnStartWork.name())
    def on_start(self, _):
        print("Handler 5. Start")

    @event_listener
    def on_progress(self, e: OnProgress):
        print("Handler 5. Progress", e.progress)

    @event_listener(OnEndWork.name())
    def on_end(self, _):
        print("Handler 5. Start")


channel.add_listeners(
    progress_handler3,
    progress_handler4,
    ProgressHandler5(),
    on_start_work=start_handler1,
    on_end_work=end_handler1,
    on_progress=[
        progress_handler1,
        progress_handler2
    ]
)

emulate_work()

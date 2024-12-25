from queue import Queue
from threading import Lock, Thread
import docker

# Initialize Docker client
client = docker.from_env()

# Create a thread-safe container pool
class ContainerPool:
    def __init__(self, image, pool_size=2):
        self.image = image
        self.pool = Queue(maxsize=pool_size)
        self.lock = Lock()

        # Pre-warm the containers
        for _ in range(pool_size):
            self.pool.put(self._create_container())

    def _create_container(self):
        container = client.containers.run(
            self.image,  # Use an image with Python
            command=["tail", "-f", "/dev/null"],
            working_dir="/sandbox",# Command to run
            stdin_open=True,  # Open stdin to interact with the container
            tty=True,  # Allocate a pseudo-TTY for interactive command execution
            detach=True
        )
        return container

    def get_container(self):
        with self.lock:
            return self.pool.get()

    def return_container(self, container):
        with self.lock:
            self.pool.put(container)

    def cleanup(self):
        while not self.pool.empty():
            container = self.pool.get()
            container.stop()
            container.remove()

# Initialize the container pool
container_pool = ContainerPool(image="logicleagueserver")

# Clean up containers on exit
import atexit
atexit.register(container_pool.cleanup)

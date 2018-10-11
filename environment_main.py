from environment_test import Env

if __name__ == "__main__":
    env = Env() # gym.make()

    while True:
        env.render()
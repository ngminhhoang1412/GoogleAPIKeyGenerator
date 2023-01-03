from google_cloud.key import GoogleApiKey
import time


if __name__ == '__main__':
    start_time = time.time()
    a = GoogleApiKey()
    a.create_multi_projects()
    # a.get_key()
    print("--- %s seconds ---" % (time.time() - start_time))


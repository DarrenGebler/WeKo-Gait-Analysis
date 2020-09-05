import datetime


class UserData:
    def __init__(self, filename):
        """
        Initialise User Data class

        :param filename: User uploaded file name
        """
        self.filename = filename

    def find_file(self):
        """
        Searches text file for user email.

        :return: filename + date/time ID if user email exists, otherwise returns None.
        """
        file = open("/home/ubuntu/userdata.txt", "r")
        emails = file.read()
        if self.filename not in emails:
            append_file = open("/home/ubuntu/userdata.txt", "a+")
            append_file.write("\n" + self.filename)
            append_file.close()
            return None
        else:
            time = datetime.datetime.now()
            return time.strftime(self.filename + "%d%m%y%H%M%S")

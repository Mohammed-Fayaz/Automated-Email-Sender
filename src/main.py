import smtplib
from email.message import EmailMessage
from string import Template


def read_data(file):
    """
    reads in data from a CSV text file
    :param file: input file path
    :return: a list
    """
    people = []
    with open(file) as fp:
        data = fp.readlines()
        for line in data:
            person_details = line.split(',')
            people.append(person_details)
    return people


def clean_data(people):
    """
    removes newline characters that may have found their way into the data
    :param people: list of people details
    :return: a list of formatted people details
    """
    for person_details in people:
        person_details[:] = person_details[1:]
        if person_details[len(person_details) - 1] == '\n':
            person_details[:] = person_details[:len(person_details) - 1]
        if person_details[len(person_details) - 1].endswith('\n'):
            person_details[len(person_details) - 1] = person_details[len(person_details) - 1][:-1]
    return people


def remove_unwanted_details(people):
    """
    retains only necessary information required for the Email
    :param people: list
    :return: list of people details
    """
    for person_details in people:
        person_details[:] = person_details[0:1] + person_details[3:4] + person_details[-3:]
    return people


def print_details(people):
    """
    prints the data onto the console
    :param people: list of people
    :return: None
    """
    print(len(people))
    for person_details in people:
        print(person_details)


def read_template(file):
    """
    reads in the file and returns a template object
    :param file: input file path
    :return: template object
    """
    with open(file) as fp:
        message = fp.read()
    return Template(message)


def create_message(temp, new_file, name, phone_no, email_id, domain):
    """
    creates a new message from the template object
    :param temp: input template object
    :param new_file: path of destination file
    :param name: mentor name
    :param phone_no: phone number of mentor
    :param email_id: email id of mentor
    :param domain: domain of interest for the participant
    :return: None
    """
    dict_subs = {'mentor_name': name, 'mentor_phone': phone_no, 'mentor_email': email_id,
                 'domain': domain}

    with open(new_file, mode='w') as fp:
        new_msg = temp.substitute(dict_subs)
        fp.write(new_msg)


def ok(person_details):
    """
    returns True is all data is filled in, False otherwise
    :param person_details: a list of person details
    :return: Boolean (True if no value is empty)
    """
    for detail in person_details:
        if detail == '':
            return False
    return True


def main():
    """
    sends an e-mail using the SMTP protocol (connecting via TLS)
    :return: None
    """
    people = read_data('data.txt')
    people = clean_data(people)
    people = remove_unwanted_details(people)

    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.starttls()
    s.login('User_email_id', 'password')

    for i in range(1, len(people)):         # creating a custom message for each recipient
        if not(ok(people[i])):
            continue
        temp = read_template('template_file.txt')
        create_message(temp, 'new_message.txt', name=people[i][2], phone_no=people[i][4],
                       email_id=people[i][3], domain=people[i][1])

        with open('new_message.txt') as fp:
            msg = EmailMessage()
            msg.set_content(fp.read())

            msg['Subject'] = 'Subject'
            msg['From'] = 'User_email_id'
            msg['To'] = people[i][0]
        s.send_message(msg)

    s.quit()


if __name__ == '__main__':
    main()

import boto3

import config


def encode_get_parameters(baseurl, arg_dict):
    queryString = baseurl + "?"
    for indx, key in enumerate(arg_dict):
        queryString += str(key) + "=" + str(arg_dict[key])
        if indx < len(arg_dict) - 1:
            queryString += "&"
    return queryString


def create_hit(client, config):
    # START IMPORTANT HIT VARIABLES
    base_url = "https://robot-embodiment-survey.name/survey"
    params_to_encode = {"v": "1.0"}
    assignments_per_hit = 100
    payment_per_assignment = 0.05
    # END IMPORTANT HIT VARIABLES

    # START DECORATIVE HIT VARIABLES
    hit_title = "Robot Embodiment Survey"
    hit_description = "Identify the embodiment of different robots"
    hit_keywords = ["robot", "image", "survey", "embodiment", "robotics", "images", "guess", "abstract", "human"]
    duration_in_seconds = 60 * 10
    lifetime_in_seconds = 60 * 60 * 24
    frame_height = 800

    # params_to_encode['host'] = config.SANDBOX_MTURK if c.SANDBOX else config.MTURK
    encoded_url = encode_get_parameters(base_url, params_to_encode)
    q_text = """<?xml version="1.0" encoding="UTF-8"?>
<ExternalQuestion xmlns="http://mechanicalturk.amazonaws.com/AWSMechanicalTurkDataSchemas/2006-07-14/ExternalQuestion.xsd">
  <ExternalURL>{}</ExternalURL>
  <FrameHeight>{}</FrameHeight>
</ExternalQuestion>""".format(encoded_url, frame_height)
    print(q_text)

    return client.create_hit(
        Title=hit_title,
        Description=hit_description,
        Keywords=",".join(hit_keywords),
        MaxAssignments=assignments_per_hit,
        LifetimeInSeconds=lifetime_in_seconds,
        AssignmentDurationInSeconds=duration_in_seconds,
        Question=q_text,
        Reward=str(payment_per_assignment)
    )


if __name__ == '__main__':
    c = config.Config()
    endpoint_url = 'https://mturk-requester{}.us-east-1.amazonaws.com'.format('' if not c.SANDBOX else '-sandbox')
    cl = boto3.client(
        'mturk',
        endpoint_url=endpoint_url,
        aws_access_key_id=c.aws_conf['aws_access_key_id'],
        aws_secret_access_key=c.aws_conf['aws_secret_access_key'],
        region_name='us-east-1'
    )
    print(create_hit(client=cl, config=c))

# Embodiment Classification Experiment 
Amazon Mechanical Turk Survey for the Robot Embodiment Study

deployed on [AWS](https://robot-embodiment-survey.name/survey)

## Goal

For a set of robots (and their corresponding images), deploy an Amazon Mechanical Turk survey that will record embodiment data for each robot such as a free form text input about design metaphor and a slider value for the robot level of abstraction. This data is collected to use a data-driven approach to define embodiment parameters into the design space, outlined in the embodiment survey paper. 

## Design considerations

In order to make the data meaningful, certain design considerations were taken to ensure useful data is collected. For each robot in the set of robots (picked from https://robots.ieee.org/robots/), the robot will be annotated by N=30 labelers. Each labeler will be assigned a task of annotation M=30 randomly selected different robots in order to complete their survey (from those that have not been sufficiently annotated according to N). These values are configurable in the implementation to assure that the desired number of annotations are completed for each robot, even if new robots are added after data is already being collected.

## Implementation

The code deploys a web server on AWS ECS Fargate using a docket image, built using code provided in the repository (https://github.com/interaction-lab/robot-embodiment-survey). The server uses a AWS RDS database to store responses. The robots presented in the survey are parsed into the database to keep track of what surveys must be presented. The robots are parsed from the ieee.org website via the following code: https://github.com/interaction-lab/robot-embodiment-survey/blob/master/util.py#L10. The images are cached locally to avoid stressing the ieee.org website.
HITs are published to Amazon Mechanical Turk via https://github.com/interaction-lab/robot-embodiment-survey/blob/master/manage_mturk.py as ExternalQuestion(s). The parameters can be adjusted for the study. The number of hits that should be published should be sufficient to annotate each robot N times (greater than # robots * N / M). The random assignment of robots to surveys will cause some robots to have more annotations than others but robots will be assigned to HITs until each robot will have N annotations.

## Work to be Done

Complete Photoshop edits of robot images (trivial but takes a bit of time--Eric can explain standardized process)
Run the experiment and process results (design discussions can happen with Eric if need be)


# pd's portfolio

This portfolio uses AWS & ReactJS.

# Technologies used
AWS: IAM, S3, CodeBuild, CloudFront, Lambda, CodePipeline, SNS, Boto3, CLI
#

Chocolatey or Brew, Git and GitHub, SSH, HTML, CSS, Font Awesome, Google Fonts

#

Python, IPython, PowerShell, Command Prompt, Atom

# Issues

1. ** 7/19/20 Deployment issues **
    - index.html is not updating in S3
    - Other files I have changed have updated
        - upload_portfolio_lambda.py
        - README.md
    - GitHub is updated successfully
    - CodePipeline everything successful
    - Log files show index.html in portfolio build

    - I manually updated index.html to S3 portfolio and it worked
    - Going to modify index.html and push it to GitHub, so CodePipeline can run another release.

2. ** Changes made to .py upload file need to be maintain in 2 places **
    - AWS Lambda
    - Local repository


- [x] test
- [ ] test test
- [ ] test test test

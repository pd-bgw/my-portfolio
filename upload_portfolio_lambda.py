# ----------------------------------------------------------------- #
# 7/18/20
# below is the code that we changed for CodePipeline
# in aws lambda editor, which is above
# ----------------------------------------------------------------- #

import boto3
import StringIO
import zipfile
import mimetypes

def lambda_handler(event, context):

    print("## Job Started ##")
    print("## upload_portfolio_lambda.py")

    # 7/18/20 if we run outside of codepipeline
    location = {
        "bucketName": 'portfoliobuild.bluegreywall.com',
        "objectKey": 'portfoliobuild.zip'
    }

    try:
        # 7/18/20 codepipeline
        job = event.get("CodePipeline.job")

        if job:
            for artifact in job["data"]["inputArtifacts"]:
                if artifact["name"] == "buildPortfolio":
                    location = artifact["location"]["s3Location"]

        # make log entry
        print("## Building portfolio from")
        print("## " + str(location))

        s3 = boto3.resource('s3')

        sns = boto3.resource('sns')
        topic = sns.Topic('arn:aws:sns:us-east-1:437570009687:deployPortfolioTopic')

        portfolio_bucket = s3.Bucket('portfolio.bluegreywall.com')
        # 7/18/20 codepipeline
        build_bucket = s3.Bucket(location["bucketName"])

        portfolio_zip = StringIO.StringIO()
        # 7/18/20 codepiple
        build_bucket.download_fileobj(location["objectKey"], portfolio_zip)

        print("## Build bucket zip files")

        with zipfile.ZipFile(portfolio_zip) as myzip:
            for nm in myzip.namelist():
                obj = myzip.open(nm)
                portfolio_bucket.upload_fileobj(obj, nm,
                ExtraArgs={'ContentType': mimetypes.guess_type(nm)[0]})
                portfolio_bucket.Object(nm).Acl().put(ACL='public-read')
                print("## " + nm)

        # make log entry
        print("## Job Completed! ##")
        topic.publish(Message="Deployed sucessfully! (lambda python boto3 sns)", Subject="Portfolio Deployed")
        # 7/18/20 we need to let codepipline know that it ran successfully.
        # codepipeline can't figure it out on its own
        if job:
            codepipeline = boto3.client('codepipeline')
            codepipeline.put_job_success_result(jobId=job["id"])
    except:
        topic.publish(Message="Deployment failed! (lambda python boto3 sns)", Subject="Portfolio Deployed")
        raise


    return 'from little blue marble'


# ----------------------------------------------------------------- #
# below is the code that we changed for SNS
# in aws lambda editor, which is above
# ----------------------------------------------------------------- #

# import boto3
# import StringIO
# import zipfile
# import mimetypes
#
# def lambda_handler(event, context):
#
#     try:
#         s3 = boto3.resource('s3')
#
#         sns = boto3.resource('sns')
#         topic = sns.Topic('arn:aws:sns:us-east-1:437570009687:deployPortfolioTopic')
#
#         portfolio_bucket = s3.Bucket('portfolio.bluegreywall.com')
#         build_bucket = s3.Bucket('portfoliobuild.bluegreywall.com')
#
#         portfolio_zip = StringIO.StringIO()
#         build_bucket.download_fileobj('portfoliobuild.zip', portfolio_zip)
#
#         with zipfile.ZipFile(portfolio_zip) as myzip:
#             for nm in myzip.namelist():
#                 obj = myzip.open(nm)
#                 portfolio_bucket.upload_fileobj(obj, nm,
#                 ExtraArgs={'ContentType': mimetypes.guess_type(nm)[0]})
#                 portfolio_bucket.Object(nm).Acl().put(ACL='public-read')
#                 #print nm
#
#
#         print "Job Completed!"
#         topic.publish(Message="Deployed sucessfully! (lambda python boto3 sns)", Subject="Portfolio Deployed")
#     except:
#         topic.publish(Message="Deployment failed! (lambda python boto3 sns)", Subject="Portfolio Deployed")
#         raise
#
#
#     return 'from little blue marble'


# ----------------------------------------------------------------- #
# below is the code that we used prior to making changes
# in aws lambda editor, which is above
# ----------------------------------------------------------------- #

# import boto3
# import StringIO
# import zipfile
# import mimetypes
#
# def lambda_handler(event, context):
#
#     s3 = boto3.resource('s3')
#
#     portfolio_bucket = s3.Bucket('portfolio.bluegreywall.com')
#     build_bucket = s3.Bucket('portfoliobuild.bluegreywall.com')
#
#     portfolio_zip = StringIO.StringIO()
#     build_bucket.download_fileobj('portfoliobuild.zip', portfolio_zip)
#
#     with zipfile.ZipFile(portfolio_zip) as myzip:
#         for nm in myzip.namelist():
#             obj = myzip.open(nm)
#             portfolio_bucket.upload_fileobj(obj, nm,
#             ExtraArgs={'ContentType': mimetypes.guess_type(nm)[0]})
#             portfolio_bucket.Object(nm).Acl().put(ACL='public-read')
#
#     return 'Hello from the little blue marble'

# ----------------------------------------------------------------- #
# below is the code that we used prior to making changes
# in aws lambda editor, which is above
# ----------------------------------------------------------------- #

# import boto3
# import StringIO
# import zipfile
# import mimetypes
#
# s3 = boto3.resource('s3')
#
# portfolio_bucket = s3.Bucket('portfolio.bluegreywall.com')
# build_bucket = s3.Bucket('portfoliobuild.bluegreywall.com')
#
# portfolio_zip = StringIO.StringIO()
# build_bucket.download_fileobj('portfoliobuild.zip', portfolio_zip)
#
# with zipfile.ZipFile(portfolio_zip) as myzip:
#     for nm in myzip.namelist():
#         obj = myzip.open(nm)
#         portfolio_bucket.upload_fileobj(obj, nm,
#         ExtraArgs={'ContentType': mimetypes.guess_type(nm)[0]})
#         portfolio_bucket.Object(nm).Acl().put(ACL='public-read')

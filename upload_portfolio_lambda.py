import boto3
import StringIO
import zipfile
import mimetypes

def lambda_handler(event, context):

    s3 = boto3.resource('s3')

    portfolio_bucket = s3.Bucket('portfolio.bluegreywall.com')
    build_bucket = s3.Bucket('portfoliobuild.bluegreywall.com')

    portfolio_zip = StringIO.StringIO()
    build_bucket.download_fileobj('portfoliobuild.zip', portfolio_zip)

    with zipfile.ZipFile(portfolio_zip) as myzip:
        for nm in myzip.namelist():
            obj = myzip.open(nm)
            portfolio_bucket.upload_fileobj(obj, nm,
            ExtraArgs={'ContentType': mimetypes.guess_type(nm)[0]})
            portfolio_bucket.Object(nm).Acl().put(ACL='public-read')

    return 'Hello from the little blue marble'

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

import boto
import boto.s3.connection
from boto.s3.connection import S3Connection
from boto.s3.key import Key
access_key = 'AKIAJYZYULDIKQ2X34MA'
secret_key = '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'

try:
	conn = S3Connection(access_key, secret_key)
	print "Successfully connected to S3"
except:
	print "Cannot connect to S3"

bucket = conn.get_bucket('sjsu195db1')
key = bucket.get_key('Hot N Cold.mp3')
key.get_contents_to_filename('/home/duc/Desktop/test_folder/Hot N Cold.mp3')

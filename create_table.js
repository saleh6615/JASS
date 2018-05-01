
var AWS = require('aws-sdk');
//var uuid = require('node-uuid');

AWS.config.update({region: "us-east-2"})
ddb = new AWS.DynamoDB({apiVersion: '2012-10-08'});

var users_schema = {
	AttributeDefinitions:[
	 	{
			AttributeName: "USER_ID",
			AttributeType: "N"
	 	},
	],
	KeySchema: [
		{
			AttributeName: "USER_ID",
			KeyType: "HASH"
		}
	],
	ProvisionedThroughput: {
		ReadCapacityUnits: 1, 
		WriteCapacityUnits: 1
	},
	TableName: "LOCK_USERS",
	StreamSpecification: {
		StreamEnabled: false
	}
};

ddb.createTable(users_schema, function(err, data){
	if(err)
		console.log("Error", err)
	else 
		console.log("Table has been created successfully:\n", data)
});
/*
// Create an S3 client
var s3 = new AWS.S3();

// Create a bucket and upload something into it
var bucketName = 'node-sdk-sample-' + uuid.v4();
var keyName = 'hello_world.txt';

s3.createBucket({Bucket: bucketName}, function() {
  var params = {Bucket: bucketName, Key: keyName, Body: 'Hello World!'};
  s3.putObject(params, function(err, data) {
    if (err)
      console.log(err)
    else
      console.log("Successfully uploaded data to " + bucketName + "/" + keyName);
  });
}); */


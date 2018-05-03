
var AWS = require('aws-sdk');
//var uuid = require('node-uuid');

AWS.config.update({region: "us-east-2"})
ddb = new AWS.DynamoDB({apiVersion: '2012-10-08'});

var users_table = {
	TableName : "USER_PERMISSIONS",
	AttributeDefinitions: [
		{
			AttributeName: "USERNAME",
			AttributeType: "S"
		}
	],
	KeySchema: [
		{
			AttributeName: "USERNAME",
			KeyType: "HASH"
		}
	],
	ProvisionedThroughput: {
		ReadCapacityUnits: 1, 
		WriteCapacityUnits: 1
	},
	StreamSpecification: {
		StreamEnabled: false
	}
}
var access_table = {
	TableName: "ACCESS_HISTORY",
	AttributeDefinitions: [
		{
			AttributeName: "AID",
			AttributeType: "N"
		}
	],
	AttributeDefinitions: [
		{
			AttributeName: "USERNAME",
			AttributeType: "S"
		}
	],
	KeySchema: [
		{
			AttributeName: "AID",
			KeyType: "HASH"
		},
		{
			AttributeName: "USERNAME",
			KeyType: "RANGE"
		}	
	],
	ProvisionedThroughput: {
		ReadCapacityUnits: 1, 
		WriteCapacityUnits: 1
	},
	StreamSpecification: {
		StreamEnabled: false
	}
}

ddb.createTable(access_table, function(err, data){
	if(err)
		console.log("Error", err)
	else 
		console.log("Access table has been created successfully:\n", data)
});
/*ddb.createTable(users_table, function(err, data){
	if(err)
		console.log("Error", err)
	else 
		console.log("Users table has been created successfully:\n", data)
}); */

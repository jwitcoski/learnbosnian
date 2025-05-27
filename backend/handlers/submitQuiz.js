'use strict';

const AWS = require('aws-sdk');
const dynamodb = new AWS.DynamoDB.DocumentClient();

module.exports.handler = async (event) => {
  try {
    const data = JSON.parse(event.body);
    const { userId, lessonId, score, answers } = data;

    const params = {
      TableName: process.env.DYNAMODB_TABLE,
      Item: {
        pk: `USER#${userId}`,
        sk: `QUIZ#${lessonId}#${Date.now()}`,
        lessonId,
        score,
        answers,
        timestamp: new Date().toISOString(),
        gsi1pk: `LESSON#${lessonId}`,
        gsi1sk: `SCORE#${score}`
      }
    };

    await dynamodb.put(params).promise();

    return {
      statusCode: 200,
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Credentials': true,
      },
      body: JSON.stringify({
        message: 'Quiz submitted successfully',
        score
      }),
    };
  } catch (error) {
    console.error('Error submitting quiz:', error);
    return {
      statusCode: 500,
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Credentials': true,
      },
      body: JSON.stringify({
        error: 'Could not submit quiz'
      }),
    };
  }
}; 
'use strict';

module.exports.hello = async (event) => {
  return {
    statusCode: 200,
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Credentials': true,
    },
    body: JSON.stringify(
      {
        message: 'Hello from Learn Bosnian API!',
        input: event,
      },
      null,
      2
    ),
  };
};

module.exports.getLesson = async (event) => {
  const { lessonId } = event.pathParameters || {};
  
  return {
    statusCode: 200,
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Credentials': true,
    },
    body: JSON.stringify({
      lessonId,
      title: 'Sample Bosnian Lesson',
      content: 'Zdravo! (Hello!)',
      vocabulary: [
        { bosnian: 'Zdravo', english: 'Hello' },
        { bosnian: 'Hvala', english: 'Thank you' },
        { bosnian: 'Molim', english: 'Please/You\'re welcome' }
      ]
    }),
  };
}; 
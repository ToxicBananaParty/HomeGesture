import amqp from 'amqplib/callback_api';

amqp.connect('amqp://ryan:XRStudios20@172.16.10.187', (err0, connection) => {
    if(err0) {
        throw err0;
    }

    connection.createChannel((err1, channel) => {
        if(err1) {
            throw err1;
        }

        const queue = 'posenet';
        channel.assertQueue(queue, {
            durable: false
        });

        channel.consume(queue, (msg) => {
            console.log("Received message: ", JSON.parse(msg!.content.toString()!));
        }, {
            noAck: true
        });
    });
});
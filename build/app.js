"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const callback_api_1 = __importDefault(require("amqplib/callback_api"));
callback_api_1.default.connect('amqp://ryan:XRStudios20@172.16.10.187', (err0, connection) => {
    if (err0) {
        throw err0;
    }
    connection.createChannel((err1, channel) => {
        if (err1) {
            throw err1;
        }
        const queue = 'posenet';
        channel.assertQueue(queue, {
            durable: false
        });
        channel.consume(queue, (msg) => {
            console.log("Received message: ", msg === null || msg === void 0 ? void 0 : msg.content.toString());
        }, {
            noAck: true
        });
    });
});

const TelegramBot = require('node-telegram-bot-api');
const Convertor = require('tgs-to-gif');
const fetch = require('node-fetch');
const fs = require('fs');
const HttpsProxyAgent = require('https-proxy-agent');
const webp = require('webp-converter');

// replace your telegram bot tocken here
const token = '';
const bot = new TelegramBot(token, {polling: true});


// download file using node-fetch
const downloadFile = (async (url, path) => {
  // if no proxy needed, simply change it to fetch
  const proxyAgent = new HttpsProxyAgent('http://127.0.0.1:8889');
  const res = await fetch(url, {agent: proxyAgent});
  const fileStream = fs.createWriteStream(path);
  await new Promise((resolve, reject) => {
    res.body.pipe(fileStream);
    res.body.on('error', reject);
    fileStream.on('finish', resolve);
  });
});

bot.on('message', (msg) => {
  const chatId = msg.chat.id;
  const messageId = msg.message_id;
  console.log(msg);
  // only process stickers
  if (msg.sticker) {
    // processing animated sticker
    if (msg.sticker.is_animated) {
      bot.sendMessage(chatId, 'Decoding and Processing...', {reply_to_message_id: messageId})
          .then((newmsg) => {
            const newmsgId = newmsg.message_id;
            const fileID = msg.sticker.file_id;
            const filename = msg.sticker.set_name + '_' + msg.sticker.file_unique_id + '.gif.1';
            // download sticker using fileID and get link
            bot.getFileLink(fileID)
                .then((link) => {
                  downloadFile(link, 'tempTGS.tgs')
                      .then(() => {
                        // convert file from .tgs to .gif
                        Convertor.convertFile('tempTGS.tgs')
                            .then(() => {
                              bot.editMessageText('Sending...', {chat_id: chatId, message_id: newmsgId});
                              const file = fs.createReadStream('tempTGS.tgs.gif');
                              // send file renaming it to .gif.1
                              bot.sendDocument(chatId, file, {reply_to_message_id: messageId}, {filename: filename})
                                  .then(function() {
                                    bot.deleteMessage(chatId, newmsgId);
                                  });
                            });
                      });
                });
          });
    } else {
      bot.sendMessage(chatId, 'Processing...', {reply_to_message_id: messageId})
          .then((newmsg) => {
            const newmsgId = newmsg.message_id;
            const fileID = msg.sticker.file_id;
            const filename = msg.sticker.set_name + '_' + msg.sticker.file_unique_id + '.png';
            bot.getFileLink(fileID)
                .then((link) => {
                  // download sticker
                  downloadFile(link, 'tempSticker.webp')
                      .then(function() {
                        // convert sticker from webp to .png using webp.dwebp
                        webp.dwebp('tempSticker.webp', 'tempSticker.png', '-o', '-v')
                            .then(function() {
                              bot.editMessageText('Sending...', {chat_id: chatId, message_id: newmsgId});
                              const file = fs.createReadStream('tempSticker.png');
                              // send file renaming to .png
                              bot.sendDocument(chatId, file, {reply_to_message_id: messageId}, {filename: filename})
                                  .then(function() {
                                    bot.deleteMessage(chatId, newmsgId);
                                  });
                            });
                      });
                });
          },
          );
    }
  } else {
    bot.sendMessage(chatId, 'Please send a sticker to me.', {reply_to_message_id: messageId});
  }
});

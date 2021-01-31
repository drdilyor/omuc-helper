#!/usr/bin/env python3
import json
import os
import sys
import time
from uuid import uuid4

import telegram as t
from telegram import ext as x


u = x.Updater(os.environ['BOT_TOKEN'])
d = u.dispatcher

def start(upd, ctx):
    upd.message.reply_text("hello world")


class Message:
    def __init__(self, title, text):
        self.title = title
        self.text = text

    def search_matches(self, search):
        return (search in self.title)

    def to_result(self):
        return t.InlineQueryResultArticle(
            id=uuid4(),
            title=self.title,
            input_message_content=t.InputTextMessageContent(
                self.text, 'HTML'
            ),
        )

    def to_dict(self):
        return {
            "title": self.title,
            "text": self.text,
        }


msgs = [Message(**i) for i in json.load(open('data.json'))]

def inline(upd, ctx):
    query = upd.inline_query.query

    start = time.perf_counter()
    result = [i.to_result() for i in msgs if i.search_matches(query)]
    end = time.perf_counter()
    print("finished search in", end - start, "seconds")

    upd.inline_query.answer(result)


def create(upd, ctx):
    text = upd.message.text
    _command, _, text = text.partition('\n')
    title, _, content = text.partition('\n')
    if title and content:
        msgs.append(Message(title, content))
        upd.message.reply_text("success")
    else:
        upd.message.reply_text("fail, example:\n/create\ntitle\ncontent...")


def save(upd, ctx):
    json.dump([i.to_dict() for i in msgs], open('data.json', 'w'), indent=4)
    upd.message.reply_text("okay")


d.add_handler(x.CommandHandler('start', start))
d.add_handler(x.CommandHandler('create', create))
d.add_handler(x.CommandHandler('save', save))
d.add_handler(x.InlineQueryHandler(inline))

u.start_polling()
u.idle()

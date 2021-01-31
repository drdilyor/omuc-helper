#!/usr/bin/env python3
import json
import time
from uuid import uuid4

import telegram as t
from telegram import ext as x

from secrets import TOKEN


u = x.Updater(TOKEN)
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

d.add_handler(x.CommandHandler('start', start))
d.add_handler(x.InlineQueryHandler(inline))
try:
    u.start_polling()
    u.idle()
finally:
    json.dump([i.to_dict() for i in msgs], 'data.json')

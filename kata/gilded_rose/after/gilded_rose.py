# -*- coding: utf-8 -*-

SULFURAS = "Sulfuras, Hand of Ragnaros"
AGED_BRIE = "Aged Brie"
BACKSTAGE = "Backstage passes to a TAFKAL80ETC concert"

maxQuantity = 50
minQuantity = 0

def increase_quality(item, amount=1):
    if item.quality < maxQuantity:
        item.quality += amount


def decrease_quality(item, amount=1):
    if item.quality > minQuantity:
        item.quality -= amount

def decrease_sell_in(item):
    item.sell_in -= 1



class GildedRose(object):

    def __init__(self, items):
        self.items = items

    def update_quality(self):
        for item in self.items:

            is_sulfuras = item.name == SULFURAS
            is_aged_brie = item.name == AGED_BRIE
            is_backstage = item.name == BACKSTAGE
            
            if not is_aged_brie and not is_backstage:
                if item.name != SULFURAS:
                    decrease_quality(item)
            else:
                if item.quality < maxQuantity:
                    increase_quality(item)
                    if is_backstage:
                        if item.sell_in < 11:
                            increase_quality(item)
                        if item.sell_in < 6:
                            increase_quality(item)

            if not is_sulfuras:
                decrease_sell_in(item)

            if item.sell_in < 0:
                if not is_aged_brie:
                    if not is_backstage:
                        if not is_sulfuras:
                            decrease_quality(item)
                    else:
                        item.quality = 0
                else:
                    increase_quality(item)


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)

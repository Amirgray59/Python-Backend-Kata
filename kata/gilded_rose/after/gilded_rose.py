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


class GildedRose(object):

    def __init__(self, items):
        self.items = items

    def update_quality(self):
        for item in self.items:
            if item.name != AGED_BRIE and item.name != BACKSTAGE:
                if item.name != SULFURAS:
                    decrease_quality(item)
            else:
                if item.quality < maxQuantity:
                    increase_quality(item)
                    if item.name == BACKSTAGE:
                        if item.sell_in < 11:
                            increase_quality(item)
                        if item.sell_in < 6:
                            increase_quality(item)

            if item.name != SULFURAS:
                item.sell_in = item.sell_in - 1
                
            if item.sell_in < 0:
                if item.name != AGED_BRIE:
                    if item.name != BACKSTAGE:
                        if item.name != SULFURAS:
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

# 第一章 python数据模型

## 1.1 一摞Python风格的纸牌

使用如下代码可以创建一个纸牌类

```python
import collections
Card = collections.namedtuple('Card', ['rank', 'suit'])

class FrenchDeck:
    ranks = [str(n) for n in range(2, 11)] + list('JQKA')
    suits = 'spades diamonds clubs hearts'.split()

    def __init__(self):
        self._cards = [Card(rank, suit) for suit in self.suits for rank in self.ranks]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]
```

上述代码中, `namedtuple` 可以用来创建一张卡牌, 且其属性可以直接获取. 例如

```python
beer_card = Card('7', 'diamond')
beer_card
>>> Card(rank='7', suit='diamond')
```

重写`__len__`可以使用`len()`来获取一叠牌的张数

```python
deck = FrenchDeck()
len(deck)
>>> 52
```

重写`__getitem__` 可以使用索引取出特定的牌, 例如

```python
deck[0]
>>> Card(rank='2', suit='spades')
```

利用 `random.choice` 可以实现随机选择一张牌, 因为它已经是一个序列.

```python
# randomly choose a card
from random import choice
choice(deck)
>>> Card(rank='7', suit='diamonds')
```

也可以使用切片

```python
deck[:3]
>>> [Card(rank='2', suit='spades'),
 Card(rank='3', suit='spades'),
 Card(rank='4', suit='spades')]
```

可以进行迭代和反向迭代

```python
for card in deck:
    print(card)
>>> Card(rank='2', suit='spades')
Card(rank='3', suit='spades')
Card(rank='4', suit='spades')
...
```

```python
# reverse iteration
for card in reversed(deck):
    print(card)
>>> Card(rank='A', suit='hearts')
Card(rank='K', suit='hearts')
...
```

可以用`in`判断是否属于

```python
Card('Q', 'hearts') in deck
>>> True
```

可以对其进行升序排序, 这里花色按照 c,d,h,s, 点数从2到A, 也就是2C, 2D, ... , AH, AS.

```python
suit_values = dict(spades=3, hearts=2, diamonds=1, clubs=0)
def spades_high(card):
    """a function to get card's value, 2C to AS"""
    rank_value = FrenchDeck.ranks.index(card.rank)
    return rank_value * len(suit_values) + suit_values[card.suit]

# ascending sort
for card in sorted(deck, key=spades_high):
    print(card)
>>> Card(rank='2', suit='clubs')
Card(rank='2', suit='diamonds')
...
Card(rank='A', suit='hearts')
Card(rank='A', suit='spades')
```

## 1.2 如何使用特殊方法

特殊方法是被Python解释器调用的, 而不需要主动去调用. 通过内置的函数(`len`, `iter`, `str`)来使用特殊方法是最好的选择.

### 1.2.1 模拟数值类型

使用一个类`Vector`来实现向量

```python
from math import hypot


class Vector:
    """class vector per example 1.2"""

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __repr__(self):
        return 'Vector(%r, %r)' % (self.x, self.y)

    def __abs__(self):
        # hypot calculates 2-norm of vector
        return hypot(self.x, self.y)

    def __bool__(self):
        return bool(abs(self))

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Vector(x, y)

    def __mul__(self, scalar):
        # multiply with a scalar
        return Vector(self.x * scalar, self.y * scalar)
```

虽然代码中有6个特殊方法, 但这些方法除了`__init__`并不会在类自身的代码中使用.

### 1.2.2 字符串表现形式

Python的内置函数`repr` 能把一个对象用字符串的形式表现出来以便辨认, 其通过`__repr__`这个特殊方法来获得一个对象的字符串.

在`__repr__`实现中, 使用了`%r`来获取对象各个属性的标准字符串表示格式. `__repr__`返回的字符串应该准确, 无歧义. 

`__repr__`和`__str__`的区别在于, 后者是在`str()`函数被使用, 或是`print`打印时, 它返回的字符串对终端用户更友好.

如果只想实现两个方法中的一种, `__repr__`是更好的选择, 因为没有`__str__`时, 解释器会用`__repr__`替代.

### 1.2.3 算术运算符

`__add__`和`__mul__`为向量类提供了`+`和`*`这两个算术运算符, 这两个方法的返回值都是新创建的向量对象, 符合中缀运算符不改变操作对象, 而是产出一个新的值的基本原则.

### 1.2.4 自定义的布尔值

`bool(x)`的背后其实是调用`x.__bool__()`的结果.

我们对`__bool__`的实现很简单, 向量模为0则为`False`, 其他情况为`True`. 

还有一种更高效的写法

```python
def __bool__(self):
    return bool(self.x or self.y)
```

## 1.3 特殊方法一览

表1-1 跟运算符无关的特殊方法

| 类别                    | 方法名                                                       |
| ----------------------- | ------------------------------------------------------------ |
| 字符串/字节序列表示形式 | `__repr__`,`__str__`,`__format__`,`__bytes__`                |
| 数值转换                | `__abs__`, `__bool__`, `__complex__`,`__int__`,`__float__`,`__hash__`,`__index__` |
| 集合模拟                | `__len__`,`__getitem__`,`__setitem__`,`__delitem__`,`__contains__` |
| 迭代枚举                | `__iter__`,`__reversed__`,`__next__`                         |
| 可调用模拟              | `__call__`                                                   |
| 上下文管理              | `__enter__`,`__exit__`                                       |
| 实例创建和销毁          | `__new__`,`__init__`,`__del__`                               |
| 属性管理                | `__getattr__`, `__getattribute__`,`__setattr__`,`__delattr__`,`__dir__` |
| 属性描述符              | `__get__`,`__set__`,`__delete__`                             |
| 跟类相关的服务          | `__prepare__`,`__instancecheck__`,`__subclasscheck__`        |

表1-2 跟运算符相关的特殊方法

| 类别               |                     方法名和对应的运算符                     |
| ------------------ | :----------------------------------------------------------: |
| 一元运算符         |         `__neg__: -`, `__pos__: +` ,`__abs__: abs()`         |
| 众多比较运算符     | `__lt__: <`,`__le__: <=`, `__eq__: ==`,`__ne__: !=`,`__gt__: >`,`__ge__: >=` |
| 算术运算符         | `__add__: +`,`__sub__: -`,`__mul__: *`,`__truediv__: /`,`__floordiv__: //`,`__mod__: %`,`__divmod__: divmod()`,`__pow__: pow(), **`,`__round__: round()` |
| 反向算术运算符     | `__radd__`,`__rsub__`,`__rmul__`,`rtruediv__`,`__rfloordiv__`,`__rmod__`,`__rdivmod__`,`rpow__` |
| 增量赋值算术运算符 | `__iadd__`,`__isub__`,`__imul__`,`__itruediv__`,`__ifloordiv__`,`__imod__`,`__ipow__` |
| 位运算符           | `__invert__: ~`,`__lshift__: <<`,`__rshift__: >>`,`__and__: &`,`__or__: |`,`__xor__: ^` |
| 反向位运算符       | `__rlshift__`,`__rrshift__`,`__rand__`,`__rxor__`,`__ror__`  |
| 增量赋值位运算符   | `__ilshift__`,`__irshift__`,`__iand__`,`__ixor__`,`__ior__`  |

## 1.4 为什么len不是普通方法

`len`之所以不是一个普通方法, 是为了让Python自带的数据结构可以走后门, `abs`也是同理. 多亏了他是特殊方法, 我们也可以把`len`用于自定义数据类型.


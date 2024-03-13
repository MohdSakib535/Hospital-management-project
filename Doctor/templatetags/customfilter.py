from django import template

register = template.Library()

@register.filter(name='Discount')
def Discount(data):
    discount_percentage=20
    discount_amount=data*(discount_percentage/100)
    final_price=data+discount_amount
    return final_price

@register.filter(name='slice_data')
def slice_data(data):
    s_data=str(data[0:1]).replace('[',' ').replace(']',' ')
    return s_data

@register.filter(name='slice_data2')
def slice_data2(data):
    s_data=str(data[1:2]).replace('[',' ').replace(']',' ')
    return s_data




# @register.filter(name='price')
# def Price(data):
#     return data
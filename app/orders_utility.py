from .models  import Order
from django.db.models import Q
from collections import defaultdict

def save_order(security_type,order_type,price,quantity,status,user):
    data=Order(security_type=security_type,order_type=order_type,price=price,quantity=quantity,status=status,user=user)
    data.save()
    return data.pk

def fetch_all_user_orders(user):
    orders=Order.objects.filter(user=user)
    return orders.values()

def fetch_all_orders(user):
    orders=Order.objects.filter(~Q(user=user),status="Pending")
    return orders.values()

def executable_orders(security_type,order_type,price,quantity,status,user):
    if order_type=="Buy":
        orders=Order.objects.filter(~Q(user=user),security_type=security_type,order_type="Sell",price=price,status="Pending").order_by("created")
    else:
        orders=Order.objects.filter(~Q(user=user),security_type=security_type,order_type="Buy",price=price,status="Pending").order_by("created")
    return orders.values()
    
def execute_order(order_id,security_type,order_type,price,quantity,status,user):
    exe_orders=executable_orders(security_type,order_type,price,quantity,status,user)
    new_record=Order.objects.get(id=order_id)
    for order in exe_orders:
        if len(exe_orders)>0:
            old_record=Order.objects.get(id=order['id'])
            if old_record.quantity > new_record.quantity:
                old_record.quantity=int(old_record.quantity)-int(new_record.quantity)
                Order.objects.create(security_type=security_type,order_type=old_record.order_type,price=price,quantity=new_record.quantity,status="Executed",user=old_record.user)
                Order.objects.create(security_type=security_type,order_type=new_record.order_type,price=price,quantity=new_record.quantity,status="Executed",user=new_record.user)
                old_record.save()
                new_record.delete()
                break

            elif new_record.quantity > old_record.quantity:
                new_record.quantity=new_record.quantity-old_record.quantity
                Order.objects.create(security_type=security_type,order_type=old_record.order_type,price=price,quantity=old_record.quantity,status="Executed",user=old_record.user)
                Order.objects.create(security_type=security_type,order_type=new_record.order_type,price=price,quantity=old_record.quantity,status="Executed",user=new_record.user)
                old_record.delete()
                new_record.save()
            else:
                Order.objects.create(security_type=security_type,order_type=old_record.order_type,price=price,quantity=old_record.quantity,status="Executed",user=old_record.user)
                Order.objects.create(security_type=security_type,order_type=new_record.order_type,price=price,quantity=old_record.quantity,status="Executed",user=new_record.user)
                old_record.delete()
                new_record.delete()
                break

def fetch_user_portfolio(user):
    record=defaultdict(lambda: defaultdict(lambda: 0))
    orders=Order.objects.filter(user=user,status="Executed")
    orders=orders.values()
    total_investment=0
    for order in orders:
        security_type=order['security_type']
        incremental_fields=['quantity','price']
        record[security_type]['name']=security_type
        
        for key in order:
            if key in incremental_fields:
                if order['order_type']=='Buy':
                    
                    if key=='price':
                        total_investment+=order[key]*order['quantity']
                        record[security_type][key] += order[key]*order['quantity']
                    else:
                        record[security_type][key] += order[key]
                else:
                    if key=='price':
                        total_investment-=order[key]*order['quantity']
                        record[security_type][key] -= order[key]*order['quantity']
                    else:
                        record[security_type][key] -= order[key]

    return record.values(),total_investment

def orders_summary(user):
    pending_orders=Order.objects.filter(user=user,status="Pending")
    executed_orders=Order.objects.filter(user=user,status="Executed")
    return len(pending_orders.values()),len(executed_orders.values())
